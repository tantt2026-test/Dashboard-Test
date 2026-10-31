#!/bin/bash
# Máy dò ô lọc cho 1 báo cáo nặng (chạy song song với lượt 1):  bash native/ci/probe.sh <k>
# Kết quả ở _probe/ (+ _probe/probe_code.txt); run.sh (STAGE=rest) ghép vào bản đã publish.
set -euo pipefail
git clone -q --depth 1 -b reports "https://github.com/${REPO}.git" _prev || mkdir -p _prev
CODE=$(python native/ci/heavy.py _prev "$1")
echo "Dò ô lọc: $CODE"
python native/pipeline/export_reports.py --app App.py --out _probe --kpi --kpi-mode default \
  --prev _prev --workers 1 --only-probe "$CODE"
echo "$CODE" > _probe/probe_code.txt
