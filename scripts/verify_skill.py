#!/usr/bin/env python3
"""Structural validation of FR entrypoints and templates."""
from pathlib import Path
import json
import re
import sys

root = Path(__file__).resolve().parent.parent
entry = (root / "SKILL.md").read_text(encoding="utf-8")
assert entry.startswith("---\n")
assert re.search(r"^name:\s*financial-research$", entry, re.MULTILINE)
for name in re.findall(r"`(references/[\w.-]+\.md|memory/[\w.-]+\.md)`", entry):
    assert (root / name).is_file(), f"Missing referenced file: {name}"
for p in [root / "templates" / "feedback.json", root / "memory" / "lessons.jsonl"]:
    assert p.exists()
feedback = json.loads((root / "templates" / "feedback.json").read_text(encoding="utf-8"))
assert feedback["safe_to_upload"] is True
print("Skill structure verified")
