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
}

(Color bg, Color fg) pctColors(PctColor c) => switch (c) {
      PctColor.red => (const Color(0xFFFED7D7), const Color(0xFF742A2A)),
      PctColor.green => (const Color(0xFFC6F6D5), const Color(0xFF22543D)),
      PctColor.purple => (const Color(0xFFE9D8FD), const Color(0xFF553C9A)),
    };

ThemeData buildTheme() {
  final base = ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.fromSeed(seedColor: Brand.navy, primary: Brand.navy),
    scaffoldBackgroundColor: Brand.pageBg,
  );
  return base.copyWith(
    appBarTheme: const AppBarTheme(
      backgroundColor: Brand.navy,
      foregroundColor: Colors.white,
      elevation: 0,
      centerTitle: false,
    ),
  );
}
