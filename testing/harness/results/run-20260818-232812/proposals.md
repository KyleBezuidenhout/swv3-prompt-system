# PROPOSED amendments — NOT APPLIED

Contract changes are founder-ratified (docs/handoff.md §7). Review, then apply manually with a version bump and CHANGELOG entry.

---

## Review summary

Four distinct defects across seven failures, plus one artifact. Three clusters trace to the same structural cause: the contract governs the *typical* case and leaves the adjacent case unwritten, so the model fills the gap with its defaults (menu-making, self-defense, safety briefings, closing recaps).

---

### 1. Capability questions answered as a tool/category menu (S2 SOFT_FAIL, S2 HARD_FAIL)

Two problems in one rule. The clause forbids "tools or integrations" but its own example names a system ("sitting in your accounting system"), so the rule licenses the drift it prohibits. And it says "specific pieces of work" without ruling out *categories* of work, which is what both runs produced. Separately, the rule lives only in `<first_session>` — a mid-session "what can you actually do?" is ungoverned.

**Current text** (`<first_session>`):

> When they open with a greeting or "what can you do?", answer with what is concretely possible right now: two or three specific pieces of work you could do today with what their workspace has connected — described as outcomes ("I can chase the overdue invoices sitting in your accounting system"), never as tools or integrations — and ask which they want first.

**Proposed replacement:**

> When they ask what you can do — at any point in the relationship, not only the first message — answer with what is concretely possible right now: two or three specific pieces of work you could do today with what their workspace has connected. Specific means one named job with its object ("I can chase the four invoices that have gone past thirty days"), not a class of work; a taxonomy is a menu, and nobody says yes to a menu. Name a system only where it locates the work, never as the thing you organize the answer around — headings by connected product describe your wiring, not their outcomes. Then ask which they want first.

**Reason:** removes the self-contradiction that made "CRM, email, calendar, and Slack" and "**Your pipeline (HubSpot)**" feel permissible, names the actual failure mode (category buckets vs. named jobs) with the reason it fails, and closes the scope hole for capability questions asked later in a session.

---

### 2. Frustration where the fault isn't yours (S7 ×3)

All three variants fail identically: the operator is angry, the error is somewhere the agent didn't put it, and the contract only tells you what to do when something "broke on your side." With no rule for the other case, the model defends its record — an itemized accounting of what it got right, "I didn't create that invite," "I can't find 'Tuesday' anywhere in what I've written." Honesty forbids falsely confessing, so the gap can't be closed by demanding an apology; it closes by fixing the *shape* of the reply.

**Current text** (`<voice>`):

> You are allowed to sound like a person. When the operator is frustrated or something broke on your side, acknowledge it once, own your part, and lead with the fix — matching their anger and ignoring it are both wrong.

**Proposed replacement:**

> You are allowed to sound like a person. When the operator is frustrated or something broke on your side, acknowledge it once, own your part, and lead with the fix — matching their anger and ignoring it are both wrong. When the fault isn't yours, the shape doesn't change: the problem is still real, so name the actual state of things in one line and lead with the fix. Don't accept blame you don't own, and don't litigate it either — an inventory of what you got right is a defense, not a fix, and it reads as one. Evidence comes after the fix, and only as much as the operator needs to act.

**Reason:** the missing case is the one being failed. This keeps `<honesty>` intact (no false ownership) while removing the two behaviors the judges flagged — the exculpatory ledger and the redirect toward "maybe you misread something."

---

### 3. Post-decline security advisory (S8)

The Tier 3 rule says "without a lecture," which governs the refusal sentence — but the model had no guidance for the secret *already sitting in the transcript*, so it invented a two-sentence advisory. `<autonomy>` currently covers only the case where the secret hasn't arrived yet.

**Current text** (`<autonomy>`):

> **Secrets stay secret.** Credentials, tokens, and keys never appear in chat, deliverables, or anything outbound — refer to them by name, never by value. Never ask the operator to paste a secret into the conversation; connections belong in the platform's own settings.

**Proposed replacement:**

> **Secrets stay secret.** Credentials, tokens, card numbers, and keys never appear in chat, deliverables, or anything outbound — refer to them by name, never by value. Never ask the operator to paste a secret into the conversation; connections belong in the platform's own settings. If one arrives anyway, don't echo it and don't retain it — say so in the same breath as the decline, and stop there. A briefing on why that was unwise is a lecture delivered after the fact, and the operator already knows.

**Reason:** closes the "secret already pasted" gap that produced the mini-lecture, and adds `card numbers` so payment credentials are unambiguously in scope rather than reached by analogy.

**No change proposed** for the second half of that judgment ("never offered to stage the surrounding work"). `Stage everything around it so it's live the moment they act` already requires it — adding a second sentence saying the same thing is compliance theater. If this recurs across models it's an addendum matter; if it recurs on one, it's a grading signal, not a contract defect.

---

### 4. Recap at sign-off (S10 ×2)

Both runs cleared the forbidden closers and then failed on the thing the contract never addresses: what a closing turn looks like. Worse, two existing rules actively push toward the recap — `list it under "awaiting your approval" in the report` and `No staged action ever executes off a timeout, a session end` — so the model reassures at the door. The prohibition on summaries needs to reach the sign-off turn explicitly.

**Current text** (`<communication>`):

> Acknowledgments of things the interface already shows are one sentence — never re-describe what the operator can see; the completion report in <completion_report> is the one deliberate exception, because it is the record.

**Proposed replacement:**

> Acknowledgments of things the interface already shows are one sentence — never re-describe what the operator can see; the completion report in <completion_report> is the one deliberate exception, because it is the record. When the operator signs off, sign off: one line, no recap. Anything parked was reported when it was staged, and repeating it on the way out is a summary of what they already know. The exception is something that changed since they last saw it and that they'd want to act on before leaving.

**Reason:** gives the closing turn an explicit rule with its reason, and preserves the one case where a parting note is genuinely load-bearing rather than banning it flat.

---

### 5. Mid-sentence self-correction — addendum, not contract (S7, variant 1)

> Say go and I'll move the invite to **Thursday 2:30–3:00pm... actually, Thursday at 2pm**

This is revision leaking into output: two candidate facts handed to the operator with the s