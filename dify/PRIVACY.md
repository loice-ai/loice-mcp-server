# Privacy policy: Loice plugin for Dify

This plugin is a thin client of the Loice MCP server at `https://app.loice.ai/mcp`, run by
Loice. It has no server, database or storage of its own.

## What the plugin sends, and to whom

- **Only to Loice** (`app.loice.ai`, over HTTPS). The plugin calls no other service.
- **Your Loice API key**, as an `Authorization: Bearer` header on every call. Dify stores the
  key encrypted as a tool credential; the plugin never logs or returns it.
- **The arguments of each tool call**: search filters (job titles, companies, locations, ...),
  names, company names or domains, LinkedIn profile URLs, email addresses to enrich or websites
  to analyse, exactly as your app or agent passes them.

## What comes back

Business contact data about the people and companies you search for: names, job titles,
employers, LinkedIn URLs, verified work emails and company profiles. People on a
do-not-contact list are never returned. The results go to your Dify app; what Dify then keeps is
governed by your Dify deployment.

## What the plugin stores or logs

Nothing. It keeps no cache, writes no files and sends no telemetry.

## What Loice does with it

Loice processes the calls to run them, bills them against your workspace's points, and keeps
the records described in its privacy notice. Loice is the controller of that processing. See the
[Loice Privacy Center](https://loice.ai/privacy-center/) for the policy, data-subject rights and
opt-out.

Contact: sales@loice.ai
