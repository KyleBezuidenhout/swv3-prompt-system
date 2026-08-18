# Model Addendum — Gemini 3.7 Flash

**model_ids:** `gemini-3.7-flash` (GA 2026-08-13; the 3.x rules below apply family-wide — derive a sibling addendum from the same sources if routing to `gemini-3.1-pro-preview`)
**status:** active · written 2026-08-18 · **review trigger:** next Gemini release, or change to the vendor pages below
**evidence:** https://ai.google.dev/gemini-api/docs/latest-model · https://ai.google.dev/gemini-api/docs/gemini-3 · https://ai.google.dev/gemini-api/docs/prompting-strategies · https://ai.google.dev/gemini-api/docs/thinking · https://ai.google.dev/gemini-api/docs/changelog (GA and deprecation dates)

## Harness configuration (API level — not prompt text)

- **Send no sampling parameters.** `temperature`/`top_p`/`top_k`/`candidate_count` are deprecated (Jul 21, 2026) — and on Gemini 3.x, lowering temperature from its 1.0 default is vendor-documented to cause looping and degraded output. Leave everything at default.
- **thinking_level** is the knob (`low`/`medium`/`high`): default `medium`; vendor recommends `medium` for complex code and agentic use.
- **No prefilled model turns** — removed in 3.7 Flash. Multi-turn goes through server-side `previous_interaction_id`.
- **FunctionResponse must match `call_id` AND `name`** — stricter than other vendors; naive multi-model harnesses break here.
- **Thought signatures must be round-tripped** across turns in function-calling flows.

## Prompt block (appended below the global contract at assembly)

```
<model_notes>
Your default register is terse. The contract's duties still stand in full:
the completion report with its numbers and artifacts, the earned-warmth
allowance, and the one-line assumption statements. Meet them — brevity never
means dropping them.
</model_notes>
```

(Vendor-documented: 3.5+ Flash is "intentionally less verbose and needs explicit steering" — this block is that steering, pointed at the contract's duties.)

## Remove / never write for this model (scaffolding that hurts)

- **Chain-of-thought scaffolding** ("think step by step", staged reasoning templates) — vendor migration guidance says drop it on Gemini 3.
- **Verbose prompt engineering.** This model "over-analyzes verbose prompt engineering" — workspace layers routed here should be linted for leanness harder than anywhere else.

## Notes for prompt authors

- Structure preferences: consistent delimiters (the contract's XML-style tags qualify — don't mix in Markdown headers as delimiters in lower layers), context before instructions, explicit verbosity requests where length matters.
- Assembly order note: Gemini wants context first and instructions last — the platform's assembly (contract early, runtime context late) is acceptable per vendor docs, but keep the final layer (user prompt) instruction-shaped, not context-shaped.

## Observed-quirk log (production evidence — every line dated + cited, expires on model bump)

*(empty at launch)*
