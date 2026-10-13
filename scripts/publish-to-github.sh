#!/usr/bin/env bash
# Run locally from extracted FR directory. Does not overwrite existing repositories.
set -euo pipefail
cd "$(dirname "$0")/.."
command -v gh >/dev/null || { echo "Install GitHub CLI (gh) and authenticate with gh auth login"; exit 1; }
command -v git >/dev/null || { echo "git is required"; exit 1; }
user="$(gh api user --jq .login)"
if gh repo view "${user}/FR" >/dev/null 2>&1; then
  echo "Repository ${user}/FR already exists. Not changing it."
  exit 2
fi
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git init -b main
fi
git add -A
if ! git diff --cached --quiet; then
  git commit -m "feat: initialize FR financial research skill"
fi
gh repo create FR --private --source=. --remote=origin --push
# Label must exist before feedback issues can trigger the labeled-event workflow.
gh label create fr-feedback --repo "${user}/FR" --color 0E8A16 --description "Structured FR learning feedback" || true
echo "Created private repository: https://github.com/${user}/FR"
