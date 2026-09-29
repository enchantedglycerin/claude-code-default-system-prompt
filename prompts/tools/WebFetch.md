# WebFetch

Fetches a URL, converts the page to markdown, and answers `prompt` against it using a small fast model.

- Fails on authenticated/private URLs — use an authenticated MCP tool or `gh` for those instead. claude.ai artifact links (claude.ai/artifact/{id} or claude.ai/code/artifact/{uuid}) are published artifacts: read them with the Artifact tool (action "read"), not WebFetch or curl.
- Fails on localhost and other hostnames without a dot; for a local server, use curl via Bash.
- HTTP is upgraded to HTTPS. Cross-host redirects are returned to you rather than followed; call again with the redirect URL.
- Responses are cached for 15 minutes per URL.

## parameters

- `url` **(required)** — string: The URL to fetch content from
- `prompt` **(required)** — string: The prompt to run on the fetched content
