import 'package:flutter/material.dart';

import '../logic/turnover_logic.dart';

// Màu lấy từ CSS của App.py để app nhìn quen như Streamlit.
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

// Màu nền mang nghĩa (đỏ / xanh lá / tím / vàng / cam của cột %, cảnh báo): giữ nguyên ở giao diện Tối.
const _keepBg = {
  0xFFFED7D7, 0xFFC6F6D5, 0xFFE9D8FD, 0xFFFEEBC8, 0xFFFEFCBF, 0xFFFBD38D, 0xFF9AE6B4, 0xFFFEB2B2,
};

/// Giao diện Tối: nền sáng trung tính (trắng, xanh nhạt, xám nhạt… do App.py truyền) → nền tối;
/// nền mang nghĩa (đỏ/xanh/tím/vàng) giữ nguyên. Giao diện Sáng: trả lại đúng màu gốc.
Color? adaptBg(BuildContext context, Color? c, {Color? dark}) {
  if (c == null || !isDark(context)) return c;
  if (_keepBg.contains(c.toARGB32())) return c;
  if (c.computeLuminance() > 0.6) return dark ?? Brand.darkTileBg;
  return c;
}

/// Giao diện Tối: chữ tối (đen, navy, xanh đậm) → chữ sáng cho dễ đọc trên nền tối.
Color? adaptFg(BuildContext context, Color? c) {
  if (c == null || !isDark(context)) return c;
  if (c.computeLuminance() >= 0.22) return c;
  final bluish = c.b > c.r + 0.08 && c.b >= c.g;
  final reddish = c.r > c.g + 0.15 && c.r > c.b + 0.15;
  if (bluish) return const Color(0xFF90CDF4);
  if (reddish) return const Color(0xFFFC8181);
  final greenish = c.g > c.r + 0.08 && c.g > c.b;
  if (greenish) return const Color(0xFF68D391);
  final purple = c.r > c.g + 0.1 && c.b > c.g + 0.1;
  if (purple) return const Color(0xFFB794F4);
  return Brand.darkText;
}

/// Khung còn nền sáng (màu mang nghĩa) ở giao diện Tối → nội dung bên trong vẽ như giao diện Sáng
/// (chữ tối trên nền sáng), tránh chữ sáng trên nền vàng/xanh nhạt.
Widget keepLight(BuildContext context, Color bg, Widget child) {
  if (!isDark(context) || bg.computeLuminance() <= 0.6) return child;
  return Theme(
    data: buildTheme(Brightness.light),
    child: DefaultTextStyle.merge(style: const TextStyle(color: Color(0xFF1A202C)), child: child),
  );
}

// ── Thẻ số liệu: 1 format chung cho mọi báo cáo (theo mẫu thẻ Báo Cáo Hiệu Suất) ──
// vạch màu nhấn ở mép trên + tiêu đề cùng màu nhấn, số to màu trung tính, dòng phụ xám.

/// Bảng màu nhấn xoay vòng (giống thứ tự thẻ Hiệu Suất, bỏ đỏ để đỏ chỉ mang nghĩa "chưa đạt").
const metricPalette = [
  Color(0xFF3182CE), Color(0xFFDD6B20), Color(0xFF805AD5), Color(0xFF38A169),
  Color(0xFFD53F8C), Color(0xFF319795), Color(0xFFD69E2E), Color(0xFF2B6CB0),
];

// màu chữ đậm App.py dùng cho thẻ → màu nhấn tươi tương ứng (cho vạch mép trên / tiêu đề)
const _vivid = {
  0xFF22543D: Color(0xFF38A169), // xanh lá đậm (Đã đạt)
  0xFF276749: Color(0xFF38A169),
  0xFF234E52: Color(0xFF319795), // xanh ngọc
  0xFFC53030: Color(0xFFE53E3E), // đỏ
  0xFF6B46C1: Color(0xFF805AD5), // tím
  0xFF2B6CB0: Color(0xFF3182CE), // xanh dương
};

/// Màu nhấn của thẻ thứ [i]: màu `ac` có sẵn (Hiệu Suất) → giữ; màu chữ mang nghĩa (đỏ/xanh lá/nhóm MBS…)
/// → màu tươi tương ứng; thẻ màu xanh mặc định (#034ea2) / không màu → màu xoay vòng theo vị trí.
Color metricAccent({Color? ac, Color? c, required int i}) {
  if (ac != null) return ac;
  // xanh mặc định / chữ đen-xám trung tính: không mang nghĩa → màu xoay vòng
  const neutral = {0xFF034EA2, 0xFF1A202C, 0xFF2D3748, 0xFF4A5568};
  if (c != null && !neutral.contains(c.toARGB32())) {
    return _vivid[c.toARGB32()] ?? c;
  }
  return metricPalette[i % metricPalette.length];
}

/// Nền thẻ số liệu (xanh nhạt ở Sáng, xám đậm ở Tối — như thẻ Hiệu Suất).
Color metricBg(BuildContext context) => isDark(context) ? Brand.darkTileBg : Brand.cardBg;

/// Số chính của thẻ: màu trung tính.
Color metricValue(BuildContext context) => isDark(context) ? Brand.darkText : const Color(0xFF1A202C);

/// Tiêu đề thẻ = màu nhấn (Tối: pha sáng thêm cho dễ đọc trên nền tối).
Color metricTitle(BuildContext context, Color accent) =>
    isDark(context) ? Color.lerp(accent, Colors.white, 0.18)! : accent;

/// Khung thẻ: nền + viền + vạch màu nhấn dày 4px ở mép trên; nội dung căn giữa.
/// [fill]: thẻ nằm trong hàng cao cố định (IntrinsicHeight) → nội dung căn giữa theo chiều dọc.
class MetricShell extends StatelessWidget {
  final Color accent;
  final Widget child;
  final EdgeInsets padding;
  final bool fill;
  const MetricShell({
    super.key,
    required this.accent,
    required this.child,
    this.padding = const EdgeInsets.fromLTRB(8, 9, 8, 10),
    this.fill = false,
  });

  @override
  Widget build(BuildContext context) {
    final body = Padding(padding: padding, child: child);
    return ClipRRect(
      borderRadius: BorderRadius.circular(8),
      child: Container(
        decoration: BoxDecoration(
          color: metricBg(context),
          borderRadius: BorderRadius.circular(8),
          border: Border.all(color: isDark(context) ? Brand.darkTileBorder : Brand.cardBorder),
        ),
        child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, mainAxisSize: MainAxisSize.min, children: [
          Container(height: 4, color: accent),
          fill ? Expanded(child: Center(child: body)) : body,
        ]),
      ),
    );
  }
}

ThemeData buildTheme(Brightness brightness) {
  final dark = brightness == Brightness.dark;
  final base = ThemeData(
    useMaterial3: true,
    brightness: brightness,
    colorScheme: ColorScheme.fromSeed(
      seedColor: Brand.navy,
      brightness: brightness,
      // giao diện Tối: màu nhấn (chữ nút, ô chọn) xanh sáng cho dễ đọc trên nền tối
      primary: dark ? const Color(0xFF90CDF4) : Brand.navy,
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
