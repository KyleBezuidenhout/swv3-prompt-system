# Changelog

## 2026-08-18 — initial release

- **Contract v1.1** — first production candidate. v1.0 drafted from the 30-company leaked-prompt corpus analysis; v1.1 after a seven-lens adversarial review (overlap, corpus fidelity, agnosticism, enforceability, operator-experience, prompt craft, future-proofing → 70+ findings) plus an independent verification pass (caught a layer-precedence inversion and an injection example that taught the weaker behavior — both fixed).
- **Addendums** for 10 routable model IDs across 4 vendors (7 files): Claude Fable 5 (+Mythos), Claude Opus 5, Claude Sonnet 5, GPT-5.6 Sol/Terra/Luna, GPT-5.3 Codex, Gemini 3.7 Flash, Grok 4.6. All claims fact-checked against live vendor pages 2026-08-18 (23/23 confirmed).
- **registry.json** starter — fallback chains provisional.
- **Docs**: handoff, implementation guide (v1.1 — post-verification: fixed stale-runtime-block cadence, lint-gate ratchet direction, subagent assembly added), vendor source catalog (50 verified sources).
