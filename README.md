# claude-code-default-system-prompt

The default system prompt that Claude Code (the `claude` CLI) sends to the model, captured from v2.1.283.

## what's actually in the system prompt

Just the identity line ("You are Claude Code…") followed by the default body. The 34 tool definitions and the live environment block (working directory, OS, model, available skills, date) are sent separately by Claude Code.

Machine-specific paths are swapped for placeholders — `<USERPROFILE>`, `<PROJECT_KEY>`, `<SESSION_ID>`. That last one is the session UUID that shows up in the scratchpad path; it's random every run unless you pin it with `--session-id <uuid>`.

## it depends on the model

Claude Code doesn't send one prompt — it sends a different one per model, and it shifts a lot between releases. This main file is Opus 4.8; `variants/` has the rest, all captured the same way:

- `opus-5-5.md` — current flagship Opus; the standard 5 sections, with a newer `# Harness` that adds a pasted-content injection guard (~1.6k tokens). Opus 5 has been retired — `claude-opus-5` now resolves to 5.5.
- `fable-5.md` — adds `# Communicating with the user` (~2.6k tokens)
- `fable-5-1.md` — now the biggest, with `# Delivering work` and `# Writing for the user` (~3.1k tokens). In older versions this was the *minimal* one (identity + `# Reporting outcomes`, ~240 tokens) — a good example of how much these move between releases.

Grab any of them yourself with `generate_default_prompt.py --model <id>`.

## using custom system prompt

- `--system-prompt "…"` replaces the body but keeps the identity line and all the tools.
- `--append-system-prompt "…"` keeps the default system prompt and tacks yours onto the end.
- Both have `-file` variants that read from a file instead. (Ex. claude --system-prompt-file default-system-prompt.md)

## regenerating

`generate_default_prompt.py` re-captures this straight from your installed CLI (`pip install pywinpty` first). Run it in a fresh folder and it auto-marks the dir trusted in `~/.claude.json` — the same thing accepting Claude Code's "do you trust this folder?" dialog does — so the capture doesn't hang. Pass `--no-trust` to skip that.
