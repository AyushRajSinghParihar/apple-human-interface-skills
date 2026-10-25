"""Release contracts for installed topic procedures and their evidence bindings."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "capabilities.py"
spec = importlib.util.spec_from_file_location("capabilities", SCRIPT)
capabilities = importlib.util.module_from_spec(spec)
spec.loader.exec_module(capabilities)


def fingerprint(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


class CapabilityTests(unittest.TestCase):
    def package(self, root):
        """One small complete source family exercises the real release boundary."""
        package = root / "skills/apple-hig"
        family = package / "subskills/apple-hig-content"
        family.mkdir(parents=True)
        (package / "references").mkdir()
        (package / "SKILL.md").write_text(
            "[Family](subskills/apple-hig-content/SKILL.md)\n"
            "[Topics](references/topic-index.md)\n")
        pages, rows, routes, index = [], [], [], []
        for slug, mode in (("charts", "design"), ("tables", "review"), ("lists", "adapt")):
            reference = family / "references" / (slug + ".md")
            skill = family / ".topics" / ("apple-hig-" + slug) / "SKILL.md"
            reference.parent.mkdir(parents=True, exist_ok=True)
            skill.parent.mkdir(parents=True)
            reference.write_text("# " + slug + "\nSource-derived guidance.\n")
            skill.write_text(
                "---\nname: apple-hig-" + slug + "\ndescription: Use when working with " + slug + ".\n---\n"
                "[Guide](../../references/" + slug + ".md)\n")
            pages.append({"slug": slug, "module": "content", "type": "article",
                          "source_hash": "source-" + slug, "destination": str(reference.relative_to(root))})
            fixture = root / "evals/fixtures" / (slug + ".md")
            rubric = root / "evals/rubrics" / (slug + ".json")
            fixture.parent.mkdir(parents=True, exist_ok=True)
            fixture.write_text("Interface fixture for " + slug)
            write_json(rubric, {"criteria": ["Complete the requested task"]})
            case = root / "evals/cases" / ("topic-" + slug + ".json")
            write_json(case, {"id": "topic-" + slug, "kind": "topic", "topic": slug,
                              "family": "content", "mode": mode, "prompt": "Work on this interface.",
                              "baseline_control": slug == "charts", "output_files": ["result.md"],
                              "fixture_path": str(fixture.relative_to(root)), "fixture_hash": fingerprint(fixture),
                              "rubric_path": str(rubric.relative_to(root)), "rubric_hash": fingerprint(rubric)})
            rows.append({"topic": slug, "family": "content", "skill_path": str(skill.relative_to(root)),
                         "reference_path": str(reference.relative_to(root)), "case_id": "topic-" + slug,
                         "case_path": str(case.relative_to(root)), "case_hash": fingerprint(case)})
            write_json(root / "coverage/skill-reviews" / (slug + ".json"), {
                "status": "reviewed", "reviewer": "independent-reviewer",
                "source_hash": "source-" + slug, "skill_hash": fingerprint(skill),
                "reference_hash": fingerprint(reference), "evidence": {
                    key: "Observed concrete " + key + " decisions for " + slug
                    for key in ("decision", "artifact", "transformation", "verification", "applicability", "handoffs", "distinctiveness")}})
            routes.append("[" + slug + "](.topics/apple-hig-" + slug + "/SKILL.md)\n")
            index.append("[" + slug + "](../subskills/apple-hig-content/.topics/apple-hig-" + slug + "/SKILL.md)\n")
        (family / "SKILL.md").write_text("".join(routes))
        (package / "references/topic-index.md").write_text("".join(index))
        (package / "references/platforms-and-tasks.md").write_text("Platform routes.\n")
        write_json(root / "coverage/manifest.json", {"pages": pages})
        write_json(root / "coverage/capabilities.json", {"schema_version": 1, "topics": rows, "stress_cases": []})
        self.approve_routes(root)
        return rows

    def approve_routes(self, root):
        package = root / "skills/apple-hig"
        write_json(root / "coverage/routing-review.json", {
            "status": "reviewed", "reviewer": "independent-route-reviewer", "reviewed_at": "2026-10-25T00:00:00Z",
            "root_hash": fingerprint(package / "SKILL.md"),
            "family_hashes": {"content": fingerprint(package / "subskills/apple-hig-content/SKILL.md")},
            "topic_index_hash": fingerprint(package / "references/topic-index.md"),
            "platform_routes_hash": fingerprint(package / "references/platforms-and-tasks.md"),
            "evidence": {key: "Inspected route semantics for " + key
                         for key in ("root", "families", "exact_topics", "cross_topic_platform_routes", "scope_limits")}})

    def test_router_approval_is_mandatory_and_bound_to_every_current_route(self):
        for change in ("missing", "reviewer", "evidence", "family-set", "root", "family", "index", "platform"):
            with self.subTest(change=change), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                self.package(root)
                approval_path = root / "coverage/routing-review.json"
                approval = json.loads(approval_path.read_text())
                if change == "missing": approval_path.unlink()
                elif change in {"reviewer", "evidence", "family-set"}:
                    if change == "reviewer": approval["reviewer"] = ""
                    if change == "evidence": approval["evidence"].pop("families")
                    if change == "family-set": approval["family_hashes"]["unreviewed"] = "0" * 64
                    write_json(approval_path, approval)
                else:
                    names = {"root": "SKILL.md", "family": "subskills/apple-hig-content/SKILL.md",
                             "index": "references/topic-index.md", "platform": "references/platforms-and-tasks.md"}
                    target = root / "skills/apple-hig" / names[change]
                    target.write_text(target.read_text() + "Changed route behavior.\n")
                result = capabilities.check(root, require_behavior=False, allow_pending=True)
                self.assertTrue(any("routing approval" in issue for issue in result["pending"]), result)

    def test_complete_source_inventory_can_pass_without_a_hardcoded_article_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.package(root)
            result = capabilities.check(root, require_behavior=False)
            self.assertEqual(result, {"errors": [], "pending": [], "topics": 3, "reviewed": 3, "behavior_passed": 0})

    def test_manifest_is_required_even_in_development_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.package(root)
            (root / "coverage/manifest.json").unlink()
            result = capabilities.check(root, require_behavior=False, allow_pending=True)
            self.assertTrue(any("manifest" in item for item in result["errors"]), result)

    def test_source_owner_cannot_be_omitted_duplicated_or_moved_to_another_family(self):
        for mutation, message in (("omit", "missing owner"), ("duplicate", "duplicate"), ("family", "family"), ("orphan", "orphan")):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                rows = self.package(root)
                if mutation == "omit":
                    rows.pop()
                elif mutation == "duplicate":
                    rows.append(copy.deepcopy(rows[0]))
                elif mutation == "family":
                    rows[0]["family"] = "patterns"
                else:
                    rows.append(dict(rows[0], topic="unknown"))
                write_json(root / "coverage/capabilities.json", {"schema_version": 1, "topics": rows})
                result = capabilities.check(root, require_behavior=False)
                self.assertTrue(any(message in item for item in result["errors"]), result)

    def test_wrong_case_identity_or_shared_case_cannot_satisfy_topic_coverage(self):
        for mutation in ("family", "topic", "id", "duplicate-case"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                rows = self.package(root)
                case_path = root / rows[0]["case_path"]
                case = json.loads(case_path.read_text())
                if mutation == "duplicate-case":
                    rows[1].update({k: rows[0][k] for k in ("case_id", "case_path", "case_hash")})
                else:
                    case[mutation] = "wrong-identity"
                    write_json(case_path, case)
                    rows[0]["case_hash"] = fingerprint(case_path)
                write_json(root / "coverage/capabilities.json", {"schema_version": 1, "topics": rows})
                result = capabilities.check(root, require_behavior=False)
                self.assertTrue(any("case" in item for item in result["errors"]), result)

    def test_frozen_case_fixture_and_rubric_mutations_invalidate_evidence(self):
        for target in ("case", "fixture", "rubric"):
            with self.subTest(target=target), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                rows = self.package(root)
                case_path = root / rows[0]["case_path"]
                case = json.loads(case_path.read_text())
                path = case_path if target == "case" else root / case[target + "_path"]
                path.write_text(path.read_text() + "\nchanged bytes\n")
                result = capabilities.check(root, require_behavior=False)
                self.assertTrue(any("hash" in item for item in result["errors"]), result)

    def test_package_and_case_bindings_cannot_escape_the_repository(self):
        for key in ("skill_path", "reference_path", "case_path"):
            with self.subTest(key=key), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                rows = self.package(root)
                rows[0][key] = "../outside.md"
                write_json(root / "coverage/capabilities.json", {"schema_version": 1, "topics": rows})
                result = capabilities.check(root, require_behavior=False, allow_pending=True)
                self.assertTrue(any("outside" in item for item in result["errors"]), result)

    def test_modified_instruction_or_reference_requires_new_semantic_approval(self):
        for key in ("skill_path", "reference_path"):
            with self.subTest(key=key), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                rows = self.package(root)
                path = root / rows[0][key]
                path.write_text(path.read_text() + "\nChanged guidance.\n")
                result = capabilities.check(root, require_behavior=False, allow_pending=True)
                self.assertEqual(result["errors"], [], result)
                self.assertEqual(result["reviewed"], 2)
                self.assertTrue(any("approval" in item for item in result["pending"]), result)
                self.assertTrue(capabilities.check(root, require_behavior=False)["errors"])

    def test_structural_checks_do_not_replace_an_independent_evidenced_review(self):
        for mutation in ("missing", "empty-reviewer", "empty-evidence", "missing-decision", "source-hash", "unbound-source"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                self.package(root)
                path = root / "coverage/skill-reviews/charts.json"
                record = json.loads(path.read_text())
                if mutation == "missing":
                    path.unlink()
                else:
                    if mutation == "empty-reviewer": record["reviewer"] = " "
                    if mutation == "empty-evidence": record["evidence"] = {}
                    if mutation == "missing-decision": record["evidence"].pop("decision")
                    if mutation == "source-hash": record["source_hash"] = "obsolete"
                    if mutation == "unbound-source":
                        manifest_path = root / "coverage/manifest.json"
                        manifest = json.loads(manifest_path.read_text())
                        manifest["pages"][0].pop("source_hash")
                        write_json(manifest_path, manifest)
                        record.pop("source_hash")
                    write_json(path, record)
                result = capabilities.check(root, require_behavior=False, allow_pending=True)
                self.assertEqual(result["reviewed"], 2)
                self.assertTrue(any("approval" in item for item in result["pending"]), result)

    def test_broken_nested_route_and_unreachable_guide_block_release(self):
        for target in ("root", "family", "topic"):
            with self.subTest(target=target), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                rows = self.package(root)
                package = root / "skills/apple-hig"
                if target == "root":
                    (package / "SKILL.md").write_text("[Missing](missing/SKILL.md)\n")
                elif target == "family":
                    (package / "subskills/apple-hig-content/SKILL.md").write_text("[Wrong](.topics/wrong/SKILL.md)\n")
                else:
                    (root / rows[0]["skill_path"]).write_text("[Wrong](../../references/missing.md)\n")
                result = capabilities.check(root, require_behavior=False, allow_pending=True)
                self.assertTrue(any("route" in item or "link" in item for item in result["errors"]), result)

    def test_family_needs_all_request_modes_when_topic_inventory_is_complete(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rows = self.package(root)
            path = root / rows[2]["case_path"]
            case = json.loads(path.read_text())
            case["mode"] = "design"
            write_json(path, case)
            rows[2]["case_hash"] = fingerprint(path)
            write_json(root / "coverage/capabilities.json", {"schema_version": 1, "topics": rows})
            result = capabilities.check(root, require_behavior=False)
            self.assertTrue(any("adapt" in item for item in result["errors"]), result)

    def test_behavior_is_required_by_default_even_with_all_structural_approvals(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.package(root)
            result = capabilities.check(root)
            self.assertEqual(result["behavior_passed"], 0)
            self.assertTrue(any("behavior" in item for item in result["errors"]), result)

    def test_unregistered_instruction_directory_cannot_hide_outside_inventory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.package(root)
            extra = root / "skills/apple-hig/subskills/apple-hig-content/.topics/apple-hig-unknown/SKILL.md"
            extra.parent.mkdir()
            extra.write_text("Unreviewed topic instruction.")
            result = capabilities.check(root, require_behavior=False, allow_pending=True)
            self.assertTrue(any("orphan" in item for item in result["errors"]), result)

    def runtime_records(self, root):
        rows = self.package(root)
        harness = root / "scripts/evaluate.py"
        harness.parent.mkdir()
        harness.write_text("# Frozen runtime harness fixture\n")
        for args in (("init", "-q"), ("add", "skills"),
                     ("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "Baseline fixture")):
            subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True)
        baseline = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip()
        inventory_path = root / "coverage/capabilities.json"
        inventory = json.loads(inventory_path.read_text())
        inventory.update(baseline_commit=baseline, requirements={"stress_cases": 0, "stress_repetitions": 3})
        write_json(inventory_path, inventory)
        records = []
        axes = ("task_completion", "hig_correctness", "artifact_usefulness", "conditions_accessibility", "evidence_honesty")
        for row in rows:
            variants = ("candidate", "baseline") if row["topic"] == "charts" else ("candidate",)
            for variant in variants:
                run_id = row["case_id"] + "." + variant + ".r1.a1"
                directory = root / "coverage/behavior" / run_id
                directory.mkdir(parents=True)
                (directory / "artifacts").mkdir()
                output = directory / "artifacts/result.md"
                output.write_text("A concrete revised interface artifact.\n")
                transcript = directory / "events.jsonl"
                thread_id = "session-" + run_id
                transcript.write_text(json.dumps({"type": "thread.started", "thread_id": thread_id}) + '\n{"type":"turn.completed"}\n')
                prefix = "skills/apple-hig/"
                required = ["SKILL.md", "subskills/apple-hig-content/SKILL.md",
                            row["skill_path"].removeprefix(prefix), row["reference_path"].removeprefix(prefix)]
                record = {"schema_version": 1, "run_id": run_id, "case_id": row["case_id"],
                          "thread_id": thread_id,
                          "variant": variant, "repetition": 1, "attempt": 1, "status": "completed",
                          "case_path": row["case_path"], "case_hash": row["case_hash"],
                          "harness_hash": fingerprint(harness), "model": "fixture-model", "cli_version": "fixture-cli",
                          "started_at": "2026-10-25T00:00:00Z", "finished_at": "2026-10-25T00:01:00Z",
                          "baseline_commit": baseline,
                          "package_dependencies": {path: fingerprint(root / prefix / path) for path in required},
                          "discovery_dependencies": {path: fingerprint(root / prefix / path) for path in required[:2]},
                          "reads": required, "required_reads": required, "routing": {"missing": [], "passed": True},
                          "artifacts": {"result.md": {"path": str(output.relative_to(root)), "hash": fingerprint(output)}},
                          "transcript": {"path": str(transcript.relative_to(root)), "hash": fingerprint(transcript)},
                          "checks": {"passed": True, "missing_artifacts": [], "adaptation_changed": True,
                                     "turn_completed": True, "exit_code": 0, "forbidden_reads": [], "package_changed": [], "malformed_event_count": 0}}
                record_path = directory / "record.json"
                write_json(record_path, record)
                grading_transcript = root / "coverage/grading" / run_id / "events.jsonl"
                grading_transcript.parent.mkdir(parents=True)
                grading_thread = "grader-" + run_id
                grading_transcript.write_text(json.dumps({"type": "thread.started", "thread_id": grading_thread}) + '\n{"type":"turn.completed"}\n')
                grade = {"record_hash": fingerprint(record_path), "case_hash": row["case_hash"],
                         "grader": "independent-grader", "reviewed_at": "2026-10-25T00:02:00Z",
                         "grading_thread_id": grading_thread,
                         "grading_transcript": {"path": str(grading_transcript.relative_to(root)), "hash": fingerprint(grading_transcript)},
                         "artifact_hashes": {name: binding["hash"] for name, binding in record["artifacts"].items()},
                         "scores": {axis: 2 for axis in axes}, "evidence": {axis: "Concrete inspected judgment about " + axis for axis in axes},
                         "critical_errors": [], "found_defect_ids": [], "invented_high_severity_findings": [], "verdict": "pass"}
                write_json(directory / "grade.json", grade)
                records.append(record_path)
        return records

    def independent_copy(self, root, source, run_id, **changes):
        """Make a separate fixture execution with its own bytes and session."""
        record = json.loads(source.read_text())
        directory = source.parent.with_name(run_id)
        directory.mkdir()
        record.update(run_id=run_id, thread_id="session-" + run_id, **changes)
        for name, binding in record["artifacts"].items():
            destination = directory / "artifacts" / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes((root / binding["path"]).read_bytes())
            record["artifacts"][name] = {"path": str(destination.relative_to(root)), "hash": fingerprint(destination)}
        transcript = directory / "events.jsonl"
        transcript.write_text(json.dumps({"type": "thread.started", "thread_id": record["thread_id"]}) + '\n{"type":"turn.completed"}\n')
        record["transcript"] = {"path": str(transcript.relative_to(root)), "hash": fingerprint(transcript)}
        path = directory / "record.json"
        write_json(path, record)
        grade = json.loads(source.with_name("grade.json").read_text())
        grade.update(record_hash=fingerprint(path), case_hash=record["case_hash"])
        write_json(path.with_name("grade.json"), grade)
        return path

    def test_current_candidate_runs_and_matched_historical_controls_satisfy_behavior(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.runtime_records(root)
            result = capabilities.check(root)
            self.assertEqual(result["errors"], [], result)
            self.assertEqual(result["pending"], [], result)
            self.assertEqual(result["behavior_passed"], 3)

    def test_behavior_grades_reject_critical_failures_missing_defects_and_invented_findings(self):
        for mutation in ("critical", "score", "invented", "missing-critical-defect", "missing-fourth-defect"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                records = self.runtime_records(root)
                record_path = next(p for p in records if ".candidate." in str(p))
                grade_path = record_path.with_name("grade.json")
                grade = json.loads(grade_path.read_text())
                if mutation == "critical": grade["critical_errors"] = ["Unsupported critical recommendation"]
                if mutation == "score": grade["scores"]["task_completion"] = 0; grade["scores"]["artifact_usefulness"] = 0
                if mutation == "invented": grade["invented_high_severity_findings"] = ["Unobserved severe defect"]
                if mutation.startswith("missing-"):
                    record = json.loads(record_path.read_text())
                    case_path = root / record["case_path"]
                    case = json.loads(case_path.read_text())
                    case["mode"] = "review"
                    case["rubric"] = {"required_findings": [{"id": str(i), "description": "Seeded defect", "critical": i == 1} for i in range(1, 6)]}
                    write_json(case_path, case)
                    case_hash = fingerprint(case_path)
                    inventory_path = root / "coverage/capabilities.json"
                    inventory = json.loads(inventory_path.read_text())
                    inventory["topics"][0]["case_hash"] = case_hash
                    write_json(inventory_path, inventory)
                    for paired in records:
                        rec = json.loads(paired.read_text())
                        if rec["case_id"] == record["case_id"]:
                            rec["case_hash"] = case_hash
                            write_json(paired, rec)
                            g = json.loads(paired.with_name("grade.json").read_text())
                            g.update(case_hash=case_hash, record_hash=fingerprint(paired), found_defect_ids=["1", "2", "3", "4"])
                            write_json(paired.with_name("grade.json"), g)
                    grade = json.loads(grade_path.read_text())
                    grade["found_defect_ids"] = ["2", "3", "4", "5"] if mutation == "missing-critical-defect" else ["1", "2", "3"]
                write_json(grade_path, grade)
                result = capabilities.behavior_issues(root, json.loads((root / "coverage/capabilities.json").read_text())["topics"])
                self.assertEqual(result["passed"], 2, result)
                self.assertTrue(result["errors"] or result["pending"], result)

    def test_behavior_records_bind_grade_artifact_transcript_harness_and_package_bytes(self):
        for mutation in ("grade", "artifact", "transcript", "harness", "package", "routing", "no-artifacts"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                records = self.runtime_records(root)
                record_path = next(p for p in records if ".candidate." in str(p))
                record = json.loads(record_path.read_text())
                if mutation == "grade":
                    record["model"] = "changed-model"
                elif mutation in ("routing", "no-artifacts"):
                    if mutation == "routing": record["reads"].pop(); record["routing"] = {"missing": [], "passed": True}
                    else: record["artifacts"] = {}
                else:
                    if mutation == "artifact": target = root / record["artifacts"]["result.md"]["path"]
                    if mutation == "transcript": target = root / record["transcript"]["path"]
                    if mutation == "harness": target = root / "scripts/evaluate.py"
                    if mutation == "package": target = root / "skills/apple-hig/SKILL.md"
                    target.write_text(target.read_text() + "\nmutation\n")
                if mutation in ("grade", "routing", "no-artifacts"):
                    write_json(record_path, record)
                    if mutation != "grade":
                        grade_path = record_path.with_name("grade.json")
                        grade = json.loads(grade_path.read_text())
                        grade["record_hash"] = fingerprint(record_path)
                        write_json(grade_path, grade)
                result = capabilities.check(root)
                self.assertTrue(result["errors"], result)
                if mutation == "grade": self.assertTrue(any("grade" in item for item in result["errors"]), result)

    def test_failed_baseline_grade_is_recorded_without_requiring_control_to_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            records = self.runtime_records(root)
            baseline = next(p for p in records if ".baseline." in str(p))
            grade_path = baseline.with_name("grade.json")
            grade = json.loads(grade_path.read_text())
            grade.update(verdict="fail", scores={axis: 0 for axis in grade["scores"]}, critical_errors=["Observed baseline defect"])
            write_json(grade_path, grade)
            result = capabilities.check(root)
            self.assertEqual(result["errors"], [], result)

    def test_baseline_dependencies_remain_bound_to_old_commit_after_candidate_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            records = self.runtime_records(root)
            package_root = root / "skills/apple-hig/SKILL.md"
            package_root.write_text(package_root.read_text() + "\nRevised candidate routing instructions.\n")
            self.approve_routes(root)
            for path in records:
                record = json.loads(path.read_text())
                if record["variant"] == "candidate":
                    record["package_dependencies"]["SKILL.md"] = fingerprint(package_root)
                    record["discovery_dependencies"]["SKILL.md"] = fingerprint(package_root)
                    write_json(path, record)
                    grade_path = path.with_name("grade.json")
                    grade = json.loads(grade_path.read_text())
                    grade["record_hash"] = fingerprint(path)
                    write_json(grade_path, grade)
            self.assertEqual(capabilities.check(root)["errors"], [])

    def test_stress_case_requires_a_current_execution_in_each_frozen_repetition(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            records = self.runtime_records(root)
            inventory_path = root / "coverage/capabilities.json"
            inventory = json.loads(inventory_path.read_text())
            row = {"id": "stress-charts", "case_path": "evals/cases/stress-charts.json", "repetitions": 3}
            case = json.loads((root / inventory["topics"][0]["case_path"]).read_text())
            case.update(id="stress-charts", kind="stress", topic=None, family=None, expected_topics=["charts"], baseline_control=False)
            write_json(root / row["case_path"], case)
            row["case_hash"] = fingerprint(root / row["case_path"])
            inventory.update(stress_cases=[row], requirements={"stress_cases": 1, "stress_repetitions": 3})
            write_json(inventory_path, inventory)
            template_path = next(path for path in records if ".candidate." in str(path))
            for repetition in (1, 2, 3):
                run_id = f"stress-charts.candidate.r{repetition}.a1"
                self.independent_copy(root, template_path, run_id, case_id=row["id"], case_path=row["case_path"], case_hash=row["case_hash"], repetition=repetition)
                result = capabilities.check(root)
                if repetition < 3:
                    self.assertTrue(any(f"repetition {repetition + 1}" in item for item in result["errors"]), result)
                else:
                    self.assertEqual(result["errors"], [], result)
            repeated = root / "coverage/behavior/stress-charts.candidate.r3.a1/record.json"
            record = json.loads(repeated.read_text())
            record["thread_id"] = "session-stress-charts.candidate.r2.a1"
            transcript = root / record["transcript"]["path"]
            transcript.write_text(json.dumps({"type": "thread.started", "thread_id": record["thread_id"]}) + '\n{"type":"turn.completed"}\n')
            record["transcript"]["hash"] = fingerprint(transcript)
            write_json(repeated, record)
            grade = json.loads(repeated.with_name("grade.json").read_text())
            grade["record_hash"] = fingerprint(repeated)
            write_json(repeated.with_name("grade.json"), grade)
            self.assertTrue(any("session" in item for item in capabilities.check(root)["errors"]))

    def test_negative_invocation_requires_no_hig_reads_and_no_fake_dependency(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            records = self.runtime_records(root)
            inventory_path = root / "coverage/capabilities.json"
            inventory = json.loads(inventory_path.read_text())
            row = inventory["topics"][2]
            case_path = root / row["case_path"]
            case = json.loads(case_path.read_text())
            case["invoke"] = False
            write_json(case_path, case)
            row["case_hash"] = fingerprint(case_path)
            write_json(inventory_path, inventory)
            path = next(path for path in records if row["case_id"] in str(path))
            record = json.loads(path.read_text())
            record.update(case_hash=row["case_hash"], reads=[], required_reads=[], package_dependencies={})
            write_json(path, record)
            grade_path = path.with_name("grade.json")
            grade = json.loads(grade_path.read_text())
            grade.update(record_hash=fingerprint(path), case_hash=row["case_hash"])
            write_json(grade_path, grade)
            self.assertEqual(capabilities.check(root)["errors"], [])
            record["reads"] = ["SKILL.md"]
            write_json(path, record)
            grade["record_hash"] = fingerprint(path)
            write_json(grade_path, grade)
            result = capabilities.check(root)
            self.assertTrue(any("negative invocation" in item for item in result["errors"]), result)

    def test_current_retry_accepts_retained_operational_failures_but_not_tampering(self):
        for earlier in ("routing-failure", "stale-harness", "old-case", "unfinished", "tampered-artifact", "tampered-transcript"):
            with self.subTest(earlier=earlier), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                records = self.runtime_records(root)
                first = next(path for path in records if ".candidate." in str(path))
                record = json.loads(first.read_text())
                self.independent_copy(root, first, first.parent.name[:-1] + "2", attempt=2)
                if earlier == "routing-failure":
                    record.update(status="routing_error", reads=[], routing={"missing": record["required_reads"], "passed": False})
                    first.with_name("grade.json").unlink()
                elif earlier == "stale-harness":
                    record["harness_hash"] = "0" * 64
                elif earlier == "old-case":
                    record["case_hash"] = "0" * 64
                elif earlier == "unfinished":
                    record.update(status="infrastructure_error", cli_version="", finished_at=None, reads=[])
                    first.with_name("grade.json").unlink()
                elif earlier == "tampered-transcript":
                    historical = root / record["transcript"]["path"]
                    historical.write_text("Changed retained transcript\n")
                else:
                    record["artifacts"]["result.md"]["hash"] = "0" * 64
                write_json(first, record)
                if first.with_name("grade.json").exists():
                    grade = json.loads(first.with_name("grade.json").read_text())
                    grade["record_hash"] = fingerprint(first)
                    grade["case_hash"] = record["case_hash"]
                    write_json(first.with_name("grade.json"), grade)
                result = capabilities.check(root)
                self.assertEqual(bool(result["errors"]), earlier in {"tampered-artifact", "tampered-transcript"}, result)

    def test_cross_run_or_symlink_evidence_cannot_satisfy_an_execution(self):
        for target in ("artifact", "transcript", "artifact-symlink", "wrong-logical-name"):
            with self.subTest(target=target), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                records = self.runtime_records(root)
                source, destination = records[0], records[2]
                first = json.loads(source.read_text())
                record = json.loads(destination.read_text())
                if target == "artifact":
                    record["artifacts"] = first["artifacts"]
                elif target == "transcript":
                    record["transcript"] = first["transcript"]
                    record["thread_id"] = first["thread_id"]
                elif target == "artifact-symlink":
                    artifact = root / record["artifacts"]["result.md"]["path"]
                    artifact.unlink()
                    artifact.symlink_to(root / first["artifacts"]["result.md"]["path"])
                else:
                    artifact = root / record["artifacts"]["result.md"]["path"]
                    moved = artifact.with_name("unrelated.md")
                    artifact.rename(moved)
                    record["artifacts"]["result.md"]["path"] = str(moved.relative_to(root))
                write_json(destination, record)
                grade_path = destination.with_name("grade.json")
                grade = json.loads(grade_path.read_text())
                grade["record_hash"] = fingerprint(destination)
                write_json(grade_path, grade)
                result = capabilities.check(root)
                self.assertTrue(any("owned" in item or "logical" in item for item in result["errors"]), result)

    def test_selected_executions_require_distinct_sessions_matching_transcripts(self):
        for mutation in ("same-session", "record-mismatch", "missing-thread"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                records = self.runtime_records(root)
                source, destination = records[0], records[2]
                record = json.loads(destination.read_text())
                if mutation == "same-session":
                    record["thread_id"] = json.loads(source.read_text())["thread_id"]
                    transcript = root / record["transcript"]["path"]
                    transcript.write_text(json.dumps({"type": "thread.started", "thread_id": record["thread_id"]}) + '\n{"type":"turn.completed"}\n')
                    record["transcript"]["hash"] = fingerprint(transcript)
                elif mutation == "record-mismatch":
                    record["thread_id"] = "invented-session"
                else:
                    record.pop("thread_id")
                write_json(destination, record)
                grade_path = destination.with_name("grade.json")
                grade = json.loads(grade_path.read_text())
                grade["record_hash"] = fingerprint(destination)
                write_json(grade_path, grade)
                result = capabilities.check(root)
                self.assertTrue(any("session" in item or "thread" in item for item in result["errors"]), result)

    def test_stale_case_history_does_not_inherit_new_outputs_or_adaptation_requirements(self):
        for change in ("output", "mode"):
            with self.subTest(change=change), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                records = self.runtime_records(root)
                inventory_path = root / "coverage/capabilities.json"
                inventory = json.loads(inventory_path.read_text())
                row = inventory["topics"][0]
                case_path = root / row["case_path"]
                case = json.loads(case_path.read_text())
                if change == "output": case["output_files"].append("extra.md")
                else: case["mode"] = "adapt"
                write_json(case_path, case)
                row["case_hash"] = fingerprint(case_path)
                write_json(inventory_path, inventory)
                for old in records:
                    record = json.loads(old.read_text())
                    if record["case_id"] != row["case_id"]:
                        continue
                    fresh = self.independent_copy(root, old, old.parent.name[:-1] + "2", attempt=2, case_hash=row["case_hash"])
                    current = json.loads(fresh.read_text())
                    if change == "output":
                        extra = fresh.parent / "artifacts/extra.md"
                        extra.write_text("A newly requested output.\n")
                        current["artifacts"]["extra.md"] = {"path": str(extra.relative_to(root)), "hash": fingerprint(extra)}
                    write_json(fresh, current)
                    grade = json.loads(fresh.with_name("grade.json").read_text())
                    grade["record_hash"] = fingerprint(fresh)
                    grade["artifact_hashes"] = {name: binding["hash"] for name, binding in current["artifacts"].items()}
                    write_json(fresh.with_name("grade.json"), grade)
                    record.pop("thread_id")
                    record["checks"].pop("adaptation_changed")
                    write_json(old, record)
                    grade = json.loads(old.with_name("grade.json").read_text())
                    grade["record_hash"] = fingerprint(old)
                    write_json(old.with_name("grade.json"), grade)
                result = capabilities.behavior_issues(root, inventory["topics"])
                self.assertEqual(result["errors"], [], result)
                self.assertEqual(result["pending"], [], result)

    def test_current_grades_bind_actual_grader_session_and_reviewed_artifacts(self):
        for variant in ("candidate", "baseline"):
            for change in ("missing", "bytes", "artifact-hash", "thread", "reuse-execution", "unfinished", "outside"):
                with self.subTest(variant=variant, change=change), tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    records = self.runtime_records(root)
                    path = next(path for path in records if f".{variant}." in str(path))
                    grade_path = path.with_name("grade.json")
                    grade = json.loads(grade_path.read_text())
                    transcript = root / grade["grading_transcript"]["path"]
                    if change == "missing": grade.pop("grading_transcript")
                    elif change == "bytes": transcript.write_text(transcript.read_text() + "changed bytes\n")
                    elif change == "artifact-hash": grade["artifact_hashes"]["result.md"] = "0" * 64
                    elif change == "thread": grade["grading_thread_id"] = "wrong-thread"
                    elif change == "outside":
                        moved = root / "unowned-grader.jsonl"
                        moved.write_bytes(transcript.read_bytes())
                        grade["grading_transcript"]["path"] = str(moved.relative_to(root))
                    else:
                        if change == "reuse-execution":
                            grade["grading_thread_id"] = json.loads(path.read_text())["thread_id"]
                            transcript.write_text(json.dumps({"type": "thread.started", "thread_id": grade["grading_thread_id"]}) + '\n{"type":"turn.completed"}\n')
                        else: transcript.write_text(json.dumps({"type": "thread.started", "thread_id": grade["grading_thread_id"]}) + "\n")
                        grade["grading_transcript"]["hash"] = fingerprint(transcript)
                    write_json(grade_path, grade)
                    result = capabilities.behavior_issues(root, json.loads((root / "coverage/capabilities.json").read_text())["topics"])
                    self.assertTrue(any("grad" in issue for issue in result["errors"] + result["pending"]), result)

    def test_declared_additional_reference_changes_require_instruction_rereview(self):
        for change in ("bytes", "missing", "malformed"):
            with self.subTest(change=change), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                self.package(root)
                extra = root / "skills/apple-hig/subskills/apple-hig-content/references/related.md"
                extra.write_text("A consequential related-source qualification.\n")
                approval_path = root / "coverage/skill-reviews/charts.json"
                approval = json.loads(approval_path.read_text())
                approval["additional_references"] = [{"path": str(extra.relative_to(root)), "hash": fingerprint(extra)}]
                write_json(approval_path, approval)
                self.assertEqual(capabilities.check(root, require_behavior=False)["errors"], [])
                if change == "bytes": extra.write_text("The cross-topic qualification changed.\n")
                elif change == "missing": extra.unlink()
                else:
                    approval["additional_references"] = "missing structured bindings"
                    write_json(approval_path, approval)
                result = capabilities.check(root, require_behavior=False, allow_pending=True)
                self.assertEqual(result["reviewed"], 2, result)
                self.assertTrue(any("additional reference" in issue for issue in result["pending"]), result)

    def test_negative_runs_are_invalidated_by_visible_skill_metadata_changes(self):
        for change in ("missing-discovery", "root", "family"):
            with self.subTest(change=change), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                records = self.runtime_records(root)
                inventory_path = root / "coverage/capabilities.json"
                inventory = json.loads(inventory_path.read_text())
                row = inventory["topics"][2]
                case_path = root / row["case_path"]
                case = json.loads(case_path.read_text())
                case["invoke"] = False
                write_json(case_path, case)
                row["case_hash"] = fingerprint(case_path)
                write_json(inventory_path, inventory)
                path = next(path for path in records if row["case_id"] in str(path))
                record = json.loads(path.read_text())
                record.update(case_hash=row["case_hash"], reads=[], required_reads=[], package_dependencies={})
                if change == "missing-discovery": record.pop("discovery_dependencies")
                else:
                    relative = "SKILL.md" if change == "root" else "subskills/apple-hig-content/SKILL.md"
                    metadata = root / "skills/apple-hig" / relative
                    metadata.write_text(metadata.read_text() + "\nChanged discovery description.\n")
                write_json(path, record)
                grade_path = path.with_name("grade.json")
                grade = json.loads(grade_path.read_text())
                grade.update(record_hash=fingerprint(path), case_hash=row["case_hash"])
                write_json(grade_path, grade)
                result = capabilities.check(root)
                self.assertTrue(any("discovery" in item for item in result["errors"]), result)

    def test_positive_runs_require_current_discovery_even_for_unread_families(self):
        for variant in ("candidate", "baseline"):
            for change in ("missing", "stale-root", "unread-family"):
                with self.subTest(variant=variant, change=change), tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    records = self.runtime_records(root)
                    path = next(path for path in records if f".{variant}." in str(path))
                    record = json.loads(path.read_text())
                    if change == "missing": record.pop("discovery_dependencies")
                    elif change == "stale-root": record["discovery_dependencies"]["SKILL.md"] = "0" * 64
                    else:
                        manifest_path = root / "coverage/manifest.json"
                        manifest = json.loads(manifest_path.read_text())
                        manifest["pages"].append({"type": "article", "module": "inputs"})
                        write_json(manifest_path, manifest)
                    write_json(path, record)
                    grade_path = path.with_name("grade.json")
                    grade = json.loads(grade_path.read_text())
                    grade["record_hash"] = fingerprint(path)
                    write_json(grade_path, grade)
                    rows = json.loads((root / "coverage/capabilities.json").read_text())["topics"]
                    result = capabilities.behavior_issues(root, rows)
                    self.assertTrue(any("discovery" in item for item in result["pending"]), result)


if __name__ == "__main__":
    unittest.main()
