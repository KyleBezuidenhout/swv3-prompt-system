# Model Addendum — GPT-5.3 Codex

**model_ids:** `gpt-5.3-codex` (coding/agentic-build lane only — not a general assistant model)
**status:** active · written 2026-08-18 · **review trigger:** next Codex release, or change to the vendor page below
**evidence:** https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide · https://developers.openai.com/api/docs/models/gpt-5.3-codex

## Harness configuration (API level — not prompt text)

- **The `phase` parameter is REQUIRED** (Responses API: `commentary` vs `final_answer`). Omitting it significantly degrades output — vendor-documented. This is the #1 integration gotcha.
- **reasoning_effort:** `low`/`medium`/`high`/`xhigh` supported — `medium` recommended for interactive coding sessions; raise for long autonomous builds.
- Use **first-class compaction** for multi-hour sessions.
- Map platform tools onto the canonical Codex tool shapes (`apply_patch`, `shell_command`, `update_plan`) — the model is trained against these.
- 400k context.

## Prompt block (appended below the global contract at assembly)

```
<model_notes>
Working cadence: acknowledge the task in one line, surface the plan, then
build — keep working-phase commentary brief and pragmatic in tone.
</model_notes>
```

## Remove / never write for this model (scaffolding that hurts)

- **Mainline GPT-5 prompt tuning, wholesale.** The vendor warns that prompts and tools optimized for mainline GPT-5 models need more significant changes on Codex models — not drop-in reuse. Never copy the gpt-5.6 addendum's calibration here; this file must earn its own lines.

## Notes for prompt authors

- Route only coding/build work here. The contract's operator-facing voice rules still apply to whatever text reaches the operator, but this model's lane is producing artifacts, not conversation.
- Preamble personality is tunable per the guide (Friendly vs Pragmatic) — we pin Pragmatic to match the contract's voice.

## Observed-quirk log (production evidence — every line dated + cited, expires on model bump)

*(empty at launch)*
