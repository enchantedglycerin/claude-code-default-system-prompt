# Write

Writes a file to the local filesystem, overwriting if one exists.

When to use: creating a new file, or fully replacing one you've already Read. Overwriting an existing file you haven't Read will fail. For partial changes, use Edit instead.

## parameters

- `file_path` **(required)** — string: The absolute path to the file to write (must be absolute, not relative)
- `content` **(required)** — string: The content to write to the file
