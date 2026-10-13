#!/usr/bin/env python3
"""Extract a single feedback JSON object from Issue body or fenced JSON block."""
import argparse
import json
import re
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("--issue-body", type=Path, required=True)
p.add_argument("--output", type=Path, required=True)
a = p.parse_args()
body = a.issue_body.read_text(encoding="utf-8")
m = re.search(r"```(?:json)?\s*\n(\{.*?\})\s*```", body, re.S | re.I)
raw = m.group(1) if m else body.strip()
data = json.loads(raw)
if not isinstance(data, dict):
    raise ValueError("Expected exactly one JSON object")
a.output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
