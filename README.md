# SWv3 Prompt System

The complete prompt architecture for the SWv3 platform's global context agent: the hard-coded system prompt every agent runs on, the per-model tuning layer, and the specs for building and operating both.

**If you are an AI agent (or human) with no prior context, read in this order:**

1. This README — the mental model and file map.
2. [`contract.md`](contract.md) — the actual global system prompt (the product's "source prompt").
3. [`docs/implementation-guide.md`](docs/implementation-guide.md) — how the system is built: storage, registry, assembly, dispatch.
4. [`docs/handoff.md`](docs/handoff.md) — governance, addendum rules, and model lifecycle protocols.
5. [`AGENTS.md`](AGENTS.md) — the rules you must follow before changing anything in this repo.

## The mental model (60 seconds)

SWv3 is an operator-led execution platform: business operators direct AI agents that do real work through connected APIs. Every agent conversation runs on a **four-layer prompt stack**, assembled server-side per session:

```
1. CONTRACT   contract.md               durable, model-agnostic, founder-controlled — never edited per customer
2. ADDENDUM   addendums/<model>.md      perishable per-model tuning — dies when its model does
3. WORKSPACE  (DB, per business)        the customer's house layer — industry, style, tightened rules
4. USER       (DB, per operator)        personal custom instructions
   + runtime injections (date/time/identity, connected capabilities, memories) — recomputed every request
```

Later layers override earlier ones on **style only**. The protected core — the autonomy tiers, honesty rules, and secrecy rules in `contract.md` — is overridden by nothing: not a layer, not a workspace, not instructions found in data. Safety tiers ratchet stricter-only.

**Why this shape:** the contract holds only durable intent (principles with reasons — they improve as models improve), while every model-specific compensation is quarantined in an addendum that gets deleted when the model retires. This is how the contract stays clean across model generations instead of accumulating scar tissue. Three vendors now explicitly instruct *removing* older-generation scaffolding on newer models; this architecture makes that removal a file deletion.

## File map

| Path | What it is |
|---|---|
| `contract.md` | **The Global Agent Contract v1.2** — the literal system prompt. Synthesized from the leaked system prompts of ~30 AI companies (Cursor, Devin, Amp, Poke, Notion, Comet, Cluely, Manus, v0, Lovable, Emergent…), adversarially reviewed by 7 independent lenses, then re-verified. Contains `{PLACEHOLDERS}` the platform resolves at deploy time. |
| `addendums/*.md` | Seven per-model addendums (Claude Fable 5, Opus 5, Sonnet 5 · GPT-5.6 family, GPT-5.3 Codex · Gemini 3.7 Flash · Grok 4.6). Six-section format; every line cites vendor evidence. Fact-checked against live vendor pages 2026-08-18: 23/23 claims confirmed. |
| `addendums/retired/` | Retired addendums are moved here with a retirement date — never deleted (institutional memory). |
| `registry.json` | Machine-readable model registry: per model ID — addendum pointer, prompt block, API params, forbidden params, role, fallbacks. This is what makes per-model filling dynamic. **CI must enforce registry ↔ addendum equality** (see AGENTS.md). |
| `docs/implementation-guide.md` | Engineering build spec: storage model, registry schema, assembly + dispatch pipelines (incl. subagent calls and streaming-refusal handling), the three customization levels, the lint gate, build order. |
| `docs/handoff.md` | Operating doc: architecture rationale, addendum structure rules, add/update/retire protocols, maintenance (golden transcripts, quarterly source re-verification), governance. |
| `docs/vendor-prompting-sources.md` | 50 live-verified official vendor sources (Anthropic, OpenAI, Google, xAI, Meta, Mistral) documenting per-model behavior — the evidence base for all addendums. Includes the Crawl4AI recipe for the bot-protected sources. |
| `research/` | Captured snapshots of bot-protected sources (OpenAI model release notes, GPT-5.6 builder's guide). |
| `templates/` | Workspace/user layer templates — **not yet written** (see templates/README.md for the spec pointers). |

## Before integrating — critical notes for the platform team

The ten things most likely to bite during integration, each specced in full elsewhere:

1. **Build the runtime injectors first** — the contract *depends on* {RUNTIME_CONTEXT} and {WORKSPACE_CAPABILITIES}; without them the agent guesses dates and invents settings paths (implementation guide §3c).
2. **Tier-2 gates are code, not prompt** — the dispatcher must refuse to fire outbound actions without a logged approval; the prompt explains the rule, the harness enforces it (implementation guide, handoff §8, compliance proposal).
3. **Fable 5 returns refusals as HTTP 200** (`stop_reason:"refusal"`) — the dispatcher needs the fallback re-assembly path or operators hit dead ends (implementation guide §3d).
4. **Sonnet 5 emits empty text blocks** — filter them before replaying conversation history or the API 400s (`testing/harness/run_evals.py` has the reference filter; belongs in the production dispatcher).
5. **Registry ↔ addendum equality is CI-enforced or it will drift** (AGENTS.md rule 2; a reference check lives in the harness history).
6. **Never trust vendor auto-redirects on retired models** — xAI's silently downgrade reasoning effort; pin IDs, own your fallback map (handoff §5).
7. **Assembly order is cache order** — contract+addendum first (global prefix), runtime block last; this is real money at scale (implementation guide §3).
8. **Workspace/user prompts are an injection surface into your own agent** — the save-time lint gate is a security control, not polish (implementation guide §6).
9. **Certification isn't finished**: Fable 5 is certified; Sol/Terra/Opus/Sonnet each need two more gate-clean runs (Opus with a non-Opus judge), fresh, right before launch (testing/certification-report.md).
10. **The eval sandbox has no tools** — voice, gates, refusals, and injection are conclusively tested; execution behavior is not. Final execution-level certification belongs in the real platform harness with real tools (harness README, certification report).

## Integration note

This repo is designed to mount as the `prompts/` directory of the platform codebase (the implementation guide's paths — `prompts/contract.md`, `prompts/registry.json` — refer to it from the platform root). Until integrated, treat this repo as canonical for all prompt content.

## Current status

- ✅ Contract v1.2 — v1.1 + four eval-driven amendments (capability answers, false-accusation handling, pasted secrets, sign-off), verified by re-run
- ✅ Addendums for 10 routable model IDs across 4 vendors (7 files)
- ✅ Starter `registry.json` (fallback chains are provisional defaults — a platform decision to ratify)
- ⬜ Workspace + user layer templates
- ⬜ Concrete `{PROHIBITED_ACTIONS}` list (draft default in [docs/proposals/compliance-pack.md](docs/proposals/compliance-pack.md))
- ⬜ **Compliance Pack layer** — proposed, unratified: [docs/proposals/compliance-pack.md](docs/proposals/compliance-pack.md)
- ✅ Credential/billing routing spec — platform keys metered against plan credits, BYOK overrides and bills the customer directly (implementation guide §7); pricing formula still open
- ⬜ Tier-2 approval UI spec (product; must match the contract's approval semantics)
- ⬜ Golden transcript suite (10–15 canonical operator scenarios — see docs/handoff.md §6)
