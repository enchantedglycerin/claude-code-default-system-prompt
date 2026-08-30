# claude-code-default-system-prompt

The default system prompt that Claude Code (the `claude` CLI) sends to the model, captured from v2.1.251.

## what's actually in system-prompt

Just the identity line ("You are Claude Code…") followed by the default body. The 34 tool definitions and the live environment block (working directory, OS, model, available skills, date) are sent seperately by claude code.

Machine-specific paths are swapped for placeholders — `<USERPROFILE>`, `<PROJECT_KEY>`, `<SESSION_ID>`. That last one is the session UUID that shows up in the scratchpad path; it's random every run unless you pin it with `--session-id <uuid>`.

## using custom system prompt

- `--system-prompt "…"` replaces the body but keeps the identity line and all the tools.
- `--append-system-prompt "…"` keeps the default system-prompt and tacks yours onto the end.
- Both have `-file` variants that read from a file instead.
claude --system-prompt-file default-system-prompt.md
```

Not official, not affiliated with Anthropic — I just pulled it out of the CLI because I was curious. It'll drift whenever they ship a new version, and the prompt text itself is Anthropic's.
