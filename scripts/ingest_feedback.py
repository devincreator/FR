#!/usr/bin/env python3
"""Append safe, structured research lessons from one conversation to FR knowledge files.

Usage:
  python scripts/ingest_feedback.py --file /tmp/feedback.json --repo .

No network access or language-model calls. The calling assistant must perform
reasoning and privacy screening before preparing feedback.json.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path

ALLOWED_CATEGORIES = {
    "source", "scope", "method", "model", "valuation", "writing", "delivery",
    "compliance", "other",
}
ACCEPTED_MIN_CONFIDENCE = 0.80
BEGIN = "<!-- BEGIN AUTO-ACCEPTED RULES -->"
END = "<!-- END AUTO-ACCEPTED RULES -->"


def require_text(data: dict, field: str, maximum: int) -> str:
    value = data.get(field)
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise ValueError(f"{field} must be nonempty text <= {maximum} chars")
    value = value.strip()
    if "\n" in value or "\r" in value:
        raise ValueError(f"{field} must be a single line")
    if re.search(r"<\s*/?(?:script|iframe|style|img|svg)\b", value, re.I):
        raise ValueError(f"{field} contains unsupported HTML")
    return value


def validate(data: dict) -> dict:
    if not isinstance(data, dict):
        raise ValueError("Feedback must be one JSON object")
    result = {
        field: require_text(data, field, limit)
        for field, limit in {
            "id": 100, "date": 10, "category": 30, "context": 200,
            "observed_problem": 320, "root_cause": 220,
            "new_rule": 450, "scope": 160, "evidence_type": 50,
        }.items()
    }
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{3,99}", result["id"]):
        raise ValueError("id must use letters, digits, underscores or hyphens")
    try:
        dt.date.fromisoformat(result["date"])
    except ValueError as exc:
        raise ValueError("date must be YYYY-MM-DD") from exc
    if result["category"] not in ALLOWED_CATEGORIES:
        raise ValueError("Unsupported category")
    if not isinstance(data.get("safe_to_upload"), bool) or not data["safe_to_upload"]:
        raise ValueError("safe_to_upload must be explicitly true")
    if not isinstance(data.get("user_confirmed"), bool):
        raise ValueError("user_confirmed must be boolean")
    result["user_confirmed"] = data["user_confirmed"]
    confidence = data.get("confidence")
    if isinstance(confidence, bool) or not isinstance(confidence, (float, int)) or not 0 <= confidence <= 1:
        raise ValueError("confidence must be number in [0,1]")
    result["confidence"] = round(float(confidence), 3)
    for field in ("evidence_refs", "affected_files"):
        val = data.get(field)
        if not isinstance(val, list) or len(val) > 10 or any(not isinstance(x, str) or len(x) > 160 or "\n" in x for x in val):
            raise ValueError(f"{field} must be a list of short strings")
        result[field] = val
    result["safe_to_upload"] = True
    return result


def ingest(data: dict, repo: Path) -> str:
    data = validate(data)
    history = repo / "memory" / "lessons.jsonl"
    accepted = repo / "memory" / "accepted_rules.md"
    if not history.exists() or not accepted.exists():
        raise ValueError("Must run inside a valid FR checkout")
    history_lines = [line for line in history.read_text(encoding="utf-8").splitlines() if line.strip()]
    if any(json.loads(line).get("id") == data["id"] for line in history_lines):
        return "duplicate: no changes"
    existing = accepted.read_text(encoding="utf-8")
    if BEGIN not in existing or END not in existing:
        raise ValueError("Accepted rule sentinels missing")
    # Keep all feedback for audit; only explicitly confirmed, high-confidence rules
    # enter the active rule set, subject to a GitHub PR review.
    history.write_text(
        "\n".join([*history_lines, json.dumps(data, ensure_ascii=False, sort_keys=True)]) + "\n",
        encoding="utf-8",
    )
    active = data["user_confirmed"] and data["confidence"] >= ACCEPTED_MIN_CONFIDENCE
    if active:
        rule = (f"- **[{data['id']}]** （{data['date']}；适用：{data['scope']}；"
                f"类别：{data['category']}）{data['new_rule']} "
                f"*缘由：{data['root_cause']}；依据类别：{data['evidence_type']}。*\n")
        existing = existing.replace(END, rule + END)
        accepted.write_text(existing, encoding="utf-8")
    return "accepted-rule candidate added" if active else "observation recorded; rule pending confirmation"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True, type=Path)
    ap.add_argument("--repo", type=Path, default=Path("."))
    args = ap.parse_args()
    data = json.loads(args.file.read_text(encoding="utf-8"))
    print(ingest(data, args.repo))


if __name__ == "__main__":
    main()
