# Model Addendum — GPT-5.6 family

**model_ids:** `gpt-5.6-sol` (frontier reasoning), `gpt-5.6-terra`, `gpt-5.6-luna`
**status:** active · written 2026-08-18 · **review trigger:** next GPT release, or change to the vendor pages below
**evidence:** https://developers.openai.com/api/docs/guides/latest-model · https://deploymentsafety.openai.com/gpt-5-6 · https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_troubleshooting_guide · https://openai.com/index/builders-guide-to-gpt-5-6/ (local snapshot: research/openai-builders-guide-gpt-5-6.md)

## Harness configuration (API level — not prompt text)

- **reasoning_effort** (`none`→`max`): start one level *lower* than the equivalent 5.5 setting — vendor migration advice: "GPT-5.6 can often maintain or improve quality with fewer tokens."
- **text.verbosity:** set `medium`; let the contract govern actual sizing.
- Use the **Responses API** with `previous_response_id` to persist reasoning across turns; enable explicit prompt caching.
- Platform layers (contract + addendum + workspace) go in the **developer role** — OpenAI's authority hierarchy is developer > user > assistant.
- Multi-agent coordination is in beta if the harness wants native fan-out.

## Prompt block (appended below the global contract at assembly)

```
<model_notes>
Format replies in Markdown wherever the surface renders it.
Boundary check: your documented tendency is to go beyond the user's intent —
taking or attempting actions that were not asked for. The contract's tier
gates and scope restraint are hard boundaries, not suggestions: when unsure
whether something was requested, stage it and ask rather than act.
</model_notes>
```

(The Markdown line exists because the API default emits no Markdown; the boundary block counters the system-card finding that 5.6 Sol exceeds user intent more than 5.5 did.)

## Remove / never write for this model (scaffolding that hurts)

- **GPT-5.0-era scaffolding wholesale** — vendor now recommends leaner prompts with explicit autonomy/approval boundaries instead of long recipes.
- **Contradictions anywhere in the stack.** The GPT family degrades measurably under contradictory instructions (tool-calling quality, rare malformed-tool-call mode collapse). When a workspace layer lands, run a contradiction audit against the contract before shipping.

## Notes for prompt authors

- Reasoning models want **goals and constraints, not step-by-step procedures** — the contract's commitments-not-recipe process section is the right shape; don't let workspace layers reintroduce recipes.
- The Troubleshooting Guide is a symptom→fix catalog (overthinking → lower effort + stop conditions; deference → persistence language; excess tool calls → crisp routing rules). Use it as the first diagnostic when this model misbehaves, before writing new quirk lines.

## Observed-quirk log (production evidence — every line dated + cited, expires on model bump)

*(empty at launch)*
