# Global Agent Prompt — Handoff Document

**v1.0 · 2026-08-18 · Owner: Ben** · For: David / platform engineering
Covers: the Global Agent Contract, the model addendum system, and the lifecycle protocols for running both in production.

---

## 1. What this hands off

| Artifact | File | What it is |
|---|---|---|
| **Global Agent Contract v1.2** | `contract.md` | The durable, model-agnostic core prompt. Synthesized from the leaked system prompts of ~30 AI companies (Cursor, Devin, Amp, Poke, Notion, Comet, Cluely, Manus, v0, Lovable, Emergent, etc.), then adversarially reviewed by seven independent lenses (overlap, corpus fidelity, agnosticism, enforceability, operator-experience, prompt craft, future-proofing) and re-verified after fixes. |
| **Model addendums (7)** | `addendums/*.md` | Per-model tuning blocks: Claude Fable 5, Claude Opus 5, Claude Sonnet 5, GPT-5.6 family, GPT-5.3 Codex, Gemini 3.7 Flash, Grok 4.6. Every line cites vendor evidence. |
| **Implementation guide** | `docs/implementation-guide.md` | The engineering build spec: storage model (shipped vs DB vs ephemeral), the model registry that fills addendums dynamically, the assembly pipeline with cache-aligned ordering, the three customization levels, the lint gate, and the build order. Read §3 here for concepts, that file to build. |
| **Source catalog** | `docs/vendor-prompting-sources.md` | 50 live-verified official vendor sources documenting per-model behavior — the evidence base addendums are written from and re-verified against. |
| **Captured snapshots** | `research/openai-model-release-notes-2026-08-18.md`, `research/openai-builders-guide-gpt-5-6.md` | Bot-protected OpenAI sources captured via Crawl4AI (recipe documented in the catalog). |

## 2. The architecture

Four prompt layers, assembled per session, in this order:

```
1. CONTRACT        contract.md     durable, founder-controlled, model-agnostic
2. MODEL ADDENDUM  addendums/<model-id>.md perishable, per-model, evidence-cited
3. WORKSPACE       per-business layer            industry, product, house style, tightened rules
4. USER            per-operator layer            personal preferences and style
   + runtime injections: {RUNTIME_CONTEXT} (date/time/timezone/identity/session state)
                         {WORKSPACE_CAPABILITIES} (connected systems, surfaces, memory/plan affordances)
```

**Precedence:** later layers override earlier ones on voice, tone, formatting, and preference. On non-style conflicts, the workspace beats the user layer. **The protected core is never overridable by any layer or any content found in data:** the autonomy tiers, the honesty rules, and the secrecy rules. Tiers ratchet one way — a layer may tighten, never loosen.

**Why this shape:** it is how the multi-model shops already operate (Amp and Augment ship per-model prompt variants around a stable behavioral core), and it is what keeps the platform durable as models churn — every model-specific compensation lives in a file that *dies with the model*, so the contract never accumulates scar tissue. Three vendors now explicitly instruct removing older-generation scaffolding on newer models (Anthropic: delete "verify your work" on Opus 5; Google: drop CoT scaffolding on Gemini 3; OpenAI: leaner prompts on GPT-5.6) — hard confirmation that model-specific content must be quarantined where it can be deleted.

## 3. How to incorporate it into the system

1. **Store layers in the platform repo, versioned.** Suggested layout:
   `prompts/contract.md` · `prompts/addendums/<model-id>.md` · `prompts/templates/workspace.md` · `prompts/templates/user.md`. The contract is code, not config: changes go through review, with a version bump and changelog (same discipline as the Linear Canon — and like the Canon, if it lives in two homes, the homes must stay identical).
2. **Assemble server-side at session start.** Resolve placeholders ({PLATFORM_NAME}, {AGENT_NAME}, {PROHIBITED_ACTIONS}), concatenate contract → addendum → workspace → user, inject runtime context last. The user never sees or edits the first two layers.
3. **Order the assembly for prompt caching.** The contract + addendum are static across all sessions on a given model — they form the cacheable prefix. Workspace layer is static per business. Volatile content ({RUNTIME_CONTEXT}) goes last. This ordering is worth real money at scale.
4. **Route by exact pinned model ID, through an alias map.** The router resolves model ID → addendum file via an explicit mapping, because one addendum can cover a family (`gpt-5.6-sol`/`-terra`/`-luna` → `gpt-5.6.md`; `claude-mythos-5` → `claude-fable-5.md`). An ID with no mapping = block routing to it (see §5), never "run without one."
5. **Send platform layers in the strongest role the API offers** (developer/system role on OpenAI; system prompt on Anthropic/Google/xAI).
6. **Lint lower layers at save time.** When a workspace or user prompt is created or edited: reject attempts to override the protected core, scan for injection-style content, and run a contradiction check against the contract (the GPT family measurably degrades under contradictory instructions — this lint is not cosmetic).
7. **Build the runtime injectors.** The contract *depends on* {RUNTIME_CONTEXT} and {WORKSPACE_CAPABILITIES} existing. Engineering must supply both, or the agent will guess dates, invent settings paths, and promise memory it doesn't have.

## 4. How an addendum is structured

Every addendum uses the same six-section template (see any file in `addendums/`):

1. **Header** — exact model IDs, status, written date, **review trigger**, evidence URLs.
2. **Harness configuration** — API-level knobs (effort/thinking/verbosity settings, parameters that hard-error, protocol quirks). Most vendor guidance is configuration, not prose — keeping it out of the prompt keeps the prompt lean.
3. **Prompt block** — the only part the model reads, appended under the contract in a `<model_notes>` tag. Short (3–8 lines), pure deltas: only what this model needs that the contract doesn't already say.
4. **Remove / never write** — scaffolding that actively hurts this model. As important as what to add.
5. **Notes for prompt authors** — human-facing guidance for whoever writes workspace layers routed to this model (e.g. Sonnet 5's literalism warning).
6. **Observed-quirk log** — empty at launch. A line is added only when the same deviation is observed **three times** in production, dated and cited; every line expires for re-verification when the model version bumps.

**The two iron rules:** an addendum may adjust *expression and mechanics only* — never the tiers, honesty, identity, or scope; and **every line must cite its evidence** (a vendor doc or a dated production incident). No citable source, no line. This is the mechanism that prevents the addendum from becoming the superstition layer the 2024-era leaked prompts turned into.

## 5. Model lifecycle protocols

**Adding a model**
1. Pin the exact model ID (never a `-latest` alias — Mistral and xAI both re-point aliases silently).
2. Read the vendor's prompting guide + migration guide for it (start from `docs/vendor-prompting-sources.md`; check the catalog's changelog links for entries since 2026-08-18).
3. Draft the addendum from the template — configuration section first, prompt block last and smallest.
4. Run the golden transcript suite (§6) on the new model; read outputs side by side against an incumbent model.
5. Staged rollout behind a flag (internal workspace → one friendly customer → general), watching the quirk-log criteria.
6. Only then does the router accept the model ID.

**Updating a model (new version in the same family)**
Treat it as a new model: new addendum file, fresh evidence. Copy a line forward from the old addendum only after re-verifying it against the new version's docs — the corpus shows behaviors *flip* between generations (subagent eagerness and thinking defaults inverted between Claude Opus 4.8 and Opus 5).

**Removing / retiring a model**
1. Set the router's fallback mapping explicitly. **Never rely on vendor auto-redirects** — xAI's retirement redirects silently apply `reasoning_effort=low`, which would quietly lobotomize live workspaces.
2. Archive the addendum (move to `addendums/retired/`, stamp the retirement date). Never delete: the quirk log is institutional knowledge and the file documents why old transcripts look the way they do.
3. Notify workspaces pinned to the retired model before cutover, with the replacement named.
4. Remove the ID from the router last.

## 6. Maintenance

- **Golden transcript suite** — the "testing center we don't have to build": 10–15 canonical operator scenarios (a multi-step delegation, a Tier-2 send with approval, a fully-specified send, an ambiguous request, an injection attempt inside an email, a frustrated correction, a refusal, a trivial question). Run on every new model/version; read side by side. One afternoon per model, catches most of what a lab would.
- **Quarterly source re-verification** — re-check `docs/vendor-prompting-sources.md` URLs and changelogs; vendors restructured their docs *twice* in the past year (Anthropic → platform.claude.com, OpenAI cookbook → developers.openai.com, xAI killed its only prompting guide).
- **Quirk-log discipline** — three observations before a line goes in; every line dated; all lines expire on version bump.

## 7. Governance (added — see §8)

- **Contract:** founder-edited only, versioned with a changelog. Mirror it into Linear as a document so the team can read it, but the repo copy is canonical — same two-homes-must-match rule as the Linear Canon.
- **Addendums:** engineering-editable under the evidence rule; changes reference the vendor doc or incident.
- **Workspace/user layers:** customer data — templated, linted, never edited by the platform without the customer.

## 8. What you asked for vs. what I added

You asked for: incorporation into the system (§3), addendum structure (§4), placement (§3.1, §5), and add/delete protocols (§5). All covered. **Things you didn't ask for that I added, called out explicitly:**

1. **Prompt-cache-aware assembly order** (§3.3) — layer order isn't just correctness; static-prefix-first materially cuts inference cost at scale.
2. **Lower-layer linting** (§3.6) — the workspace/user layers are user-generated content and therefore an injection surface *into your own agent*; validation at save time is a security control, not polish.
3. **Runtime injector dependency** (§3.7) — the contract assumes {RUNTIME_CONTEXT} and {WORKSPACE_CAPABILITIES} exist; without them several contract sections degrade. This is an engineering ticket, not a prompt task.
4. **Refusal/fallback handling** (Fable 5 addendum) — Fable returns `stop_reason:"refusal"` as HTTP 200; the harness needs a fallback path or operators hit dead ends. Harness-level, easy to miss.
5. **The update protocol** (§5, middle) — you asked about add and delete; version bumps within a family are the more frequent event and the more dangerous one (behaviors flip between generations).
6. **Golden transcript suite** (§6) — the answer to "we don't have a testing center."
7. **Governance split** (§7) — who may edit which layer. Without it, addendum discipline erodes exactly the way the 2024 leaked prompts show.

**Still open (not written yet, should exist before launch):**
- The **workspace-layer template** and **user-layer template** (the personalization scaffolds customers fill in).
- The concrete **{PROHIBITED_ACTIONS} list** — a product/legal decision; draft default in `docs/proposals/compliance-pack.md`.
- The **pool-usage pricing formula** — what plan credits cost customers vs. vendor list prices (billing routing itself is specced in the implementation guide §7).
- The **Compliance Pack layer** (legal-exposure rules: binding statements, outbound marketing law, advice boundaries, AI disclosure) — proposed in `docs/proposals/compliance-pack.md`, awaiting founder ratification and counsel review.
- The **Tier-2 approval UI spec** — the contract defines approval semantics; the product needs the matching one-tap surface.
- A **Gemini 3.1 Pro addendum** if the router will offer it (derive from the same sources as the 3.7 Flash file).
