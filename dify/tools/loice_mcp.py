"""The one client of the Loice MCP server (https://app.loice.ai/mcp).

Every tool of this plugin is a thin declaration over the same call: JSON-RPC `tools/call` over
Streamable HTTP, authorized with the workspace API key as a Bearer token. Prices, validation,
refusals and billing are all the server's; this module only maps Dify's flat parameters to the
tool's arguments and the answer back to Dify messages.
"""

from __future__ import annotations

import json
import uuid
from collections.abc import Generator
from typing import Any

import requests

MCP_URL = "https://app.loice.ai/mcp"
PROTOCOL_VERSION = "2025-06-18"
USER_AGENT = "loice-dify-plugin/0.0.1"
# Long enough for wait_seconds (25 s) plus the server's own work; a lookup never hangs a workflow.
TIMEOUT_SECONDS = 60


class LoiceError(Exception):
    """A transport or authorization failure (never a business refusal: those are tool results)."""


# ---- parameter mapping -------------------------------------------------------------------------


def _blank(value: Any) -> bool:
    return value is None or (isinstance(value, str) and value.strip() == "")


def split_list(value: Any) -> list[str]:
    """A multi-value text field: a JSON array, or values separated by ';' or new lines.

    Commas are NOT separators: LinkedIn industry labels contain them ("Bars, Taverns, and
    Nightclubs").
    """
    if _blank(value):
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if not _blank(v)]
    text = str(value).strip()
    if text.startswith("["):
        try:
            parsed = json.loads(text)
            if isinstance(parsed, list):
                return [str(v).strip() for v in parsed if not _blank(v)]
        except ValueError:
            pass
    parts = text.replace("\r", "\n").replace(";", "\n").split("\n")
    return [part.strip() for part in parts if part.strip()]


def _int(value: Any) -> int | None:
    if _blank(value):
        return None
    return int(float(value))


def _bool(value: Any) -> bool | None:
    if value is None or value == "":
        return None
    if isinstance(value, str):
        return value.strip().lower() in ("true", "1", "yes")
    return bool(value)


def _compact(args: dict[str, Any]) -> dict[str, Any]:
    """Drops unset values: the server's schemas are strict and an empty string is not 'unset'."""
    out: dict[str, Any] = {}
    for key, value in args.items():
        if value is None or value == [] or value == {}:
            continue
        if isinstance(value, str):
            value = value.strip()
            if value == "":
                continue
        out[key] = value
    return out


def _billing(params: dict[str, Any]) -> dict[str, Any]:
    return {"dry_run": _bool(params.get("dry_run")), "idempotency_key": params.get("idempotency_key")}


def _search_leads(p: dict[str, Any]) -> dict[str, Any]:
    filters = _compact(
        {
            "jobTitle": split_list(p.get("job_title")),
            "company": split_list(p.get("company")),
            "location": split_list(p.get("location")),
            "industry": split_list(p.get("industry")),
            "seniorityLevel": split_list(p.get("seniority_level")),
            "function": split_list(p.get("function")),
            "headcount": split_list(p.get("headcount")),
            "yearsExperience": split_list(p.get("years_experience")),
            "keywords": split_list(p.get("keywords")),
            "people": split_list(p.get("people")),
        }
    )
    return {
        "filters": filters,
        "count": _int(p.get("count")),
        "continue_from_run_id": p.get("continue_from_run_id"),
        **_billing(p),
    }


def _find_employees(p: dict[str, Any]) -> dict[str, Any]:
    filters = _compact(
        {
            "title": split_list(p.get("title")),
            "seniority": split_list(p.get("seniority")),
            "department": split_list(p.get("department")),
            "location": split_list(p.get("location")),
        }
    )
    return {"company": p.get("company"), "count": _int(p.get("count")), "filters": filters, **_billing(p)}


def _wait(p: dict[str, Any], key: str) -> dict[str, Any]:
    return {key: p.get(key), "wait_seconds": _int(p.get("wait_seconds"))}


ARGUMENTS = {
    "get_account": lambda p: {},
    "list_filter_values": lambda p: {"key": p.get("key"), "query": p.get("query")},
    "search_leads": _search_leads,
    "find_employees": _find_employees,
    "get_run": lambda p: _wait(p, "run_id"),
    "cancel_run": lambda p: {"run_id": p.get("run_id")},
    "get_results": lambda p: {"handle": p.get("handle"), "cursor": p.get("cursor")},
    "list_lead_lists": lambda p: {"query": p.get("query"), "page": _int(p.get("page"))},
    "add_to_lead_list": lambda p: {
        "result_ids": split_list(p.get("result_ids")),
        "list_id": p.get("list_id"),
        "new_list_name": p.get("new_list_name"),
    },
    "find_email": lambda p: {
        "mode": p.get("mode"),
        "name": p.get("name"),
        "company": p.get("company"),
        "url": p.get("url"),
        **_billing(p),
    },
    "enrich_email": lambda p: {"email": p.get("email"), **_billing(p)},
    "find_linkedin_profile": lambda p: {
        "firstName": p.get("first_name"),
        "lastName": p.get("last_name"),
        "company": p.get("company"),
        **_billing(p),
    },
}


def arguments_for(tool: str, params: dict[str, Any]) -> dict[str, Any]:
    args = _compact(ARGUMENTS[tool](params or {}))
    if tool == "search_leads" and "filters" not in args:
        args["filters"] = {}
    return args


# ---- transport ---------------------------------------------------------------------------------


def _parse(response: requests.Response, request_id: str) -> dict[str, Any]:
    """A JSON-RPC answer, sent either as JSON or as a server-sent event stream."""
    kind = response.headers.get("Content-Type", "")
    # MCP is UTF-8 (JSON); an event stream names no charset and requests would guess Latin-1.
    body = response.content.decode("utf-8", errors="replace")
    if "text/event-stream" in kind:
        for line in body.splitlines():
            if not line.startswith("data:"):
                continue
            try:
                message = json.loads(line[5:].strip())
            except ValueError:
                continue
            if isinstance(message, dict) and message.get("id") == request_id:
                return message
        raise LoiceError("The Loice MCP server sent no answer to the call.")
    try:
        return json.loads(body)
    except ValueError as exc:
        raise LoiceError(f"The Loice MCP server answered with something that is not JSON (HTTP {response.status_code}).") from exc


def call_tool(api_key: str, tool: str, arguments: dict[str, Any], url: str = MCP_URL) -> dict[str, Any]:
    """Calls one Loice MCP tool and returns its result (`content`, `structuredContent`, `isError`)."""
    if _blank(api_key):
        raise LoiceError("A Loice API key is required (Settings → API in the Loice app).")
    request_id = str(uuid.uuid4())
    try:
        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {api_key.strip()}",
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
                "MCP-Protocol-Version": PROTOCOL_VERSION,
                "User-Agent": USER_AGENT,
            },
            json={
                "jsonrpc": "2.0",
                "id": request_id,
                "method": "tools/call",
                "params": {"name": tool, "arguments": arguments},
            },
            timeout=TIMEOUT_SECONDS,
        )
    except requests.RequestException as exc:
        raise LoiceError(f"Could not reach Loice ({type(exc).__name__}). Nothing was charged; try again.") from exc

    if response.status_code in (401, 403):
        raise LoiceError("Loice refused the API key: check it under Settings → API in the Loice app.")
    if response.status_code == 429:
        raise LoiceError("Loice rate limit reached. Nothing was charged; wait a moment and try again.")
    if response.status_code >= 500:
        raise LoiceError(f"Loice is unavailable right now (HTTP {response.status_code}). Nothing was charged; try again.")

    message = _parse(response, request_id)
    if "error" in message:
        error = message["error"] or {}
        raise LoiceError(f"Loice MCP error {error.get('code')}: {error.get('message')}")
    result = message.get("result")
    if not isinstance(result, dict):
        raise LoiceError("The Loice MCP server sent an empty result.")
    return result


def _text_of(result: dict[str, Any]) -> str:
    parts = [c.get("text", "") for c in result.get("content") or [] if isinstance(c, dict) and c.get("type") == "text"]
    return "\n".join(part for part in parts if part)


def invoke(tool_self: Any, tool: str, params: dict[str, Any]) -> Generator[Any, None, None]:
    """The body of every tool: call Loice, then hand Dify the structured answer and its text.

    A refusal (not enough points, a card required, a run already active, ...) is a tool RESULT
    with a reason code and a next step, so an agent can act on it; it is passed through as such.
    """
    api_key = tool_self.runtime.credentials.get("loice_api_key", "")
    result = call_tool(api_key, tool, arguments_for(tool, params))
    structured = result.get("structuredContent")
    text = _text_of(result)
    if isinstance(structured, dict):
        yield tool_self.create_json_message(structured)
    if not text and isinstance(structured, dict):
        text = json.dumps(structured, ensure_ascii=False)
    if text:
        yield tool_self.create_text_message(text)
