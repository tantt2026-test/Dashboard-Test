#!/bin/bash
# Đẩy thư mục JSON lên branch `reports` (ghi đè, không giữ lịch sử để repo không phình).
#   TOKEN=... REPO=owner/name bash native/ci/publish.sh <thư mục> "<message>"
set -euo pipefail
DIR="$1"
MSG="$2"
TMP=$(mktemp -d)
cp -R "$DIR"/. "$TMP"/
cd "$TMP"
rm -rf .git
git init -q -b reports
git config user.name  "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
git add -A
git commit -q -m "$MSG"
git push -q -f "https://x-access-token:${TOKEN}@github.com/${REPO}.git" reports
echo "Đã publish: $(du -sh . | cut -f1)"
