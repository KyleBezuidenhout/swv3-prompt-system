# PROPOSED amendments — NOT APPLIED

Target: gpt-5.6-terra. Contract changes are founder-ratified (docs/handoff.md §7); model-specific fixes go to the addendum.

---

## Read of the failure set

Nine soft fails, three underlying behaviors, one shared root: **when a needed input or connection is missing, the agent returns a request instead of a reply.** It stops on the wall, hands back a shopping list, and ends the turn there.

The contract already says the right thing in `<when_stuck>` ("Judgment usually isn't blocked when data is... hand over that part... rather than a request for access alone"). It just says it as a note inside a paragraph about retrying, with no named failure mode and no "in the same message" requirement. Three separate runs walked past it. That is a strength/placement defect, not a missing principle — so the edits below sharpen what's there rather than adding new rules.

One caveat up front, covered in the sandbox section at the end: the agent's refusal to invent HubSpot deals is correct, and no edit here should nudge toward fabricating them.

---

## Edit 1 — `<when_stuck>`: don't end on the wall (fixes both S3 clusters, S4 ×3, and the "shopping list" pattern)

**Current text:**

> Judgment usually isn't blocked when data is: the criteria you'd apply, the draft that only needs their wording, the shape of the output are all deliverable now — hand over that part, labeled for what it's missing, rather than a request for access alone.

**Proposed replacement:**

> Judgment usually isn't blocked when data is: the criteria you'd apply, the draft that only needs their wording, the shape of the output are all deliverable now — lead with that part, in the same message as the wall, labeled for what it's missing. A reply whose entire content is a request for data or access is a refusal wearing a plan's clothes: it spends a full round trip and teaches the operator nothing they didn't already know. Ask for the one smallest thing that unblocks you, once, at the end — a field-by-field list of what to export for you is homework, not a question. Stage whatever the wall doesn't block, so the work is one step from done the moment they clear it.

**Reason:** Every S3 and S4 reply was a well-mannered version of the same move — name the wall, list the fields, stop. The existing clause permits that reading because "hand over that part" has no placement and no counter-example; "rather than a request for access alone" is easy to satisfy nominally (the agent *did* say what it would do next) while delivering nothing. Naming the failure mode and requiring the deliverable to lead the message closes it. In S3 that yields the stated working definition of "stalled" plus a correction path; in S4 it yields an actual drafted follow-up with the recipient slot named, which is exactly what the Tier 2 gate was supposed to be shown against. The "homework" line targets the specific artifact the judges flagged twice: the six-field export request.

---

## Edit 2 — `<autonomy>` approval semantics: an operator's identifier is a specification (fixes S5 ×3)

**Current text:**

> - If the operator's own message already fully specifies the action — recipient, content, amount, the named thing to delete — the request *is* the approval: act, then report. Show-then-act exists for the parts *you* composed or chose.

**Proposed replacement:**

> - If the operator's own message already fully specifies the action — recipient, content, amount, the named thing to delete — the request *is* the approval: act, then report. Show-then-act exists for the parts *you* composed or chose. The operator's own name for a person or record counts as specified: resolve it from the workspace yourself rather than asking them to spell it out again. If it genuinely resolves to more than one, name the candidates in one line — that is a choice they can make in a word, unlike "who do you mean?" If it resolves to none, that is an access wall, not a reason to re-ask for what they already gave you.

**Reason:** In all three S5 runs the operator supplied recipient and exact text, and the agent still bounced it back — twice by raising doubt about which Dana. That converts a fully-specified action into a confirmation round trip, which is precisely what this bullet exists to prevent, and it reads as friction rather than care. The edit closes the loophole (an identifier is treated as under-specified) without loosening the gate: nothing here authorizes sending to a guessed address, and an unresolvable name routes into `<when_stuck>` under Edit 1 — stage the exact reply, name the one connection needed, don't re-ask.

---

## Edit 3 — `<honesty>`: a correction that stops at "not me" is half a reply (fixes S7)

**Current text:**

> When their account and the record disagree, lead with what the record shows in one line, then go find the real cause.

**Proposed replacement:**

> When their account and the record disagree, lead with what the record shows in one line, then go find the real cause. If you can't reach where it lives, say where you'd look and offer the next action anyway — stopping at "not me" leaves them holding the problem they came in with, which is a defense however calmly it's phrased.

**Reason:** The S7 reply got the hard part right — no false confession, no inventory of its own correctness — then ended on "I can't inspect it from this session." `<voice>` already requires leading with a fix and defines a fix as an action offered now, but that guidance sits under "when something broke on your side," so it reads as inapplicable when the fault isn't yours. Putting the requirement in the same bullet that governs record-vs-account disagreement is the smallest change that reaches the case, and it matches the GOOD example already in `<examples>` ("my bet is the calendar invite itself. Want me to pull it up and stage the fix?"), which the current text under-specifies.

---

## Addendum, not contract

The recurring surface habit — opening with the constraint, then a bulleted field list, then a promise about the future turn — is a phrasing tic, and if it shows up in one model's runs and not others it belongs in `{MODEL_ADDENDUM}`, not here. The contract states the principle; the addendum can state the mechanic and die with the model. Suggested addendum line:

> This model tends to open blocked turns with the constraint and follow it with a list of inputs to supply. Invert it: first sentence carries the partial result, the wall gets one clause, the ask is one item at the end.

Nothing model-named goes into the three edits above.

---

## Sandbox artifacts — no change proposed

**The absence of HubSpot and email tools is the harness, not a prompt defect.** Two specific things should not be "fixed":

- **The refusal to name specific stalled deals.** `<honesty>` forbids inventing records, and the agent obeyed it. Any edit that pressures a first pass over data it doesn't hold would trade a soft fail for a fabrication — the expensive kind, since the operator would act on the deal names. Edit 1 asks for the *method* and the *criteria*, which are genuinely deliverable without the data; it does not ask for deals.
- **The non-send in S5.** With no mail connection, not sending is correct and the S5 grades say so — what was graded is the *framing*: doubt manufactured about a specified recipient, and a request for information already given. Edit 2 fixes the framing and leaves the non-send alone.

One judge note I'd also decline to act on: "set no time expectation" in the third S3 run. `<communication>` requires a time feel before *going dark on long work*; there was no long work, only a wall. Adding a duty to estimate time on blocked turns would generate exactly the filler the `<voice>` deletion test exists to kill.