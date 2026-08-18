# Working in this repo — rules for AI agents

This repo is the SWv3 platform's prompt system. Read `README.md` first for the mental model. These are the operating rules; they exist because prompt systems rot in specific, well-documented ways (see docs/handoff.md), and every rule below prevents one of them.

## Iron rules (never violate)

1. **Every addendum line cites evidence.** A claim about model behavior enters an addendum only with a citable source: an official vendor doc URL, or a dated production incident observed three times. No source, no line. This prevents the addendum layer becoming superstition.
2. **Registry and addendum change in the same commit.** `registry.json`'s `prompt_block`, `api_params`, and `forbidden_params` must exactly match the corresponding addendum's Prompt block and Harness configuration sections for every non-retired entry. If you edit one, edit the other.
3. **The contract's protected core is untouchable from below.** Nothing in an addendum, template, or generated layer may weaken the autonomy tiers, honesty rules, or secrecy rules in `contract.md`. Tightening is allowed (tiers ratchet stricter-only); loosening never.
4. **Addendums adjust expression and mechanics only** — never identity, scope, or intent. If a change feels like it belongs in every model's addendum, it belongs in the contract instead (and needs the contract's change process).
5. **Nothing in `contract.md` may name a model, provider, or version.** Model-specific content lives only in `addendums/` and dies with its model.
6. **Never delete a retired addendum.** Move it to `addendums/retired/`, stamp the retirement date in its header, set `status: "retired"` + `retirement_date` in the registry, and update its `addendum` path. Retired files are institutional memory.
7. **Contract edits are founder-level.** Do not modify `contract.md` without explicit instruction from the repo owner; every change bumps the version in the title line and gets a CHANGELOG.md entry.

## Workflows

### Adding a model
1. Pin the exact model ID (never a `-latest` alias — vendors re-point them silently).
2. Read the vendor's prompting + migration guides for it. Start from `docs/vendor-prompting-sources.md`; check the vendor changelog for entries newer than the catalog's verification date (2026-08-18). Bot-protected sources: use the Crawl4AI recipe in that file.
3. Copy the six-section structure from any existing addendum (Header with evidence + review trigger / Harness configuration / Prompt block ≤8 lines / Remove-never-write / Notes for prompt authors / empty quirk log).
4. Add the registry entry (same commit). Fallback target must be an `active` entry.
5. Verify: fact-check every claim in the new addendum against the cited pages before committing (fetch them — do not trust memory or training data; docs move and models change).
6. Run the golden transcript suite if it exists; note results in the PR.

### Updating a model (new version, same family)
Treat as a NEW model: new addendum file, new registry entry, fresh evidence. Copy a line forward only after re-verifying it against the new version's docs — behaviors flip between generations (thinking defaults and subagent eagerness inverted between Claude Opus 4.8 → Opus 5; vendors now instruct *removing* prior-generation scaffolding).

### Retiring a model
1. Set the router fallback explicitly first (never rely on vendor auto-redirects — xAI's silently downgrade reasoning effort).
2. Move the addendum to `addendums/retired/`, stamp the date, update the registry entry (`status`, `retirement_date`, path).
3. Remove the ID from routing last.

### Editing docs
`docs/handoff.md` and `docs/implementation-guide.md` are specs the platform is built against — if you change architecture (layer precedence, assembly order, registry schema), change the contract's `<layers>` section, both docs, and this file *consistently*, and say so in the commit message. Precedence rules live canonically in `contract.md` `<layers>`; everything else must agree with it.

## Style

- Prompt blocks: 3–8 lines, pure deltas — only what the model needs that the contract doesn't already say. Never restate contract rules.
- Rules carry their reasons ("X, because Y") — reasoned rules generalize as models improve; bare rules don't.
- No compliance theater: no threats, no ALL-CAPS pressure, no duplicated warnings. If a model needs a rule stated twice, the rule is wrong.

## Verification bar

Before any PR that touches `contract.md`, an addendum, or `registry.json`: state in the PR what you verified and how (which vendor pages fetched, which checks run). Claims of model behavior without verification notes should not be merged.
