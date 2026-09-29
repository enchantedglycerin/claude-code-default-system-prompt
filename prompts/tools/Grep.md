# Grep

Content search built on ripgrep. Prefer this over `grep`/`rg` via Bash — results integrate with the permission UI and file links.

- Full regex syntax (e.g. "log.*Error", "function\s+\w+"). Ripgrep, not grep — escape literal braces (`interface\{\}`).
- Filter with `glob` (e.g. "**/*.tsx") or `type` (e.g. "js", "py", "rust").
- `output_mode`: "content" (matching lines), "files_with_matches" (paths only, default), or "count".
- `multiline: true` for patterns that span lines.

## parameters

- `pattern` **(required)** — string: The regular expression pattern to search for in file contents
- `path` — string: File or directory to search in (rg PATH). Defaults to current working directory.
- `glob` — string: Glob pattern to filter files (e.g. "*.js", "*.{ts,tsx}") - maps to rg --glob
- `output_mode` — string: Output mode: "content" shows matching lines (supports -A/-B/-C context, -n line numbers, head_limit), "files_with_matches" shows file paths (supports head_limit), "count" shows match counts (supports head_limit). Defaults to "files_with_matches".
- `-B` — number: Number of lines to show before each match (rg -B). Requires output_mode: "content", ignored otherwise.
- `-A` — number: Number of lines to show after each match (rg -A). Requires output_mode: "content", ignored otherwise.
- `-C` — number: Alias for context.
- `context` — number: Number of lines to show before and after each match (rg -C). Requires output_mode: "content", ignored otherwise.
- `-n` — boolean: Show line numbers in output (rg -n). Requires output_mode: "content", ignored otherwise. Defaults to true.
- `-i` — boolean: Case insensitive search (rg -i)
- `-o` — boolean: Print only the matched (non-empty) parts of each matching line, one match per output line (rg -o / --only-matching). Requires output_mode: "content", ignored otherwise. Defaults to false.
- `type` — string: File type to search (rg --type). Common types: js, py, rust, go, java, etc. More efficient than include for standard file types.
- `head_limit` — number: Limit output to first N lines/entries, equivalent to "| head -N". Works across all output modes: content (limits output lines), files_with_matches (limits file paths), count (limits count entries). Defaults to 250 when unspecified. Pass 0 for unlimited (use sparingly — large result sets waste context).
- `offset` — number: Skip first N lines/entries before applying head_limit, equivalent to "| tail -n +N | head -N". Works across all output modes. Defaults to 0.
- `multiline` — boolean: Enable multiline mode where . matches newlines and patterns can span lines (rg -U --multiline-dotall). Default: false.
