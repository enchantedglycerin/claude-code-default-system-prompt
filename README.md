# claude-code-reversed

**What Claude Code actually sends the model — pulled out of the binary, with the method shown so you can redo it yourself.**

Claude Code ships as a Bun-compiled binary. This is its prompt surface, reverse-engineered from **v2.1.285**: the per-model system prompts, the full gated harness, every tool definition, and the subagent/variant prompts — plus the scripts that extract them, so it stays reproducible instead of rotting like the older dumps.

There's no single "default" prompt: Claude Code composes a different one per model and mode from conditionally-gated sections. This covers the whole thing, not one slice.

## layout

```
harness/
  HARNESS.md     every section + the exact condition that turns it on
  sections/      each harness section as its own file (~25)
prompts/
  models/        the assembled system prompt per model (opus-4-8, opus-5-5, fable-5, fable-5-1)
  tools/         every tool's description + schema (~36) — sent in the tools array each turn
  subagents/     the wrapper built-in subagents run their thread under
  variants/      the SDK/-p prompt, the output-style opener
scripts/         the method: capture + extract + analyze
```

## highlights

- **The harness map** — [`harness/HARNESS.md`](harness/HARNESS.md) lists every section Claude Code *can* inject, each with its gate (env var / experiment flag / model / mode), including ones no capture ever shows: the expanded-mode `# System` and `# Executing actions with care`, the Fable identity block, the opus-5 delegation limiter.
- **Per-model, and it moves.** Fable 5.1 went from a ~240-token minimal prompt to ~3k tokens across releases; Opus 5 was retired into 5.5. Re-run the scripts each version and diff.
- **The method is in the repo** — the part the other prompt dumps leave out.

## reproduce it

```bash
pip install pywinpty
python scripts/generate_default_prompt.py --model claude-opus-5-5   # live-capture any model
python scripts/extract_bundle.py                                    # carve the JS bundle from your own claude
python scripts/analyze.py --fn <name>                               # read any function from the bundle
```

Live capture points a real `claude` run at a localhost logger and records the request it builds — nothing reaches Anthropic, no tokens spent. Static extraction pulls the gated sections a capture can't trigger. The extracted bundle is Anthropic's code, so it's gitignored — run the tools on your own install.

## custom system prompts

- `--system-prompt "…"` replaces the body but keeps the identity line and all the tools
- `--append-system-prompt "…"` keeps the default and tacks yours onto the end
- both have `-file` variants: `claude --system-prompt-file prompts/models/opus-5-5.md`

## caveats

Unofficial, extracted for research; prompt text © Anthropic. Captured at v2.1.285. Sections are conditionally gated, so no single session contains them all, and dynamic pieces (model IDs, paths, git, date) fill at runtime. Not affiliated with or endorsed by Anthropic.
