# Bash

Executes a bash command and returns its output.

This tool runs Git Bash (POSIX sh), not cmd.exe or PowerShell. Use Unix shell syntax: `/dev/null` not `NUL`, forward slashes, `$VAR` not `%VAR%` or `$env:VAR`. Do not use PowerShell here-strings (`@'…'@`) or backtick continuation here — for multi-line strings use a heredoc.

- Working directory persists between calls, but prefer absolute paths — `cd` in a compound command can trigger a permission prompt. Shell state (env vars, functions) does not persist; the shell is initialized from the user's profile.
- Command output is displayed to you, not reliably to the user.
- `timeout` is in milliseconds: default 120000, max 600000 for a foreground command.
- `run_in_background` runs the command detached: it keeps running across turns and re-invokes you when it exits. With it, `timeout` is how long the command may run in the background (default 1800000, max 7200000); at that limit it is stopped and you are re-invoked. No `&` needed. Foreground `sleep` is blocked; use Monitor with an until-loop to wait on a condition.

# Git
- Interactive flags (`-i`, e.g. `git rebase -i`, `git add -i`) are not supported in this environment.
- Use the `gh` CLI for GitHub operations (PRs, issues, API).
- Commit or push only when the user asks. If on the default branch, branch first.
- End git commit messages and PR bodies with the attribution lines given in the conversation's system-reminder, when one is present.

## parameters

- `command` **(required)** — string: The command to execute
- `timeout` — number: Optional timeout in milliseconds (max 600000 for a foreground command)
- `description` — string: Clear, concise description of what this command does in active voice. Never use words like "complex" or "risk" in the description - just describe what it does.  Say what the command does in plain words: do not echo the command's text, its flags, or file paths - the user reads this description, often without seeing the command.  For simple commands (git, npm, standard CLI tools), keep it brief (5-10 words): - ls → "List files in current directory" - git status → "Show working tree status" - npm install → "Install package dependencies"  For commands that are harder to parse at a glance (piped commands, obscure flags, etc.), add enough context to clarify what it does: - find . -name "*.tmp" -exec rm {} \; → "Find and delete all .tmp files recursively" - git reset --hard origin/main → "Discard all local changes and match remote main" - curl -s url | jq '.data[]' → "Fetch JSON from URL and extract data array elements"
- `run_in_background` — boolean: Set to true to run this command in the background. With it, `timeout` limits how long the command may run in the background before it is stopped (default 1800000 ms, max 7200000 ms).
- `dangerouslyDisableSandbox` — boolean: Set this to true to dangerously override sandbox mode and run commands without sandboxing.
