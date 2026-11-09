#!/usr/bin/env bash
# Run the Claude Code eval suite in quality/evals against a temporary copy of
# the apple-hig plugin. The eval cases stay out of the installed skill folder.
#
# Usage: scripts/claude-eval.sh LABEL [claude plugin eval options...]
# Example:
#   scripts/claude-eval.sh v1.0-before --tag task --ablation with-without \
#     --runs 1 --model sonnet --max-cost-usd 20
#
# Results go to quality/results/LABEL/. The HTML report stays local.
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
label="${1:?usage: scripts/claude-eval.sh LABEL [claude plugin eval options...]}"
shift
case "$label" in
  */* | .* | "") echo "claude-eval: LABEL must be a plain name" >&2; exit 2 ;;
esac

work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

# cp -R keeps the hidden .topics and .claude-plugin folders.
cp -R "$root/skills/apple-hig" "$work/apple-hig"
cp -R "$root/quality/evals" "$work/apple-hig/evals"

out="$root/quality/results/$label"
mkdir -p "$out"
claude plugin eval "$work/apple-hig" --trust-plugin --no-publish --output-dir "$out" "$@"
