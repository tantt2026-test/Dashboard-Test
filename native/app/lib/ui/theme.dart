import 'package:flutter/material.dart';

import '../logic/turnover_logic.dart';

// Màu lấy từ CSS của App.py để app nhìn quen như Streamlit.
// Bảng báo cáo / thẻ số liệu luôn giữ các màu này (nền sáng) ở cả giao diện Tối, để màu đỏ/xanh/tím
// báo kết quả không đổi và khớp với bản Streamlit. Dark mode chỉ đổi màu khung app (menu, nền trang).
class Brand {
  static const navy = Color(0xFF1A365D);
  static const blue = Color(0xFF034EA2);
  static const border = Color(0xFF2B6CB0);
  static const zebra = Color(0xFFE6F4FC);
  static const cellBorder = Color(0xFFBCE2F5);
  static const cardBg = Color(0xFFEBF8FF);
  static const cardBorder = Color(0xFFBEE3F8);
  static const cardText = Color(0xFFC53030);
  static const salary = Color(0xFF7A1F1F);
  static const accent = Color(0xFFF6AD55);
  static const pageBg = Color(0xFFF7FAFC);
  static const muted = Color(0xFF4A5568);

  // Giao diện Tối: chỉ dùng cho khung app (nền trang, menu, thanh tiêu đề) — không dùng trong bảng báo cáo.
  static const darkPageBg = Color(0xFF0E1621);
  static const darkPanelBg = Color(0xFF16212E);
  static const darkTileBg = Color(0xFF1C2A3A);
  static const darkTileBorder = Color(0xFF2B3C4F);
  static const darkTileHover = Color(0xFF233247);
  static const darkText = Color(0xFFE2E8F0);
  static const darkMuted = Color(0xFF94A3B8);
}

(Color bg, Color fg) pctColors(PctColor c) => switch (c) {
      PctColor.red => (const Color(0xFFFED7D7), const Color(0xFF742A2A)),
      PctColor.green => (const Color(0xFFC6F6D5), const Color(0xFF22543D)),
      PctColor.purple => (const Color(0xFFE9D8FD), const Color(0xFF553C9A)),
    };

/// true khi app đang hiện giao diện Tối.
bool isDark(BuildContext context) => Theme.of(context).brightness == Brightness.dark;

/// Nền khung menu / thanh bên (trắng ở giao diện Sáng, xám đậm ở giao diện Tối).
Color panelBg(BuildContext context) => isDark(context) ? Brand.darkPanelBg : Colors.white;

/// Nền 1 mục trong menu khi KHÔNG chọn (card trắng ở Sáng, card xám ở Tối).
Color tileBg(BuildContext context, {bool hover = false}) =>
    isDark(context) ? (hover ? Brand.darkTileHover : Brand.darkTileBg) : (hover ? Brand.cardBg : Colors.white);

/// Viền 1 mục trong menu khi KHÔNG chọn.
Color tileBorder(BuildContext context, {bool hover = false}) =>
    isDark(context) ? Brand.darkTileBorder : (hover ? Brand.border : Brand.cardBorder);

/// Chữ 1 mục trong menu khi KHÔNG chọn (navy ở Sáng, chữ sáng ở Tối).
Color tileText(BuildContext context) => isDark(context) ? Brand.darkText : Brand.navy;

/// Chữ phụ (ghi chú nhỏ) theo giao diện.
Color mutedText(BuildContext context) => isDark(context) ? Brand.darkMuted : Brand.muted;

ThemeData buildTheme(Brightness brightness) {
  final dark = brightness == Brightness.dark;
  final base = ThemeData(
    useMaterial3: true,
    brightness: brightness,
    colorScheme: ColorScheme.fromSeed(
      seedColor: Brand.navy,
      brightness: brightness,
      primary: Brand.navy,
    ),
    scaffoldBackgroundColor: dark ? Brand.darkPageBg : Brand.pageBg,
  );
  return base.copyWith(
    appBarTheme: const AppBarTheme(
      backgroundColor: Brand.navy,
      foregroundColor: Colors.white,
      elevation: 0,
      centerTitle: false,
    ),
    cardColor: dark ? Brand.darkPanelBg : Colors.white,
    dividerColor: dark ? Brand.darkTileBorder : null,
  );
}
