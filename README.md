# claude-code-default-system-prompt

The default system prompt that Claude Code (the `claude` CLI) sends to the model, captured from v2.1.251.

## what's actually in system-prompt

Just the identity line ("You are Claude Code…") followed by the default body. The 34 tool definitions and the live environment block (working directory, OS, model, available skills, date) are sent seperately by claude code.

Machine-specific paths are swapped for placeholders — `<USERPROFILE>`, `<PROJECT_KEY>`, `<SESSION_ID>`. That last one is the session UUID that shows up in the scratchpad path; it's random every run unless you pin it with `--session-id <uuid>`.

## using custom system prompt

- `--system-prompt "…"` replaces the body but keeps the identity line and all the tools.
- `--append-system-prompt "…"` keeps the default system-prompt and tacks yours onto the end.
- Both have `-file` variants that read from a file instead. (Ex. claude --system-prompt-file default-system-prompt.md)

## regenerating

`generate_default_prompt.py` re-captures this straight from your installed CLI (`pip install pywinpty` first). Run it in a fresh folder and it auto-marks the dir trusted in `~/.claude.json` — the same thing accepting Claude Code's "do you trust this folder?" dialog does — so the capture doesn't hang. Pass `--no-trust` to skip that.
