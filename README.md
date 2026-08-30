# Claude Code — default system prompt

The default **system prompt** that Claude Code (the `claude` CLI) sends to the model, captured live from the running binary — plus a script to regenerate it for whatever version you have installed.

- **Captured from:** Claude Code `v2.1.251` (`cc_entrypoint=cli`, model `claude-opus-4-8`)
- **[`default-system-prompt.md`](default-system-prompt.md)** — the `system` field: the identity line + the default behavioral body
- **[`generate_default_prompt.py`](generate_default_prompt.py)** — regenerate it yourself, so it's never stale

> ⚠️ **Unofficial.** Community-extracted for transparency/research. This is **not** published by Anthropic, may change between versions, and the prompt text is © Anthropic. Not affiliated with or endorsed by Anthropic.

## How it was captured (no API calls, no tokens)

Claude Code assembles its request locally, then sends it to Anthropic. This tool points `ANTHROPIC_BASE_URL` at a **localhost** logger, runs `claude`, and records the assembled `POST /v1/messages` body before it would go out. Nothing reaches Anthropic and nothing is billed.

Why capture instead of reading it from the binary? The system prompt is only fully materialized at request-build time (it embeds live paths and per-session values), so capturing the built request is the only way to get it *exactly*. Static reconstruction from the binary is approximate and drifts every version.

## Regenerate it

```bash
pip install pywinpty                                # interactive capture (Windows)
python generate_default_prompt.py                  # exact, current version, real paths
python generate_default_prompt.py --genericize     # paths replaced with <PLACEHOLDERS>
python generate_default_prompt.py --identity       # include the "You are Claude Code" identity line
python generate_default_prompt.py --mode print     # leaner SDK / -p prompt (no pywinpty needed)
```

## What's in this file — and what isn't

The full request the model receives has three parts; **only the first is in this repo:**

1. **`system` field** — the identity line (auto-added) + the default body → *this file*
2. **`tools` array** — 34 tool schemas (Bash, Edit, Read, Grep, …) — sent separately, not in the prompt
3. **`role=system` message** — the live environment (cwd, git status, OS, model, skills list, date) — dynamic, sent inside `messages`

## Placeholders (genericized file)

- `<USERPROFILE>` — your home directory
- `<PROJECT_KEY>` — the working directory with `:` `\` `/` replaced by `-`
- `<SESSION_ID>` — the session UUID in the scratchpad path

The scratchpad UUID **is** the session id. Random per session by default, but controllable:

- `claude --session-id <uuid> …` — used verbatim, or
- `CLAUDE_CODE_REMOTE_SESSION_ID=<str>` — derived deterministically as
  `uuid5("3ab19d7e-9f35-45c2-926e-75e271cc60b3", str)`

## How `--system-prompt` interacts with this

- `--system-prompt "X"` replaces **only the body** (block 2). The identity line is auto-kept, and all tools + the environment message are preserved.
- `--system-prompt ''` yields identity + tools + env with **no** behavioral body.
- `--append-system-prompt "X"` keeps the default body and appends `X`.
- `--system-prompt-file <path>` / `--append-system-prompt-file <path>` — same, from a file.

So to run Claude Code on an edited copy of this prompt: edit `default-system-prompt.md`, then
`claude --system-prompt-file default-system-prompt.md` (omit the identity line — it's auto-added).
