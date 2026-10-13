import json
import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from ingest_feedback import ingest, validate

ROOT = Path(__file__).resolve().parent.parent


class FeedbackTests(unittest.TestCase):
    def fixture(self):
        return json.loads((ROOT / "templates" / "feedback.json").read_text(encoding="utf-8"))

    def test_reject_private(self):
        data = self.fixture()
        data["safe_to_upload"] = False
        with self.assertRaises(ValueError):
            validate(data)

    def test_ingest_dedup(self):
        with tempfile.TemporaryDirectory() as d:
            r = Path(d)
            (r / "memory").mkdir()
            (r / "memory" / "lessons.jsonl").write_text("", encoding="utf-8")
            (r / "memory" / "accepted_rules.md").write_text(
                "# Accepted\n<!-- BEGIN AUTO-ACCEPTED RULES -->\n<!-- END AUTO-ACCEPTED RULES -->\n",
                encoding="utf-8",
            )
            first = ingest(self.fixture(), r)
            self.assertIn("candidate", first)
            self.assertEqual(ingest(self.fixture(), r), "duplicate: no changes")
            text = (r / "memory" / "accepted_rules.md").read_text(encoding="utf-8")
            self.assertEqual(text.count("example-20261012-a"), 1)
            self.assertEqual(len((r / "memory" / "lessons.jsonl").read_text().splitlines()), 1)

    def test_low_confidence_logs_only(self):
        with tempfile.TemporaryDirectory() as d:
            r = Path(d)
            (r / "memory").mkdir()
            (r / "memory" / "lessons.jsonl").write_text("", encoding="utf-8")
            (r / "memory" / "accepted_rules.md").write_text(
                "<!-- BEGIN AUTO-ACCEPTED RULES -->\n<!-- END AUTO-ACCEPTED RULES -->\n",
                encoding="utf-8",
            )
            data = self.fixture()
            data["confidence"] = 0.5
            self.assertIn("pending", ingest(data, r))
            self.assertNotIn(data["id"], (r / "memory" / "accepted_rules.md").read_text())


if __name__ == "__main__":
    unittest.main()
