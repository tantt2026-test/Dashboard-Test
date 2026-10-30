#!/bin/bash
# Build app Mac có máy tính tại chỗ: Python 3.12 + thư viện (như Streamlit Cloud) + pipeline
# được chép vào "KPI Dashboard.app/Contents/Resources/py".
#   bash native/macpy/build_mac.sh            (chạy ở gốc repo, cần ~/.kpi_gh_token)
# Python gốc: bản standalone (python-build-standalone, relocatable) — đặt PYSRC nếu ở chỗ khác.
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
PYSRC=${PYSRC:-$(ls -d ~/.local/share/uv/python/cpython-3.12.*-macos-aarch64-none | sort -V | tail -1)}
STAGE="$ROOT/native/app/build/macpy"
if [ ! -f "$STAGE/.ok" ] || [ "$ROOT/requirements.txt" -nt "$STAGE/.ok" ]; then
  rm -rf "$STAGE"; mkdir -p "$STAGE"
  cp -R "$PYSRC" "$STAGE/python"
  rm -f "$STAGE"/python/lib/python3.12/EXTERNALLY-MANAGED   # bản chép riêng cho app
  # streamlit không cần (pipeline giả lập) → cài thư viện còn lại, có phụ thuộc
  grep -v -i '^streamlit' "$ROOT/requirements.txt" > "$STAGE/req.txt"
  "$STAGE/python/bin/python3" -m pip install -q --no-cache-dir --disable-pip-version-check \
    -r "$STAGE/req.txt" beautifulsoup4
  "$STAGE/python/bin/python3" -m pip uninstall -y -q streamlit 2>/dev/null || true
  # bớt dung lượng
  P="$STAGE/python/lib/python3.12"
  rm -rf "$P"/test "$P"/idlelib "$P"/tkinter "$P"/turtledemo "$P"/ensurepip "$STAGE/python/share" \
         "$STAGE/python/include" "$P"/site-packages/pip* "$STAGE/python/lib/tcl"* "$STAGE/python/lib/tk"* \
         "$STAGE/python/lib/itcl"* "$STAGE/python/lib/thread"*
  find "$STAGE/python" -name '__pycache__' -prune -exec rm -rf {} +
  find "$STAGE/python" -path '*/tests' -prune -exec rm -rf {} +
  touch "$STAGE/.ok"
fi
cd "$ROOT/native/app"
flutter build macos --release --dart-define=GH_TOKEN="$(tr -d '[:space:]' < ~/.kpi_gh_token)"
APP="build/macos/Build/Products/Release/KPI Dashboard.app"
R="$APP/Contents/Resources/py"
rm -rf "$R"; mkdir -p "$R/engine"
cp -R "$STAGE/python" "$R/python"
cp "$ROOT"/native/pipeline/{local_engine,headless,report_doc,export_kpi,filters_probe,run_request}.py "$R/engine/"
# thêm file vào Resources → ký lại (ad-hoc), giữ nguyên entitlements của app (sandbox + mạng)
codesign --force -s - --entitlements "$ROOT/native/app/macos/Runner/Release.entitlements" "$APP"
codesign --verify --strict "$APP"
mkdir -p "$ROOT/native/dist"; rm -f "$ROOT/native/dist/KPIDashboard-mac.zip"
(cd "$(dirname "$APP")" && ditto -c -k --keepParent "KPI Dashboard.app" "$ROOT/native/dist/KPIDashboard-mac.zip")
du -sh "$APP" "$ROOT/native/dist/KPIDashboard-mac.zip"
