#!/usr/bin/env bash
set -euo pipefail

# Simple repository secret scanner for common Discord tokens and AWS keys
echo "Scanning repository for suspicious tokens..."

PATTERNS=(
  "MTQ[0-9A-Za-z_.-]\{20,}\" # partial Discord token (base64-like)
  "aws_secret_access_key"      # AWS secret key indicator
)

FOUND=0

# Search working tree
for p in "MTQ[0-9A-Za-z_.-]\{20,\}"; do
  if grep -R --line-number -E "$p" . --exclude-dir=.git --binary-files=without-match; then
    FOUND=1
  fi
done

if [ "$FOUND" -eq 1 ]; then
  echo "Potential secrets found. Please inspect before committing." >&2
  exit 2
fi

echo "No obvious secrets found in working tree."
exit 0
