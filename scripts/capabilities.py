"""Deterministic release checks for topic procedures, reviews, and case bindings.

This gate validates evidence identities, not semantic quality. Only independent
review records can approve instructions; runtime records are a separate gate.
"""
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import urllib.parse


_spec = importlib.util.spec_from_file_location("_capabilities_hig", Path(__file__).with_name("hig.py"))
hig = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(hig)

EVIDENCE_KEYS = ("decision", "artifact", "transformation", "verification", "applicability", "handoffs", "distinctiveness")
MODES = {"design", "review", "adapt"}
AXES = ("task_completion", "hig_correctness", "artifact_usefulness", "conditions_accessibility", "evidence_honesty")
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LOCAL_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)")


def _present(value):
    return isinstance(value, str) and bool(value.strip())


def _json(path, errors, label):
    try:
        value = json.loads(path.read_text())
    except (OSError, UnicodeError, ValueError) as exc:
        errors.append(f"{label}: invalid JSON: {exc}")
        return None
    if not isinstance(value, dict):
        errors.append(f"{label}: expected a JSON object")
        return None
    return value


def _path(root, value, errors, label, within=None):
    if not _present(value):
        errors.append(f"{label}: missing path")
        return None
    path = (root / value).resolve()
    boundary = (within or root).resolve()
    if Path(value).is_absolute() or not path.is_relative_to(boundary):
        errors.append(f"{label}: path outside {boundary.name}: {value}")
        return None
    return path


def _links(path):
    if not path.is_file():
        return set()
    links = set()
    for target in LOCAL_LINK.findall(path.read_text()):
        if target.startswith(("http:", "https:", "mailto:", "data:")):
            continue
        filename = urllib.parse.unquote(target.strip("<>").partition("#")[0])
        links.add((path.parent / filename).resolve() if filename else path.resolve())
    return links


def _routing_approval(root, families, errors, pending):
    """A source or leaf approval cannot approve the routing instructions."""
    path = root / "coverage/routing-review.json"
    approval = _json(path, errors, "routing approval") if path.is_file() else None
    evidence_keys = ("root", "families", "exact_topics", "cross_topic_platform_routes", "scope_limits")
    evidence = approval.get("evidence") if approval else None
    if (not approval or approval.get("status") != "reviewed"
            or not _present(approval.get("reviewer")) or not _present(approval.get("reviewed_at"))
            or not isinstance(evidence, dict) or any(not _present(evidence.get(key)) for key in evidence_keys)):
        pending.append("routing approval: independent evidenced review missing or incomplete")
        return
    hashes = approval.get("family_hashes")
    if not isinstance(hashes, dict) or set(hashes) != set(families):
        pending.append("routing approval: reviewed family set does not match current source families")
        hashes = hashes if isinstance(hashes, dict) else {}
    package = root / "skills/apple-hig"
    bindings = [("root", package / "SKILL.md", approval.get("root_hash")),
                ("topic index", package / "references/topic-index.md", approval.get("topic_index_hash")),
                ("platform routes", package / "references/platforms-and-tasks.md", approval.get("platform_routes_hash"))]
    bindings.extend((family, package / f"subskills/apple-hig-{family}/SKILL.md", hashes.get(family))
                    for family in families)
    for label, target, fingerprint in bindings:
        if not target.is_file() or fingerprint != hig.digest(target.read_bytes()):
            pending.append(f"routing approval: stale or missing {label} hash")


def _bindings(root, node, errors, pending, label):
    """Validate explicit file/hash pairs; embedded inputs are covered by case_hash."""
    if isinstance(node, list):
        for index, item in enumerate(node):
            _bindings(root, item, errors, pending, f"{label}[{index}]")
        return
    if not isinstance(node, dict):
        return
    pairs = [(key, key[:-5] + "_hash") for key in node if key.endswith("_path")]
    if "path" in node and "hash" in node:
        pairs.append(("path", "hash"))
    for path_key, hash_key in pairs:
        target = _path(root, node[path_key], errors, f"{label}.{path_key}")
        fingerprint = node.get(hash_key)
        if not isinstance(fingerprint, str) or not re.fullmatch(r"[a-fA-F0-9]{64}", fingerprint):
            errors.append(f"{label}.{hash_key}: missing or invalid hash")
        elif target and not target.is_file():
            pending.append(f"{label}: missing bound file {node[path_key]}")
        elif target and hig.digest(target.read_bytes()) != fingerprint.lower():
            errors.append(f"{label}.{hash_key}: frozen file hash mismatch")
    for key, item in node.items():
        if isinstance(item, (dict, list)):
            _bindings(root, item, errors, pending, f"{label}.{key}")


def _record_binding(root, binding, errors, label, owner=None, expected=None):
    if not isinstance(binding, dict):
        errors.append(f"{label}: missing file/hash binding")
        return False
    target = _path(root, binding.get("path"), errors, label)
    if not target or not target.is_file():
        errors.append(f"{label}: bound file missing")
        return False
    if owner is not None and not target.is_relative_to(owner.resolve()):
        errors.append(f"{label}: evidence is not owned by its execution directory")
        return False
    if expected is not None and target != expected.resolve():
        errors.append(f"{label}: evidence path does not match its logical artifact name")
        return False
    if binding.get("hash") != hig.digest(target.read_bytes()):
        errors.append(f"{label}: file hash mismatch")
        return False
    return True


def _execution_integrity(root, record_path, record, errors, pending):
    """Historical evidence keeps its own bindings, independent of today's case."""
    owner = record_path.parent
    label = f"behavior {owner.name}"
    artifacts = record.get("artifacts", {})
    if not isinstance(artifacts, dict):
        errors.append(f"{label}: malformed historical artifacts")
        artifacts = {}
    for name, binding in artifacts.items():
        _record_binding(root, binding, errors, f"{label} artifact {name}", owner=owner)
    for key in ("transcript", "final_message"):
        if record.get(key):
            _record_binding(root, record[key], errors, f"{label} {key}", owner=owner)
    if record_path.with_name("grade.json").is_file():
        _grade(root, record_path, record, {}, errors, pending, validate_only=True)


def _thread_identity(root, record, pending, label):
    """Read the runtime's identity from bound events, never from an asserted flag."""
    binding = record.get("transcript", {})
    if not isinstance(binding, dict) or not _present(binding.get("path")):
        pending.append(f"{label}: runtime thread transcript binding missing")
        return None
    path = root / binding.get("path", "")
    try:
        events = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
        identities = [event.get("thread_id") for event in events if isinstance(event, dict) and event.get("type") == "thread.started"]
    except (OSError, UnicodeError, ValueError):
        identities = []
    if len(identities) != 1 or not _present(identities[0]) or record.get("thread_id") != identities[0]:
        pending.append(f"{label}: runtime thread identity missing or does not match transcript")
        return None
    return identities[0]


def _grade(root, record_path, record, case, errors, pending, validate_only=False):
    label = record_path.parent.name
    path = record_path.with_name("grade.json")
    if not path.is_file():
        pending.append(f"behavior {label}: independent grade missing")
        return False
    if not path.resolve().is_relative_to(record_path.parent.resolve()):
        errors.append(f"behavior {label}: grade is not owned by its execution directory")
        return False
    grade = _json(path, errors, f"behavior {label} grade")
    if grade is None:
        return False
    if grade.get("record_hash") != hig.digest(record_path.read_bytes()) or grade.get("case_hash") != record.get("case_hash"):
        errors.append(f"behavior {label}: stale grade hash binding")
        return False
    scores, evidence = grade.get("scores"), grade.get("evidence")
    lists = ("critical_errors", "found_defect_ids", "invented_high_severity_findings")
    if (not _present(grade.get("grader")) or not _present(grade.get("reviewed_at"))
            or not isinstance(scores, dict) or any(type(scores.get(axis)) is not int or not 0 <= scores[axis] <= 2 for axis in AXES)
            or not isinstance(evidence, dict) or any(not _present(evidence.get(axis)) for axis in AXES)
            or any(not isinstance(grade.get(key), list) for key in lists) or grade.get("verdict") not in {"pass", "fail"}):
        errors.append(f"behavior {label}: malformed independent grade")
        return False
    grading = grade.get("grading_transcript")
    grading_path = None
    if grading is not None:
        grading_path = _path(root, grading.get("path") if isinstance(grading, dict) else None,
                             errors, f"behavior {label} grading transcript", within=root / "coverage/grading")
        if grading_path:
            relative = grading_path.relative_to((root / "coverage/grading").resolve())
            if len(relative.parts) != 2 or relative.name != "events.jsonl":
                errors.append(f"behavior {label}: grading transcript is not owned by a grading session")
                grading_path = None
            elif not _record_binding(root, grading, errors, f"behavior {label} grading transcript",
                                     owner=root / "coverage/grading"):
                grading_path = None
    # Retained legacy pilots predate provenance fields. Any declared transcript
    # still keeps its byte binding, but only current fully proven grades count.
    if validate_only:
        return True
    if not grading_path:
        pending.append(f"behavior {label}: independent grading transcript missing or invalid")
        return False
    try:
        events = [json.loads(line) for line in grading_path.read_text().splitlines() if line.strip()]
        identities = [event.get("thread_id") for event in events if isinstance(event, dict) and event.get("type") == "thread.started"]
        completed = any(isinstance(event, dict) and event.get("type") == "turn.completed" for event in events)
    except (OSError, UnicodeError, ValueError):
        identities, completed = [], False
    identity = grade.get("grading_thread_id")
    if (len(identities) != 1 or not _present(identity) or identities[0] != identity
            or identity == record.get("thread_id") or not completed):
        pending.append(f"behavior {label}: independent grading session identity/completion invalid")
        return False
    artifacts = record.get("artifacts", {})
    expected_hashes = {name: binding.get("hash") for name, binding in artifacts.items()
                       if isinstance(binding, dict)} if isinstance(artifacts, dict) else {}
    if not expected_hashes or grade.get("artifact_hashes") != expected_hashes:
        pending.append(f"behavior {label}: grading artifact hashes do not match execution artifacts")
        return False
    # A historical control is an observation, including when its outcome failed.
    if record["variant"] == "baseline":
        return True
    accepted = (grade["verdict"] == "pass" and sum(scores[axis] for axis in AXES) >= 8
                and not grade["critical_errors"] and not grade["invented_high_severity_findings"])
    findings = case.get("rubric", {}).get("required_findings", [])
    if isinstance(findings, list) and findings:
        required = {str(item["id"]) for item in findings if isinstance(item, dict) and "id" in item}
        critical = {str(item["id"]) for item in findings if isinstance(item, dict) and item.get("critical") and "id" in item}
        found = {str(item) for item in grade["found_defect_ids"]}
        threshold = 4 if len(required) == 5 else len(required)
        accepted = accepted and critical <= found and len(required & found) >= threshold
    if not accepted:
        pending.append(f"behavior {label}: candidate grade does not meet acceptance criteria")
    return accepted


def behavior_issues(root, rows):
    """Validate retained executions, then satisfy each frozen required run slot."""
    root = Path(root).resolve()
    errors, pending = [], []
    result = {"errors": errors, "pending": pending, "passed": 0}
    inventory = _json(root / "coverage/capabilities.json", errors, "behavior inventory")
    if inventory is None:
        return result
    requirements = inventory.get("requirements")
    if not isinstance(requirements, dict) or type(requirements.get("stress_cases")) is not int or requirements["stress_cases"] < 0 or requirements.get("stress_repetitions") != 3:
        pending.append("behavior: frozen stress-case requirements missing or invalid")
        requirements = {"stress_cases": 8, "stress_repetitions": 3}
    stress_rows = inventory.get("stress_cases", [])
    if not isinstance(stress_rows, list):
        errors.append("behavior: stress_cases must be an array")
        stress_rows = []
    if len(stress_rows) != requirements["stress_cases"]:
        pending.append(f"behavior: expected {requirements['stress_cases']} frozen stress cases, found {len(stress_rows)}")
    baseline_commit = inventory.get("baseline_commit")
    if not isinstance(baseline_commit, str) or not re.fullmatch(r"[a-fA-F0-9]{7,40}", baseline_commit):
        pending.append("behavior: frozen baseline commit missing or invalid")
        baseline_commit = None
    cases, slots, control_families = {}, set(), set()
    topic_rows = {row.get("topic"): row for row in rows if isinstance(row, dict) and _present(row.get("topic"))}
    topic_case_ids = set()
    for row, stress in [(row, False) for row in rows] + [(row, True) for row in stress_rows]:
        if not isinstance(row, dict):
            errors.append("behavior: malformed case inventory row")
            continue
        case_id = row.get("id") if stress else row.get("case_id")
        if not _present(case_id):
            errors.append("behavior: frozen case id missing")
            continue
        if case_id in cases:
            errors.append(f"behavior: duplicate frozen case id {case_id}")
            continue
        case_path = _path(root, row.get("case_path"), errors, f"behavior {case_id} case")
        if not case_path or not case_path.is_file():
            pending.append(f"behavior {case_id}: frozen case missing")
            continue
        if hig.digest(case_path.read_bytes()) != row.get("case_hash"):
            errors.append(f"behavior {case_id}: frozen case hash mismatch")
            continue
        case = _json(case_path, errors, f"behavior {case_id} case")
        if case is None:
            continue
        if (case.get("id") != case_id
                or (not stress and (case.get("topic") != row.get("topic") or case.get("family") != row.get("family")))):
            errors.append(f"behavior {case_id}: frozen case identity mismatch")
            continue
        if stress:
            expected_topics = case.get("expected_topics")
            if (case.get("kind") != "stress" or row.get("repetitions") != 3 or not isinstance(expected_topics, list)
                    or any(not isinstance(topic, str) or topic not in topic_rows for topic in expected_topics)
                    or (case.get("invoke") is not False and not expected_topics)):
                errors.append(f"behavior {case_id}: invalid frozen stress topics/repetitions")
                continue
        _bindings(root, case, errors, pending, f"behavior {case_id} case")
        cases[case_id] = (case, row)
        repetitions = 3 if stress else 1
        slots.update((case_id, "candidate", repetition) for repetition in range(1, repetitions + 1))
        if not stress:
            topic_case_ids.add(case_id)
            if case.get("baseline_control") is True:
                slots.add((case_id, "baseline", 1))
                family = case.get("family")
                if family in control_families:
                    errors.append(f"behavior: duplicate baseline control family {family}")
                control_families.add(family)
    families = {row.get("family") for row in rows if isinstance(row, dict)}
    if "baseline_controls" in requirements and requirements["baseline_controls"] != len(families):
        pending.append("behavior: frozen baseline-control requirement does not match source families")
    for family in sorted(families - control_families):
        pending.append(f"behavior {family}: matched baseline control missing")
    harness = root / "scripts/evaluate.py"
    harness_hash = hig.digest(harness.read_bytes()) if harness.is_file() else None
    if harness_hash is None:
        pending.append("behavior: runtime harness missing")
    selected, record_ids = {}, set()
    baseline_cache = {}
    source_manifest = _json(root / "coverage/manifest.json", errors, "behavior source manifest")
    visible = {"SKILL.md"}
    if source_manifest is not None:
        visible.update(f"subskills/apple-hig-{page['module']}/SKILL.md"
                       for page in source_manifest.get("pages", []) if isinstance(page, dict)
                       and page.get("type") == "article" and _present(page.get("module")))
    for record_path in sorted((root / "coverage/behavior").glob("*/record.json")):
        before_errors, before_pending = len(errors), len(pending)
        record = _json(record_path, errors, "behavior record")
        if record is None:
            continue
        label = f"behavior {record_path.parent.name}"
        variant, repetition, attempt = record.get("variant"), record.get("repetition"), record.get("attempt")
        case_id = record.get("case_id")
        if (record.get("schema_version") != 1 or variant not in {"candidate", "baseline"}
                or type(repetition) is not int or repetition < 1 or type(attempt) is not int or attempt < 1
                or not _present(case_id) or record.get("run_id") != record_path.parent.name
                or record.get("run_id") != f"{case_id}.{variant}.r{repetition}.a{attempt}"
                or record.get("status") not in {"completed", "infrastructure_error", "artifact_error", "routing_error", "timed_out"}
                or any(not _present(record.get(key)) for key in ("model", "started_at"))
                or (record.get("status") == "completed" and any(not _present(record.get(key)) for key in ("cli_version", "finished_at")))):
            errors.append(f"{label}: malformed runtime identity/status")
            continue
        if record["run_id"] in record_ids:
            errors.append(f"{label}: duplicate runtime identity")
        record_ids.add(record["run_id"])
        _execution_integrity(root, record_path, record, errors, pending)
        if case_id not in cases:
            continue
        case, row = cases[case_id]
        current_case = record.get("case_path") == row.get("case_path") and record.get("case_hash") == row.get("case_hash")
        current_harness = record.get("harness_hash") == harness_hash and harness_hash is not None
        if not current_case:
            pending.append(f"{label}: stale runtime case hash/path binding")
        if not current_harness:
            pending.append(f"{label}: stale runtime harness hash")
        if not current_case or not current_harness or record["status"] != "completed":
            continue
        dependencies = record.get("package_dependencies")
        if not isinstance(dependencies, dict) or (not dependencies and case.get("invoke") is not False and record["status"] == "completed"):
            errors.append(f"{label}: package dependencies missing")
            dependencies = {}
        if variant == "baseline" and (not baseline_commit or record.get("baseline_commit") != baseline_commit):
            errors.append(f"{label}: baseline commit identity mismatch")
        for relative, fingerprint in dependencies.items():
            target = _path(root / "skills/apple-hig", relative, errors, f"{label} dependency")
            if target is None:
                continue
            if variant == "candidate":
                actual = hig.digest(target.read_bytes()) if target.is_file() else None
            else:
                key = (baseline_commit, relative)
                if key not in baseline_cache:
                    completed = subprocess.run(["git", "-C", str(root), "show", f"{baseline_commit}:skills/apple-hig/{relative}"], capture_output=True)
                    baseline_cache[key] = hig.digest(completed.stdout) if completed.returncode == 0 else None
                actual = baseline_cache[key]
            if actual != fingerprint or actual is None:
                pending.append(f"{label}: stale {variant} package dependency {relative}")
        discovery = record.get("discovery_dependencies")
        if not isinstance(discovery, dict) or not visible <= set(discovery):
            pending.append(f"{label}: discovery dependencies do not bind every visible skill entrypoint")
        else:
            for relative, fingerprint in discovery.items():
                target = _path(root / "skills/apple-hig", relative, errors, f"{label} discovery dependency")
                if target is None:
                    continue
                if variant == "candidate":
                    actual = hig.digest(target.read_bytes()) if target.is_file() else None
                else:
                    key = (baseline_commit, relative)
                    if key not in baseline_cache:
                        completed = subprocess.run(["git", "-C", str(root), "show", f"{baseline_commit}:skills/apple-hig/{relative}"], capture_output=True)
                        baseline_cache[key] = hig.digest(completed.stdout) if completed.returncode == 0 else None
                    actual = baseline_cache[key]
                if actual != fingerprint or actual is None:
                    pending.append(f"{label}: stale discovery dependency {relative}")
        reads, required_reads = record.get("reads"), record.get("required_reads")
        if (not isinstance(reads, list) or not isinstance(required_reads, list)
                or any(not _present(item) for item in (reads or []) + (required_reads or []))):
            errors.append(f"{label}: malformed read trace")
            reads, required_reads = [], []
        prefix = "skills/apple-hig/"
        targets = [topic_rows[topic] for topic in case.get("expected_topics", [])] if case.get("kind") == "stress" else [row]
        expected = {"SKILL.md"}
        for target in targets:
            family = target.get("family", "")
            expected.update({f"subskills/apple-hig-{family}/SKILL.md", target.get("reference_path", "").removeprefix(prefix)})
            if variant == "candidate":
                expected.add(target.get("skill_path", "").removeprefix(prefix))
        if case.get("invoke") is False:
            if reads or required_reads:
                errors.append(f"{label}: negative invocation unexpectedly read HIG instructions")
        elif record["status"] == "completed":
            if not expected <= set(required_reads) or not set(required_reads) <= set(reads):
                pending.append(f"{label}: required root/family/topic/reference routing reads missing")
            if not (set(required_reads) | set(reads)) <= set(dependencies):
                pending.append(f"{label}: consumed reads lack package dependency hashes")
        routing = record.get("routing")
        if record["status"] == "completed" and (not isinstance(routing, dict) or routing.get("passed") is not True or routing.get("missing") != []):
            pending.append(f"{label}: routing did not pass")
        artifacts = record.get("artifacts")
        if not isinstance(artifacts, dict):
            errors.append(f"{label}: malformed artifacts")
            artifacts = {}
        for name, binding in artifacts.items():
            if not _present(name) or not (record_path.parent / "artifacts" / name).resolve().is_relative_to((record_path.parent / "artifacts").resolve()):
                errors.append(f"{label}: invalid logical artifact name")
                continue
            _record_binding(root, binding, errors, f"{label} artifact {name}", owner=record_path.parent,
                            expected=record_path.parent / "artifacts" / name)
        if record.get("transcript"):
            _record_binding(root, record["transcript"], errors, f"{label} transcript", owner=record_path.parent,
                            expected=record_path.parent / "events.jsonl")
        elif record["status"] == "completed":
            errors.append(f"{label}: transcript missing")
        if record.get("final_message"):
            _record_binding(root, record["final_message"], errors, f"{label} final message", owner=record_path.parent,
                            expected=record_path.parent / "final-message.txt")
        if record["status"] == "completed":
            if not artifacts or not set(case.get("output_files", [])) <= set(artifacts):
                pending.append(f"{label}: required artifact outputs missing")
            checks = record.get("checks")
            if (not isinstance(checks, dict) or checks.get("passed") is not True or checks.get("turn_completed") is not True
                    or checks.get("exit_code") != 0 or checks.get("missing_artifacts") != []
                    or checks.get("forbidden_reads") != [] or checks.get("package_changed") != []
                    or checks.get("malformed_event_count") != 0
                    or (case.get("mode") == "adapt" and checks.get("adaptation_changed") is not True)):
                pending.append(f"{label}: runtime completion checks failed")
            thread_id = _thread_identity(root, record, pending, label)
            accepted = _grade(root, record_path, record, case, errors, pending)
            if accepted and len(errors) == before_errors and len(pending) == before_pending:
                slot = (case_id, variant, repetition)
                if slot not in selected or attempt > selected[slot][0]:
                    selected[slot] = (attempt, thread_id, record_path)
    satisfied = set(selected)
    sessions = {}
    for slot, (_, thread_id, record_path) in selected.items():
        if thread_id in sessions:
            errors.append(f"behavior {record_path.parent.name}: selected execution reused runtime session {thread_id} from {sessions[thread_id]}")
        else:
            sessions[thread_id] = record_path.parent.name
    # A failed attempt remains visible on disk without poisoning a later valid pass.
    # Integrity errors above remain errors even when a different attempt passed.
    pending[:] = [issue for issue in pending if not any(
        issue.startswith(f"behavior {case_id}.{variant}.r{rep}.a")
        for case_id, variant, rep in satisfied)]
    for case_id, variant, repetition in sorted(slots - satisfied):
        pending.append(f"behavior {case_id} {variant} repetition {repetition}: current accepted execution missing")
    result["passed"] = sum((case_id, "candidate", 1) in satisfied for case_id in topic_case_ids)
    return result


def check(root, require_behavior=True, allow_pending=False):
    root = Path(root).resolve()
    package = root / "skills/apple-hig"
    errors, pending = [], []
    result = {"errors": errors, "pending": pending, "topics": 0, "reviewed": 0, "behavior_passed": 0}
    manifest_path = root / "coverage/manifest.json"
    if not manifest_path.is_file():
        errors.append("source manifest is required: coverage/manifest.json")
        return result
    manifest = _json(manifest_path, errors, "source manifest")
    if manifest is None:
        return result
    pages = manifest.get("pages")
    if not isinstance(pages, list):
        errors.append("source manifest: pages must be an array")
        return result
    articles = {}
    for page in pages:
        if not isinstance(page, dict):
            errors.append("source manifest: page must be an object")
            continue
        if page.get("type") != "article":
            continue
        slug, family = page.get("slug"), page.get("module")
        if not isinstance(slug, str) or not SLUG.fullmatch(slug) or not isinstance(family, str) or not SLUG.fullmatch(family):
            errors.append("source manifest: article needs a valid slug and family")
            continue
        if slug in articles:
            errors.append(f"source manifest: duplicate article {slug}")
        articles[slug] = page
    if not articles:
        errors.append("source manifest: no article owners")
        return result
    _routing_approval(root, {page["module"] for page in articles.values()}, errors, pending)
    capability_path = root / "coverage/capabilities.json"
    if not capability_path.is_file():
        pending.append("capability inventory missing: coverage/capabilities.json")
        if not allow_pending:
            errors.extend(pending)
        return result
    inventory = _json(capability_path, errors, "capability inventory")
    if inventory is None:
        return result
    if inventory.get("schema_version") != 1:
        errors.append("capability inventory: unsupported schema_version")
    rows = inventory.get("topics")
    if not isinstance(rows, list):
        errors.append("capability inventory: topics must be an array")
        return result
    reachable = hig.reachable_files(package)
    # Reuse the source gate's parser for missing files, anchors, and escapes.
    errors.extend("route link: " + issue for issue in hig.link_errors(package))
    owners, case_ids, case_paths = set(), set(), set()
    family_modes = {page["module"]: set() for page in articles.values()}
    for row in rows:
        if not isinstance(row, dict):
            errors.append("capability inventory: topic row must be an object")
            continue
        slug = row.get("topic")
        if not isinstance(slug, str) or not SLUG.fullmatch(slug):
            errors.append("capability inventory: invalid topic slug")
            continue
        if slug in owners:
            errors.append(f"{slug}: duplicate topic owner")
        owners.add(slug)
        page = articles.get(slug)
        if page is None:
            errors.append(f"{slug}: orphan topic has no source article")
            continue
        result["topics"] += 1
        family = page["module"]
        if row.get("family") != family:
            errors.append(f"{slug}: wrong family; expected {family}")
        family_dir = package / "subskills" / ("apple-hig-" + family)
        expected_skill = family_dir / ".topics" / ("apple-hig-" + slug) / "SKILL.md"
        expected_reference = family_dir / "references" / (slug + ".md")
        skill = _path(root, row.get("skill_path"), errors, f"{slug} skill", package)
        reference = _path(root, row.get("reference_path"), errors, f"{slug} reference", package)
        source_reference = _path(root, page.get("destination"), errors, f"{slug} source reference", package)
        if skill and skill != expected_skill.resolve():
            errors.append(f"{slug}: skill path does not match its topic/family")
        if reference and (reference != expected_reference.resolve() or reference != source_reference):
            errors.append(f"{slug}: reference path does not match its source owner")
        for label, target in (("skill", skill), ("reference", reference)):
            if target and not target.is_file():
                pending.append(f"{slug}: missing {label} file")
            elif target and target not in reachable:
                errors.append(f"{slug}: {label} route is unreachable from installed root")
        if skill and skill.is_file():
            if skill not in _links(family_dir / "SKILL.md"):
                errors.append(f"{slug}: family route must enter the topic procedure")
            if skill not in _links(package / "references/topic-index.md"):
                errors.append(f"{slug}: exact-topic index route must enter the topic procedure")
            if reference and reference not in _links(skill):
                errors.append(f"{slug}: topic route must link its primary reference")
            frontmatter = re.match(r"\A---\s*\n(.*?)\n---(?:\n|$)", skill.read_text(), re.S)
            try:
                import yaml
                metadata = yaml.safe_load(frontmatter.group(1)) if frontmatter else None
            except (ImportError, ValueError) as exc:
                errors.append(f"{slug}: cannot validate skill frontmatter: {exc}")
                metadata = None
            except Exception as exc:
                errors.append(f"{slug}: invalid skill frontmatter: {exc}")
                metadata = None
            if not isinstance(metadata, dict) or metadata.get("name") != "apple-hig-" + slug or not _present(metadata.get("description")):
                errors.append(f"{slug}: skill frontmatter name/description invalid")
        case_id = row.get("case_id")
        case_path = _path(root, row.get("case_path"), errors, f"{slug} case")
        if not _present(case_id):
            errors.append(f"{slug}: missing case id")
        elif case_id in case_ids:
            errors.append(f"{slug}: duplicate case id {case_id}")
        case_ids.add(case_id if isinstance(case_id, str) else "")
        if case_path in case_paths and case_path is not None:
            errors.append(f"{slug}: duplicate case path")
        case_paths.add(case_path)
        if case_path and not case_path.is_file():
            pending.append(f"{slug}: missing frozen case file")
        elif case_path:
            fingerprint = row.get("case_hash")
            if not isinstance(fingerprint, str) or hig.digest(case_path.read_bytes()) != fingerprint:
                errors.append(f"{slug}: frozen case hash mismatch")
            case = _json(case_path, errors, f"{slug} case")
            if case is not None:
                if case.get("id") != case_id or case.get("topic") != slug or case.get("family") != family:
                    errors.append(f"{slug}: case identity/topic/family mismatch")
                if case.get("mode") not in MODES:
                    errors.append(f"{slug}: case mode must be design, review, or adapt")
                else:
                    family_modes[family].add(case["mode"])
                _bindings(root, case, errors, pending, f"{slug} case")
        review_path = root / "coverage/skill-reviews" / (slug + ".json")
        approval = _json(review_path, errors, f"{slug} approval") if review_path.is_file() else None
        evidence = approval.get("evidence", {}) if approval else {}
        extra_errors, extra_pending = [], []
        additional = approval.get("additional_references", []) if approval else []
        if (not isinstance(additional, list) or any(not isinstance(item, dict)
                or "path" not in item or "hash" not in item for item in additional)):
            extra_errors.append("malformed declared bindings")
        else:
            _bindings(root, additional, extra_errors, extra_pending, f"{slug} additional reference")
        if extra_errors or extra_pending:
            pending.extend(f"{slug}: additional reference approval stale: {issue}" for issue in extra_errors + extra_pending)
        valid = bool(approval and approval.get("status") == "reviewed" and _present(approval.get("reviewer"))
                     and not extra_errors and not extra_pending
                     and _present(page.get("source_hash"))
                     and approval.get("source_hash") == page.get("source_hash")
                     and skill and skill.is_file() and approval.get("skill_hash") == hig.digest(skill.read_bytes())
                     and reference and reference.is_file() and approval.get("reference_hash") == hig.digest(reference.read_bytes())
                     and isinstance(evidence, dict) and all(_present(evidence.get(key)) for key in EVIDENCE_KEYS))
        if valid:
            result["reviewed"] += 1
        else:
            pending.append(f"{slug}: independent instruction approval missing, incomplete, or stale")
    for slug in sorted(set(articles) - owners):
        pending.append(f"{slug}: missing owner in capability inventory")
    declared_paths = {str(row.get("skill_path")) for row in rows if isinstance(row, dict)}
    for path in package.glob("subskills/*/.topics/*/SKILL.md"):
        if str(path.relative_to(root)) not in declared_paths:
            errors.append(f"orphan instruction file has no capability owner: {path.relative_to(root)}")
    if owners == set(articles):
        for family, modes in sorted(family_modes.items()):
            missing = MODES - modes
            if missing:
                pending.append(f"{family}: missing case modes {', '.join(sorted(missing))}")
    if require_behavior:
        behavior = behavior_issues(root, rows)
        errors.extend(behavior["errors"])
        pending.extend(behavior["pending"])
        result["behavior_passed"] = behavior["passed"]
    # Keep pending separately visible even when the release gate also rejects it.
    if not allow_pending:
        errors.extend(pending)
    return result
