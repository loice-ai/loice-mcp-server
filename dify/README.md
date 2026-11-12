# Loice for Dify

**Author:** loice · **Version:** 0.0.1 · **Type:** tool

[Loice](https://loice.ai) finds and verifies B2B contacts. This plugin gives Dify agents, chatflows
and workflows the tools of the hosted Loice MCP server (`https://app.loice.ai/mcp`): lead search,
a company's employees, verified work emails, email and LinkedIn enrichment and lead lists.

- Source: https://github.com/loice-ai/loice-mcp-server (folder `dify/`)
- Contact: welcome@loice.ai
- Docs: [MCP server](https://docs.loice.ai/mcp-server) (tools, prices, errors) ·
  [Plans and points](https://docs.loice.ai/plans-and-points)

## Setup

1. Sign up at [app.loice.ai](https://app.loice.ai). New workspaces get free points.
2. In the Loice app open **Settings → API** and create an API key (`loice_sk_…`).
3. In Dify, install **Loice** from the Marketplace, open **Tools → Loice → Authorize** and
   paste the key. Dify checks it with `get_account`, which is free.

Connection requirements: outbound HTTPS from the Dify plugin daemon to `app.loice.ai` (port 443).
Nothing else is called.

## Tools

| Tool | What it does | Cost |
| --- | --- | --- |
| `get_account` | Workspace, points balance, live price of every billed tool, rate limits | Free |
| `list_filter_values` | Exact labels a search filter accepts (industry, function, seniority, ...) | Free |
| `search_leads` | People by job title, company, location, industry, seniority, function, headcount, keywords. A background run | Per lead delivered |
| `find_employees` | Current employees of one company (domain or LinkedIn company URL). A background run | Per company + per employee delivered |
| `get_run` / `cancel_run` | Status of a run (with `wait_seconds`), or stop it | Free |
| `get_results` | People of a run (`run:<id>`) or a list (`list:<id>`), 25 per page | Free |
| `list_lead_lists` / `add_to_lead_list` | Your lead lists; save rows to one | Free |
| `find_email` | A verified work email from name + domain, name + company name, or a LinkedIn URL. Never a guess | Per completed lookup |
| `enrich_email` | The person and company behind an email address | Per completed lookup |
| `find_linkedin_profile` | A LinkedIn profile from name + employer | Per completed search |

Live prices are in `get_account`. Billed tools take `dry_run: true` for an exact quote that
charges nothing, and an optional `idempotency_key`: a retry with the same key is never charged
twice. A lookup that completes but finds nothing is charged; a provider outage or an invalid
argument is never charged.

Multi-value fields (job titles, locations, industries, row ids, ...) take values separated by
`;` or new lines, or a JSON array. Commas are not separators, because some industry labels
contain them.

## Usage

**Agent:** add the Loice tools to an Agent app and ask, for example: *"Find 25 Heads of Sales at
SaaS companies in Germany with 51-200 employees, then find verified emails for the first five."*
The agent quotes with `dry_run`, runs `search_leads`, polls `get_run`, reads `get_results` and
calls `find_email` in `linkedin` mode for the rows you pick.

**Workflow:** a typical chain is `search_leads` → `get_run` (`wait_seconds: 25`, in a loop until
`completed`) → `get_results` → `find_email`.

Every tool returns the Loice answer as JSON (the `json` output variable) and as text.

## Errors

A refusal is returned as a normal tool result with a reason code and the next step, so an agent
can act on it: `insufficient_credits`, `card_required` and `trial_ended` carry the Billing link in
`details.url`; `run_already_active` means a search is still running in the workspace (wait with
`get_run` or stop it with `cancel_run`). A wrong API key fails the call with
"Loice refused the API key".

## Privacy

See [PRIVACY.md](PRIVACY.md) and the [Loice Privacy Center](https://loice.ai/privacy-center/).
