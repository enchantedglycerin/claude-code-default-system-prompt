# claude-code-default-system-prompt

The prompts Claude Code (the `claude` CLI) sends to the model — captured and extracted from **v2.1.285**, with the **method included** so it's reproducible and won't go stale.

There's no single "default": Claude Code composes a different system prompt per model and mode, from a set of conditionally-gated sections. This repo covers the whole surface, not just one slice.

## layout

```
harness/
  HARNESS.md        the full map — every section + the exact gate that turns it on
  sections/         each harness section as its own file (~25)
prompts/
  models/           the assembled system prompt per model (opus-4-8, opus-5-5, fable-5, fable-5-1)
  tools/            every tool's description + schema (~36) — sent in the `tools` array each turn
  subagents/        the wrapper built-in subagents run their thread under
  variants/         the SDK/-p prompt, the output-style opener
scripts/            the method (below)
```

## the pieces

- **`prompts/models/`** — the `system`-field prompt each model actually receives (identity + body). Model-dependent, and it shifts between releases (Fable 5.1 went from a ~240-token minimal prompt to ~3k tokens across versions). Paths are placeholdered.
- **`harness/HARNESS.md`** — the superset: every section Claude Code *can* inject, each with its condition (env var / experiment flag / model / mode) — including ones no single capture shows: the expanded-mode `# System` and `# Executing actions with care`, the Fable identity block, the opus-5 delegation limiter. `harness/sections/` splits it one-per-file.
- **`prompts/tools/`** — the ~36 tool definitions. They ride in the API `tools` array every turn, so they're part of what the model sees (just not in the `system` field).
- **`prompts/subagents/`** — subagents run the *same* harness; this is the extra opener + notes their thread is wrapped with.
- **`prompts/variants/`** — the leaner SDK/`-p` prompt and the output-style opener.

## the method (`scripts/`)

- `generate_default_prompt.py` — **live capture**: points a real `claude` run at a localhost logger and records the request it builds. `--model <id>` for any model. Nothing reaches Anthropic; no tokens spent.
- `extract_bundle.py` — carves the Bun-embedded JS bundle out of your own `claude` binary (it's JavaScript *source* — no decompiler needed).
- `analyze.py` — beautify-on-demand: `--fn <name>` pulls any whole function from the bundle.

Two passes: **static extraction** gets every gated section + its condition (even ones a capture can't trigger); **live capture** confirms which fire and fills the dynamic values (model-ID line, paths). The extracted bundle is Anthropic's code, so it's gitignored — run the tools on your own install.

## using a custom system prompt

- `--system-prompt "…"` replaces the body but keeps the identity line and all the tools.
- `--append-system-prompt "…"` keeps the default and tacks yours onto the end.
- Both have `-file` variants: `claude --system-prompt-file prompts/models/opus-5-5.md`

## caveats

Unofficial, extracted for research; prompt text © Anthropic. v2.1.285. Sections are conditionally gated, so no single session contains them all — dynamic pieces (model IDs, paths, git, date) are filled at runtime. Not affiliated with or endorsed by Anthropic.
