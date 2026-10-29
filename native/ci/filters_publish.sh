#!/bin/bash
# Đẩy kết quả bộ lọc tính sẵn/theo yêu cầu lên branch `filters` (cộng dồn, không ghi đè lịch sử).
# Giữ thư mục của commit dữ liệu hiện tại + 1 commit trước, xoá cũ hơn.
#   TOKEN=... REPO=owner/name bash native/ci/filters_publish.sh <thư mục _filters> "<message>"
set -euo pipefail
SRC=$(cd "$1" && pwd); MSG="$2"
URL="https://x-access-token:${TOKEN}@github.com/${REPO}.git"
W=$(mktemp -d)
if git clone -q --depth 1 -b filters "$URL" "$W" 2>/dev/null; then :; else
  git init -q -b filters "$W"; git -C "$W" remote add origin "$URL"; fi
cd "$W"
git config user.name  "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
for attempt in 1 2 3 4 5; do
  cp -R "$SRC"/. ./
  CUR=$(ls -d "$SRC"/*/ 2>/dev/null | head -1 | xargs -n1 basename || true)
  if [ -n "$CUR" ]; then
    PREV=$(cat last.txt 2>/dev/null || true)
    if [ "$PREV" != "$CUR" ]; then
      for d in */; do d=${d%/}; [ "$d" = "$CUR" ] || [ "$d" = "$PREV" ] || rm -rf "$d"; done
      echo "$CUR" > last.txt
    fi
  fi
  git add -A
  git diff --cached --quiet && { echo "Không có gì mới"; exit 0; }
  git commit -q -m "$MSG"
  if git push -q origin filters; then echo "Đã lưu: $(git show --stat --oneline HEAD | tail -1)"; exit 0; fi
  # lượt khác vừa đẩy → lấy về rồi thử lại
  git fetch -q --depth 1 origin filters && git reset -q --hard origin/filters
  sleep $((attempt * 3))
done
echo "Không đẩy được sau 5 lần" >&2; exit 1
