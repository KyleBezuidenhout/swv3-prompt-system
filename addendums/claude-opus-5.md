# Model Addendum — Claude Opus 5

**model_ids:** `claude-opus-5`
**status:** active · written 2026-08-18 · **review trigger:** next Claude release, or change to the vendor page below
**evidence:** https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5 · https://platform.claude.com/docs/en/about-claude/models/whats-new-opus-5 · https://platform.claude.com/docs/en/about-claude/models/migration-guide (sampling-params/prefill 400s) · https://platform.claude.com/docs/en/build-with-claude/effort

## Harness configuration (API level — not prompt text)

- **Effort:** start `high` (vendor recommendation for Opus 5; the 4.8-era `xhigh` default no longer applies). Effort controls thinking depth, **not** visible reply length.
- **Thinking on by default**; disabling it 400-errors at `xhigh`/`max` effort.
- **Never send** sampling params (`temperature`/`top_p`/`top_k`) or assistant prefill — 400 errors.
- **max_tokens:** retune upward for the new tokenizer.
- Delegation is eager on this model — cap subagent spawn depth deterministically in the harness.
- 1M context / 128k output. Fast mode available where latency matters.

## Prompt block (appended below the global contract at assembly)

```
<model_notes>
Your default is longer replies and running narration, including narrating
self-corrections and verifications. The contract's sizing and quiet-work rules
win: state results, not the story of checking them.
Your tendency is to expand scope beyond the request. The contract's scope
restraint is the boundary — adjacent work is offered in one line, never done.
</model_notes>
```

## Remove / never write for this model (scaffolding that hurts)

- **All legacy "verify your work" / "double-check before finishing" instructions** — Opus 5 self-verifies unprompted; these lines cause over-verification loops (vendor-documented).
- **"Be conservative" in review-style prompts** — vendor-documented backfire.
- Length-padding instructions from older models — this model already runs long; prompt for brevity, not fullness.

## Notes for prompt authors

- If a deliverable needs a specific length, say the length explicitly — effort won't control it.
- Thinking-disabled runs can leak artifacts (tool calls as text, internal XML) — keep thinking on in production.

## Observed-quirk log (production evidence — every line dated + cited, expires on model bump)

*(empty at launch)*
