# claude-code-default-system-prompt

The default system prompt that Claude Code (the `claude` CLI) sends to the model, captured from v2.1.251. `default-system-prompt.md` is the prompt itself; `generate_default_prompt.py` is the script I used to pull it, so you can re-run it against whatever version you happen to have installed.

## how it was captured

Claude Code assembles the whole request on your machine before it sends anything. So rather than trying to carve it out of the 217 MB Bun-compiled binary, the script takes the easy road: it stands up a tiny local HTTP server, sets `ANTHROPIC_BASE_URL` to point at it, and runs `claude`. Claude builds its real request and POSTs it to the local server, which just logs the body and returns an error. Nothing ever reaches Anthropic, so it doesn't cost a token.

Capturing it live turned out to be the only reliable way. The prompt isn't a static string sitting in the binary — it's stitched together at runtime from a pile of fragments plus live values (your working directory, the session id, and so on), and the exact set of sections depends on how you launched it. Reconstructing that statically just gives you a stale, slightly-wrong guess.

```bash
pip install pywinpty
python generate_default_prompt.py --identity --genericize
```

## what's actually in here

Just the `system` field: the identity line ("You are Claude Code…") followed by the default body. The 34 tool definitions and the live environment block (working directory, OS, model, available skills, date) are sent as separate parts of the request, so they're not in this file.

Machine-specific paths are swapped for placeholders — `<USERPROFILE>`, `<PROJECT_KEY>`, `<SESSION_ID>`. That last one is the session UUID that shows up in the scratchpad path; it's random every run unless you pin it with `--session-id <uuid>`.

## the --system-prompt flags, while we're here

- `--system-prompt "…"` replaces the body but keeps the identity line and all the tools.
- `--system-prompt ''` leaves you with identity + tools + environment and no behavioral instructions at all.
- `--append-system-prompt "…"` keeps the default and tacks yours onto the end.
- Both have `-file` variants that read from a file instead.

So to run Claude Code on an edited copy of this, drop the identity line (it gets added back automatically) and point it at your file:

```bash
claude --system-prompt-file default-system-prompt.md
```

## fine print

Not official, not affiliated with Anthropic — I just pulled it out of the CLI because I was curious. It'll drift whenever they ship a new version, and the prompt text itself is Anthropic's.
