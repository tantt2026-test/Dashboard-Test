import 'dart:math' as math;

import 'package:flutter/material.dart';

import 'report_view.dart' show hexColor;
import 'theme.dart';

const _palette = [
  Color(0xFF3182CE), Color(0xFFED7D31), Color(0xFF38A169), Color(0xFF805AD5),
  Color(0xFFD69E2E), Color(0xFFE53E3E), Color(0xFF319795), Color(0xFFD53F8C),
];

bool _transparent(Object? c) => c is String && c.replaceAll(' ', '').endsWith(',0)');

String _fmt(num v) {
  if (v == v.roundToDouble()) return v.toInt().toString();
  return v.abs() >= 100 ? v.toStringAsFixed(0) : v.toStringAsFixed(1);
}

Widget _title(String? t) => (t == null || t.isEmpty)
    ? const SizedBox.shrink()
    : Padding(
        padding: const EdgeInsets.only(bottom: 8),
        child: Text(t,
            textAlign: TextAlign.center,
            style: const TextStyle(fontWeight: FontWeight.w800, color: Brand.navy, fontSize: 14)),
      );

BoxDecoration get _frame => BoxDecoration(
      color: Colors.white,
      borderRadius: BorderRadius.circular(8),
      border: Border.all(color: Brand.cardBorder),
    );

/// Biểu đồ cột Plotly → thanh ngang: mỗi hạng mục 1 dòng, mỗi trace 1 thanh.
class BarChartView extends StatelessWidget {
  final Map<String, dynamic> data;
  const BarChartView({super.key, required this.data});

  @override
  Widget build(BuildContext context) {
    final traces = (data['tr'] as List).cast<Map<String, dynamic>>();
    // trace trong suốt (overlay) chỉ để in nhãn → gộp nhãn vào trace thật
    final visible = traces.where((t) => !_transparent(t['color'])).toList();
    final labelOnly = traces.where((t) => _transparent(t['color'])).toList();
    if (visible.isEmpty) return const SizedBox.shrink();

    List<String> cats(Map t) => [for (final c in ((t['h'] == 1 ? t['y'] : t['x']) as List? ?? const [])) '$c'];
    List<double?> vals(Map t) =>
        [for (final v in ((t['h'] == 1 ? t['x'] : t['y']) as List? ?? const [])) v is num ? v.toDouble() : null];

    final categories = cats(visible.first);
    final refs = [
      for (final r in (data['ref'] as List? ?? const []).cast<Map>())
        if (r['y0'] is num && r['y0'] == r['y1'] && visible.first['h'] != 1)
          ((r['y0'] as num).toDouble(), hexColor(r['c']) ?? Brand.muted)
        else if (r['x0'] is num && r['x0'] == r['x1'] && visible.first['h'] == 1)
          ((r['x0'] as num).toDouble(), hexColor(r['c']) ?? Brand.muted)
    ];

    final all = [for (final t in visible) ...vals(t).whereType<double>()];
    final sorted = [...all.where((v) => v > 0)]..sort();
    final median = sorted.isEmpty ? 1.0 : sorted[sorted.length ~/ 2];
    var maxV = [
      ...all.where((v) => v <= median * 5),
      ...refs.map((r) => r.$1),
      1.0,
    ].reduce(math.max);
    maxV *= 1.08;

    Color colorOf(Map t, int i, int ti) {
      final c = t['color'];
      if (c is List && i < c.length) return hexColor(c[i]) ?? _palette[i % _palette.length];
      return hexColor(c) ?? _palette[ti % _palette.length];
    }

    // Nhãn = text của thanh (vd "124/184") + text của trace chỉ-nhãn (vd "67.4%")
    String labelOf(int i, int ti, double? v) {
      final parts = <String>[];
      for (final t in [visible[ti], if (ti == 0) ...labelOnly]) {
        final tx = t['text'];
        if (tx is List && i < tx.length && '${tx[i]}'.isNotEmpty) parts.add('${tx[i]}');
      }
      if (parts.isEmpty && v != null) parts.add(_fmt(v));
      return parts.join(' · ');
    }

    final nameW = math.min(150.0, categories.fold<int>(6, (m, c) => math.max(m, c.length)) * 7.2 + 8);

    return Container(
      padding: const EdgeInsets.all(12),
      decoration: _frame,
      child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
        _title(data['title'] as String?),
        if (visible.length > 1 || refs.isNotEmpty)
          Padding(
            padding: const EdgeInsets.only(bottom: 8),
            child: Wrap(spacing: 12, runSpacing: 4, alignment: WrapAlignment.center, children: [
              if (visible.length > 1)
                for (var ti = 0; ti < visible.length; ti++)
                  _legend(colorOf(visible[ti], 0, ti), visible[ti]['name'] as String? ?? ''),
              for (final r in refs) _legend(r.$2, 'Mốc ${_fmt(r.$1)}', line: true),
            ]),
          ),
        for (var i = 0; i < categories.length; i++)
          Padding(
            padding: const EdgeInsets.symmetric(vertical: 3),
            child: Row(crossAxisAlignment: CrossAxisAlignment.center, children: [
              SizedBox(
                width: nameW,
                child: Text(categories[i],
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                    style: const TextStyle(fontSize: 11.5, color: Color(0xFF2D3748))),
              ),
              const SizedBox(width: 6),
              Expanded(
                child: LayoutBuilder(builder: (ctx, c) {
                  final w = c.maxWidth;
                  return Stack(children: [
                    Column(children: [
                      for (var ti = 0; ti < visible.length; ti++)
                        () {
                          final vs = vals(visible[ti]);
                          final v = i < vs.length ? vs[i] : null;
                          final frac = v == null ? 0.0 : (v / maxV).clamp(0.0, 1.0);
                          final label = labelOf(i, ti, v);
                          return Padding(
                            padding: const EdgeInsets.symmetric(vertical: 1),
                            child: Row(children: [
                              Container(
                                width: math.max(2, w * frac * 0.78),
                                height: visible.length > 1 ? 11 : 16,
                                decoration: BoxDecoration(
                                  color: colorOf(visible[ti], i, ti),
                                  borderRadius: BorderRadius.circular(3),
                                ),
                              ),
                              const SizedBox(width: 4),
                              Flexible(
                                child: Text(label,
                                    maxLines: 1,
                                    overflow: TextOverflow.ellipsis,
                                    style: const TextStyle(fontSize: 10.5, fontWeight: FontWeight.w600)),
                              ),
                            ]),
                          );
                        }(),
                    ]),
                    for (final r in refs)
                      Positioned(
                        left: w * (r.$1 / maxV).clamp(0.0, 1.0) * 0.78,
                        top: 0,
                        bottom: 0,
                        child: Container(width: 1.5, color: r.$2.withValues(alpha: 0.8)),
                      ),
                  ]);
                }),
              ),
            ]),
          ),
      ]),
    );
  }

  Widget _legend(Color c, String text, {bool line = false}) => Row(mainAxisSize: MainAxisSize.min, children: [
        Container(width: line ? 14 : 10, height: line ? 2 : 10, color: c),
        const SizedBox(width: 4),
        Text(text, style: const TextStyle(fontSize: 11, color: Brand.muted)),
      ]);
}

/// Biểu đồ tròn / donut.
class PieChartView extends StatelessWidget {
  final Map<String, dynamic> data;
  const PieChartView({super.key, required this.data});

  @override
  Widget build(BuildContext context) {
    final t = (data['tr'] as List).first as Map<String, dynamic>;
    final labels = [for (final l in t['labels'] as List) '$l'];
    final values = [for (final v in t['values'] as List) v is num ? v.toDouble() : 0.0];
    final cols = t['colors'] as List?;
    final colors = [
      for (var i = 0; i < labels.length; i++)
        (cols != null && i < cols.length ? hexColor(cols[i]) : null) ?? _palette[i % _palette.length]
    ];
    final total = values.fold<double>(0, (a, b) => a + b);
    final hole = ((t['hole'] as num?) ?? 0).toDouble();

    final pie = SizedBox(
      width: 170,
      height: 170,
      child: CustomPaint(painter: _PiePainter(values, colors, hole), child: Center(
        child: hole > 0
            ? Text(_fmt(total), style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 18, color: Brand.navy))
            : null,
      )),
    );
    final legend = Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      for (var i = 0; i < labels.length; i++)
        Padding(
          padding: const EdgeInsets.symmetric(vertical: 3),
          child: Row(children: [
            Container(width: 10, height: 10, decoration: BoxDecoration(color: colors[i], shape: BoxShape.circle)),
            const SizedBox(width: 6),
            Expanded(child: Text(labels[i], style: const TextStyle(fontSize: 12))),
            Text('${_fmt(values[i])} · ${total > 0 ? (values[i] / total * 100).toStringAsFixed(1) : '0'}%',
                style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w700)),
          ]),
        ),
    ]);

    return Container(
      padding: const EdgeInsets.all(12),
      decoration: _frame,
      child: Column(children: [
        _title(data['title'] as String?),
        LayoutBuilder(builder: (ctx, c) => c.maxWidth > 560
            ? Row(children: [pie, const SizedBox(width: 20), Expanded(child: legend)])
            : Column(children: [pie, const SizedBox(height: 12), legend])),
      ]),
    );
  }
}

class _PiePainter extends CustomPainter {
  final List<double> values;
  final List<Color> colors;
  final double hole;
  _PiePainter(this.values, this.colors, this.hole);

  @override
  void paint(Canvas canvas, Size size) {
    final total = values.fold<double>(0, (a, b) => a + b);
    if (total <= 0) return;
    final r = math.min(size.width, size.height) / 2;
    final rect = Rect.fromCircle(center: size.center(Offset.zero), radius: r);
    var start = -math.pi / 2;
    for (var i = 0; i < values.length; i++) {
      final sweep = values[i] / total * 2 * math.pi;
      canvas.drawArc(rect, start, sweep, true, Paint()..color = colors[i]);
      canvas.drawArc(rect, start, sweep, true,
          Paint()
            ..color = Colors.white
            ..style = PaintingStyle.stroke
            ..strokeWidth = 1.5);
      start += sweep;
    }
    if (hole > 0) {
      canvas.drawCircle(size.center(Offset.zero), r * hole, Paint()..color = Colors.white);
    }
  }

  @override
  bool shouldRepaint(_PiePainter old) => old.values != values;
}
