"""Review maintenance must find stale hashes and never approve content by itself."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
spec = importlib.util.spec_from_file_location("approvals", SCRIPTS / "approvals.py")
approvals = importlib.util.module_from_spec(spec)
spec.loader.exec_module(approvals)

EVIDENCE = {key: "Checked " + key for key in
            ("decision", "artifact", "transformation", "verification", "applicability", "handoffs", "distinctiveness")}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path


def write_json(path, value):
    write(path, json.dumps(value, indent=2) + "\n")


class ApprovalTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name).resolve()
        package = self.root / "skills/apple-hig"
        family = package / "subskills/apple-hig-presentation"
        self.root_skill = write(package / "SKILL.md", "---\nname: apple-hig\n---\nRouter\n")
        self.index = write(package / "references/topic-index.md", "Index\n")
        self.routes = write(package / "references/platforms-and-tasks.md", "Routes\n")
        self.family = write(family / "SKILL.md", "Family\n")
        self.skill = write(family / ".topics/apple-hig-alerts/SKILL.md", "Procedure\n")
        self.reference = write(family / "references/alerts.md", "Guide\n")
        self.extra = write(family / "references/sheets.md", "Supplement\n")
        self.media = write(package / "references/media/alerts.md", "Media notes\n")
        rel = lambda path: path.relative_to(self.root).as_posix()
        write_json(self.root / "coverage/manifest.json", {"pages": [
            {"slug": "alerts", "type": "article", "module": "presentation",
             "source_hash": "source-alerts", "destination": rel(self.reference)}]})
        write_json(self.root / "coverage/capabilities.json", {"topics": [
            {"topic": "alerts", "skill_path": rel(self.skill), "reference_path": rel(self.reference)}]})
        write_json(self.root / "coverage/skill-reviews/alerts.json", {
            "topic": "alerts", "reviewer": "auditor", "reviewed_at": "2026-10-25", "status": "reviewed",
            "source_hash": "source-alerts", "skill_hash": sha(self.skill), "reference_hash": sha(self.reference),
            "additional_references": [], "evidence": dict(EVIDENCE)})
        write_json(self.root / "coverage/reviews/alerts.json", {
            "review": {"slug": "alerts", "status": "reviewed", "reviewer": "reviewer-a", "reviewed_at": "2026-10-25",
                       "source_hash": "source-alerts", "destination_hash": sha(self.reference),
                       "evidence": "Checked every section.",
                       "units": [{"id": "u1", "status": "reviewed", "evidence": "Moved to sheets.",
                                  "destination": rel(self.extra), "destination_hash": sha(self.extra)}]},
            "media": {"m1": {"status": "reviewed", "reviewer": "auditor", "evidence": "Inspected frames.",
                             "supporting_files": [{"path": rel(self.media), "hash": sha(self.media)}]}}})
        write_json(self.root / "coverage/routing-review.json", {
            "status": "reviewed", "reviewer": "auditor", "reviewed_at": "2026-10-25",
            "root_hash": sha(self.root_skill), "topic_index_hash": sha(self.index),
            "platform_routes_hash": sha(self.routes), "family_hashes": {"presentation": sha(self.family)},
            "evidence": {"root": "Read the root."}})

    def tearDown(self):
        self.directory.cleanup()

    def record(self, relative):
        return json.loads((self.root / relative).read_text())

    def test_current_records_have_no_stale_hash_or_marker(self):
        self.assertEqual(approvals.stale(self.root), [])
        self.assertEqual(approvals.marker_errors(self.root), [])

    def test_changed_procedure_is_listed_drafted_and_blocked(self):
        self.skill.write_text("Procedure, rewritten\n")
        issues = approvals.stale(self.root)
        self.assertEqual([(i["record"], i["field"]) for i in issues], [("coverage/skill-reviews/alerts.json", "/skill_hash")])
        self.assertEqual(approvals.draft(self.root, "coverage/skill-reviews/alerts.json"), ["/skill_hash"])
        record = self.record("coverage/skill-reviews/alerts.json")
        self.assertEqual(record["status"], "draft")
        self.assertEqual(record["reviewer"], "")
        self.assertEqual(record["previous_review"]["reviewer"], "auditor")
        self.assertTrue(all(value.startswith(approvals.TODO_MARK) for value in record["evidence"].values()))
        self.assertEqual(approvals.stale(self.root), [])
        self.assertTrue(approvals.marker_errors(self.root))

    def test_approval_needs_a_reviewer_and_rewritten_evidence(self):
        self.reference.write_text("Guide, corrected\n")
        approvals.draft(self.root, "coverage/skill-reviews/alerts.json")
        with self.assertRaisesRegex(ValueError, "reviewer"):
            approvals.approve(self.root, "coverage/skill-reviews/alerts.json", " ")
        with self.assertRaisesRegex(ValueError, "TODO"):
            approvals.approve(self.root, "coverage/skill-reviews/alerts.json", "second-reviewer")
        path = self.root / "coverage/skill-reviews/alerts.json"
        record = json.loads(path.read_text())
        record["evidence"] = {key: "Rechecked " + key for key in EVIDENCE}
        path.write_text(json.dumps(record))
        self.assertEqual(approvals.approve(self.root, "coverage/skill-reviews/alerts.json", "second-reviewer"), 1)
        record = self.record("coverage/skill-reviews/alerts.json")
        self.assertEqual((record["status"], record["reviewer"]), ("reviewed", "second-reviewer"))
        self.assertNotIn("previous_review", record)
        self.assertEqual(approvals.marker_errors(self.root), [])

    def test_approval_refuses_a_record_that_went_stale_again(self):
        self.skill.write_text("First edit\n")
        approvals.draft(self.root, "coverage/skill-reviews/alerts.json")
        path = self.root / "coverage/skill-reviews/alerts.json"
        record = json.loads(path.read_text())
        record["evidence"] = dict(EVIDENCE)
        path.write_text(json.dumps(record))
        self.skill.write_text("Second edit after the draft\n")
        with self.assertRaisesRegex(ValueError, "stale"):
            approvals.approve(self.root, "coverage/skill-reviews/alerts.json", "second-reviewer")

    def test_media_and_unit_changes_draft_only_their_own_owner(self):
        self.media.write_text("Media notes, expanded\n")
        self.extra.write_text("Supplement, expanded\n")
        changed = approvals.draft(self.root, "coverage/reviews/alerts.json")
        self.assertEqual(sorted(changed), ["/media/m1/supporting_files/0/hash", "/review/units/0/destination_hash"])
        record = self.record("coverage/reviews/alerts.json")
        self.assertEqual(record["review"]["status"], "reviewed")
        self.assertEqual(record["review"]["units"][0]["status"], "draft")
        self.assertEqual(record["media"]["m1"]["status"], "draft")

    def test_route_changes_are_bound_to_the_routing_review(self):
        self.family.write_text("Family, rewritten\n")
        self.index.write_text("Index, compact\n")
        fields = {issue["field"] for issue in approvals.stale(self.root)}
        self.assertEqual(fields, {"/family_hashes/presentation", "/topic_index_hash"})

    def test_a_missing_bound_file_cannot_be_drafted(self):
        self.reference.unlink()
        with self.assertRaisesRegex(ValueError, "missing"):
            approvals.draft(self.root, "coverage/skill-reviews/alerts.json")

    def test_records_outside_coverage_are_rejected(self):
        with self.assertRaises(ValueError):
            approvals.draft(self.root, "skills/apple-hig/SKILL.md")

    def test_cli_reports_drafts_every_stale_record_and_fails_until_approval(self):
        self.skill.write_text("Procedure, rewritten\n")
        command = [sys.executable, str(SCRIPTS / "hig.py")]
        stale = subprocess.run(command + ["stale", "--root", str(self.root)], capture_output=True, text=True)
        self.assertEqual(stale.returncode, 1, stale.stderr)
        self.assertEqual(json.loads(stale.stdout)["stale_count"], 1)
        drafted = subprocess.run(command + ["review-draft", "--all", "--root", str(self.root)], capture_output=True, text=True)
        self.assertEqual(drafted.returncode, 0, drafted.stderr)
        self.assertIn("coverage/skill-reviews/alerts.json", json.loads(drafted.stdout)["drafted"])
        refused = subprocess.run(command + ["review-approve", "coverage/skill-reviews/alerts.json",
                                            "--reviewer", "second-reviewer", "--root", str(self.root)],
                                 capture_output=True, text=True)
        self.assertEqual(refused.returncode, 2)
        self.assertIn("TODO", refused.stderr)


if __name__ == "__main__":
    unittest.main()
