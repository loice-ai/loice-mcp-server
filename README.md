<p align="center">
  <img src="assets/icon.svg" alt="Loice" width="72" height="72">
</p>

<h1 align="center">Loice MCP server</h1>

<p align="center">
  B2B lead search, a company's employees, verified work emails and enrichment
  for Claude, ChatGPT, Cursor, VS Code, Gemini CLI or your own agent.
</p>

<p align="center">
  <a href="https://docs.loice.ai/mcp-server">Docs</a> ·
  <a href="https://docs.loice.ai/connect-mcp">Connect a client</a> ·
  <a href="https://docs.loice.ai/plans-and-points">Plans and points</a> ·
  <a href="https://app.loice.ai">app.loice.ai</a>
</p>

---

[Loice](https://loice.ai) runs a remote **MCP server**. An AI assistant that speaks the
[Model Context Protocol](https://modelcontextprotocol.io) can search for leads, find a company's
employees, find verified emails, enrich contacts and save people to your lead lists. It spends points from your workspace at the same prices as the
app and the API.

```text
https://app.loice.ai/mcp
```

The server is hosted, so there is nothing to install or run locally. This repository is the
[Agent Plugins](https://agent-plugins.org/) package (spec **1.0.0**) for it: the server entry plus
an [Agent Skill](https://agentskills.io/) that teaches an agent the workflows and spending rules.

## Our data

Live data, not a stale database. Lead search and the employee finder run on live
sources at request time:

| Source | Company profiles | Status |
| --- | --- | --- |
| **LinkedIn** | **70M+** | 🟢 Live |
| **Google Maps** | **110M+** | 🟢 Live |
| **Corporate registry** | **100M+** | 🟢 Live |

An email is returned only when it is verified; otherwise the answer is "not found", never a guess.

## Contents

- [Our data](#our-data)
- [What you can ask](#what-you-can-ask)
- [Quick start](#quick-start)
- [Connect a client](#connect-a-client)
- [Sign-in and permissions](#sign-in-and-permissions)
- [Tools](#tools)
- [Prompts](#prompts)
- [What is charged](#what-is-charged)
- [Limits](#limits)
- [Errors](#errors)
- [Troubleshooting](#troubleshooting)
- [What's in this repository](#whats-in-this-repository)
- [Also available as](#also-available-as)

## What you can ask

Once connected, you work in plain language and the assistant picks the tools:

- *"Find 100 VPs of Marketing at fintech companies in the UK with 200–1,000 employees."*
- *"Who works in sales at stripe.com? Save the ones based in Dublin to my EMEA list."*
- *"Find the work email of Satya Nadella at microsoft.com."*
- *"What do we know about the person behind jane.doe@acme.io?"*
- *"How many points do I have left, and what would 500 more leads from that search cost?"*

A good assistant quotes the cost of a large operation before running it; the server tells it to.

## Quick start

1. **Create a Loice account** at [app.loice.ai](https://app.loice.ai) with **Continue with
   Google** or a work email and password. Personal mailboxes (Gmail, Outlook…) are not accepted.
2. **Set up your workspace**: company name and website. A connection works in one workspace and
   its calls are billed there.
3. **Start the free trial.** A new workspace starts with no points. Click **Add payment method and
   start trial** under [Settings → Billing](https://app.loice.ai/settings/account?tab=billing).
   The workspace gets **500 welcome points** for a 14-day trial, and nothing is charged today.
   Only an Owner or Admin can start the trial.
4. **Add `https://app.loice.ai/mcp` to your client** (see below), sign in to Loice in the browser
   window that opens, and approve.

## Connect a client

Every client connects to the same URL. There are two ways to authenticate:

- **OAuth sign-in** for AI assistants and editors. You add the URL, a browser opens, you sign in
  and approve. Nothing to choose, copy or store.
- **API key** for automations, scripts and your own agents (n8n, Make, a server with no browser).

| Client | OAuth sign-in | API key |
| --- | --- | --- |
| [Claude](#claude-claudeai-and-claude-desktop) | Yes | — |
| [ChatGPT](#chatgpt) | Yes | — |
| [Claude Code](#claude-code) | Yes | — |
| [Cursor](#cursor) | Yes | — |
| [VS Code](#vs-code-github-copilot) | Yes | — |
| [Gemini CLI](#gemini-cli) | Yes | — |
| [MCP Inspector](#mcp-inspector) | Yes | — |
| [Other clients](#other-clients) (n8n, Make, scripts, your own agent) | Yes, if the client supports MCP authorization | Yes |

If a client asks whether to register automatically or use a pre-registered identity, choose
**register automatically**. There is no client ID or secret to enter.

### Agent Plugins

A client that installs [Agent Plugins](https://agent-plugins.org/) can install this repository
directly: it reads [`mcp.json`](mcp.json) for the server and
[`skills/loice-prospecting`](skills/loice-prospecting/SKILL.md) for the skill. The first
connection opens the Loice sign-in.

### Claude (claude.ai and Claude Desktop)

Custom connectors are available on Free (one connector), Pro, Max, Team and Enterprise plans.

1. Open **Customize → Connectors**, click **+ Add**, choose **Add custom connector**, name it
   `Loice`, paste `https://app.loice.ai/mcp` and click **Continue**.
2. Click **Connect**, sign in to Loice in the window that opens, and approve.
3. In a conversation, click **+** → **Connectors** and switch Loice on.

On Team and Enterprise plans an Owner adds the connector once under **Organization settings →
Connectors**; members then click **Connect** on it to sign in with their own account. A connector
added on claude.ai is also available in Claude Desktop and the Claude mobile apps.

### ChatGPT

1. Open **ChatGPT Plugins**, click **+** and choose **Add custom MCP server**.
2. Name `Loice`, MCP server URL `https://app.loice.ai/mcp`, Authentication **OAuth**. Leave the
   client credentials empty — Loice supports dynamic client registration.
3. Confirm, click **Create as a plugin**, sign in to Loice and approve. In a new conversation type
   `@` and select Loice.

If you don't see **Add custom MCP server**, ask a workspace admin to allow it.

### Claude Code

```bash
claude mcp add --transport http loice https://app.loice.ai/mcp
```

Then start `claude`, run `/mcp`, select `loice` and follow the browser sign-in. Add
`--scope user` to make it available in every project, or `--scope project` to share it with your
team through `.mcp.json`.

### Cursor

`~/.cursor/mcp.json` (all projects) or `.cursor/mcp.json` (one project):

```json
{
  "mcpServers": {
    "loice": {
      "url": "https://app.loice.ai/mcp"
    }
  }
}
```

Enable Loice under **Customize**, then sign in in the browser window Cursor opens.

### VS Code (GitHub Copilot)

Run **MCP: Add Server** and choose **HTTP**, or add it to `.vscode/mcp.json`:

```json
{
  "servers": {
    "loice": {
      "type": "http",
      "url": "https://app.loice.ai/mcp"
    }
  }
}
```

Run **MCP: List Servers**, pick `loice`, choose **Start Server** and finish the sign-in.

### Gemini CLI

```bash
gemini mcp add --transport http loice https://app.loice.ai/mcp
```

or in `~/.gemini/settings.json` (use `httpUrl`; a bare `url` is treated as SSE):

```json
{
  "mcpServers": {
    "loice": {
      "httpUrl": "https://app.loice.ai/mcp"
    }
  }
}
```

Start `gemini` and run `/mcp auth loice`. No `oauth` block is needed. The sign-in needs a browser
on the same machine; on a remote shell or in a container, use an API key.

### MCP Inspector

```bash
npx @modelcontextprotocol/inspector
```

Open the printed link, choose **Streamable HTTP**, enter `https://app.loice.ai/mcp`, run the OAuth
flow from the authentication settings, then connect.

### Other clients

Any client that speaks MCP's Streamable HTTP transport works.

- **OAuth sign-in:** if the client supports MCP authorization (OAuth 2.1 with PKCE and dynamic
  client registration), point it at the URL and it offers to sign in.
- **API key:** create a workspace key under
  [Settings → API](https://app.loice.ai/settings/account?tab=api) (it is shown once) and send it as
  a header:

  ```text
  Authorization: Bearer loice_sk_…
  ```

  Never put the key in the URL — Loice refuses it there — and never in `mcp.json`: the Agent
  Plugins spec forbids secrets in plugin files. Read it from an environment variable or a secret
  manager.

Clients that only speak SSE or stdio can connect through an MCP proxy such as `mcp-remote`.

## Sign-in and permissions

Assistants connect with **OAuth 2.1** — you never paste a key into them. Loice asks you to sign in
(Google or email and password, as in the app) and shows one approval screen:

- **Who is asking.** An app that identifies itself with a Client ID Metadata Document shows its
  verified domain; any other app is marked **Unverified app**. Approve an unverified app only if
  you started the connection yourself.
- **Workspace.** The connection works in exactly one workspace and is billed there. If you belong
  to more than one, you pick it here.

Approving grants every permission your role in that workspace allows. There is no
per-connection spend cap and no confirmation threshold: the workspace balance is the only limit.

| Permission | What it allows | Spends points |
| --- | --- | --- |
| `loice:read` | Balance, prices, your lists and the results of searches already run | No |
| `loice:search` | Run lead searches and find a company's employees; stop a run | Yes |
| `loice:enrich` | Find verified emails, enrich emails and find LinkedIn profiles | Yes |
| `loice:lists` | Add people to your lead lists | No |

A tool whose permission the connection lacks is still listed, and answers `insufficient_scope`.

**Tokens.** Access tokens last an hour. Refresh tokens last 30 days, are renewed on use and live
at most 90 days. A refresh token used twice revokes the whole connection.

**Standards.** Authorization code with PKCE (S256 only), resource indicators (RFC 8707 — tokens
work only for `/mcp`), `iss` in the authorization response (RFC 9207), Client ID Metadata
Documents with Dynamic Client Registration as a fallback, protected-resource metadata (RFC 9728),
refresh-token rotation with reuse detection, and token revocation (RFC 7009).

**API keys** act for the whole workspace with every permission, so keep them in a secret store.

**Disconnecting.** Revoke a sign-in connection in the app under **MCP → Connected apps** —
removing the server from the client alone does not revoke it. A connection also ends when you
leave the workspace, when your role no longer allows a permission it holds, or when you change
your password. Revoke an API key under **Settings → API**.

### Transport and protocol

- **Transport:** Streamable HTTP.
- **Protocol revisions:** MCP **2026-07-28** (stateless, `server/discover`, multi-round-trip
  input), with fallback to **2025-11-25**, **2025-06-18** and **2025-03-26**.
- **Server version:** reported in `serverInfo`; currently **1.0.0**.

## Tools

| Tool | What it does | Permission | Billed |
| --- | --- | --- | --- |
| `get_account` | Balance, live prices, what this connection spent today, rate limits | `loice:read` | No |
| `list_filter_values` | The exact labels a search filter accepts (search the 434 industries) | `loice:read` | No |
| `search_leads` | People matching criteria (title, location, industry, headcount, seniority…), as a background run | `loice:search` | Per lead delivered |
| `find_employees` | One company's current employees, as a background run | `loice:search` | Per company + per employee delivered |
| `get_run` | A run's status; can wait up to 25 s for progress | `loice:read` | No |
| `cancel_run` | Stops a run; leads already delivered stay | `loice:search` | No |
| `get_results` | One page of 25 rows of a run or a lead list | `loice:read` | No |
| `find_email` | A verified work email from a name and company, or not found | `loice:enrich` | Per lookup |
| `enrich_email` | The person and company behind an email address | `loice:enrich` | Per lookup |
| `find_linkedin_profile` | A LinkedIn profile that states the name and employer | `loice:enrich` | Per search |
| `list_lead_lists` | Your lead lists | `loice:read` | No |
| `add_to_lead_list` | Save people from a run to a list | `loice:lists` | No |

**Resources:** `loice://runs/{id}` and `loice://lists/{id}` expose a run or a list to clients that
read resources.

**Prices.** Every tool description carries its current price, and `get_account` lists all prices.
Call a billed tool with `dry_run: true` for an exact quote without charging anything.

**Results.** Every tool declares an `outputSchema`, and every result — an answer, a `dry_run`
quote or an error — returns `structuredContent` that conforms to it. The text block repeats it: a
short summary, a blank line, then the same `structuredContent` as compact JSON. A billed tool's
result adds a `billing` block (`charged_points`, `quote_points`, `price_key`, `replayed`). A
`get_results` row carries its company once, as `person.company`.

**Filters.** Closed-set filters (headcount, seniority, job function, years of experience) are
listed in each tool's schema; industry labels come from `list_filter_values`. A value outside the
list is refused for free, and the refusal names the allowed values (or the closest industry
labels). Unknown arguments are refused, never ignored.

**Annotations.** `cancel_run` is marked destructive and every billed tool is marked not
read-only, so assistants that honour tool annotations ask before calling them.

**Emails.** Search results carry no email unless your workspace already bought it. To get emails
for people from a search, the assistant calls `find_email` in `linkedin` mode with each person's
LinkedIn URL, after quoting the total. It never guesses or constructs an address.

### A typical session

1. **Quote.** `get_account` (balance, prices), then `search_leads` with `dry_run: true`; the
   assistant tells you the cost.
2. **Run and poll.** `search_leads` for real returns a run id; `get_run` until the run finishes.
3. **Page.** `get_results`, 25 rows per page, instead of repeating the search.
4. **Save or enrich.** `add_to_lead_list` for the people you want, or `find_email` for verified
   emails for some of them.

## Prompts

Assistants that show MCP prompts (often as slash commands) offer three ready-made workflows:

| Prompt | What it does |
| --- | --- |
| `build_prospect_list` | From an ideal-customer description to a saved lead list, then optional emails |
| `find_decision_makers` | The senior people at one company, then optional emails |
| `enrich_contacts` | Verified emails for contacts you already have (LinkedIn URLs, names, emails) |

A prompt only writes the plan into the conversation: it spends nothing, and every billed step is
quoted first. Industry, seniority and function arguments offer completion.

## What is charged

Billing is the same as in the app and the [API](https://docs.loice.ai/billing), at the same
prices:

| Outcome | Charged |
| --- | --- |
| Answered with a result | Yes, the price in the tool description |
| Answered "not found" (the lookup completed and found nothing) | Yes, the same price |
| A lead or employee run that delivers 0 rows | No |
| Provider unavailable or timed out, or a failure on our side | **No** |
| Validation error, missing permission, sign-in error, balance refusal, rate limited, do-not-contact refusal | **No** |
| Retry with the same idempotency key (sent, or derived from an identical call within 10 minutes) | **No** — the first outcome is replayed (`replayed: true`) |
| Cancelled run | Only the rows delivered before the cancel |

Every billed result says what it cost in `billing.charged_points`; a `dry_run: true` call quotes
the most a call can charge (`billing.quote_points`) and charges nothing.

## Limits

- **Spending:** the workspace balance is the only limit. A call the balance cannot cover answers
  `insufficient_credits` and is not charged.
- **One search at a time:** a workspace runs one lead or employee search at a time
  (`run_already_active`). Follow it with `get_run`, or stop it with `cancel_run`.
- **Request budgets:** each tool family has a per-workspace request budget, shared with the app
  and the API (see [Rate limits](https://docs.loice.ai/rate-limits)); `get_account` lists them
  under `limits`. A spent budget answers `rate_limited` with `retry_after_seconds`, before any
  billable work, and is never charged.
- **Sizes:** `get_results` and `list_lead_lists` return 25 rows per page; `search_leads` delivers
  up to 10,000 leads per run; `add_to_lead_list` takes up to 500 rows per call; `get_run` waits at most
  25 seconds.

## Errors

A business outcome is a tool result with `isError: true` and
`structuredContent.error = { code, message, retryable, charged, retry_after_seconds?, details? }`.
The codes are the API's (see [Errors](https://docs.loice.ai/errors)) plus:

| Code | Meaning |
| --- | --- |
| `card_required` | No payment method is added, so the trial has not started and paid tools are off. Not charged. |
| `trial_ended` | The trial is over and the balance cannot cover the call. Not charged. |
| `insufficient_credits` | The balance cannot cover the call. Not charged; `retryable` is false. |
| `insufficient_scope` | The connection was not granted the permission this tool needs. |
| `provider_unavailable` | A data provider did not answer. Not charged; `retryable` says whether retrying can help (a blocked page is not retryable: use `search_leads` with the company name). |

`card_required`, `trial_ended` and `insufficient_credits` say what to do in `message` and carry
the Billing page in `details.url`, with `details.action` (`attach_card`, `choose_plan`,
`buy_points`) and, when known, `details.required` and `details.available`. A run the balance stops
mid-way keeps what it delivered; `get_run` then adds `stopped_by` and `billing_url`.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| The client can't sign in or "can't register" | The URL must be exactly `https://app.loice.ai/mcp`. |
| Every call fails with `401` | The credential was revoked, expired or is wrong. For a sign-in connection, remove the server from the client and add it again. For an API key, create a new one under **Settings → API**. |
| The browser sign-in never opens | The client may not support MCP authorization, or you are on a machine without a browser. Use an API key ([Other clients](#other-clients)). |
| A call says `card_required` | Add a payment method under [Settings → Billing](https://app.loice.ai/settings/account?tab=billing) to start the free trial; nothing is charged today. |
| A call says `trial_ended` | Choose a plan under [Settings → Billing](https://app.loice.ai/settings/account?tab=billing); the refused call was not charged. |
| A call says `insufficient_credits` | Buy points or change the plan under [Settings → Billing](https://app.loice.ai/settings/account?tab=billing); the refused call was not charged. |
| A call says `insufficient_scope` | Your role does not allow that tool, or the client asked for less than it needs. Reconnect, or ask a workspace owner about your role. |
| A tool is missing | The client caps or filters tools, or the connection lacks the permission. Check the client's tools picker. |

## What's in this repository

| Path | What it is |
| --- | --- |
| [`plugin.json`](plugin.json) | Agent Plugins manifest (spec 1.0.0) |
| [`mcp.json`](mcp.json) | The hosted Loice MCP server: `https://app.loice.ai/mcp` (Streamable HTTP) |
| [`skills/loice-prospecting/`](skills/loice-prospecting/SKILL.md) | An Agent Skill with workflows and spending rules for the Loice tools |
| `assets/icon.png`, `assets/icon.svg` | Plugin icon |

## Also available as

- **MCP Registry:** `ai.loice/mcp` on
  [registry.modelcontextprotocol.io](https://registry.modelcontextprotocol.io/v0.1/servers?search=ai.loice/mcp)
- **Direct URL:** add `https://app.loice.ai/mcp` as a remote MCP server in any client

## Docs

- [MCP server](https://docs.loice.ai/mcp-server): tools, prices, permissions, errors, changelog
- [Connect MCP](https://docs.loice.ai/connect-mcp): per-client setup
- [Plans and points](https://docs.loice.ai/plans-and-points) · [Rate limits](https://docs.loice.ai/rate-limits) · [Errors](https://docs.loice.ai/errors)

## License

[MIT](LICENSE)
