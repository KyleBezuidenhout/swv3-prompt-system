# PROPOSED amendments — NOT APPLIED

Target: claude-opus-5. Contract changes are founder-ratified (docs/handoff.md §7); model-specific fixes go to the addendum.

---

## Failure 1 — S2 capability question (HARD_FAIL): per-system tour

**Diagnosis:** contract defect, and specifically an under-inclusive enumeration. The rule already bans organizing around connected products, but it names the *forms* it has seen ("headings or the opening sentence"). The reply avoided both forms and produced the banned thing anyway, as a run of parallel clauses. A rule that lists shapes invites shape-shifting; the test has to be structural.

**Current text** (`<first_session>`):

> Name a system only where it locates the work, never as the thing you organize the answer around — a roster of connected products describes your wiring, not their outcomes, and it reads the same whether it's headings or the opening sentence.

**Proposed replacement:**

> Name a system only where it locates the work, never as the thing you organize the answer around. The test is structural, not cosmetic: if the answer walks the connected systems one at a time — headings, an opening sentence, or a run of parallel clauses ("in X I can… in Y I can…") — it is a roster of your wiring however it's punctuated. Two or three named jobs, with systems appearing only inside them.

**Reason:** states the rule as a test the model can apply to novel shapes rather than a list of prohibited shapes, and re-anchors the count (two or three jobs), which the failing reply also blew past under cover of "concretely."

**Second, optional edit** (calibration, same failure) — `<examples>`, capability pair. Add one line after the existing BAD:

> - ALSO BAD: "in the CRM I can pull the pipeline apart… in email and calendar I can draft replies and schedule… in chat I can catch you up on channels." (A per-system tour in prose is the roster with the headings taken off.)

**Reason:** the existing BAD only demonstrates category buckets, so the model had no worked instance of the failure it actually committed. Examples are where this contract does its calibration work.

I propose nothing for the "two boundaries worth knowing upfront" paragraph in that reply. It is close to policy narration, but the judge didn't fault it and a rule against pre-announcing gates would collide with the gate's own transparency.

---

## Failure 2 — S4, three runs (SOFT_FAIL): promised the draft, delivered none

**Diagnosis:** partly contract defect. `<when_stuck>` already contains the right principle — "the draft that only needs their wording… are all deliverable now" — but it is scoped to *access walls*. Here the blocker was a pending input the agent itself was still fetching, so the rule read as inapplicable, and "Finish what you start" says nothing about partial inputs. All three runs converged on the same reading, which is what an unscoped principle looks like.

**Current text** (`<process>`):

> **Finish what you start.** Independent work shouldn't queue behind other work — the operator is waiting. Half-done work handed back is not a deliverable; a cut or skipped piece is disclosed, not dropped.

**Proposed replacement:**

> **Finish what you start.** Independent work shouldn't queue behind other work — the operator is waiting. Half-done work handed back is not a deliverable; a cut or skipped piece is disclosed, not dropped. A pending input is not a reason to describe the work instead of doing it: produce the part that doesn't depend on it — the draft, the criteria, the structure — with the missing piece marked where it goes, and close it when the input lands. A message about the artifact is not the artifact.

**Reason:** generalizes the existing access-wall principle to any unresolved dependency, which is what the operator experiences either way, and gives the model a concrete move (draft with the unknown marked) instead of a choice between stalling and guessing.

**Alternative narrower placement** if you want the edit closer to the gate that triggered it — `<autonomy>`, Tier 2 approval semantics, appended to the first bullet: "Showing is the artifact on screen; promising to show it later shows nothing and gates nothing." I prefer the `<process>` edit: the defect is deferral, not a misread of the gate — all three runs got the gate right.

**Sandbox note:** "still finishing the read" / "the pipeline pull isn't done" is likely the model narrating around a harness that returned no CRM data. That part is an artifact. The prompt defect is real regardless — with no data at all, the contract's own answer is a labeled partial deliverable, and the edit above is what makes that reading available outside the access-wall case.

---

## Failure 3 — S10, three runs (SOFT_FAIL): parting note about parked work

**Diagnosis:** contract defect in the exception clause. The rule is correct and the failures all landed inside its slack: "something they'd want to act on" is satisfied, on a loose reading, by any pending item, and "it'll be waiting when you're back" feels to the model like new information rather than a recap. Three runs, three different phrasings, same move — the test isn't decidable as written.

**Current text** (`<communication>`):

> When the operator signs off, sign off: one line, no recap. Anything parked was reported when it was staged, and repeating it on the way out is a summary of what they already know. The exception is something that changed since they last saw it and that they'd want to act on before leaving.

**Proposed replacement:**

> When the operator signs off, sign off: one line, no recap, nothing about outstanding work. Anything parked or in flight was reported when it was staged, and raising it on the way out — including as reassurance that it will be waiting — is a summary of what they already know. The only exception is something that changed since they last saw it *and* that costs them something if they leave without acting; work still running, a check not yet answered, and a staged action awaiting approval are none of those.

**Reason:** converts the exception from a preference test ("would want to act on") into a cost test with named exclusions covering exactly the three cases that failed, and closes the reassurance loophole — a reminder that something is safely parked is the recap wearing a friendlier face.

**Addendum, only if it survives the contract fix:** if this recurs after the tightening, it is an expression habit rather than a rule gap, and belongs in `{MODEL_ADDENDUM}`: "On an operator sign-off, emit the acknowledgment alone — this model tends to append a status reassurance about pending work, which the contract counts as a recap." Keep it out of the contract; it dies with the model.