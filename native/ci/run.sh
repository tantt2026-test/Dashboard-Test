#!/bin/bash
# Toàn bộ các bước của GitHub Action (workflow chỉ gọi file này → sửa quy trình không cần
# dán lại workflow). Chạy ở thư mục gốc repo. Cần: python + requirements, flutter, TOKEN, REPO.
set -euo pipefail
P=native/pipeline

echo "::group::Lấy bản reports trước"
git clone -q --depth 1 -b reports "https://github.com/${REPO}.git" _prev || mkdir -p _prev
echo "::endgroup::"

echo "::group::Lượt 1: Turnover + báo cáo/tab ngày mặc định (có đo ô lọc)"
python $P/export_reports.py --app App.py --out _reports --kpi --kpi-mode default --prev _prev --workers 4
echo "::endgroup::"

echo "::group::Đối chiếu số Turnover + bộ lọc (App vs App.py)"
(cd native/app && flutter pub get >/dev/null)
python $P/parity_check.py --app App.py --json _reports --dart-app native/app --combos 5
python $P/parity_filters.py --app App.py --json _reports --dart-app native/app --cases 2
echo "::endgroup::"

bash native/ci/publish.sh _reports "Lượt 1 từ ${GITHUB_SHA::7}"

echo "::group::Lượt 2: các ngày cũ + tháng trước"
python $P/export_reports.py --app App.py --out _reports --kpi --kpi-mode history --prev _reports --workers 4
echo "::endgroup::"

bash native/ci/publish.sh _reports "Đầy đủ từ ${GITHUB_SHA::7}"
