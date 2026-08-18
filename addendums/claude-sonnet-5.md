# Model Addendum — Claude Sonnet 5

**model_ids:** `claude-sonnet-5`
**status:** active · written 2026-08-18 · **review trigger:** next Claude release, or change to the vendor page below
**evidence:** https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5 · https://platform.claude.com/docs/en/build-with-claude/effort · https://platform.claude.com/docs/en/build-with-claude/thinking

## Harness configuration (API level — not prompt text)

- **Effort:** start `medium` — vendor maps Sonnet 5 `medium` ≈ Sonnet 4.6 `high`. Avoid `low` for judgment-heavy work: this model adheres to effort strictly and will genuinely under-think.
- **Thinking:** adaptive, on by default. Note tool-use triggering differs with thinking off — keep it on for agentic lanes.
- **Never send** sampling params (`temperature`/`top_p`/`top_k`) — now 400 errors.
- **max_tokens:** retune upward ~30% for the new tokenizer.

## Prompt block (appended below the global contract at assembly)

```
<model_notes>
For customer-facing visual or frontend deliverables: do not fall back on your
default design conventions — derive look and feel from the workspace's brand
and the operator's materials, and say what you derived it from.
</model_notes>
```

## Remove / never write for this model (scaffolding that hurts)

- Vague or contradictory instructions in workspace/user layers. **This model follows instructions more literally than its predecessors** — ambiguity gets executed as written, not resolved by vibes. Lint lower layers for precision before they ship.
- Verbosity-padding or "be thorough" filler — verbosity is already task-calibrated.

## Notes for prompt authors

- Literalism is a feature for the contract (its rules are precise) and a hazard for sloppy workspace layers — this is the model where a badly written customer layer will misbehave first.
- Vendor documents a persistent frontend design "house style"; the prompt block above is the documented counter.

## Observed-quirk log (production evidence — every line dated + cited, expires on model bump)

*(empty at launch)*
