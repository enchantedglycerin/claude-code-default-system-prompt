# claude-code-default-system-prompt

The system prompt Claude Code (the `claude` CLI) sends to the model, captured from v2.1.285. There's no single "default" — Claude Code sends a different prompt per model, so `prompts/` has one file per model. For the *complete* set of sections (not just what one model emits), see [`HARNESS.md`](HARNESS.md).

## what's in each file

Just the identity line ("You are Claude Code…") followed by that model's default body. The tool definitions and the live environment block (working directory, OS, model, available skills, date) are sent separately by Claude Code, so they're not in here.

Machine-specific paths are swapped for placeholders — `<USERPROFILE>`, `<PROJECT_KEY>`, `<SESSION_ID>`. That last one is the session UUID that shows up in the scratchpad path; it's random every run unless you pin it with `--session-id <uuid>`.

## prompts/ — one per model

The prompt differs per model, and shifts a lot between releases:

- `opus-4-8.md` — standard 5 sections (~1.5k tokens)
- `opus-5-5.md` — current flagship Opus; standard 5 sections, with a newer `# Harness` that adds a pasted-content injection guard (~1.6k tokens). Opus 5 has been retired — `claude-opus-5` now resolves to 5.5.
- `fable-5.md` — adds `# Communicating with the user` (~2.6k tokens)
- `fable-5-1.md` — the biggest, with `# Delivering work` and `# Writing for the user` (~3.1k tokens). In older versions this was the *minimal* one (identity + `# Reporting outcomes`, ~240 tokens) — a good example of how much these move between releases.

Grab any model yourself with `generate_default_prompt.py --model <id>`.

## the whole harness

A per-model file only shows the sections that fired for that model. [`HARNESS.md`](HARNESS.md) is the full map — **every** section Claude Code can put in the prompt, each with the exact condition that switches it on (env var, experiment flag, model, mode) — including ones no capture triggers, like the expanded-mode `# System` block, the Fable identity, and the opus-5 delegation limiter. Reconstructed by static extraction from the binary and cross-checked against the live captures.

The method is in [`tools/`](tools): `extract_bundle.py` carves the JS bundle out of your own `claude` binary (it's Bun-compiled — JavaScript source, no decompiler needed), and `analyze.py` reads/beautifies any function from it. The extracted bundle is Anthropic's code, so it's gitignored, not shipped — run the tools on your own install.

## using a custom system prompt

- `--system-prompt "…"` replaces the body but keeps the identity line and all the tools.
- `--append-system-prompt "…"` keeps the default system prompt and tacks yours onto the end.
- Both have `-file` variants that read from a file instead. (Ex. `claude --system-prompt-file prompts/opus-5-5.md`)

## regenerating

`generate_default_prompt.py` re-captures these straight from your installed CLI (`pip install pywinpty` first). Run it in a fresh folder and it auto-marks the dir trusted in `~/.claude.json` — the same thing accepting Claude Code's "do you trust this folder?" dialog does — so the capture doesn't hang. Pass `--no-trust` to skip that.
