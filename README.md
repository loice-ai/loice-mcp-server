# Loice plugin

An [Agent Plugins](https://agent-plugins.org/) package (spec **1.0.0**) for
[Loice](https://loice.ai). It gives an AI agent B2B lead search, a company's employees,
verified work emails, email and LinkedIn enrichment, and ideal-customer profiles built from a
website.

## What's inside

| Path | What it is |
| --- | --- |
| `plugin.json` | Manifest |
| `mcp.json` | The hosted Loice MCP server: `https://app.loice.ai/mcp` (Streamable HTTP) |
| `skills/loice-prospecting/` | An [Agent Skill](https://agentskills.io/) with workflows and spending rules for the Loice tools |
| `assets/icon.png`, `assets/icon.svg` | Plugin icon |

The MCP server is remote, so there is nothing to install or run locally.

## Sign-in

The first connection opens a browser to sign in to Loice and approve access (OAuth 2.1 with
PKCE). There's no API key to configure. You need a Loice account. Billed tools spend points
from your workspace. See [Connect MCP](https://docs.loice.ai/connect-mcp) and
[Plans and points](https://docs.loice.ai/plans-and-points).

For an unattended agent with no browser, create an API key under **Settings → API** in the
app. Configure it in your client as an `Authorization: Bearer loice_sk_…` header. Don't put it
in `mcp.json`: the spec forbids secrets in plugin files.

## Also available as

- **MCP Registry:** `ai.loice/mcp` on [registry.modelcontextprotocol.io](https://registry.modelcontextprotocol.io/v0.1/servers?search=ai.loice/mcp)
- **Direct URL:** add `https://app.loice.ai/mcp` as a remote MCP server in any client

## Docs

- [MCP server](https://docs.loice.ai/mcp-server): tools, prices, permissions, errors
- [Connect MCP](https://docs.loice.ai/connect-mcp): per-client setup

## License

MIT
