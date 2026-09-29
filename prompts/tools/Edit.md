# Edit

Performs exact string replacement in a file.

- You must Read the file in this conversation before editing, or the call will fail.
- `old_string` must match the file exactly, including indentation, and be unique — the edit fails otherwise. Strip the Read line prefix (line number + tab) before matching.
- `replace_all: true` replaces every occurrence instead.

## parameters

- `file_path` **(required)** — string: The absolute path to the file to modify
- `old_string` **(required)** — string: The text to replace
- `new_string` **(required)** — string: The text to replace it with (must be different from old_string)
- `replace_all` — boolean: Replace all occurrences of old_string (default false)
