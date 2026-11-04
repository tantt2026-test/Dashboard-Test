#!/bin/bash
# 1 máy trong nhóm chạy song song của lượt 1:  TEAM=tan|vy|all bash native/ci/shard.sh <i> <n>
# 3 báo cáo nặng nhất chỉ xuất số (máy probe.sh dò ô lọc riêng). Kết quả ở _shard/
# (workflow tải lên làm artifact; job publish ghép bằng merge_shards.py).
set -euo pipefail
source native/ci/team_env.sh
git clone -q --depth 1 -b reports "https://github.com/${REPO}.git" _prev || mkdir -p _prev
PREV=_prev/$PREFIX; mkdir -p "$PREV"
# PROBE_JOBS=1: workflow có 3 máy dò riêng (build-reports.yml mới) → bỏ dò 3 báo cáo nặng ở đây
HEAVY=$([ "${PROBE_JOBS:-}" = 1 ] && python native/ci/heavy.py "$PREV" || true)
python native/pipeline/export_reports.py --app "$ROOT/App.py" --out _shard --kpi --kpi-mode default \
  --prev "$PREV" --workers 4 --shard "$1/$2" --skip-probe "$HEAVY"
