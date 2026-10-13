#!/usr/bin/env bash
# POST-SESSION helper: submit privacy-screened JSON then add label as a separate event.
set -euo pipefail
if [[ $# -ne 1 ]]; then echo "Usage: $0 feedback.json"; exit 2; fi
cd "$(dirname "$0")/.."
file="$(realpath "$1")"
python scripts/parse_issue_feedback.py --issue-body "$file" --output /tmp/fr-submit-preview.json
python - "$file" <<'PY'
import json,sys
from pathlib import Path
sys.path.insert(0,'scripts')
from ingest_feedback import validate
validate(json.loads(Path(sys.argv[1]).read_text(encoding='utf-8')))
print('Feedback schema and upload flag validated')
PY
remote="$(gh repo view --json nameWithOwner --jq '.nameWithOwner')"
url="$(gh issue create --repo "$remote" --title "[FR feedback] $(date +%F)" --body-file "$file")"
number="${url##*/}"
gh issue edit "$number" --repo "$remote" --add-label fr-feedback
echo "Created feedback issue: $url"
