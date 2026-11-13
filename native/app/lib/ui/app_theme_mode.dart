import 'dart:io';

import 'package:flutter/material.dart';

import '../data/app_dirs.dart';

/// Giao diện Sáng / Tối của app. Lưu lại cho lần mở sau (giống AppScale).
class AppThemeMode extends ValueNotifier<ThemeMode> {
  AppThemeMode() : super(ThemeMode.light);

  File _file() => File('${appDataDir()}/theme_mode.txt');

  Future<void> load() async {
    try {
      final v = (await _file().readAsString()).trim();
      if (v == 'dark') value = ThemeMode.dark;
      if (v == 'light') value = ThemeMode.light;
    } catch (_) {}
  }

  void _save() {
    () async {
      try {
        final f = _file();
        await f.parent.create(recursive: true);
        await f.writeAsString(value == ThemeMode.dark ? 'dark' : 'light');
      } catch (_) {}
    }();
  }

  bool get isDark => value == ThemeMode.dark;

  void toggle() {
    value = value == ThemeMode.dark ? ThemeMode.light : ThemeMode.dark;
    _save();
  }

  static final _fallback = AppThemeMode();
  static AppThemeMode of(BuildContext context) =>
      context.dependOnInheritedWidgetOfExactType<AppThemeModeScope>()?.notifier ?? _fallback;
}

class AppThemeModeScope extends InheritedNotifier<AppThemeMode> {
  const AppThemeModeScope({super.key, required AppThemeMode mode, required super.child}) : super(notifier: mode);
}

/// Nút ☀️/🌙 trên thanh tiêu đề: đổi giao diện Sáng ↔ Tối (lưu lại cho lần mở sau).
class ThemeModeButton extends StatelessWidget {
  const ThemeModeButton({super.key});

  @override
  Widget build(BuildContext context) {
    final mode = AppThemeMode.of(context);
    return ValueListenableBuilder<ThemeMode>(
      valueListenable: mode,
      builder: (ctx, v, _) => IconButton(
        tooltip: v == ThemeMode.dark ? 'Giao diện Sáng' : 'Giao diện Tối',
        icon: Icon(v == ThemeMode.dark ? Icons.light_mode_outlined : Icons.dark_mode_outlined),
        onPressed: mode.toggle,
      ),
    );
  }
}
