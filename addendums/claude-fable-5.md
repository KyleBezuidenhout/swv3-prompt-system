# Model Addendum — Claude Fable 5

**model_ids:** `claude-fable-5` (Mythos 5 is the same underlying model, approved orgs only)
**status:** active · written 2026-08-18 · **review trigger:** next Claude release, or change to the vendor page below
**evidence:** https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5 · https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5 · https://platform.claude.com/docs/en/build-with-claude/effort

## Harness configuration (API level — not prompt text)

- **Effort is the primary knob.** Start `high` (vendor recommendation for this model — not `xhigh`); raise only on evidence.
- **Thinking is adaptive and always on — cannot be disabled** (400 error). `thinking.display` defaults to omitted; set `summarized` only if the UI shows reasoning.
- **Never send** `temperature` / `top_p` / `top_k` or assistant prefill — hard 400 errors on this generation.
- **Refusal handling:** safety classifiers return `stop_reason: "refusal"` as HTTP 200. The harness must catch this and fall back (server-side fallbacks mode, or a client-side fallback — the vendor's documented recommendation is Claude Opus 4.8; falling back to Sonnet 5 instead is a platform choice to make deliberately). The operator should never see a dead end.
- **max_tokens:** retune upward ~30–35% — the new tokenizer produces more tokens for the same text.
- 1M context. Compliance note: 30-day retention, no ZDR — check against customer data agreements.

## Prompt block (appended below the global contract at assembly)

```
<model_notes>
Your context window is large and the platform manages long-run compaction.
Never cut work short or summarize prematurely to conserve context.
Long turns are expected: minutes-to-hours of continuous work is normal here.
</model_notes>
```

## Remove / never write for this model (scaffolding that hurts)

- **Over-prescriptive step-by-step instructions.** Instruction following is strong; short instructions beat enumeration. Lean workspace layers, not recipes.
- **Any instruction asking the model to reproduce or restate its reasoning** — anywhere in any layer — triggers the `reasoning_extraction` refusal classifier.
- Redundant restatements: one clear statement with the reason attached is followed reliably.

## Notes for prompt authors

- Give-the-reason prompting works especially well — the global contract's reason-attached style is optimal here as-is.
- Eager parallel-subagent dispatch is native; if the harness exposes delegation, cap depth deterministically in the harness, not in prompt text.
- Grounding progress claims in tool evidence is a documented strength — the contract's `<honesty>` rules land well without reinforcement.

## Observed-quirk log (production evidence — every line dated + cited, expires on model bump)

*(empty at launch — add entries only after the same deviation is observed three times)*
