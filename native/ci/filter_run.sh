#!/bin/bash
# GitHub Action "filter-run": app nhờ tính 1 tổ hợp bộ lọc chưa có sẵn.
#   REQ='<json>' TOKEN=... REPO=... bash native/ci/filter_run.sh
# App.py + data theo commit app đang xem (đã checkout); script native/ lấy bản mới nhất trên main.
set -euo pipefail
git fetch -q --depth 1 origin main && git checkout -q FETCH_HEAD -- native || true
python native/pipeline/precompute_filters.py --app App.py --req "$REQ" --out _filters
bash native/ci/filters_publish.sh _filters "Tính theo yêu cầu"
