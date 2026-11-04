#!/bin/bash
# Chuẩn bị bộ data theo Sale Sup (source file này):  TEAM=tan|vy|all [DSC=<commit Vyntt>] source native/ci/team_env.sh
# Đặt biến: ROOT (thư mục có App.py + data/), PREFIX (thư mục con trên branch reports), TEAM_DSC.
#   tan → repo này (data/)                 → reports gốc (app cũ vẫn đọc như trước)
#   vy  → data/ của Tantt2026/Vyntt_Dashboard → reports/t/vy
#   all → data 2 team ghép (team_data.py)    → reports/t/all
TEAM=${TEAM:-tan}
VY_REPO=${VY_REPO:-Tantt2026/Vyntt_Dashboard}
case "$TEAM" in
  tan) ROOT=.; PREFIX=''; TEAM_DSC='' ;;
  vy|all)
    if [ ! -d _vysrc/data ]; then
      rm -rf _vysrc && mkdir _vysrc && git -C _vysrc init -q
      git -C _vysrc fetch -q --depth 1 "https://github.com/${VY_REPO}.git" "${DSC:-HEAD}"
      git -C _vysrc checkout -q FETCH_HEAD
    fi
    TEAM_DSC=$(git -C _vysrc rev-parse HEAD)
    ROOT=_team/$TEAM
    if [ ! -f "$ROOT/App.py" ]; then
      python native/pipeline/team_data.py prepare "$TEAM" "$ROOT" --app App.py --tan data --vy _vysrc/data
    fi
    PREFIX="t/$TEAM"
    ;;
  *) echo "TEAM không hợp lệ: $TEAM" >&2; exit 2 ;;
esac
export TEAM ROOT PREFIX TEAM_DSC
