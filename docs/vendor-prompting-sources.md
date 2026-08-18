# Vendor Prompting Guidance — Verified Source Catalog

Every URL below was live-fetched and content-verified on **2026-08-18**. These are the official, vendor-published sources documenting how each model wants to be prompted and how models differ between versions — the raw material for writing `{MODEL_ADDENDUM}` blocks.

**How to use this for the corpus comparison:** pull the vendor guide for a model, then diff it against the per-model prompt variants the companies ship (in the leaked-prompts repo: `Amp/claude-4-sonnet.yaml` vs `Amp/gpt-5.yaml`, `Augment Code/gpt-5-agent-prompts.txt` vs their Sonnet variant, the per-model files under `VSCode Agent/`). Whatever a company added on top of the vendor guidance — or ignored from it — is the translation pattern you're hunting.

---

## Anthropic / Claude

The big finding: Anthropic now publishes **literal per-model prompting pages** whose sections are named behavioral quirks with tested drop-in system-prompt snippets. These are vendor-authored addendums — lift from them directly. Note the docs moved from docs.claude.com to **platform.claude.com**.

| Source | URL | Why it matters for addendums |
|---|---|---|
| Prompting best practices (hub) | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | The baseline that applies to every Claude model; links out to the per-model delta pages |
| **Prompting Claude Fable 5** | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5 | A vendor-written Fable 5 addendum: effort as primary knob, short instructions beat enumeration, evidence-grounded progress claims, eager subagent dispatch, early-stopping quirks |
| **Prompting Claude Opus 5** | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5 | Counterintuitive rules only the vendor knows: *remove* legacy "verify your work" lines (causes over-verification), scope-expansion tendency, narration habits |
| **Prompting Claude Sonnet 5** | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5 | Literalism, effort ladder (Sonnet 5 medium ≈ Sonnet 4.6 high), new tokenizer ~30% more tokens, design "house style" and how to break it |
| Prompting Claude Opus 4.8 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-4-8 | The 4.x-generation page — contrast with Opus 5 shows which behaviors *flipped* between generations (thinking default, subagent eagerness) |
| **Migration guide** | https://platform.claude.com/docs/en/about-claude/models/migration-guide | The densest model-vs-model behavioral diff doc: which old prompt patterns now break or backfire |
| What's new in Opus 5 | https://platform.claude.com/docs/en/about-claude/models/whats-new-opus-5 | Vendor changelog of Opus 5 behavior changes with runnable examples |
| Introducing Fable 5 & Mythos 5 | https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5 | Fable-specific hard constraints: `stop_reason:"refusal"` handling, thinking can't be disabled, summarized-only reasoning |
| Effort reference | https://platform.claude.com/docs/en/build-with-claude/effort | Per-model recommended effort tables — the setting differs per model; pin the right default per addendum |
| Thinking reference | https://platform.claude.com/docs/en/build-with-claude/thinking | Per-model thinking defaults (off on 4.8 → adaptive on 5s → always-on on Fable/Mythos) |
| System cards hub | https://www.anthropic.com/system-cards | 17 cards; deepest account of behavioral tendencies (Fable 5/Mythos 5 card: https://www.anthropic.com/claude-fable-5-mythos-5-system-card) |
| Claude Cookbook | https://platform.claude.com/cookbook | Runnable code for every knob, incl. model-specific workaround recipes |

Highest-value Claude deltas: thinking default flipped each generation; sampling params (temperature/top_p/top_k) and prefill **400-error** on Opus 4.7+; effort replaced thinking budgets; Opus 5/Fable 5 self-verify and delegate eagerly — legacy verification instructions now *hurt*; Fable prompts asking the model to reproduce its reasoning trigger a refusal classifier.

---

## OpenAI / GPT

The Cookbook moved: cookbook.openai.com → **developers.openai.com/cookbook**. The prompting-guide lineage is GPT-5 → 5.1 → 5.2 → 5.4 → the rolling "Using GPT-5.6" platform doc. There is **no** 5.3 or 5.5 guide (5.3 shipped only as Codex, folded into the Codex guide; 5.5 was folded into the rolling latest-model doc).

| Source | URL | Why it matters for addendums |
|---|---|---|
| **Using GPT-5.6** (rolling flagship guide) | https://developers.openai.com/api/docs/guides/latest-model | Every current knob (reasoning_effort incl. new `max`, text.verbosity), lean-prompt preference, migration advice from 5.5/5.4 ("test reasoning one level lower") |
| **Codex Prompting Guide** | https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide | The Codex quirk sheet: `phase` parameter *required* for gpt-5.3-codex, explicit warning that mainline GPT-5 prompts need rework, preamble cadence |
| GPT-5.2 Prompting Guide | https://developers.openai.com/cookbook/examples/gpt-5/gpt-5-2_prompting_guide | Best behavior-delta doc in the family: "Key Behavioral Differences" section + migration table mapping old models to 5.2 settings |
| GPT-5.1 Prompting Guide | https://developers.openai.com/cookbook/examples/gpt-5/gpt-5-1_prompting_guide | 5.1 quirks: over-conciseness tendency, `none` reasoning mode needing GPT-4.1-era prompting style |
| GPT-5 Prompting Guide (original) | https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide | The genre's template: agentic eagerness control both directions, tool preambles, contradiction sensitivity, Cursor's real-world tuning case study |
| Using GPT-5.4 | https://developers.openai.com/cookbook/examples/gpt-5/gpt-5-4_prompting_guide | 5.4-generation capabilities (tool search, 1M context, computer use) + mini/nano variant guidance |
| **GPT-5 Troubleshooting Guide** | https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_troubleshooting_guide | A ready-made quirks list: symptom → prompt-level fix, translates almost verbatim into addendum lines |
| Reasoning models guide | https://developers.openai.com/api/docs/guides/reasoning | The core principle separating reasoning models: give goals and constraints, don't prescribe steps |
| Prompt engineering guide | https://developers.openai.com/api/docs/guides/prompt-engineering | Role-authority hierarchy (developer > user > assistant), reasoning-vs-GPT "senior vs junior coworker" framing |
| GPT-5 New Params and Tools | https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_new_params_and_tools | Verbosity param, freeform tool calls, context-free grammars — harness-config details |
| API Changelog | https://developers.openai.com/api/docs/changelog | Dated record of every model release and default change — pins which addendum applies to which snapshot |
| GPT-5.6 System Card | https://deploymentsafety.openai.com/gpt-5-6 | Documents that 5.6 Sol "goes beyond the user's intent" more than 5.5 — exactly the tendency an addendum counters with autonomy boundaries |
| **ChatGPT Model Release Notes** (help center) | https://help.openai.com/en/articles/9624314-model-release-notes | The dated behavior/personality change log per release — e.g. May 2026 GPT-5.5 Instant restyle: "fewer overly long or bullet-heavy responses." Continuously updated |
| The builder's guide to GPT-5.6 | https://openai.com/index/builders-guide-to-gpt-5-6/ | Applied-AI post (Aug 13, 2026): production prompting lessons from startups — model selection, out-of-the-box behavior changes, prompt caching |

Fetching note: openai.com and help.openai.com block plain HTTP fetchers (Cloudflare), but both yield to Crawl4AI headless Chromium — help.openai.com works headless; openai.com needs `headless=False`. Local snapshots captured 2026-08-18: `research/openai-model-release-notes-2026-08-18.md` and `research/openai-builders-guide-gpt-5-6.md` in this repo. System cards are also mirrored fetchably at deploymentsafety.openai.com (5.5's is at /gpt-5-5).

---

## Google / Gemini

Vertex AI generative docs are rebranded "Gemini Enterprise Agent Platform" under docs.cloud.google.com. Newest GA model as of verification: **Gemini 3.7 Flash** (Aug 13, 2026); no Gemini 4 exists officially.

| Source | URL | Why it matters for addendums |
|---|---|---|
| **Gemini 3 Developer Guide** | https://ai.google.dev/gemini-api/docs/gemini-3 | Densest Gemini quirk source: temperature must stay 1.0 (looping risk), thinking_level replaces thinking_budget, "drop chain-of-thought scaffolding" |
| **What's new in Gemini 3.7 Flash** | https://ai.google.dev/gemini-api/docs/latest-model | Current flagship: sampling params deprecated entirely, prefilled model turns removed, stricter FunctionResponse matching |
| Prompt design strategies | https://ai.google.dev/gemini-api/docs/prompting-strategies | Vendor's own Gemini 3 section: direct, delimiter-consistent, context-first/instructions-last, default params |
| What's new in Gemini 3.5 Flash | https://ai.google.dev/gemini-api/docs/whats-new-gemini-3.5 | Version deltas: thinking default high→medium, thought preservation, intentionally terse — chatty personas need explicit steering |
| Gemini thinking guide | https://ai.google.dev/gemini-api/docs/thinking | Per-model thinking matrix + thought-signature round-trip rules agent platforms must respect |
| API release notes | https://ai.google.dev/gemini-api/docs/changelog | Dated deprecations (sampling params deprecated Jul 21, 2026) |
| Cloud: Get started with Gemini 3 | https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/start/get-started-with-gemini-3 | Cloud/Vertex-side migration guide confirming the 3.x deltas |
| DeepMind model cards hub | https://deepmind.google/models/model-cards/ | Dated cards for the whole 3.x family |
| Gemini 3 Pro model card (PDF) | https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-Pro-Model-Card.pdf | Primary-source limitations and knowledge cutoff |
| Models catalog | https://ai.google.dev/gemini-api/docs/models | Which model IDs exist, stability tier, positioning |
| Official cookbook repo | https://github.com/google-gemini/cookbook | Google-authored runnable prompts for the newest models |
| Cloud prompt-design intro | https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/introduction-prompt-design | Per-topic pages sometimes carry guidance the API docs omit |

Highest-value Gemini deltas: **keep temperature at 1.0** on 3.x; thinking_level is the knob; Gemini 3.x is deliberately terse and over-analyzes verbose prompt engineering — lean prompts win.

---

## xAI / Grok (+ Meta, Mistral)

docs.x.ai was restructured (old /docs/guides/* paths are **dead**, including the well-known Grok Code prompting guide — do not cite it). xAI currently publishes **no general prompt-engineering guide**; quirks are scattered across capability pages. Grok 5 is not released as of Aug 2026.

| Source | URL | Why it matters for addendums |
|---|---|---|
| Models overview | https://docs.x.ai/developers/models | Model/context/parameter matrix incl. logprobs unsupported on 4.20+ |
| **Reasoning capability page** | https://docs.x.ai/developers/model-capabilities/text/reasoning | Densest Grok page: per-model effort support, reasoning can't be disabled, presence/frequency/stop params rejected |
| Grok 4.6 model page | https://docs.x.ai/developers/grok-4-6 | Flagship capabilities + vendor advice (prompt_cache_key, context compaction) |
| May 2026 retirement/migration guide | https://docs.x.ai/developers/migration/may-15-retirement | Silent-default traps: auto-redirects apply reasoning_effort=low — pin model + effort explicitly |
| Grok 4.20 system card (PDF) | https://data.x.ai/2026-04-07-grok-4-20-model-card.pdf | Single-agent vs multi-agent modes, refusal posture |
| Grok 4.1 model card (PDF) | https://data.x.ai/2025-11-17-grok-4-1-model-card.pdf | Thinking/Non-Thinking split, deliberately narrow refusal policy |
| Multi-agent capability page | https://docs.x.ai/developers/model-capabilities/text/multi-agent | grok-4.20-multi-agent: effort selects 4 vs 16 agents; no client-side function calling, no max_tokens |
| Function calling | https://docs.x.ai/developers/tools/function-calling | Parallel calls default-on; function calls arrive whole in one stream chunk |
| Release notes | https://docs.x.ai/developers/release-notes | Dated behavior-knob changes Nov 2024 → Aug 2026 |
| Grok 4.6 announcement | https://x.ai/news/grok-4-6 | Vendor's own 4.5→4.6 behavioral characterization (more self-verification) |

**Meta Llama** (llama.com 301s to developer.meta.com): guidance is concentrated at the *template* level. The gold: per-generation "Model Cards and Prompt formats" pages — Llama 4: https://developer.meta.com/ai/docs/model-cards-and-prompt-formats/llama4/ (includes Meta's own suggested system prompt discouraging templated/moralizing language — effectively a vendor-authored behavioral addendum), Llama 3.1: https://developer.meta.com/ai/docs/model-cards-and-prompt-formats/llama3_1/ (the eot_id-vs-eom_id trap, "Environment: ipython" magic string). GitHub model card: https://github.com/meta-llama/llama-models/blob/main/models/llama4/MODEL_CARD.md. Newest documented generation remains Llama 4 (Apr 2025).

**Mistral**: publishes almost no per-model prompting differences — that absence is itself the finding. What exists: Reasoning page https://docs.mistral.ai/capabilities/reasoning (thinking-chunk preservation across turns is a hard requirement), Models overview https://docs.mistral.ai/models (alias lifecycle — `-latest` aliases silently re-point; pin versions), Changelog https://docs.mistral.ai/resources/changelogs, generic Prompting guide https://docs.mistral.ai/guides/prompting_capabilities.

---

## The cross-vendor pattern (preview for your comparison)

Reading all four side by side, the same addendum categories keep appearing, which suggests your addendum template should have exactly these slots:

1. **Effort/thinking knob defaults** — every vendor now has one (Anthropic effort, OpenAI reasoning_effort, Google thinking_level, xAI reasoning_effort), each with different per-model recommended settings.
2. **Eagerness calibration** — every vendor documents whether the model over- or under-acts (GPT-5.6 "goes beyond user intent," Opus 5 scope-expands, GPT-5.1 over-concise, Gemini 3.x terse) and gives counter-prompts.
3. **Scaffolding to REMOVE** — the newest theme: Opus 5 ("delete verify-your-work lines"), Gemini 3 ("drop chain-of-thought scaffolding"), GPT-5.6 ("leaner prompts"). Newer models are hurt by older models' scaffolding — direct confirmation of the future-proofing principle in your contract.
4. **Hard parameter constraints** — what 400-errors or silently breaks (sampling params on Claude 4.7+/Gemini 3.x, prefill removal, phase requirement on Codex).
5. **Version-delta migration notes** — every vendor now ships them; they are the addendum's changelog.
