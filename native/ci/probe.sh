#!/bin/bash
# Máy dò ô lọc cho 1 báo cáo nặng (chạy song song với lượt 1):  TEAM=… bash native/ci/probe.sh <k>
# Kết quả ở _probe/ (+ _probe/probe_code.txt); run.sh (STAGE=probes) ghép vào bản đã publish.
set -euo pipefail
source native/ci/team_env.sh
git clone -q --depth 1 -b reports "https://github.com/${REPO}.git" _prev || mkdir -p _prev
PREV=_prev/$PREFIX; mkdir -p "$PREV"
CODE=$(python native/ci/heavy.py "$PREV" "$1")
echo "Dò ô lọc ($TEAM): $CODE"
python native/pipeline/export_reports.py --app "$ROOT/App.py" --out _probe --kpi --kpi-mode default \
  --prev "$PREV" --workers 1 --only-probe "$CODE"
echo "$CODE" > _probe/probe_code.txt
