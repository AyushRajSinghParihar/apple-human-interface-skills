"""Published claims, versions and context budgets must match the shipped package."""
import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "skills/apple-hig"

# Upper limits in bytes. They stop silent growth of the files that an agent
# reads on every route. Lower them when a release makes the files smaller.
ROOT_SKILL_BUDGET = 8_500
TOPIC_INDEX_BUDGET = 68_000
FAMILY_SKILL_BUDGET = 4_000
TOPIC_SKILL_BUDGET = 8_000


def frontmatter(path):
    match = re.match(r"---\n(.*?)\n---\n", path.read_text(), re.S)
    if not match:
        return {}
    import yaml
    return yaml.safe_load(match.group(1)) or {}


class PackageContractTests(unittest.TestCase):
    def test_every_declared_version_is_the_same(self):
        versions = {}
        cursor = json.loads((ROOT / ".cursor-plugin/plugin.json").read_text())
        versions[".cursor-plugin/plugin.json"] = cursor.get("version")
        marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
        for plugin in marketplace.get("plugins", []):
            if plugin.get("name") == "apple-hig" and "version" in plugin:
                versions[".claude-plugin/marketplace.json"] = plugin["version"]
        claude_plugin = ROOT / ".claude-plugin/plugin.json"
        if claude_plugin.is_file():
            versions[".claude-plugin/plugin.json"] = json.loads(claude_plugin.read_text()).get("version")
        metadata = frontmatter(PACKAGE / "SKILL.md").get("metadata", {})
        if "version" in metadata:
            versions["skills/apple-hig/SKILL.md"] = str(metadata["version"])
        released = re.search(r"^## \[(\d+\.\d+\.\d+)\]", (ROOT / "CHANGELOG.md").read_text(), re.M)
        self.assertIsNotNone(released, "CHANGELOG.md needs a released version heading")
        versions["CHANGELOG.md"] = released.group(1)
        self.assertGreaterEqual(len(versions), 3)
        self.assertEqual(len(set(versions.values())), 1, versions)

    def test_readme_counts_match_the_source_manifest(self):
        manifest = json.loads((ROOT / "coverage/manifest.json").read_text())
        pages = manifest["pages"]
        articles = [page for page in pages if page.get("type") == "article"]
        families = {page["module"] for page in articles}
        readme = (ROOT / "README.md").read_text()
        self.assertIn(f"{len(articles)} topics across {len(families)} areas", readme)
        self.assertIn(f"{len(articles)} English HIG articles", readme)
        self.assertIn(f"{len(pages)} routes", readme)
        topics = list(PACKAGE.glob("subskills/*/.topics/*/SKILL.md"))
        self.assertEqual(len(topics), len(articles))
        self.assertIsNone(re.search(r"\*\*\d+ automated tests\*\*", readme),
                          "Do not state a fixed test count; it goes stale with each new test")

    def test_files_on_every_route_stay_within_their_budget(self):
        self.assertLessEqual(len((PACKAGE / "SKILL.md").read_bytes()), ROOT_SKILL_BUDGET)
        self.assertLessEqual(len((PACKAGE / "references/topic-index.md").read_bytes()), TOPIC_INDEX_BUDGET)
        for path in PACKAGE.glob("subskills/*/SKILL.md"):
            with self.subTest(family=path.parent.name):
                self.assertLessEqual(len(path.read_bytes()), FAMILY_SKILL_BUDGET)
        for path in PACKAGE.glob("subskills/*/.topics/*/SKILL.md"):
            with self.subTest(topic=path.parent.name):
                self.assertLessEqual(len(path.read_bytes()), TOPIC_SKILL_BUDGET)


if __name__ == "__main__":
    unittest.main()
