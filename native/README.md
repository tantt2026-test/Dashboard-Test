# KPI Dashboard – Native (Android + macOS)

```
Onetech sync → GitHub main (data/*.xlsx)
      └─ GitHub Action: chạy chính hàm của App.py → JSON → đối chiếu số → branch `reports`
              └─ App Flutter (Android / macOS) đọc JSON, lọc NV/ngày trên máy, xem offline được
Streamlit Cloud vẫn chạy y như cũ từ branch main.
```

## Giai đoạn 2: 18 báo cáo tab "📊 BÁO CÁO KPI"
`pipeline/headless.py` chạy **nguyên App.py** (cả phần giao diện) với streamlit giả: widget trả về
lựa chọn đặt sẵn (tháng, ngày, ĐDKD, báo cáo), mọi st.markdown / plotly / caption được ghi lại.
`pipeline/report_doc.py` chuyển HTML đó thành JSON (bảng gộp ô + màu, thẻ số, nhận xét, biểu đồ)
→ app vẽ native. Số, format, màu đều lấy thẳng từ App.py.

Biến thể xuất sẵn: **Tất cả ĐDKD** cho mọi ngày có data; **từng ĐDKD** cho ngày mặc định (T-1).
Báo cáo 1 (Turnover) vẫn dùng logic Dart riêng (chọn nhiều ĐDKD được).

## Thư mục
| | |
|---|---|
| `pipeline/app_logic.py` | Nạp hàm từ App.py bằng AST + `streamlit` giả (không chép code) |
| `pipeline/export_reports.py` | Xuất `manifest.json` + `turnover/<Thang>.json` |
| `pipeline/parity_check.py` | So từng ô app (Dart) vs `build_turnover_report` (Python). Lệch → exit 1 |
| `app/lib/logic/` | Phần logic chạy trên app: lọc NV, sort, dòng Tổng, %, GAP, BQ, làm tròn kiểu Python |
| `app/lib/ui/` | Giao diện |
| `pipeline/headless.py`, `report_doc.py`, `export_kpi.py` | Giai đoạn 2 (18 báo cáo KPI) |
| `app/test/report_render_test.dart` | Dựng giao diện mọi file JSON để bắt lỗi layout |
| `ci/build-reports.yml`, `ci/publish.sh` | Workflow GitHub Action (2 lượt publish) |

## Đưa lên GitHub (làm 1 lần)
1. Copy `pipeline/` và `app/` vào repo `Dashboard-Test` thành `native/pipeline/` và `native/app/`.
2. Copy `ci/build-reports.yml` → `.github/workflows/build-reports.yml`
   (tạo qua giao diện web GitHub: token Onetech không có quyền `workflow`).
3. Commit + push lên `main`. Action chạy ~3–5 phút, tạo branch `reports`.
4. Từ đó mỗi lần Onetech sync (7:50 / 13:30 / 18:30) Action tự chạy lại.

## Chạy thử trên máy
```bash
cd pipeline && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python export_reports.py --app ~/Dashboard-Test/App.py --out out
.venv/bin/python parity_check.py --app ~/Dashboard-Test/App.py --json out --dart-app ../app
.venv/bin/python export_reports.py --app ~/Dashboard-Test/App.py --out out --kpi   # + 18 báo cáo KPI
cd ../app && ALL=1 REPORTS_DIR=../pipeline/out/kpi/Thang10 flutter test test/report_render_test.dart
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
