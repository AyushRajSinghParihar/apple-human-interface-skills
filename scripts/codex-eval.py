#!/usr/bin/env python3
"""Run the quality/evals benchmark with the Codex CLI, then grade it with Codex.

Each case runs in a temporary project. The "with" arm installs the skill at
.agents/skills/apple-hig; the "without" arm installs nothing. Every other
Codex skill on the machine is turned off with skills.config overrides, and
user config, rules and plugins are ignored.

Web search is off unless you pass --web; the shell sandbox has no network.
A separate Codex session grades each answer against the case's llm graders.
The judge does not know which arm made the answer, and it has no skills. Each
answer gets VOTES judge sessions; a grader passes on a majority of PASS votes.
tool_used graders are computed from the trace: the skill "fired" when a
command in the run reads a file of the installed skill.

Usage:
  scripts/codex-eval.py LABEL [--tag task|trigger] [--case GLOB]
                              [--arms with,without] [--workers 3] [--votes 3]
                              [--model MODEL]

Results go to quality/results/LABEL/: one answer and one record for each run,
summary.json and SUMMARY.md. Raw event traces go to raw/, which git ignores.
"""
import argparse
import concurrent.futures
import datetime as dt
import fnmatch
import importlib.util
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import threading

import yaml


ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "quality/evals"
_spec = importlib.util.spec_from_file_location("_codex_eval_legacy", Path(__file__).with_name("evaluate.py"))
legacy = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(legacy)

VISIBLE_WITH = 14
JUDGE_SCHEMA = {
    "type": "object",
    "properties": {"verdicts": {"type": "array", "items": {
        "type": "object",
        "properties": {"grader": {"type": "string"},
                       "verdict": {"type": "string", "enum": ["PASS", "FAIL"]},
                       "reason": {"type": "string"}},
        "required": ["grader", "verdict", "reason"],
        "additionalProperties": False}}},
    "required": ["verdicts"],
    "additionalProperties": False,
}
_print_lock = threading.Lock()


def log(message):
    with _print_lock:
        print(message, flush=True)


def front_matter(path):
    text = path.read_text()
    if not text.startswith("---\n"):
        return {}, text
    _, head, body = text.split("---\n", 2)
    return yaml.safe_load(head) or {}, body.strip()


def load_cases(tag=None, pattern=None):
    cases = []
    for prompt in sorted(EVALS.rglob("prompt.md")):
        meta, body = front_matter(prompt)
        name = meta.get("name", prompt.parent.name)
        if tag and tag not in meta.get("tags", []):
            continue
        if pattern and not fnmatch.fnmatch(name, pattern):
            continue
        graders = []
        for path in sorted((prompt.parent / "graders").glob("*.md")):
            gmeta, gbody = front_matter(path)
            graders.append({"name": path.stem, **gmeta, "criteria": gbody})
        cases.append({"name": name, "meta": meta, "prompt": body, "graders": graders})
    return cases


def isolation(project, package=None):
    """Turn off every discovered skill outside the installed package and check the result."""
    skills = legacy.discovery(project)
    overrides = legacy.skill_overrides(skills, package or (project / ".agents/skills/apple-hig"))
    visible = [s for s in legacy.discovery(project, overrides) if s.get("enabled", True)]
    expected = VISIBLE_WITH if package else 0
    if len(visible) != expected:
        raise RuntimeError(f"expected {expected} visible skills, found {len(visible)}: "
                           f"{[s.get('name') for s in visible][:5]}")
    return overrides


def codex(project, prompt, overrides, timeout, model=None, schema=None, raw=None, web=False):
    final = project / ".codex-final.txt"
    command = ["codex", "exec", "--disable", "plugins", "--ignore-user-config", "--ignore-rules",
               "--ephemeral", "--json", "--skip-git-repo-check", "--sandbox", "read-only",
               "-c", 'approval_policy="never"', "-c", 'web_search="live"' if web else 'web_search="disabled"',
               *overrides, "--cd", str(project), "-o", str(final)]
    if model:
        command += ["--model", model]
    if schema:
        schema_path = project / ".codex-schema.json"
        schema_path.write_text(json.dumps(schema))
        command += ["--output-schema", str(schema_path)]
    command.append("-")
    process = subprocess.Popen(command, cwd=project, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True, start_new_session=True)
    status = "completed"
    try:
        stdout, stderr = process.communicate(prompt, timeout=timeout)
    except subprocess.TimeoutExpired:
        status = "timeout"
        os.killpg(process.pid, signal.SIGTERM)
        try:
            stdout, stderr = process.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            stdout, stderr = process.communicate()
    if status == "completed" and process.returncode != 0:
        status = f"exit-{process.returncode}"
    events = []
    for line in stdout.splitlines():
        try:
            events.append(json.loads(line))
        except ValueError:
            continue
    if raw:
        raw.parent.mkdir(parents=True, exist_ok=True)
        raw.write_text(stdout + ("\n# stderr\n" + stderr if stderr else ""))
    answer = final.read_text() if final.is_file() else ""
    return {"status": status, "events": events, "answer": answer, "stderr": stderr[-2000:]}


def commands(events):
    for event in events:
        item = event.get("item", {})
        if event.get("type") == "item.completed" and item.get("type") == "command_execution":
            yield item.get("command", "")


def usage(events):
    total = {}
    for event in events:
        if event.get("type") == "turn.completed":
            for key, value in (event.get("usage") or {}).items():
                if isinstance(value, int):
                    total[key] = total.get(key, 0) + value
    return total


def run_arm(case, arm, out, timeout_cap, model, web=False):
    with tempfile.TemporaryDirectory(prefix="hig-codex-") as temporary:
        project = Path(temporary).resolve()
        package = None
        if arm == "with":
            package = project / ".agents/skills/apple-hig"
            shutil.copytree(ROOT / "skills/apple-hig", package)
        overrides = isolation(project, package)
        timeout = min(int(case["meta"].get("timeout_seconds", 300)), timeout_cap)
        started = dt.datetime.now(dt.timezone.utc)
        result = codex(project, case["prompt"], overrides, timeout, model,
                       raw=out / "raw" / f"{case['name']}.{arm}.events.jsonl", web=web)
        marker = str(package) if package else ".agents/skills/apple-hig"
        touched = [c for c in commands(result["events"]) if marker in c or "apple-hig/" in c]
        reads = legacy.consumed_reads(result["events"], project, package)[0] if package else []
    return {"case": case["name"], "arm": arm, "status": result["status"],
            "seconds": round((dt.datetime.now(dt.timezone.utc) - started).total_seconds(), 1),
            "fired": bool(touched or reads), "skill_reads": reads, "skill_commands": len(touched),
            "web_searches": sum(1 for e in result["events"] if e.get("type") == "item.completed"
                                and e.get("item", {}).get("type") == "web_search"),
            "usage": usage(result["events"]), "answer": result["answer"], "stderr": result["stderr"]}


def judge(case, answer, votes, judge_overrides, model):
    graders = [g for g in case["graders"] if g.get("type") == "llm"]
    if not graders:
        return {}
    if not answer.strip():
        return {g["name"]: {"passed": False, "votes": [], "reasons": ["empty answer"]} for g in graders}
    criteria = "\n\n".join(f"### {g['name']}\n{g['criteria']}" for g in graders)
    prompt = (
        "You grade one answer to a user request. Someone else wrote the answer. Judge it only "
        "against the criteria below and do not add requirements of your own. Each criterion "
        "gives PASS and FAIL conditions; if any FAIL condition applies, the verdict is FAIL. "
        "Do not run commands or read files.\n\n"
        f"## User request\n\n{case['prompt']}\n\n"
        f"## Answer to grade\n\n<<<ANSWER\n{answer.strip()}\nANSWER>>>\n\n"
        f"## Criteria\n\n{criteria}\n\n"
        f"Return one verdict for each criterion: {', '.join(g['name'] for g in graders)}. "
        "Give a one-sentence reason for each.")
    tally = {g["name"]: [] for g in graders}
    reasons = {g["name"]: [] for g in graders}
    for _ in range(votes):
        with tempfile.TemporaryDirectory(prefix="hig-judge-") as temporary:
            result = codex(Path(temporary).resolve(), prompt, judge_overrides, 300, model, schema=JUDGE_SCHEMA)
        try:
            verdicts = json.loads(result["answer"])["verdicts"]
        except (ValueError, KeyError, TypeError):
            verdicts = []
        for verdict in verdicts:
            if verdict.get("grader") in tally:
                tally[verdict["grader"]].append(verdict.get("verdict") == "PASS")
                reasons[verdict["grader"]].append(verdict.get("reason", ""))
    return {name: {"passed": sum(v) * 2 > votes, "votes": v, "reasons": reasons[name]}
            for name, v in tally.items()}


def score(case, arm, record, verdicts):
    """Mirror claude plugin eval: in a two-arm task case, the skill indicator is not scored."""
    results, scored = {}, []
    for grader in case["graders"]:
        name = grader["name"]
        if grader.get("type") == "llm":
            passed = verdicts.get(name, {}).get("passed", False)
            results[name] = passed
            scored.append(passed)
        elif grader.get("type") == "tool_used":
            silent = grader.get("max") == 0
            passed = (not record["fired"]) if silent else record["fired"]
            results[name] = passed
            if "task" not in case["meta"].get("tags", []) or grader.get("arm") == "both":
                scored.append(passed)
    return results, (sum(scored) / len(scored) if scored else None)


def summarize(label, out, records):
    tasks = sorted({r["case"] for r in records if r["kind"] == "task"})
    lines = [f"# Codex benchmark: {label}", "",
             f"Run at {dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')} with "
             f"{records[0]['codex']} ({records[0]['model'] or 'Codex default model'}), "
             f"web search {'on' if records[0].get('web') else 'off'}.", ""]
    summary = {"label": label, "tasks": {}, "triggers": {}}
    if tasks:
        lines += ["## Task quality", "", "| Case | With skill | Without skill | Δ | Skill fired |", "|---|---:|---:|---:|---|"]
        totals = {"with": [], "without": []}
        for name in tasks:
            row = {r["arm"]: r for r in records if r["case"] == name and r["kind"] == "task"}
            w, wo = row.get("with", {}).get("score"), row.get("without", {}).get("score")
            delta = (w - wo) if w is not None and wo is not None else None
            totals["with"].append(w) if w is not None else None
            totals["without"].append(wo) if wo is not None else None
            fired = row.get("with", {}).get("fired")
            fmt = lambda v: "–" if v is None else f"{v:.2f}"
            lines.append(f"| {name} | {fmt(w)} | {fmt(wo)} | {fmt(delta) if delta is None else f'{delta:+.2f}'} | "
                         f"{'yes' if fired else 'no' if fired is not None else '–'} |")
            summary["tasks"][name] = {"with": w, "without": wo, "delta": delta, "fired": fired}
        mean = lambda xs: sum(xs) / len(xs) if xs else None
        mw, mwo = mean(totals["with"]), mean(totals["without"])
        summary["task_mean"] = {"with": mw, "without": mwo}
        if mw is not None and mwo is not None:
            lines.append(f"| **Mean** | **{mw:.2f}** | **{mwo:.2f}** | **{mw - mwo:+.2f}** | |")
        lines.append("")
    triggers = [r for r in records if r["kind"] == "trigger"]
    if triggers:
        should = [r for r in triggers if r["expect_fire"]]
        should_not = [r for r in triggers if not r["expect_fire"]]
        hit = sum(r["fired"] for r in should)
        false = sum(r["fired"] for r in should_not)
        summary["triggers"] = {"should_fire": len(should), "fired": hit,
                               "should_not_fire": len(should_not), "false_fires": false,
                               "cases": {r["case"]: r["fired"] for r in triggers}}
        lines += ["## Triggers", "",
                  f"- Requests that must start the skill: **{hit} of {len(should)}** started it.",
                  f"- Near misses that must not start it: **{false} of {len(should_not)}** started it.", ""]
        missed = [r["case"] for r in should if not r["fired"]] + [r["case"] for r in should_not if r["fired"]]
        if missed:
            lines += ["Wrong results: " + ", ".join(missed), ""]
    errors = [f"{r['case']}.{r['arm']}: {r['status']}" for r in records if r["status"] != "completed"]
    if errors:
        lines += ["## Run errors", ""] + [f"- {e}" for e in errors] + [""]
    lines += ["One run for each case gives a coarse signal. Do not report a difference of one case as an improvement.", ""]
    (out / "SUMMARY.md").write_text("\n".join(lines))
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print("\n".join(lines))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("label")
    parser.add_argument("--tag")
    parser.add_argument("--case")
    parser.add_argument("--arms", default=None, help="Comma list; default: with,without for task cases, with for triggers")
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--votes", type=int, default=3)
    parser.add_argument("--model")
    parser.add_argument("--timeout-cap", type=int, default=900)
    parser.add_argument("--web", action="store_true", help="Let the runs use web search (off by default; the judge never uses it)")
    args = parser.parse_args(argv)
    if "/" in args.label or args.label.startswith("."):
        parser.error("LABEL must be a plain name")
    cases = load_cases(args.tag, args.case)
    if not cases:
        parser.error("no cases matched")
    out = ROOT / "quality/results" / args.label
    (out / "runs").mkdir(parents=True, exist_ok=True)
    version = subprocess.run(["codex", "--version"], capture_output=True, text=True).stdout.strip()
    with tempfile.TemporaryDirectory(prefix="hig-judge-iso-") as temporary:
        judge_overrides = isolation(Path(temporary).resolve())
    jobs = []
    for case in cases:
        kind = "task" if "task" in case["meta"].get("tags", []) else "trigger"
        arms = args.arms.split(",") if args.arms else (["with", "without"] if kind == "task" else ["with"])
        jobs += [(case, kind, arm) for arm in arms]
    log(f"{len(jobs)} runs with {version}; results in {out.relative_to(ROOT)}")

    def execute(job):
        case, kind, arm = job
        try:
            record = run_arm(case, arm, out, args.timeout_cap, args.model, args.web)
        except Exception as error:  # keep the suite going; the record shows the failure
            record = {"case": case["name"], "arm": arm, "status": f"error: {error}", "fired": False,
                      "skill_reads": [], "answer": "", "usage": {}}
        verdicts = judge(case, record["answer"], args.votes, judge_overrides, args.model)
        record["graders"], record["score"] = score(case, arm, record, verdicts)
        record.update({"kind": kind, "verdicts": verdicts, "codex": version, "model": args.model, "web": args.web,
                       "expect_fire": kind == "trigger" and "should-trigger" in case["meta"].get("tags", [])})
        base = out / "runs" / f"{case['name']}.{arm}"
        Path(f"{base}.md").write_text(record["answer"])
        Path(f"{base}.json").write_text(json.dumps({k: v for k, v in record.items() if k != "answer"}, indent=2) + "\n")
        log(f"{case['name']:34} {arm:8} {record['status']:10} fired={record['fired']!s:5} score={record['score']}")
        return record

    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        records = list(pool.map(execute, jobs))
    summarize(args.label, out, records)
    return 0


if __name__ == "__main__":
    sys.exit(main())
