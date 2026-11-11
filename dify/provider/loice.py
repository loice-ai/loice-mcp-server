from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from tools import loice_mcp


class LoiceProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        # get_account is free and read-only: it proves the key without spending a point.
        try:
            result = loice_mcp.call_tool(credentials.get("loice_api_key", ""), "get_account", {})
        except loice_mcp.LoiceError as exc:
            raise ToolProviderCredentialValidationError(str(exc)) from exc
        if result.get("isError"):
            raise ToolProviderCredentialValidationError(loice_mcp._text_of(result) or "Loice refused the API key.")
