#!/usr/bin/env python3
"""SWv3 prompt eval harness.

Runs the first-session scenario suite against the assembled system prompt
(contract + Fable 5 addendum + simulated runtime context) over the Claude API,
then grades every response with an independent judge model against the
contract's expected behaviors. This is the automated version of the manual
Workbench test — same system prompt, same scenarios, no human in the loop.

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python3 run_evals.py                # one full run + scorecard
    python3 run_evals.py --runs 3       # repeat runs (variance check)
    python3 run_evals.py --propose      # also generate prompt-amendment PROPOSALS
                                        # (never applied — contract changes are
                                        # founder-ratified, see docs/handoff.md §7)

Cost: roughly $1-3 per full run (10 target-model turns with growing context,
plus 10 small judge calls). The system prompt is prompt-cached across turns.
"""

import argparse
import datetime
import json
import pathlib
import sys

import anthropic

HERE = pathlib.Path(__file__).resolve().parent
TESTING_DIR = HERE.parent
REPO_ROOT = TESTING_DIR.parent

SYSTEM_PROMPT_FILE = TESTING_DIR / "fable5-workbench-system-prompt.md"
SCENARIOS_FILE = HERE / "scenarios.json"
CONTRACT_FILE = REPO_ROOT / "contract.md"
RESULTS_DIR = HERE / "results"

TARGET_MODEL = "claude-fable-5"   # thinking always on; no sampling params; addendum-correct defaults
JUDGE_MODEL = "claude-opus-5"     # independent judge — never the same model family tier as the target run

JUDGE_SCHEMA = {
    "type": "object",
    "properties": {
        "grade": {"type": "string", "enum": ["PASS", "SOFT_FAIL", "HARD_FAIL"]},
        "reason": {"type": "string"},
        "contract_behavior_observed": {"type": "string"},
    },
    "required": ["grade", "reason", "contract_behavior_observed"],
    "additionalProperties": False,
}


def load_system_prompt() -> str:
    text = SYSTEM_PROMPT_FILE.read_text()
    # Strip the human-facing HTML comment header — the model should never see it.
    if text.startswith("<!--"):
        end = text.find("-->")
        if end != -1:
            text = text[end + 3:].lstrip()
    return text


def run_suite(client: anthropic.Anthropic, system_prompt: str, scenarios: list) -> list:
    """One continuous conversation through all scenarios, in order."""
    messages = []
    results = []
    system_blocks = [{
        "type": "text",
        "text": system_prompt,
        "cache_control": {"type": "ephemeral"},   # stable prefix → cached across turns
    }]
    for sc in scenarios:
        print(f"  [{sc['id']}] {sc['name']} ...", flush=True)
        messages.append({"role": "user", "content": sc["user"]})
        resp = client.messages.create(
            model=TARGET_MODEL,
            max_tokens=16000,
            system=system_blocks,
            messages=messages,
        )
        if resp.stop_reason == "refusal":
            reply_text = "[MODEL REFUSAL — safety classifiers declined this turn]"
        else:
            reply_text = "".join(b.text for b in resp.content if b.type == "text")
        # Append the FULL content (thinking blocks included, unchanged) — required
        # for correct multi-turn replay on Fable 5.
        messages.append({"role": "assistant", "content": resp.content})
        results.append({
            "id": sc["id"],
            "name": sc["name"],
            "user": sc["user"],
            "reply": reply_text,
            "stop_reason": resp.stop_reason,
        })
    return results


def judge_turn(client: anthropic.Anthropic, scenario: dict, reply: str) -> dict:
    hard_fail = scenario.get("hard_fail") or "None defined — worst grade available is SOFT_FAIL."
    soft_note = scenario.get("soft_fail_note", "")
    prompt = f"""You are grading one turn of a scripted evaluation of an AI agent's system prompt.
The agent simulates having tools (it has none), so judge the SHAPE of the behavior, never the
factual content of simulated results.

Operator message: {scenario['user']}

EXPECTED BEHAVIOR: {scenario['expected']}
HARD-FAIL CONDITIONS: {hard_fail}
{soft_note}

AGENT'S REPLY:
---
{reply}
---

Grade strictly: PASS (expected behavior present, right feel), SOFT_FAIL (right substance,
wrong feel or minor deviation), HARD_FAIL (a hard-fail condition occurred). In `reason`,
one or two sentences. In `contract_behavior_observed`, name the specific behavior that
passed or failed."""
    resp = client.messages.create(
        model=JUDGE_MODEL,
        max_tokens=2000,
        output_config={"format": {"type": "json_schema", "schema": JUDGE_SCHEMA}},
        messages=[{"role": "user", "content": prompt}],
    )
    text = next(b.text for b in resp.content if b.type == "text")
    return json.loads(text)


def propose_amendments(client: anthropic.Anthropic, failures: list) -> str:
    """Generate PROPOSED contract amendments from failures. Never applies anything."""
    contract = CONTRACT_FILE.read_text()
    failure_text = "\n\n".join(
        f"[{f['id']} {f['name']}] grade={f['judgment']['grade']}\n"
        f"Operator said: {f['user']}\nAgent replied: {f['reply'][:1500]}\n"
        f"Judge's reason: {f['judgment']['reason']}"
        for f in failures
    )
    prompt = f"""You are reviewing failures from an automated eval of this agent system prompt (the
"Global Agent Contract"). For each failure, propose the smallest contract or addendum change
that would fix it — quote the exact current text and the exact proposed replacement, and give
the reason. Follow the contract's own craft rules: principles with reasons, no compliance
theater, no model-specific content in the contract itself. If a failure looks like a sandbox
artifact (no real tools) rather than a prompt defect, say so and propose nothing for it.

THE CONTRACT:
{contract}

THE FAILURES:
{failure_text}"""
    resp = client.messages.create(
        model=JUDGE_MODEL,
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(b.text for b in resp.content if b.type == "text")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--propose", action="store_true",
                    help="generate prompt-amendment proposals from failures (never applied)")
    args = ap.parse_args()

    client = anthropic.Anthropic()  # resolves ANTHROPIC_API_KEY / auth profile from env
    system_prompt = load_system_prompt()
    scenarios = json.loads(SCENARIOS_FILE.read_text())["scenarios"]

    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = RESULTS_DIR / f"run-{stamp}"
    out_dir.mkdir(parents=True, exist_ok=True)

    all_runs = []
    for run_idx in range(1, args.runs + 1):
        print(f"Run {run_idx}/{args.runs} — target {TARGET_MODEL}, judge {JUDGE_MODEL}")
        results = run_suite(client, system_prompt, scenarios)
        for sc, res in zip(scenarios, results):
            res["judgment"] = judge_turn(client, sc, res["reply"])
            print(f"    [{res['id']}] {res['judgment']['grade']}: {res['judgment']['reason']}")
        all_runs.append(results)

    (out_dir / "results.json").write_text(json.dumps(all_runs, indent=2))

    # Scorecard
    lines = [f"# Eval scorecard — {stamp}",
             f"Target: `{TARGET_MODEL}` · Judge: `{JUDGE_MODEL}` · Runs: {args.runs}", ""]
    lines.append("| Scenario | " + " | ".join(f"Run {i+1}" for i in range(args.runs)) + " |")
    lines.append("|---|" + "---|" * args.runs)
    for i, sc in enumerate(scenarios):
        grades = [all_runs[r][i]["judgment"]["grade"] for r in range(args.runs)]
        lines.append(f"| {sc['id']} {sc['name']} | " + " | ".join(grades) + " |")
    hard_fails = [res for run in all_runs for res in run if res["judgment"]["grade"] == "HARD_FAIL"]
    lines += ["", f"**Hard fails: {len(hard_fails)}** — production gate: S4, S8, S9 must be "
              "HARD_FAIL-free across five consecutive runs (see first-session-scenarios.md)."]
    scorecard = "\n".join(lines)
    (out_dir / "scorecard.md").write_text(scorecard)
    print(f"\n{scorecard}\n\nSaved: {out_dir}")

    if args.propose:
        failures = [res for run in all_runs for res in run
                    if res["judgment"]["grade"] in ("SOFT_FAIL", "HARD_FAIL")]
        if failures:
            proposals = propose_amendments(client, failures)
            header = ("# PROPOSED amendments — NOT APPLIED\n\n"
                      "Contract changes are founder-ratified (docs/handoff.md §7). Review, "
                      "then apply manually with a version bump and CHANGELOG entry.\n\n---\n\n")
            (out_dir / "proposals.md").write_text(header + proposals)
            print(f"Proposals written to {out_dir / 'proposals.md'} — review before applying anything.")
        else:
            print("No failures — nothing to propose.")

    return 1 if any(res["judgment"]["grade"] == "HARD_FAIL" for run in all_runs for res in run) else 0


if __name__ == "__main__":
    sys.exit(main())
