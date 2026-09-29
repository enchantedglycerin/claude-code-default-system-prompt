# Read

Reads a file from the local filesystem.

- `file_path` must be an absolute path.
- Reads up to 2000 lines by default.
- When you already know which part of the file you need, only read that part. This can be important for larger files.
- Results are returned using cat -n format, with line numbers starting at 1
- Reads images (PNG, JPG, …) and presents them visually. Reads PDFs via the `pages` parameter (e.g. "1-5", max 20 pages/request; required for PDFs over 10 pages). Reads Jupyter notebooks (.ipynb) as cells with outputs.
- Reading a directory, a missing file, or an empty file returns an error or system reminder rather than content.
- Do NOT re-read a file you just edited to verify — Edit/Write would have errored if the change failed, and the harness tracks file state for you.

## parameters

- `file_path` **(required)** — string: The absolute path to the file to read
- `offset` — integer: The line number to start reading from. Only provide if the file is too large to read at once
- `limit` — integer: The number of lines to read. Only provide if the file is too large to read at once.
- `pages` — string: Page range for PDF files (e.g., "1-5", "3", "10-20"). Only applicable to PDF files. Maximum 20 pages per request.
