# Changelog

## 2026-08-18 — initial release

- **Contract v1.1** — first production candidate. v1.0 drafted from the 30-company leaked-prompt corpus analysis; v1.1 after a seven-lens adversarial review (overlap, corpus fidelity, agnosticism, enforceability, operator-experience, prompt craft, future-proofing → 70+ findings) plus an independent verification pass (caught a layer-precedence inversion and an injection example that taught the weaker behavior — both fixed).
- **Addendums** for 10 routable model IDs across 4 vendors (7 files): Claude Fable 5 (+Mythos), Claude Opus 5, Claude Sonnet 5, GPT-5.6 Sol/Terra/Luna, GPT-5.3 Codex, Gemini 3.7 Flash, Grok 4.6. All claims fact-checked against live vendor pages 2026-08-18 (23/23 confirmed).
- **registry.json** starter — fallback chains provisional.
- **Docs**: handoff, implementation guide (v1.1 — post-verification: fixed stale-runtime-block cadence, lint-gate ratchet direction, subagent assembly added), vendor source catalog (50 verified sources).

## 2026-08-19 — Contract v1.2

Four eval-driven amendments, ratified by founder from the first automated run (results/run-20260818-232812, 1 hard fail + 5 soft fails across 30 turns):

1. **Capability answers** (`<first_session>`) — named jobs with objects, never category menus or per-product headings; rule now applies at any point in the relationship, not just the first message. (Fixes the S2 hard fail.)
2. **Frustration where the fault isn't yours** (`<voice>`) — same shape as owned errors: state + fix, no defensive ledger, no false confession. (Fixes S7 ×3.)
3. **Pasted secrets** (`<autonomy>`) — added card numbers explicitly; if a secret arrives, decline + don't echo + stop — no after-the-fact lecture. (Fixes S8.)
4. **Sign-off** (`<communication>`) — one line, no recap of parked items; exception only for something new since last seen. (Fixes S10 ×2.)

Also: eval rubric (scenarios.json) and manual scenario doc synced to v1.2; test assembly regenerated. Parked: mid-sentence self-correction observation (1/3 toward the Fable 5 addendum quirk-log bar).

## 2026-08-19 — Contract v1.2.1 (regression fix)

The v1.2 re-run (results/run-20260819-011357) confirmed all four amendments fixed their targets (S2 3×PASS, S7 3×PASS) — and caught a regression the first amendment introduced: its replacement text dropped the greeting trigger, sending S1 from 3×PASS to 3×HARD_FAIL. Two intent-completion patches, no new policy:

- **A:** restored "When they open with a greeting, or ask what you can do…" to the capability rule.
- **B:** engagement-bait ban now covers paraphrases ("I'm here when you need me") per the ratified sign-off intent.
- Rubric: S8 no longer penalizes the contract-mandated one-line non-retention statement.

## 2026-08-19 — Contract v1.3

Two worked example pairs added (ratification delegated by founder), targeting the v1.2.1 feel-level residuals: capability answers as prose vs. category buckets (S2), and false-accusation tone — state + fix vs. defensive ledger (S7). Examples, not rules, per the calibrate-by-example principle. Also: eval harness gains a GPT-5.6 target (Responses API, developer role, effort/verbosity per the gpt-5.6 addendum) for cross-vendor runs with the same scenarios and judge.
