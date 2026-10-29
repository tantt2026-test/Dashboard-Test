import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import 'theme.dart';

/// Tỷ lệ hiển thị chung của app (chữ, bảng, thẻ, biểu đồ). Lưu lại cho lần mở sau.
class AppScale extends ValueNotifier<double> {
  AppScale() : super(1.0);

  static const min = 0.6, max = 1.8, step = 0.1;

  File _file() {
    final base = Platform.isAndroid
        ? '${Directory.systemTemp.parent.path}/files'
        : '${Platform.environment['HOME'] ?? Directory.systemTemp.path}/Library/Application Support/kpi_reports';
    return File('$base/ui_scale.txt');
  }

  Future<void> load() async {
    try {
      final v = double.tryParse((await _file().readAsString()).trim());
      if (v != null) value = v.clamp(min, max);
    } catch (_) {}
  }

  void set(double v) {
    value = double.parse(v.clamp(min, max).toStringAsFixed(2));
    () async {
      try {
        final f = _file();
        await f.parent.create(recursive: true);
        await f.writeAsString('$value');
      } catch (_) {}
    }();
  }

  void zoomIn() => set(value + step);
  void zoomOut() => set(value - step);
  void reset() => set(1.0);

  static final _fallback = AppScale();
  static AppScale of(BuildContext context) =>
      context.dependOnInheritedWidgetOfExactType<AppScaleScope>()?.notifier ?? _fallback;
}

class AppScaleScope extends InheritedNotifier<AppScale> {
  const AppScaleScope({super.key, required AppScale scale, required super.child}) : super(notifier: scale);
}

/// Bọc app: chữ theo tỷ lệ + phím tắt ⌘+ / ⌘− / ⌘0 (Mac), Ctrl trên máy khác.
class ScaledApp extends StatelessWidget {
  final AppScale scale;
  final Widget child;
  const ScaledApp({super.key, required this.scale, required this.child});

  @override
  Widget build(BuildContext context) {
    final mods = Platform.isMacOS ? (meta: true, control: false) : (meta: false, control: true);
    SingleActivator k(LogicalKeyboardKey key) =>
        SingleActivator(key, meta: mods.meta, control: mods.control);
    return AppScaleScope(
      scale: scale,
      child: ValueListenableBuilder<double>(
        valueListenable: scale,
        builder: (ctx, v, _) => CallbackShortcuts(
          bindings: {
            k(LogicalKeyboardKey.equal): scale.zoomIn,
            k(LogicalKeyboardKey.add): scale.zoomIn,
            k(LogicalKeyboardKey.numpadAdd): scale.zoomIn,
            k(LogicalKeyboardKey.minus): scale.zoomOut,
            k(LogicalKeyboardKey.numpadSubtract): scale.zoomOut,
            k(LogicalKeyboardKey.digit0): scale.reset,
          },
          child: Focus(
            autofocus: true,
            child: MediaQuery(
              data: MediaQuery.of(ctx).copyWith(textScaler: TextScaler.linear(v)),
              child: child,
            ),
          ),
        ),
      ),
    );
  }
}

/// Nút "Aa" trên thanh tiêu đề: chỉnh tỷ lệ hiển thị toàn app.
class ScaleButton extends StatelessWidget {
  const ScaleButton({super.key});

  @override
  Widget build(BuildContext context) {
    final scale = AppScale.of(context);
    return IconButton(
      tooltip: 'Tỷ lệ hiển thị (${(scale.value * 100).round()}%)',
      icon: const Icon(Icons.text_fields),
      onPressed: () => showModalBottomSheet(
        context: context,
        showDragHandle: true,
        builder: (ctx) => _ScaleSheet(scale: scale),
      ),
    );
  }
}

class _ScaleSheet extends StatelessWidget {
  final AppScale scale;
  const _ScaleSheet({required this.scale});

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder<double>(
      valueListenable: scale,
      builder: (ctx, v, _) => SafeArea(
        child: Padding(
          padding: const EdgeInsets.fromLTRB(20, 0, 20, 20),
          child: Column(mainAxisSize: MainAxisSize.min, children: [
            const Text('Tỷ lệ hiển thị', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w700)),
            const SizedBox(height: 4),
            const Text('Áp dụng cho toàn bộ nội dung trong app',
                style: TextStyle(fontSize: 12, color: Brand.muted)),
            const SizedBox(height: 12),
            Row(children: [
              IconButton.filledTonal(onPressed: scale.zoomOut, icon: const Icon(Icons.remove)),
              Expanded(
                child: Slider(
                  value: v,
                  min: AppScale.min,
                  max: AppScale.max,
                  divisions: ((AppScale.max - AppScale.min) / AppScale.step).round(),
                  label: '${(v * 100).round()}%',
                  onChanged: scale.set,
                ),
              ),
              IconButton.filledTonal(onPressed: scale.zoomIn, icon: const Icon(Icons.add)),
            ]),
            Wrap(spacing: 8, children: [
              for (final p in const [0.7, 0.85, 1.0, 1.15, 1.3])
                ChoiceChip(
                  label: Text('${(p * 100).round()}%'),
                  selected: (v - p).abs() < 0.01,
                  onSelected: (_) => scale.set(p),
                ),
            ]),
          ]),
        ),
      ),
    );
  }
}
