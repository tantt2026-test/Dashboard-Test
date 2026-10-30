#!/bin/bash
# 1 máy trong nhóm chạy song song của lượt 1:  bash native/ci/shard.sh <i> <n>
# Kết quả ở _shard/ (workflow tải lên làm artifact; job publish ghép bằng merge_shards.py).
set -euo pipefail
git clone -q --depth 1 -b reports "https://github.com/${REPO}.git" _prev || mkdir -p _prev
python native/pipeline/export_reports.py --app App.py --out _shard --kpi --kpi-mode default \
  --prev _prev --workers 4 --shard "$1/$2"
