# WebSearch

Search the web. Returns result blocks with titles and URLs. US-only.

- The current month is (provided in the conversation below) — use this when searching for recent information.
- `allowed_domains` / `blocked_domains` filter results.
- After answering from results, end with a "Sources:" list of the URLs you used as markdown links.

## parameters

- `query` **(required)** — string: The search query to use
- `allowed_domains` — array: Only include search results from these domains
- `blocked_domains` — array: Never include search results from these domains
