# claude-code-default-system-prompt

The system prompt Claude Code (the `claude` CLI) sends to the model, captured from v2.1.283. There's no single "default" — Claude Code sends a different prompt per model, so `prompts/` has one file per model.

## what's in each file

Just the identity line ("You are Claude Code…") followed by that model's default body. The 34 tool definitions and the live environment block (working directory, OS, model, available skills, date) are sent separately by Claude Code, so they're not in here.

Machine-specific paths are swapped for placeholders — `<USERPROFILE>`, `<PROJECT_KEY>`, `<SESSION_ID>`. That last one is the session UUID that shows up in the scratchpad path; it's random every run unless you pin it with `--session-id <uuid>`.

## prompts/ — one per model

The prompt differs per model, and shifts a lot between releases:

- `opus-4-8.md` — standard 5 sections (~1.5k tokens)
- `opus-5-5.md` — current flagship Opus; standard 5 sections, with a newer `# Harness` that adds a pasted-content injection guard (~1.6k tokens). Opus 5 has been retired — `claude-opus-5` now resolves to 5.5.
- `fable-5.md` — adds `# Communicating with the user` (~2.6k tokens)
- `fable-5-1.md` — the biggest, with `# Delivering work` and `# Writing for the user` (~3.1k tokens). In older versions this was the *minimal* one (identity + `# Reporting outcomes`, ~240 tokens) — a good example of how much these move between releases.

Grab any model yourself with `generate_default_prompt.py --model <id>`.

## using a custom system prompt

- `--system-prompt "…"` replaces the body but keeps the identity line and all the tools.
- `--append-system-prompt "…"` keeps the default system prompt and tacks yours onto the end.
- Both have `-file` variants that read from a file instead. (Ex. `claude --system-prompt-file prompts/opus-5-5.md`)

## regenerating

`generate_default_prompt.py` re-captures these straight from your installed CLI (`pip install pywinpty` first). Run it in a fresh folder and it auto-marks the dir trusted in `~/.claude.json` — the same thing accepting Claude Code's "do you trust this folder?" dialog does — so the capture doesn't hang. Pass `--no-trust` to skip that.
