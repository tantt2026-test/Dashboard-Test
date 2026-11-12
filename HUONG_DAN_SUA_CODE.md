# Tự sửa báo cáo — không cần build lại app

## App lấy số từ đâu?
App (APK / Mac / Windows) **không tự tính số**. Mỗi lần có commit mới, GitHub chạy chính file
`App.py` của repo **tantt2026-test/Dashboard-Test** (Streamlit giả lập) cho cả 3 Sale Sup
(Tân, Vy, Cả 2) rồi xuất kết quả lên branch `reports`. App chỉ tải về và hiển thị.

=> **Sửa `App.py` của Dashboard-Test = sửa app.** Không cần build, không cần cài lại.

## Cách sửa
1. Mở https://github.com/tantt2026-test/Dashboard-Test → file `App.py` → nút ✏️ (Edit) → dán code mới → **Commit changes**.
2. Chờ GitHub chạy xong (tab **Actions** → "Build native reports" có dấu ✅, khoảng 20–30 phút).
   App tự có số mới (kéo xuống để tải lại).
3. Muốn Streamlit giống app: dán cùng code vào `App.py` của **Dashboard-Masan** và **Vyntt_Dashboard**
   (chỉ đổi tên Sup / Trung Đoàn ở `page_title`, `_ss_name_m` và tiêu đề `<h1>/<h2>`).

> ⚠️ Chỉ sửa ở Vyntt_Dashboard thì **app không đổi**. App luôn chạy App.py của Dashboard-Test,
> kể cả số của team Vy.

## App tự nhận được
- Báo cáo mới: thêm dòng vào danh sách báo cáo (vd `'21. BÁO CÁO ABC': 'ABC'`) → app tự có mục mới.
- Bảng, thẻ (metric card), biểu đồ, nhận xét do `st.markdown(html)` / `st.dataframe` tạo ra.
- Ô lọc `st.multiselect / selectbox / radio / checkbox / toggle / text_input / date_input`.
  GitHub tự dò cách lọc: lọc được tại chỗ thì app lọc ngay; không thì app nhờ GitHub tính (1–2 phút).

## Lưu ý để không lỗi / không nặng
- **Commit liên tục sẽ huỷ lượt đang chạy.** Sửa xong một lần rồi chờ ✅ mới commit tiếp.
- Đừng xuất bảng hàng nghìn dòng cho mọi ngày. Repo đang ~500MB, mỗi ngày × mỗi báo cáo × mỗi NV đều là 1 file.
  Bảng chi tiết lớn → chỉ hiện khi bật ô lọc có khoá kết thúc bằng `__ondemand`
  (GitHub không tính sẵn, app chỉ tính khi người dùng bật). Mẫu: hàm `_render_detail_slicers_and_tables`.
- Muốn code chỉ chạy trên app (không ảnh hưởng Streamlit): `if hasattr(st, '_rec'):`.
- Lỗi Python sẽ làm báo cáo đó trống trên app → xem tab **Actions** (dấu ❌) để biết dòng lỗi.

## Khi nào mới cần build lại app?
Chỉ khi đổi **giao diện / cách hoạt động của app** (thư mục `native/app`, ngôn ngữ Dart),
ví dụ kiểu ô lọc mới, màn hình đăng nhập, icon. Khi đó:
- Tăng `version:` trong `native/app/pubspec.yaml` → GitHub tự build bản **Windows** (tab Actions → "Build Windows app" → Artifacts).
- APK Android và bản Mac cần build trên máy Mac (có Flutter + Xcode).
