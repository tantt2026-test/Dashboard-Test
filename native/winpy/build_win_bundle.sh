#!/bin/bash
# Ráp thư mục "py" (Python 3.12 Windows x64 + thư viện như bản Mac + pipeline) rồi ghép vào bản
# Windows do GitHub build (KPIDashboard-windows-<ver>.zip) → native/dist/KPIDashboard-windows.zip
#   bash native/winpy/build_win_bundle.sh <zip GitHub build>
# Mac không build được .exe → .exe do workflow build-windows.yml build; Python ráp trên Mac
# (bản standalone của python-build-standalone + wheel win_amd64 tải bằng pip --platform).
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
EXE_ZIP=${1:?cần đường dẫn zip Windows do GitHub build}
PYURL=https://github.com/astral-sh/python-build-standalone/releases/download/20261026/cpython-3.12.16%2B20261026-x86_64-pc-windows-msvc-install_only_stripped.tar.gz
STAGE="$ROOT/native/app/build/winpy"
MACPY="$ROOT/native/app/build/macpy/python/bin/python3"   # chỉ dùng pip để tải wheel Windows
if [ ! -f "$STAGE/.ok" ]; then
  rm -rf "$STAGE"; mkdir -p "$STAGE/dl"
  curl -fsSL -o "$STAGE/dl/py.tar.gz" "$PYURL"
  tar -xzf "$STAGE/dl/py.tar.gz" -C "$STAGE"            # → $STAGE/python (python.exe, pythonw.exe, Lib/)
  # đúng phiên bản thư viện như bản Mac
  "$MACPY" -m pip --version >/dev/null 2>&1 || "$MACPY" -m ensurepip -q 2>/dev/null || true
  uv pip install --python-platform x86_64-pc-windows-msvc --python-version 3.12 \
    --target "$STAGE/python/Lib/site-packages" --only-binary :all: -q \
    pandas==3.1.1 numpy==2.5.4 openpyxl==3.1.5 xlsxwriter==3.3.1 plotly==7.1.0 \
    python-calamine==0.9.1 beautifulsoup4==4.15.0 tzdata
  P="$STAGE/python/Lib"
  rm -rf "$P"/test "$P"/idlelib "$P"/tkinter "$P"/turtledemo "$P"/ensurepip "$STAGE/python/tcl" \
         "$STAGE/python/include" "$STAGE/python/Scripts"
  find "$STAGE/python" -name '__pycache__' -prune -exec rm -rf {} +
  find "$STAGE/python" -path '*/tests' -prune -exec rm -rf {} +
  rm -rf "$STAGE/dl"; touch "$STAGE/.ok"
fi
OUT="$ROOT/native/app/build/winbundle"
rm -rf "$OUT"; mkdir -p "$OUT/app"
unzip -q "$EXE_ZIP" -d "$OUT/app"
mkdir -p "$OUT/app/py/engine"
cp -R "$STAGE/python" "$OUT/app/py/python"
cp "$ROOT"/native/pipeline/{local_engine,headless,report_doc,export_kpi,filters_probe,run_request,app_logic,export_reports,team_data,team_merge}.py "$OUT/app/py/engine/"
mkdir -p "$ROOT/native/dist"; rm -f "$ROOT/native/dist/KPIDashboard-windows.zip"
(cd "$OUT/app" && zip -qr -9 "$ROOT/native/dist/KPIDashboard-windows.zip" .)
du -sh "$OUT/app" "$ROOT/native/dist/KPIDashboard-windows.zip"
