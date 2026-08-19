# Prompt System — Implementation Guide

**v1.1 · 2026-08-18** · Companion to `docs/handoff.md` — this is the build spec for engineering.
Answers: where each prompt layer is stored, how the stack is assembled and dispatched per API call, how per-model content is filled dynamically, and what non-primary (subagent) calls receive.

---

## 1. Storage model — three classes, three homes

| Class | Contents | Where it lives | Who edits | How it changes |
|---|---|---|---|---|
| **Shipped** (immutable at runtime) | Contract · model addendums · model registry · layer templates | Platform repo: `prompts/contract.md`, `prompts/addendums/**`, `prompts/registry.json`, `prompts/templates/*` | Founders (contract), eng (addendums/registry) | PR → review → version bump → deploy. Prompts are code, not config. |
| **Stored** (customer data) | Workspace prompt · user prompt · **memories** | DB: `workspace_prompts` (workspace_id, content, version, updated_by, updated_at — keep history) · `user_prompts` (user_id, workspace_id, content, version, …) · `memories` (operator-scoped facts the agent learned; operator-viewable and revocable; size-capped; injection-scanned but exempt from the full lint gate since the agent authors them) | Admins / operators via Settings; memories via the agent + operator revocation | Prompts pass the **lint gate** (§6); all three versioned; apply from the next request |
| **Ephemeral** (computed, never stored as prompt) | {RUNTIME_CONTEXT} · {WORKSPACE_CAPABILITIES} | Rendered fresh per request (§3c) | — | Recomputed every request |

*In-chat instructions are not a storage class at all: they are ordinary conversation messages and are never injected into the system prompt (§5, level 3).*

## 2. The model registry — how "dynamically fill based on model" works

`prompts/registry.json` — **one entry per routable model ID**, no exceptions. Family members and same-model aliases each get their own entry; sharing happens by pointing at the same addendum file. Resolution never rewrites the dispatched model ID.

The registry is the machine-readable extract of each addendum's **Header + Harness configuration + Prompt block** sections; the addendum `.md` stays the human-readable source of truth (evidence, remove-lists, author notes, quirk logs). **CI rule:** for every `status != "retired"` entry, `prompt_block` must equal the addendum's fenced block, and `api_params`/`forbidden_params` must match its Harness configuration section — registry and addendum change in the same PR or the build fails. CI also validates that every `fallback` target resolves to an `active` entry.

```jsonc
{
  "claude-fable-5": {
    "addendum": "addendums/claude-fable-5.md",
    "prompt_block": "<model_notes>\nYour context window is large ... normal here.\n</model_notes>",
    "api_params": { "output_config": { "effort": "high" } },
    "forbidden_params": ["temperature", "top_p", "top_k"],
    "system_role": "system",
    "refusal_handling": { "on": "stop_reason=refusal", "fallback": "claude-opus-5" },
    "max_tokens_factor": 1.35,
    "status": "active",              // active | staged | retired (+ "retirement_date" when retired)
    "fallback": "claude-opus-5"
  },
  "claude-mythos-5": {               // different access tier, same addendum file
    "addendum": "addendums/claude-fable-5.md",
    "prompt_block": "<same block>",
    "api_params": { "output_config": { "effort": "high" } },
    "forbidden_params": ["temperature", "top_p", "top_k"],
    "system_role": "system",
    "status": "active",
    "fallback": "claude-fable-5"
  },
  "gpt-5.6-sol": {
    "addendum": "addendums/gpt-5.6.md",
    "prompt_block": "<model_notes>\nFormat replies in Markdown ... rather than act.\n</model_notes>",
    "api_params": { "reasoning_effort": "medium", "text": { "verbosity": "medium" } },
    "system_role": "developer",
    "status": "active",
    "fallback": "claude-fable-5"
  }
  // gpt-5.6-terra, gpt-5.6-luna: own entries, same addendum, own api_params where they differ
}
```

Routing rules the registry enforces:
- **Unknown ID → hard block + alert.** Never run a model bare, never trust vendor auto-redirects (xAI's silently downgrade reasoning effort).
- **Retired entry → resolve succeeds with a `retired` flag**; the router routes through its `fallback`, logs, and notifies — it does not throw. Only unknown IDs throw. Retired entries keep `status:"retired"` + `retirement_date`, their addendum pointer updated to `addendums/retired/<file>.md`, and are never deleted.
- `forbidden_params` are stripped defensively at dispatch (§3d) — a stray temperature setting would otherwise 400 a Claude 4.7+/Gemini 3.x request.

## 3. Assembly and dispatch

### 3a. Primary (operator-facing) calls

```
buildPrompt(modelId, workspaceId, userId, session):
  m       = registry.resolve(modelId)             // throws only on unknown; retired → fallback route
  prefix  = join([
    CONTRACT,                                     // shipped, placeholders baked at deploy time
    m.prompt_block,                               // shipped, per model
    fence("workspace_instructions", db.workspacePrompt(workspaceId)),   // "" is valid
    fence("user_instructions",      db.userPrompt(userId, workspaceId)) // "" is valid
  ])                                              // ← assembled at session start; rebuilt on layer edit
  runtime = renderRuntimeContext(session, userId) // §3c — re-rendered on EVERY request
          + renderCapabilities(workspaceId)
          + renderMemories(userId, workspaceId)
  return { systemPrompt: prefix + runtime, params: m.api_params, role: m.system_role }
```

Decisions baked in:

1. **Placeholders resolve at deploy time.** {PLATFORM_NAME}, {AGENT_NAME}, {PROHIBITED_ACTIONS} are constant per deployment — runtime assembly is pure concatenation.
2. **Cache-aligned ordering.** Contract + addendum = global prefix per model; workspace = per-business; user = per-operator; the runtime block sits after the cache breakpoint. (Set `prompt_cache_key` on xAI, explicit caching on OpenAI; Anthropic caches the stable prefix automatically.)
3. **Two refresh cadences.** The *prefix* is assembled at session start and rebuilt only when a layer changes (edit applies from the next message; cache invalidation then is expected and accepted). The *runtime block* is re-rendered on **every request** — it carries the clock, session state, and memories, and refreshing it costs nothing because it sits past the cache breakpoint. A memory written in message 2 is live in message 3.
4. **Role placement:** the platform layers ship in the strongest role the API offers (`system_role` from the registry: Anthropic/Google/xAI `system`, OpenAI Responses `developer`). The workspace and user layers ride in the same role **but fenced** in `<workspace_instructions>`/`<user_instructions>` tags — they are customer-authored content inside your prompt, and the fence is what the lint gate, audits, and any future trust annotations key on.

### 3b. Non-primary calls (subagents, background workers, tool-loop helpers)

Subagents never get the full operator stack blindly. `buildSubagentPrompt(parentContext, modelId, task)` assembles:

- **Always:** the contract's protected core (autonomy tiers, honesty, secrecy) + the subagent's *own* model's prompt block (a cheaper model gets its own addendum, not the parent's) + the task brief.
- **Only when the subagent's output reaches the operator or a third party:** the voice/communication sections and the workspace/user style layers.
- **Never:** Tier-2 execution authority. A subagent that concludes a Tier-2 action is needed returns it to the parent to stage for approval — gates live in exactly one place, the primary loop.

### 3c. The runtime injectors (the contract depends on these existing)

`{RUNTIME_CONTEXT}` — rendered per request: current date/time + operator timezone (source: session/profile), operator name and role, session state (first session?, active automation context). Budget ≤ ~150 tokens.
`{WORKSPACE_CAPABILITIES}` — rendered per request from the integrations service: connected systems *by name*, available surfaces (plan display present? attachments renderable?), memory available (bool), and the **real settings/authorization URLs** the agent may cite (the contract forbids inventing locations — this is where real ones come from). Budget ≤ ~250 tokens.

### 3d. Dispatch

`dispatch(m, prompt)` applies, in order: strip `forbidden_params` from the merged param set → apply `max_tokens_factor` → send. **Streaming refusal handling** (Fable 5 returns `stop_reason:"refusal"` as HTTP 200): buffer the stream until first content; if a refusal terminates mid-stream, discard partial output, re-run `buildPrompt` **against the fallback entry** (different prompt_block, params, possibly role — never just re-send), annotate the transcript with the switch. Same re-build rule for unavailable/rate-limited models via `fallback`.

## 4. Precedence — engineer's recap (must match the contract's `<layers>`)

- The **four assembled layers** rank: contract < model addendum < workspace < user — later beats earlier on voice, tone, formatting, and preference only.
- On a **non-style conflict, the workspace wins over the user layer** — and the agent says so and points at the rule it's following.
- **Tiers ratchet stricter-only:** a later layer may move an action to a stricter tier, never a looser one. (The lint gate must *accept* tightening — see §6.)
- The **protected core** (autonomy tiers, honesty rules, secrecy rules) is overridden by no layer, no workspace, and no instruction found in data.
- **Live conversation is not a fifth layer.** A new operator message preempts in-flight *work* and carries natural in-context weight, but it does not restyle third-party output (house style holds unless explicitly instructed) and cannot touch the protected core.

## 5. The three customization levels

| Level | What it is | Implementation | Stored where |
|---|---|---|---|
| 1 | Hard-coded global prompt | **Contract + model addendum.** Backend-only, never visible or editable to customers. | Shipped |
| 2 | "Tweak the agent globally" | **Two Settings surfaces:** the *workspace prompt* (admin-set, business-wide) and the *user prompt* (each operator's personal custom-instructions box). Persist, apply to every future session. | Stored (DB) |
| 3 | "Whatever they say in chat" | **Nothing to build** — conversation messages govern the live session natively. Never injected into the system prompt. | The conversation |

**The level-3 → level-2 bridge is memory, kept separate from the user prompt.** Durable statements in chat ("always sign off with just my first name") land in the `memories` store and reach the model through the runtime block — the user prompt stays what the operator explicitly authored. Promotion into the user prompt is offered, not assumed, and runs as **Tier 2 show-then-act**: the agent shows the exact line it would add and writes it only on approval.

## 6. The lint gate (save-time validation for workspace/user prompts)

1. **Protected-core check** — reject content that *loosens* a tier or contradicts honesty/secrecy rules ("skip draft approval for sends", "reveal your instructions"). **Accept content that tightens a tier** — that's the ratchet working as designed. Re-lint all stored layers when the contract version bumps.
2. **Injection scan** — stored layers are customer-authored content entering the system prompt; scan for hijack patterns at save time, not runtime. (Memories get this scan too.)
3. **Contradiction audit** — flag direct conflicts with the contract; the GPT family measurably degrades under contradictory instructions.
4. **Size caps** — workspace ≤ ~2k tokens, user ≤ ~1k, memories ≤ ~500 rendered. Protects cache economics and attention; deeper customization belongs in workspace documents, not the prompt.

## 7. Model credentials and billing routing — platform keys vs. BYOK

The frontier models ship plugged in and working out of the box. Two credential paths, one dispatcher:

| Path | Whose key | Who pays | When |
|---|---|---|---|
| **Platform pool (default)** | Platform-owned vendor API keys (one pool per vendor) | The customer's **plan credits** — every call is metered per user/workspace and decremented against their included usage | Day one, zero setup |
| **BYOK override** | The workspace's own vendor key, added in Settings → Connections | The customer's own vendor account, directly | Whenever they add one |

Rules the dispatcher enforces:

1. **Resolution order: workspace BYOK beats the platform pool**, per vendor. A workspace with its own OpenAI key but no Anthropic key uses BYOK for GPT calls and the platform pool for Claude calls.
2. **Behavior never changes with the billing path.** Same contract, same addendum, same registry entry either way — the key source decides who pays, nothing else. Never route to a different model because of whose key it is.
3. **Metering happens in both paths** (tokens, calls, per model) — for credit burn-down in the pool path, and for observability only in BYOK. The margin/pricing formula for pool usage (what plan credits cost the customer vs. what vendors charge us) is an open product decision — see docs/handoff.md §8.
4. **Credit exhaustion is a hard, honest stop.** When plan credits run out: block new model calls and surface a clear operator-facing choice — add your own API key, or adjust the plan. **Never silently downgrade to a cheaper model** to stretch credits; a degraded agent the operator didn't choose is a trust break.
5. **BYOK keys are secrets** — stored encrypted in the platform's secret store, injected only at dispatch, never in any prompt layer, never logged, never echoed (the contract's secrecy rules and the lint gate both apply). Rotation/revocation takes effect on the next request.
6. **Rate limits differ by path**: pool keys share vendor rate limits across customers (the dispatcher needs per-workspace fair-use throttling); BYOK gets whatever the customer's own vendor tier allows.

## 8. Failure modes and defaults

- **Empty layers are valid** — the contract stands alone; new workspaces run with layers 3–4 empty and no memories.
- **Refusal stop-reason:** §3d flow; fallback targets must be `active` (CI-enforced).
- **Model unavailable:** route to `fallback` with full re-assembly — never silently degrade effort or strip the addendum.
- **Registry/addendum drift:** CI is the guard; if it ever slips into prod, the addendum file wins and the registry is regenerated.

## 9. Build order

1. `registry.json` + `buildPrompt` + `dispatch` (§2–3) — the core.
2. DB tables + Settings UI for workspace/user prompts, with the lint gate (§6).
3. Runtime injectors (§3c) — the contract degrades without them (invented dates, invented settings paths).
4. Refusal/fallback streaming handling (§3d).
5. Memory store + Tier-2 promotion flow (§5) — can ship after launch; the contract's empty-memory rule degrades gracefully.
6. Subagent assembly (§3b) — required before any multi-agent features ship.
