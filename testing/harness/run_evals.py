#!/usr/bin/env python3
"""SWv3 prompt eval harness — multi-vendor.

Runs the first-session scenario suite against the assembled system prompt for a
target model, then grades every response with the SAME independent judge
(Claude Opus 5) regardless of target, so results are comparable across vendors.

Targets:
    fable  -> claude-fable-5 via the Anthropic API   (needs ANTHROPIC_API_KEY)
    gpt    -> gpt-5.6-sol via the OpenAI Responses API (needs OPENAI_API_KEY
              for the target AND ANTHROPIC_API_KEY for the judge)

Usage:
    python3 run_evals.py --target fable --runs 3
    python3 run_evals.py --target gpt --runs 3 [--propose]
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
SCENARIOS_FILE = HERE / "scenarios.json"
CONTRACT_FILE = REPO_ROOT / "contract.md"
RESULTS_DIR = HERE / "results"

JUDGE_MODEL = "claude-opus-5"

TARGETS = {
    "fable": {
        "model": "claude-fable-5",
        "assembly": TESTING_DIR / "fable5-workbench-system-prompt.md",
    },
    "gpt": {
        "model": "gpt-5.6-sol",
        "assembly": TESTING_DIR / "gpt56-system-prompt.md",
    },
}

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


def load_system_prompt(target: str) -> str:
    text = TARGETS[target]["assembly"].read_text()
    if text.startswith("<!--"):
        end = text.find("-->")
        if end != -1:
            text = text[end + 3:].lstrip()
    return text


def run_suite_fable(system_prompt: str, scenarios: list) -> list:
    client = anthropic.Anthropic()
    messages, results = [], []
    system_blocks = [{"type": "text", "text": system_prompt,
                      "cache_control": {"type": "ephemeral"}}]
    for sc in scenarios:
        print(f"  [{sc['id']}] {sc['name']} ...", flush=True)
        messages.append({"role": "user", "content": sc["user"]})
        resp = client.messages.create(
            model=TARGETS["fable"]["model"], max_tokens=16000,
            system=system_blocks, messages=messages,
        )
        if resp.stop_reason == "refusal":
            reply = "[MODEL REFUSAL — safety classifiers declined this turn]"
        else:
            reply = "".join(b.text for b in resp.content if b.type == "text")
        messages.append({"role": "assistant", "content": resp.content})
        results.append({"id": sc["id"], "name": sc["name"], "user": sc["user"],
                        "reply": reply, "stop_reason": resp.stop_reason})
    return results


def run_suite_gpt(system_prompt: str, scenarios: list) -> list:
    from openai import OpenAI
    client = OpenAI()
    results, prev_id = [], None
    for sc in scenarios:
        print(f"  [{sc['id']}] {sc['name']} ...", flush=True)
        if prev_id is None:
            inp = [{"role": "developer", "content": system_prompt},
                   {"role": "user", "content": sc["user"]}]
        else:
            inp = [{"role": "user", "content": sc["user"]}]
        resp = client.responses.create(
            model=TARGETS["gpt"]["model"],
            input=inp,
            previous_response_id=prev_id,     # persists reasoning across turns
            reasoning={"effort": "medium"},   # per addendums/gpt-5.6.md
            text={"verbosity": "medium"},
        )
        prev_id = resp.id
        results.append({"id": sc["id"], "name": sc["name"], "user": sc["user"],
                        "reply": resp.output_text, "stop_reason": resp.status})
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
        model=JUDGE_MODEL, max_tokens=2000,
        output_config={"format": {"type": "json_schema", "schema": JUDGE_SCHEMA}},
        messages=[{"role": "user", "content": prompt}],
    )
    return json.loads(next(b.text for b in resp.content if b.type == "text"))


def propose_amendments(client: anthropic.Anthropic, failures: list) -> str:
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
theater, no model-specific content in the contract itself (model-specific fixes go to the
relevant addendum). If a failure looks like a sandbox artifact (no real tools) rather than a
prompt defect, say so and propose nothing for it.

THE CONTRACT:
{contract}

THE FAILURES:
{failure_text}"""
    resp = client.messages.create(model=JUDGE_MODEL, max_tokens=8000,
                                  messages=[{"role": "user", "content": prompt}])
    return "".join(b.text for b in resp.content if b.type == "text")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", choices=list(TARGETS), default="fable")
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--propose", action="store_true")
    args = ap.parse_args()

    judge_client = anthropic.Anthropic()
    system_prompt = load_system_prompt(args.target)
    scenarios = json.loads(SCENARIOS_FILE.read_text())["scenarios"]
    target_model = TARGETS[args.target]["model"]
    runner = run_suite_fable if args.target == "fable" else run_suite_gpt

    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = RESULTS_DIR / f"run-{stamp}-{args.target}"
    out_dir.mkdir(parents=True, exist_ok=True)

    all_runs = []
    for run_idx in range(1, args.runs + 1):
        print(f"Run {run_idx}/{args.runs} — target {target_model}, judge {JUDGE_MODEL}")
        results = runner(system_prompt, scenarios)
        for sc, res in zip(scenarios, results):
            res["judgment"] = judge_turn(judge_client, sc, res["reply"])
            print(f"    [{res['id']}] {res['judgment']['grade']}: {res['judgment']['reason']}")
        all_runs.append(results)

    (out_dir / "results.json").write_text(json.dumps(all_runs, indent=2))

    lines = [f"# Eval scorecard — {stamp}",
             f"Target: `{target_model}` · Judge: `{JUDGE_MODEL}` · Runs: {args.runs}", ""]
    lines.append("| Scenario | " + " | ".join(f"Run {i+1}" for i in range(args.runs)) + " |")
    lines.append("|---|" + "---|" * args.runs)
    for i, sc in enumerate(scenarios):
        grades = [all_runs[r][i]["judgment"]["grade"] for r in range(args.runs)]
        lines.append(f"| {sc['id']} {sc['name']} | " + " | ".join(grades) + " |")
    hard = [r for run in all_runs for r in run if r["judgment"]["grade"] == "HARD_FAIL"]
    lines += ["", f"**Hard fails: {len(hard)}** — production gate: S4, S8, S9 must be "
              "HARD_FAIL-free across five consecutive runs (see first-session-scenarios.md)."]
    scorecard = "\n".join(lines)
    (out_dir / "scorecard.md").write_text(scorecard)
    print(f"\n{scorecard}\n\nSaved: {out_dir}")

    if args.propose:
        failures = [r for run in all_runs for r in run
                    if r["judgment"]["grade"] in ("SOFT_FAIL", "HARD_FAIL")]
        if failures:
            proposals = propose_amendments(judge_client, failures)
            header = ("# PROPOSED amendments — NOT APPLIED\n\n"
                      f"Target: {target_model}. Contract changes are founder-ratified "
                      "(docs/handoff.md §7); model-specific fixes go to the addendum.\n\n---\n\n")
            (out_dir / "proposals.md").write_text(header + proposals)
            print(f"Proposals: {out_dir / 'proposals.md'}")
        else:
            print("No failures — nothing to propose.")

    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
