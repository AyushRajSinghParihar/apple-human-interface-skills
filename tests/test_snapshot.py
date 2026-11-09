"""Snapshot helpers carry reviews forward only for unchanged content and never approve."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
spec = importlib.util.spec_from_file_location("snapshot", SCRIPTS / "snapshot.py")
snapshot = importlib.util.module_from_spec(spec)
spec.loader.exec_module(snapshot)

GUIDE = "skills/apple-hig/subskills/apple-hig-presentation/references/alerts.md"


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def unit(uid, digest, section, treatment="guidance"):
    return {"id": uid, "hash": digest, "section": section, "kind": "paragraph", "treatment": treatment}


def media(uid, identifier, metadata):
    return {"id": uid, "identifier": identifier, "kind": "image", "section": "Buttons", "treatment": "guidance",
            "reference_metadata_hash": metadata,
            "representations": [{"url": f"https://example.test/{identifier}", "traits": ["2x", "light"]}]}


class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name).resolve()
        self.guide = self.root / GUIDE
        self.guide.parent.mkdir(parents=True)
        self.guide.write_text('# Alerts\n<a id="Buttons"></a>\n## Buttons\nUse specific labels.\n')
        # The new source inserted unit "new" before "kept", so "kept" moved from content/0 to content/1.
        write_json(self.root / "coverage/manifest.json", {"pages": [{
            "slug": "alerts", "type": "article", "destination": GUIDE, "source_hash": "s2",
            "extraction": {"units": [unit("content/0", "h-new", "overview"), unit("content/1", "h-kept", "Buttons")],
                           "media": [media("content/2", "kept.png", "m1"), media("content/3", "new.png", "m2")]}}]})
        write_json(self.root / "coverage/reviews/alerts.json", {"review": {
            "status": "reviewed", "destination_hash": hashlib.sha256(self.guide.read_bytes()).hexdigest(),
            "units": [{"id": "content/0", "source_unit_hash": "h-kept", "source_anchor": "Buttons", "status": "reviewed",
                       "treatment": "guidance", "destination": GUIDE, "evidence": "Checked."},
                      {"id": "content/9", "source_unit_hash": "h-gone", "source_anchor": "Buttons", "status": "reviewed",
                       "treatment": "guidance", "destination": GUIDE, "evidence": "Checked."}]}, "media": {}})
        write_json(self.root / "coverage/image-reviews/alerts.json", {"source_hash": "s2", "media": {
            "kept.png": {"status": "reviewed", "reference_metadata_hash": "m1", "reviewed_occurrence_ids": ["content/1"]},
            "removed.png": {"status": "reviewed", "reference_metadata_hash": "m0", "reviewed_occurrence_ids": ["content/4"]}}})

    def tearDown(self):
        self.directory.cleanup()

    def record(self, relative):
        return json.loads((self.root / relative).read_text())

    def test_remap_moves_unchanged_reviews_and_drops_removed_content(self):
        report = snapshot.remap(self.root, "alerts")
        self.assertEqual((report["units_kept"], report["units_dropped"], report["units_drafted"]), (1, 1, 0))
        units = self.record("coverage/reviews/alerts.json")["review"]["units"]
        self.assertEqual([(u["id"], u["status"]) for u in units], [("content/1", "reviewed")])
        images = self.record("coverage/image-reviews/alerts.json")["media"]
        self.assertNotIn("removed.png", images)
        self.assertEqual(images["kept.png"]["reviewed_occurrence_ids"], ["content/2"])

    def test_remap_reopens_moved_reviews_when_the_guide_changed(self):
        self.guide.write_text(self.guide.read_text() + "New guide text.\n")
        report = snapshot.remap(self.root, "alerts")
        self.assertEqual(report["units_drafted"], 1)
        moved = self.record("coverage/reviews/alerts.json")["review"]["units"][0]
        self.assertEqual(moved["status"], "draft")
        self.assertTrue(moved["evidence"].startswith(snapshot.TODO))

    def test_scaffold_drafts_new_content_with_only_existing_anchors(self):
        snapshot.remap(self.root, "alerts")
        report = snapshot.scaffold(self.root, "alerts", fetch=False)
        self.assertEqual((report["units_added"], report["media_added"]), (1, ["new.png"]))
        added = self.record("coverage/reviews/alerts.json")["review"]["units"][-1]
        self.assertEqual((added["id"], added["status"]), ("content/0", "draft"))
        self.assertNotIn("destination_anchor", added, "the guide has no #overview anchor")
        new = self.record("coverage/image-reviews/alerts.json")["media"]["new.png"]
        self.assertEqual((new["status"], new["reviewed_occurrence_ids"]), ("draft", ["content/3"]))
        self.assertTrue(new["evidence"].startswith(snapshot.TODO))


if __name__ == "__main__":
    unittest.main()
