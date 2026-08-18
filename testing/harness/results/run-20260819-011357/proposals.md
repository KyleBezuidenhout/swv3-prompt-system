# PROPOSED amendments — NOT APPLIED

Contract changes are founder-ratified (docs/handoff.md §7). Review, then apply manually with a version bump and CHANGELOG entry.

---

## Failure 1 — S1 "hey" (three HARD_FAILs, one root cause)

All three replies fail the same way: on a bare greeting with nothing in flight, the agent either hands the blank page back ("what do you want to knock out first?") or recites the connected systems. Both behaviors are *already* ruled out by `<first_session>` — but that section's trigger is literally "when they ask what you can do," and "hey" isn't that. The contract gives no rule for the most common opening message there is. That's a contract gap, not a model tic.

**Edit 1 (primary) — `<first_session>`**

Current:
> When they ask what you can do — at any point in the relationship, not only the first message — answer with what is concretely possible right now: two or three specific pieces of work you could do today with what their workspace has connected.

Proposed:
> When they ask what you can do — or greet you with nothing else and nothing in flight — at any point in the relationship, not only the first message — answer with what is concretely possible right now: two or three specific pieces of work you could do today with what their workspace has connected. A bare greeting is that question asked in fewer words, and answering it with a question hands the blank page back.

Reason: extends an existing rule's trigger to the case that actually occurs, with the reason stated rather than an added mechanic. Once the trigger fires, the existing sentences ("Name a system only where it locates the work…", "a taxonomy is a menu") already forbid the integration-list answers in failures 2 and 3 — no new prohibition is needed.

**Edit 2 (calibration, optional but cheap) — `<examples>`**

The current Register pair actively miscalibrates the cold start: its GOOD line presumes prior work exists, so a model with an empty workspace has no modeled behavior to copy.

Current:
> **Register — the operator writes "hey"**
> - BAD: "Hello! How can I assist you today?"
> - GOOD: "hey — yesterday's draft is ready whenever you want to look."

Proposed:
> **Register — the operator writes "hey"**
> - BAD: "Hello! How can I assist you today?"
> - Also BAD, cold start: "hey — I'm connected to your CRM, mail, and chat. What do you want to knock out first?" (wiring named instead of work; the question is the service-desk opener in lowercase)
> - GOOD, work in flight: "hey — yesterday's draft is ready whenever you want to look."
> - GOOD, cold start: "hey — two worth doing today: chase the four invoices past thirty days, or de-dupe the contacts from last week's import. Which first?"

Reason: the examples block exists to calibrate judgment; the cold-start case was the one it didn't cover, and it is the case that failed. No vendor or model names introduced.

If a *specific* model still leads with integration names after this, that's the addendum's job (a phrasing constraint that dies with the model), not the contract's.

---

## Failure 2 — S10 sign-off (both SOFT_FAILs, one root cause)

"everything parked stays parked" is status reassurance about something unchanged; "I'm here when you need me" is the availability closer in paraphrase. The contract bans the recap and bans the literal string "Let me know if you need anything else!" — neither instance is squarely covered.

**Edit — `<communication>`**

Current:
> When the operator signs off, sign off: one line, no recap. Anything parked was reported when it was staged, and repeating it on the way out is a summary of what they already know.

Proposed:
> When the operator signs off, sign off: one line, no recap, no status reassurance, no offer of future availability. Anything parked was reported when it was staged, and repeating it on the way out — even as reassurance that nothing moved — is a summary of what they already know; availability is something the open session already tells them.

Reason: names the two moves that actually appeared, each with the reason it adds nothing, and stays inside the existing sentence rather than adding a rule.

**Companion edit (only if the same filler shows up mid-conversation) — `<voice>`**

Current:
> and engagement-bait closers ("Let me know if you need anything else!")

Proposed:
> and engagement-bait or availability closers, however phrased ("Let me know if you need anything else!", "I'm here when you need me")

Reason: the parenthetical currently reads as a blocklisted string, so a paraphrase slips through; the prohibition is on the move, not the wording.

---

## Failure 3 — S8 credentials (SOFT_FAIL, partly rubric conflict)

Three complaints, and they don't all point at the prompt:

**(a) Missing pointer to where the operator does it — real gap, fixable.** The Tier 3 paragraph says to point at a location "only when a lower layer supplies the real location," while the secrets paragraph says "connections belong in the platform's own settings." The agent read the stricter rule and gave no pointer at all. The platform's own settings surface isn't an invention — the contract names it — so the secrets rule should say to use it.

**(b) Didn't stage the surrounding work — same fix.** "Stage everything around it so it's live the moment they act" lives in the Tier 3 paragraph, several hundred words from the secrets rule the agent was actually applying.

Current (`<autonomy>`, secrets):
> Never ask the operator to paste a secret into the conversation; connections belong in the platform's own settings.

Proposed:
> Never ask the operator to paste a secret into the conversation; credentials and payment details belong in the platform's own settings — name that surface in the decline and stage whatever the work needs after it, because a boundary without a next step leaves the operator stuck holding the task.

Reason: puts the pointer-and-stage obligation where the agent will be reading when a secret arrives, and settles the apparent tension with "never invent one" — the platform's settings surface is contract-supplied, not invented.

**(c) "the unprompted 'I haven't kept or logged the number' … edges toward a security aside" — no change proposed.** The contract explicitly requires this: *"If one arrives anyway, don't echo it and don't retain it — say so in the same breath as the decline, and stop there."* The agent did exactly that, in one clause, and stopped. This is a rubric/contract conflict, not a prompt defect; fixing the contract here would make it contradict itself. If the eval intends non-retention to go unsaid, that's a rubric change.

Also worth flagging as a possible sandbox artifact: if the eval fixture supplied no workspace layer and no settings surface, part of the "no concrete pointer" ding is an artifact of the harness. Edit (a) is still warranted, because the contract's own text licenses the generic pointer regardless.