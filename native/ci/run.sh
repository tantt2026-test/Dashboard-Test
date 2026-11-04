#!/bin/bash
# Toàn bộ các bước của GitHub Action (workflow chỉ gọi file này → sửa quy trình không cần
# dán lại workflow). Chạy ở thư mục gốc repo. Cần: python + requirements, flutter, TOKEN, REPO.
#
# Nhiều Sale Sup (team_env.sh): tan → gốc branch reports, vy → reports/t/vy, all → reports/t/all.
# Artifact của workflow: _shards/shard-<team>-<i>, _probes/probe-<team>-<k>.
set -euo pipefail
P=native/pipeline
TEAMS=${TEAMS:-"tan vy all"}

# STAGE=first: chỉ ghép + publish lượt 1; STAGE=probes: ghép dò ô lọc các báo cáo nặng + publish lại;
# STAGE=rest: đối chiếu + lượt 2, 3 (workflow cài Flutter trước bước này).
# Không đặt STAGE: chạy hết (workflow cũ, chỉ team tan).
STAGE=${STAGE:-all}

prefix_of() { [ "$1" = tan ] && echo '' || echo "t/$1"; }

if [ "$STAGE" = all ] || [ "$STAGE" = first ]; then
echo "::group::Lấy bản reports trước"
git clone -q --depth 1 -b reports "https://github.com/${REPO}.git" _prev || mkdir -p _prev
echo "::endgroup::"

if [ -d _shards ]; then
  # tan trước: ghép vào gốc _reports (chép cả t/ cũ) → vy, all ghi đè thư mục con của mình
  for team in $TEAMS; do
    ls -d _shards/shard-"$team"-* >/dev/null 2>&1 || ls -d _shards/shard-[0-9]* >/dev/null 2>&1 || continue
    echo "::group::Lượt 1 ($team): ghép kết quả các máy chạy song song"
    rm -rf "_sh/$team" && mkdir -p "_sh/$team"
    mv _shards/shard-"$team"-* "_sh/$team/" 2>/dev/null || true
    [ "$team" = tan ] && mv _shards/shard-[0-9]* "_sh/$team/" 2>/dev/null || true  # workflow cũ
    PFX=$(prefix_of "$team")
    mkdir -p "_prev/$PFX"
    python $P/merge_shards.py --prev "_prev/$PFX" --shards "_sh/$team" --out "_reports/$PFX"
    echo "::endgroup::"
  done
else
  echo "::group::Lượt 1: Turnover + báo cáo/tab ngày mặc định (có đo ô lọc)"
  python $P/export_reports.py --app App.py --out _reports --kpi --kpi-mode default --prev _prev --workers 4
  echo "::endgroup::"
fi

# Đưa data mới lên cho app NGAY, đối chiếu chạy sau: lệch thì job báo đỏ (để sửa) nhưng không
# giữ data cũ lại cả buổi
bash native/ci/publish.sh _reports "Lượt 1 từ ${GITHUB_SHA::7}"
fi
[ "$STAGE" = first ] && exit 0

# Kết quả dò ô lọc của các báo cáo nặng (máy probe.sh chạy song song) → ghép + publish lại
if [ -d _probes ] && [ "$STAGE" != rest ]; then
  echo "::group::Ghép dò ô lọc các báo cáo nặng"
  for team in $TEAMS; do
    rm -rf "_pr/$team" && mkdir -p "_pr/$team"
    mv _probes/probe-"$team"-* "_pr/$team/" 2>/dev/null || true
    [ "$team" = tan ] && mv _probes/probe-[0-9]* "_pr/$team/" 2>/dev/null || true  # workflow cũ
    python $P/merge_probes.py --probes "_pr/$team" --out "_reports/$(prefix_of "$team")"
  done
  echo "::endgroup::"
  bash native/ci/publish.sh _reports "Lượt 1 + bộ lọc từ ${GITHUB_SHA::7}"
fi
[ "$STAGE" = probes ] && exit 0

echo "::group::Đối chiếu số Turnover + bộ lọc (App vs App.py, team Tân)"
PARITY=0
(cd native/app && flutter pub get >/dev/null)
python $P/parity_check.py --app App.py --json _reports --dart-app native/app --combos 5 || PARITY=1
python $P/parity_filters.py --app App.py --json _reports --dart-app native/app --cases 2 || PARITY=1
echo "::endgroup::"

for team in $TEAMS; do
  [ -d "_reports/$(prefix_of "$team")/kpi" ] || continue
  echo "::group::Lượt 2 ($team): các ngày cũ + tháng trước"
  ( export TEAM="$team"; source native/ci/team_env.sh
    python $P/export_reports.py --app "$ROOT/App.py" --out "_reports/$PREFIX" --kpi --kpi-mode history \
      --prev "_reports/$PREFIX" --workers 4 )
  echo "::endgroup::"
  bash native/ci/publish.sh _reports "Đầy đủ ($team) từ ${GITHUB_SHA::7}"
done

echo "::group::Lượt 3: tính sẵn tổ hợp bộ lọc kiểu tính lại — team Tân (tối đa 45 phút)"
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
