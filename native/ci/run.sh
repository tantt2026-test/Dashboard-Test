#!/bin/bash
# Toàn bộ các bước của GitHub Action (workflow chỉ gọi file này → sửa quy trình không cần
# dán lại workflow). Chạy ở thư mục gốc repo. Cần: python + requirements, flutter, TOKEN, REPO.
set -euo pipefail
P=native/pipeline

echo "::group::Lấy bản reports trước"
git clone -q --depth 1 -b reports "https://github.com/${REPO}.git" _prev || mkdir -p _prev
echo "::endgroup::"

if [ -d _shards ]; then
  echo "::group::Lượt 1: ghép kết quả các máy chạy song song"
  python $P/merge_shards.py --prev _prev --shards _shards --out _reports
else
  echo "::group::Lượt 1: Turnover + báo cáo/tab ngày mặc định (có đo ô lọc)"
  python $P/export_reports.py --app App.py --out _reports --kpi --kpi-mode default --prev _prev --workers 4
fi
echo "::endgroup::"

# Đưa data mới lên cho app NGAY, đối chiếu chạy sau: lệch thì job báo đỏ (để sửa) nhưng không
# giữ data cũ lại cả buổi
bash native/ci/publish.sh _reports "Lượt 1 từ ${GITHUB_SHA::7}"

echo "::group::Đối chiếu số Turnover + bộ lọc (App vs App.py)"
PARITY=0
(cd native/app && flutter pub get >/dev/null)
python $P/parity_check.py --app App.py --json _reports --dart-app native/app --combos 5 || PARITY=1
python $P/parity_filters.py --app App.py --json _reports --dart-app native/app --cases 2 || PARITY=1
echo "::endgroup::"

echo "::group::Lượt 2: các ngày cũ + tháng trước"
python $P/export_reports.py --app App.py --out _reports --kpi --kpi-mode history --prev _reports --workers 4
echo "::endgroup::"

bash native/ci/publish.sh _reports "Đầy đủ từ ${GITHUB_SHA::7}"

echo "::group::Lượt 3: tính sẵn tổ hợp bộ lọc kiểu tính lại (tối đa 45 phút)"
# 3 đợt × 15 phút, mỗi đợt lưu ngay (bị huỷ giữa chừng vẫn giữ phần đã tính)
for round in 1 2 3; do
  python $P/precompute_filters.py --app App.py --reports _reports --out _filters --budget 900 || true
  bash native/ci/filters_publish.sh _filters "Tính sẵn từ ${GITHUB_SHA::7} (đợt $round)" || true
done
echo "::endgroup::"

if [ "$PARITY" != 0 ]; then
  echo "::error::Đối chiếu app vs App.py có chỗ lệch (xem nhóm Đối chiếu ở trên) — data vẫn đã publish"
  exit 1
fi
