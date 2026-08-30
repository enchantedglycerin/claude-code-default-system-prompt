# claude-code-default-system-prompt

Claude Code's default system prompt, pulled straight out of the CLI (v2.1.251).
`default-system-prompt.md` is the prompt itself; `generate_default_prompt.py` re-grabs it if you want to check a newer build.

### how it was grabbed

Claude Code builds its request locally before sending it off. The script points `ANTHROPIC_BASE_URL` at a little local server, runs `claude`, and captures the request body it tries to send — so nothing actually reaches Anthropic and it costs nothing. This is really the only reliable way to get it: the prompt is assembled at runtime with your paths baked in, so you can't just grep it out of the binary.

```bash
pip install pywinpty
python generate_default_prompt.py --identity --genericize
```

### a few things worth knowing

- This is only the `system` field. The 34 tool definitions and the environment block (cwd, OS, model, date…) get sent separately and aren't in here.
- Paths are swapped for placeholders. `<SESSION_ID>` is the session UUID — random each run unless you pass `--session-id`.
- `--system-prompt "…"` replaces the body but keeps the "You are Claude Code" line and all the tools. `--append-system-prompt` adds to it instead.

Not official and not from Anthropic — just extracted out of curiosity, and it'll probably drift on the next release. The prompt text is Anthropic's.
