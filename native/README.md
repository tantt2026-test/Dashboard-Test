# KPI Dashboard – Native (giai đoạn 1: Turnover)

```
Onetech sync → GitHub main (data/*.xlsx)
      └─ GitHub Action: chạy chính hàm của App.py → JSON → đối chiếu số → branch `reports`
              └─ App Flutter (Android / macOS) đọc JSON, lọc NV/ngày trên máy, xem offline được
Streamlit Cloud vẫn chạy y như cũ từ branch main.
```

## Thư mục
| | |
|---|---|
| `pipeline/app_logic.py` | Nạp hàm từ App.py bằng AST + `streamlit` giả (không chép code) |
| `pipeline/export_reports.py` | Xuất `manifest.json` + `turnover/<Thang>.json` |
| `pipeline/parity_check.py` | So từng ô app (Dart) vs `build_turnover_report` (Python). Lệch → exit 1 |
| `app/lib/logic/` | Phần logic chạy trên app: lọc NV, sort, dòng Tổng, %, GAP, BQ, làm tròn kiểu Python |
| `app/lib/ui/` | Giao diện |
| `ci/build-reports.yml` | Workflow GitHub Action |

## Đưa lên GitHub (làm 1 lần)
1. Copy `pipeline/` và `app/` vào repo `Dashboard-Test` thành `native/pipeline/` và `native/app/`.
2. Copy `ci/build-reports.yml` → `.github/workflows/build-reports.yml`.
3. Commit + push lên `main`. Action chạy ~3–5 phút, tạo branch `reports`.
4. Từ đó mỗi lần Onetech sync (7:50 / 13:30 / 18:30) Action tự chạy lại.

## Chạy thử trên máy
```bash
cd pipeline && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python export_reports.py --app ~/Dashboard-Test/App.py --out out
.venv/bin/python parity_check.py --app ~/Dashboard-Test/App.py --json out --dart-app ../app
```

## Build app
```bash
cd app
flutter build apk --release --split-per-abi      # Android: app-arm64-v8a-release.apk
flutter build macos --release                     # Mac: cần cài Xcode (App Store)
```
Test với JSON local: thêm `--dart-define=DATA_BASE_URL=http://10.0.2.2:8000/` (emulator)
hoặc `http://localhost:8000/` (Mac), rồi `python3 -m http.server 8000` trong `pipeline/out`.

## Khi sửa App.py
- Sửa logic tính toán bên trong các hàm → pipeline tự theo, không cần sửa app.
- Đổi tên/tham số `build_turnover_report`, `load_main_data`, `get_turnover_targets`,
  `get_timegone_stats`, hoặc đổi cách tính % / GAP / BQ / dòng Tổng → Action sẽ báo lệch
  (không publish số sai), cần cập nhật `app/lib/logic/turnover_logic.dart`.
