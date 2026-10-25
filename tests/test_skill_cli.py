"""The operational release CLI must fail closed on absent evidence."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class OperationalCLITests(unittest.TestCase):
    def test_missing_inventory_is_a_reported_release_failure(self):
        script = Path(__file__).resolve().parents[1] / "scripts/hig.py"
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, str(script), "check-skills", "--root", directory],
                text=True, capture_output=True, check=False,
            )
        self.assertEqual(result.returncode, 1, result.stderr)
        report = json.loads(result.stdout)
        self.assertTrue(report["errors"])
        self.assertEqual(report["behavior_passed"], 0)


if __name__ == "__main__":
    unittest.main()
