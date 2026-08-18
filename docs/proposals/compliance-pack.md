# Proposal: Compliance Pack layer

**Status: PROPOSED — not ratified, not implemented.** · Raised 2026-08-19 · Origin: legal-exposure gap analysis of Contract v1.1
Ratification: founder decision (docs/handoff.md §7). Applying this proposal means a contract version bump, a `<layers>` update, implementation-guide changes, and a CHANGELOG entry — in one reviewed change.

---

## Problem

Contract v1.1 is strong on **behavioral trust** (tier gates, honesty, scope restraint — protecting the operator from the agent) and thin on **legal exposure** (protecting the platform from what the agent says and does in the world). The canonical precedent is *Moffatt v. Air Canada* (2024): a chatbot invented a refund policy, and the tribunal held the company liable — the "separate entity" defense failed. SWv3 agents speak in the operator's name to real third parties, at scale, in the most actively enforced marketing-law territory there is (B2B outbound). Nothing in v1.1 addresses that class of risk.

## Proposed architecture

Add a **Compliance Pack** as a new platform-managed prompt layer, and move a small set of rules into the protected core:

```
1. CONTRACT           durable, model-agnostic core            (unchanged)
2. {MODEL_ADDENDUM}   per-model tuning                        (unchanged)
3. {COMPLIANCE_PACK}  ← NEW: platform-managed, per-vertical / per-jurisdiction legal rules
4. {WORKSPACE_PROMPT} the business's layer                    (unchanged)
5. {USER_PROMPT}      the operator's layer                    (unchanged)
```

The split answers "removable but not too strict":

- **Protected core (immovable — nobody removes these, including the customer):** binding-statement grounding, the default Tier 3 prohibited-actions list, the protected-class rule, secrets hygiene (already core).
- **Compliance pack (removable — but only by the platform):** vertical- and jurisdiction-specific rules (outbound marketing law, advice boundaries per market, AI-disclosure policy). Workspaces may tighten it (the existing ratchet); loosening is a *platform* decision made per market/vertical — never a customer prompt edit.

## Proposed protected-core additions (contract text, to be drafted for v1.2)

1. **Binding statements are grounded or gated.** Statements of price, policy, terms, warranty, or commitment come only from workspace-approved sources; with no source, the agent says it will check — it never improvises terms. A commitment to a third party is a Tier 2 act even though it is only words: a promise is irreversible outbound.
2. **Default Tier 3 list** (fills the still-empty `{PROHIBITED_ACTIONS}` placeholder — draft, product/legal to ratify):
   - entering, storing, or transmitting payment credentials, card numbers, or government IDs
   - executing financial transfers, trades, or crypto transactions
   - creating accounts or authenticating as the operator (passwords, 2FA, OAuth grants)
   - permanently deleting data
   - bypassing CAPTCHAs or bot detection; helping evade a platform's enforcement, rate limits, or terms
3. **Protected-class rule.** No decision, filter, score, or selection keyed to protected characteristics; personal data goes only where the task requires; no compiling personal profiles beyond the task.

## Proposed compliance-pack contents (per-market templates)

| Area | Rule sketch | Why |
|---|---|---|
| Outbound marketing law | A revoked consent is permanent and honored everywhere; outreach never misrepresents sender identity or purpose; jurisdiction slots for CAN-SPAM / GDPR-PECR / CASL / TCPA specifics | The platform's reference workflow is outbound at scale — the most likely enforcement surface |
| Regulated advice | Help with information; never deliver a licensed-professional determination (legal / medical / financial / tax); name the moment a professional is needed | Operators will ask; speech-based risk the action tiers don't cover |
| AI disclosure | `{DISCLOSURE_POLICY}` slot: whether/how the agent identifies as an AI to third parties, set per jurisdiction (EU AI Act transparency, bot-disclosure laws) | Must be a deliberate policy, not an accident |
| Third-party IP | No wholesale reproduction of copyrighted or scraped content in deliverables/outreach | Content generation at scale |

## Enforcement principle (implementation-guide addition)

**If a rule matters legally, code enforces it and the prompt explains it.** The prompt is the first layer; the harness is the defense: Tier 2 gates enforced in the dispatcher (a send cannot fire without a logged approval), an **immutable audit log** of every approval (who, exact content, when — the audit log is the legal defense), suppression lists checked in the send pipeline, spend caps in code, retention in the database. Assume the model can fail.

## Caveats

Drafted by an AI from a gap analysis; **not legal advice**. Before real customer traffic, this pack plus ToS/DPA needs counsel review per market. Related parked item: the four eval-driven contract amendments in `testing/harness/results/run-20260818-232812/proposals.md` — ratify together as v1.2 or separately.
