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

/// Biểu đồ tròn / donut — vẽ y như go.Pie của Plotly trên Streamlit (render_mbs_pie_chart):
/// sort giảm dần, lát đầu bắt đầu ở 12 giờ (theo chiều kim đồng hồ), các lát sau đi ngược chiều;
/// textinfo 'percent+label' nằm ngoài, % 3 chữ số có nghĩa ("33%", "2.91%"); viền trắng 1px;
/// chú thích nằm ngang bên dưới (bấm để ẩn/hiện lát); rê chuột / chạm lát → khung hover.
class PieChartView extends StatefulWidget {
  final Map<String, dynamic> data;
  const PieChartView({super.key, required this.data});

  @override
  State<PieChartView> createState() => _PieChartViewState();
}

/// % kiểu Plotly (d3 '.3~p'): 3 chữ số có nghĩa, bỏ số 0 thừa.
String plotlyPct(double frac) {
  final p = frac * 100;
  if (p == 0) return '0%';
  var s = p.toStringAsPrecision(3);
  if (s.contains('e')) s = p.toStringAsFixed(2);
  if (s.contains('.')) s = s.replaceFirst(RegExp(r'0+$'), '').replaceFirst(RegExp(r'\.$'), '');
  return '$s%';
}

class _Slice {
  final int i; // vị trí gốc
  final String label;
  final double value;
  final Color color;
  _Slice(this.i, this.label, this.value, this.color);
}

class _PieChartViewState extends State<PieChartView> {
  final Set<String> _hidden = {};
  Offset? _hoverPos;
  int? _hoverSlice;

  static const _labelColor = Color(0xFF808495); // chữ ngoài lát (theme Streamlit)
  static const _textColor = Color(0xFF31333F); // chú thích

  @override
  Widget build(BuildContext context) {
    final t = (widget.data['tr'] as List).first as Map<String, dynamic>;
    final labels = [for (final l in t['labels'] as List) '$l'];
    final values = [for (final v in t['values'] as List) v is num ? v.toDouble() : 0.0];
    final cols = t['colors'] as List?;
    final all = <_Slice>[
      for (var i = 0; i < labels.length; i++)
        _Slice(i, labels[i], i < values.length ? values[i] : 0,
            (cols != null && i < cols.length ? hexColor(cols[i]) : null) ?? _palette[i % _palette.length])
    ];
    // Plotly sort=True: giảm dần theo giá trị (bằng nhau giữ thứ tự gốc)
    if (t['sort'] != false) {
      all.sort((a, b) => b.value != a.value ? b.value.compareTo(a.value) : a.i.compareTo(b.i));
    }
    final shown = [for (final s in all) if (!_hidden.contains(s.label) && s.value > 0) s];
    final hole = ((t['hole'] as num?) ?? 0).toDouble();
    final info = '${t['textinfo'] ?? 'percent+label'}';
    final outside = '${t['textposition'] ?? 'outside'}' == 'outside';
    final hover = t['hovertemplate'] as String?;

    final chart = LayoutBuilder(builder: (ctx, c) {
      final size = Size(c.maxWidth, 300);
      final geo = _PieGeo(shown, size, hole, info, outside, DefaultTextStyle.of(ctx).style.fontFamily);
      String? tip;
      if (_hoverSlice != null && _hoverSlice! < shown.length) {
        final s = shown[_hoverSlice!];
        final pct = plotlyPct(s.value / geo.total);
        tip = (hover ?? '%{label}<br>%{value} (%{percent})')
            .replaceAll(RegExp(r'<extra>.*?</extra>'), '')
            .replaceAll('%{label}', s.label)
            .replaceAll('%{value}', _fmt(s.value))
            .replaceAll('%{percent}', pct)
            .replaceAll('<br>', '\n');
      }
      void track(Offset p) {
        final k = geo.hit(p);
        if (k != _hoverSlice || (k != null && p != _hoverPos)) {
          setState(() {
            _hoverSlice = k;
            _hoverPos = p;
          });
        }
      }

      return MouseRegion(
        onHover: (e) => track(e.localPosition),
        onExit: (_) => setState(() => _hoverSlice = null),
        child: GestureDetector(
          onTapDown: (d) => track(d.localPosition),
          child: SizedBox(
            width: size.width,
            height: size.height,
            child: Stack(clipBehavior: Clip.none, children: [
              CustomPaint(size: size, painter: _PiePainter(geo)),
              if (tip != null && _hoverPos != null)
                Positioned(
                  left: (_hoverPos!.dx + 12).clamp(0, math.max(0, size.width - 220)).toDouble(),
                  top: (_hoverPos!.dy - 10).clamp(0, size.height - 40).toDouble(),
                  child: IgnorePointer(
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 5),
                      decoration: BoxDecoration(
                        color: shown[_hoverSlice!].color,
                        borderRadius: BorderRadius.circular(3),
                        border: Border.all(color: Colors.white),
                      ),
                      child: Text(tip, style: const TextStyle(color: Colors.white, fontSize: 12.5, height: 1.3)),
                    ),
                  ),
                ),
            ]),
          ),
        ),
      );
    });

    // Chú thích ngang (orientation='h'), canh giữa, các cột thẳng hàng như Plotly
    final legend = LayoutBuilder(builder: (ctx, c) {
      final style = TextStyle(fontSize: 11, color: _textColor, fontFamily: DefaultTextStyle.of(ctx).style.fontFamily);
      double tw(String s) => (TextPainter(text: TextSpan(text: s, style: style), textDirection: TextDirection.ltr)
            ..layout())
          .width;
      // mỗi ô = chữ dài nhất + ô màu + khoảng cách, chia đều thành cột như legend ngang của Plotly
      final itemW = math.min(c.maxWidth, all.map((s) => tw(s.label)).fold<double>(0, math.max) + 30);
      return Wrap(alignment: WrapAlignment.center, runSpacing: 4, children: [
        for (final s in all)
          InkWell(
            onTap: () => setState(() {
              _hoverSlice = null;
              _hidden.contains(s.label) ? _hidden.remove(s.label) : _hidden.add(s.label);
            }),
            child: SizedBox(
              width: itemW,
              child: Opacity(
                opacity: _hidden.contains(s.label) ? 0.5 : 1,
                child: Row(children: [
                  Container(width: 13, height: 13, color: s.color),
                  const SizedBox(width: 6),
                  Expanded(child: Text(s.label, style: style, maxLines: 1, overflow: TextOverflow.ellipsis)),
                ]),
              ),
            ),
          ),
      ]);
    });

    return Container(
      padding: const EdgeInsets.fromLTRB(12, 14, 12, 12),
      decoration: _frame,
      child: Column(children: [
        if ((widget.data['title'] as String?)?.isNotEmpty == true)
          Padding(
            padding: const EdgeInsets.only(bottom: 4),
            child: Text(widget.data['title'] as String,
                textAlign: TextAlign.center,
                style: const TextStyle(fontWeight: FontWeight.w700, color: Color(0xFF1A365D), fontSize: 14)),
          ),
        chart,
        const SizedBox(height: 6),
        legend,
      ]),
    );
  }
}

/// Hình học của donut: góc từng lát + vị trí nhãn ngoài (né chồng chữ như Plotly).
class _PieGeo {
  final List<_Slice> slices;
  final Size size;
  final double hole;
  final String info;
  final bool outside;
  late final double total;
  late final Offset center;
  late final double r;
  final List<(double, double)> arcs = []; // (bắt đầu, độ quét) — radian, chiều kim đồng hồ dương
  final List<(TextPainter, Offset, Offset, Offset)> labels = []; // chữ, góc trên-trái, điểm mép lát, điểm gãy

  final String? font;

  _PieGeo(this.slices, this.size, this.hole, this.info, this.outside, this.font) {
    final style = TextStyle(fontSize: 12, color: _PieChartViewState._labelColor, height: 1.2, fontFamily: font);
    total = slices.fold<double>(0, (a, s) => a + s.value);
    center = size.center(Offset.zero);
    // chữ từng lát
    final texts = <TextPainter>[];
    for (final s in slices) {
      final parts = <String>[
        if (info.contains('label')) s.label,
        if (info.contains('value')) _fmt(s.value),
        if (info.contains('percent')) plotlyPct(total > 0 ? s.value / total : 0),
      ];
      texts.add(TextPainter(
          text: TextSpan(text: parts.join('\n'), style: style),
          textAlign: TextAlign.center,
          textDirection: TextDirection.ltr)
        ..layout(maxWidth: math.max(90, size.width * 0.36)));
    }
    final maxW = texts.fold<double>(0, (a, t) => math.max(a, t.width));
    final byW = outside ? (size.width - 2 * maxW - 40) / 2 : size.width / 2 - 10;
    r = math.max(50, math.min(size.height / 2 - 34, byW));
    if (total <= 0) return;
    // Plotly: lát đầu từ 12 giờ theo chiều kim đồng hồ, các lát sau nối tiếp ngược chiều từ 12 giờ
    const top = -math.pi / 2;
    var ccw = top;
    for (var k = 0; k < slices.length; k++) {
      final sweep = slices[k].value / total * 2 * math.pi;
      if (k == 0) {
        arcs.add((top, sweep));
      } else {
        ccw -= sweep;
        arcs.add((ccw, sweep));
      }
    }
    if (!outside) {
      for (var k = 0; k < slices.length; k++) {
        final mid = arcs[k].$1 + arcs[k].$2 / 2;
        final rr = r * (1 + hole) / 2;
        final p = center + Offset(math.cos(mid), math.sin(mid)) * rr;
        labels.add((texts[k], p - Offset(texts[k].width / 2, texts[k].height / 2), p, p));
      }
      return;
    }
    // nhãn ngoài: đặt ở góc giữa lát, mỗi bên (trái/phải) đẩy xuống cho khỏi chồng nhau
    final items = <(int, double, Offset)>[]; // k, góc giữa, điểm neo
    for (var k = 0; k < slices.length; k++) {
      final mid = arcs[k].$1 + arcs[k].$2 / 2;
      items.add((k, mid, center + Offset(math.cos(mid), math.sin(mid)) * (r + 14)));
    }
    final placed = List<Offset?>.filled(slices.length, null);
    for (final right in [true, false]) {
      final side = items.where((e) => (math.cos(e.$2) >= 0) == right).toList()
        ..sort((a, b) => a.$3.dy.compareTo(b.$3.dy));
      var lastBottom = -double.infinity;
      for (final e in side) {
        final tp = texts[e.$1];
        var y = e.$3.dy - tp.height / 2;
        if (y < lastBottom + 2) y = lastBottom + 2;
        lastBottom = y + tp.height;
        final x = right ? e.$3.dx : e.$3.dx - tp.width;
        placed[e.$1] = Offset(x, y);
      }
      // tràn đáy → kéo cả cụm lên
      final overflow = lastBottom - size.height;
      if (overflow > 0) {
        for (final e in side) {
          placed[e.$1] = placed[e.$1]! - Offset(0, overflow);
        }
      }
    }
    for (var k = 0; k < slices.length; k++) {
      final mid = items[k].$2;
      final edge = center + Offset(math.cos(mid), math.sin(mid)) * r;
      final tp = texts[k];
      final pos = placed[k]!;
      final right = math.cos(mid) >= 0;
      final elbow = Offset(right ? pos.dx - 2 : pos.dx + tp.width + 2, pos.dy + tp.height / 2);
      labels.add((tp, pos, edge, elbow));
    }
  }

  int? hit(Offset p) {
    final d = p - center;
    final dist = d.distance;
    if (dist > r || dist < r * hole || total <= 0) return null;
    final a = math.atan2(d.dy, d.dx);
    for (var k = 0; k < arcs.length; k++) {
      var x = a - arcs[k].$1;
      while (x < 0) {
        x += 2 * math.pi;
      }
      while (x >= 2 * math.pi) {
        x -= 2 * math.pi;
      }
      if (x <= arcs[k].$2) return k;
    }
    return null;
  }
}

class _PiePainter extends CustomPainter {
  final _PieGeo g;
  _PiePainter(this.g);

  @override
  void paint(Canvas canvas, Size size) {
    if (g.total <= 0) return;
    final rect = Rect.fromCircle(center: g.center, radius: g.r);
    for (var k = 0; k < g.arcs.length; k++) {
      final (start, sweep) = g.arcs[k];
      canvas.drawArc(rect, start, sweep, true, Paint()..color = g.slices[k].color);
    }
    for (var k = 0; k < g.arcs.length; k++) {
      final (start, sweep) = g.arcs[k];
      canvas.drawArc(rect, start, sweep, true,
          Paint()
            ..color = Colors.white
            ..style = PaintingStyle.stroke
            ..strokeWidth = 1);
    }
    if (g.hole > 0) canvas.drawCircle(g.center, g.r * g.hole, Paint()..color = Colors.white);
    final line = Paint()
      ..color = _PieChartViewState._labelColor
      ..strokeWidth = 1;
    for (final (tp, pos, edge, elbow) in g.labels) {
      // đường dẫn khi chữ bị đẩy xa khỏi lát (như Plotly)
      if (g.outside && (elbow - edge).distance > 18) {
        canvas.drawLine(edge, elbow, line);
      }
      tp.paint(canvas, pos);
    }
  }

  @override
  bool shouldRepaint(_PiePainter old) => true;
}
