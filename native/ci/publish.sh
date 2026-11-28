#!/bin/bash
# Đẩy thư mục JSON lên branch `reports` (ghi đè, không giữ lịch sử để repo không phình).
#   TOKEN=... REPO=owner/name bash native/ci/publish.sh <thư mục> "<message>"
# Nhanh: không chép thư mục; lấy trước cây thư mục của bản đang có (không tải file, --filter=blob:none)
# → git push chỉ gửi file mới/đổi thay vì gửi lại cả branch (trước đây ~12 GB mỗi lần).
set -euo pipefail
DIR=$(cd "$1" && pwd)
MSG="$2"
URL=${PUBLISH_URL:-"https://x-access-token:${TOKEN}@github.com/${REPO}.git"}
export GIT_DIR
GIT_DIR=$(mktemp -d)/g.git
git init -q -b reports
git config user.name  "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
git config core.bigFileThreshold 16m
if git fetch -q --depth 1 --filter=blob:none "$URL" "+refs/heads/reports:refs/remotes/origin/reports" 2>/dev/null; then
  echo "Đã lấy cây bản trước $(git rev-parse --short refs/remotes/origin/reports) — chỉ gửi phần thay đổi"
fi
git --work-tree="$DIR" add -A
TREE=$(git write-tree)
C=$(git commit-tree "$TREE" -m "$MSG")
git push -q -f "$URL" "$C:refs/heads/reports"
echo "Đã publish: $(du -sh "$DIR" | cut -f1)"
rm -rf "$(dirname "$GIT_DIR")"
