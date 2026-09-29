### experiment sections (`heron_brook` / `brook_heron` / `willow_tern`)  · gate: `tengu_*` flags
Client-data / effort-tuned experiment text (content served from the model-config layer, not a fixed literal).

---

## Not in the harness anymore

- **`# Scratchpad Directory`** — removed from the system prompt in a version between 2.1.251 and 2.1.283. The scratchpad still exists per-session; its instruction moved to a **dynamic runtime reminder** delivered through the messages channel, not the `system` field.

## The dynamic pieces (filled at runtime, not static text)

- `# Environment` model-ID line (from the live model registry)
- `# Memory` path, scratchpad path — from session id + cwd
- the live `<env>` block (cwd, git status, OS, date) — rides the `messages` layer, not the `system` field

Run `generate_default_prompt.py --model <id>` to fill these with real values for a given model/session.
