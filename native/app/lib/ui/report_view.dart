import 'package:flutter/material.dart';

import 'charts.dart';
import 'filter_widgets.dart';
import 'report_table.dart';
import 'theme.dart';

/// Vẽ native danh sách item do pipeline/report_doc.py xuất ra từ App.py.
Color? hexColor(Object? v) {
  if (v is! String || !v.startsWith('#') || v.length < 7) return null;
  final n = int.tryParse(v.substring(1, 7), radix: 16);
  return n == null ? null : Color(0xFF000000 | n);
}

TextAlign _align(Object? a) => switch (a) {
      'c' => TextAlign.center,
      'r' => TextAlign.right,
      _ => TextAlign.left,
    };

List<InlineSpan> runSpans(List runs, {Color? color, double? size}) => [
      for (final r in runs.cast<Map>())
        TextSpan(
          text: r['x'] as String,
          style: TextStyle(
            fontWeight: r['b'] == 1 ? FontWeight.w700 : null,
            fontStyle: r['i'] == 1 ? FontStyle.italic : null,
            color: hexColor(r['c']) ?? color,
            fontSize: size,
          ),
        )
    ];

class ReportItems extends StatelessWidget {
  final List<Map<String, dynamic>> items;
  final bool wide;
  const ReportItems({super.key, required this.items, required this.wide});

  @override
  Widget build(BuildContext context) {
    // tiêu đề gần nhất phía trên mỗi bảng → tên bảng khi xem toàn màn hình
    String? lastTitle;
    final children = <Widget>[];
    for (final it in items) {
      if (it['t'] == 'h') {
        lastTitle = (it['r'] as List).map((r) => (r as Map)['x']).join().trim();
      }
      children.add(_item(context, it, lastTitle));
    }
    return Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: children);
  }

  Widget _item(BuildContext context, Map<String, dynamic> it, String? title) {
    switch (it['t']) {
      case 'h':
        final lv = (it['lv'] as int?) ?? 3;
        return Padding(
          padding: EdgeInsets.only(top: lv <= 3 ? 10 : 14, bottom: 6),
          child: Text.rich(
            TextSpan(children: runSpans(it['r'] as List, color: Brand.blue)),
            textAlign: lv <= 3 ? TextAlign.center : _align(it['al']),
            style: TextStyle(
              fontSize: lv <= 2 ? 18 : (lv == 3 ? 16 : 14),
              fontWeight: FontWeight.w800,
              color: Brand.blue,
            ),
          ),
        );
      case 'p':
        final cap = it['cap'] == 1;
        final li = it['li'] == 1;
        final text = Text.rich(
          TextSpan(children: runSpans(it['r'] as List)),
          textAlign: cap ? TextAlign.center : _align(it['al']),
          style: TextStyle(
            fontSize: cap ? 12 : 13,
            height: 1.45,
            color: cap ? Brand.muted : const Color(0xFF1A202C),
          ),
        );
        return Padding(
          padding: const EdgeInsets.symmetric(vertical: 3),
          child: li
              ? Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  const Padding(padding: EdgeInsets.only(right: 6, top: 1), child: Text('•')),
                  Expanded(child: text),
                ])
              : text,
        );
      case 'box':
        final bd = hexColor(it['bd']) ?? Brand.blue;
        return Container(
          margin: const EdgeInsets.symmetric(vertical: 8),
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: hexColor(it['bg']) ?? const Color(0xFFF0F7FF),
            borderRadius: BorderRadius.circular(8),
            border: Border(left: BorderSide(color: bd, width: 4)),
          ),
          child: ReportItems(items: (it['ch'] as List).cast<Map<String, dynamic>>(), wide: wide),
        );
      case 'cards':
        return Padding(
          padding: const EdgeInsets.symmetric(vertical: 6),
          child: _Cards(cards: (it['it'] as List).cast<Map<String, dynamic>>(), wide: wide),
        );
      case 'msg':
        final (bg, fg, icon) = switch (it['lv']) {
          'error' => (const Color(0xFFFED7D7), const Color(0xFF742A2A), Icons.error_outline),
          'warning' => (const Color(0xFFFEFCBF), const Color(0xFF744210), Icons.warning_amber),
          'success' => (const Color(0xFFC6F6D5), const Color(0xFF22543D), Icons.check_circle_outline),
          _ => (const Color(0xFFEBF8FF), const Color(0xFF2A4365), Icons.info_outline),
        };
        return Container(
          margin: const EdgeInsets.symmetric(vertical: 6),
          padding: const EdgeInsets.all(10),
          decoration: BoxDecoration(color: bg, borderRadius: BorderRadius.circular(6)),
          child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Icon(icon, size: 18, color: fg),
            const SizedBox(width: 8),
            Expanded(child: Text(it['x'] as String, style: TextStyle(color: fg, fontSize: 13))),
          ]),
        );
      case 'tbl':
        return Padding(
          padding: const EdgeInsets.symmetric(vertical: 6),
          child: ReportTable(data: it, title: title),
        );
      case 'filters':
        return StreamlitFilterGroup(item: it);
      case 'bar':
        return Padding(padding: const EdgeInsets.symmetric(vertical: 8), child: BarChartView(data: it));
      case 'pie':
        return Padding(padding: const EdgeInsets.symmetric(vertical: 8), child: PieChartView(data: it));
      default:
        return const SizedBox.shrink();
    }
  }
}

class _Cards extends StatelessWidget {
  final List<Map<String, dynamic>> cards;
  final bool wide;
  const _Cards({required this.cards, required this.wide});

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(builder: (ctx, c) {
      final perRow = wide ? (cards.length >= 6 ? 6 : 4) : 2;
      final w = (c.maxWidth - 8 * (perRow - 1)) / perRow;
      return Wrap(spacing: 8, runSpacing: 8, children: [
        for (final card in cards)
          Container(
            width: w,
            padding: EdgeInsets.fromLTRB(8, card['ac'] != null ? 13 : 10, 8, 10),
            decoration: BoxDecoration(
              color: hexColor(card['bg']) ?? Brand.cardBg,
              borderRadius: BorderRadius.circular(8),
              border: Border.all(color: Brand.cardBorder),
              // vạch màu nhấn ở mép trên (border-top-color của App.py)
              gradient: card['ac'] != null
                  ? LinearGradient(
                      begin: Alignment.topCenter,
                      end: Alignment.bottomCenter,
                      stops: const [0, 0.035, 0.035],
                      colors: [hexColor(card['ac'])!, hexColor(card['ac'])!, hexColor(card['bg']) ?? Colors.white],
                    )
                  : null,
            ),
            child: Column(children: [
              Text(card['l'] as String,
                  textAlign: TextAlign.center,
                  style: TextStyle(
                      color: hexColor(card['ac']) ?? hexColor(card['c']) ?? Brand.cardText,
                      fontWeight: FontWeight.w800,
                      fontSize: 12.5)),
              const SizedBox(height: 4),
              // số ngắn: to, tự co cho vừa thẻ; nội dung dài (vd "OFF: 458/1188 CH ... ON: ..."):
              // cỡ vừa, xuống dòng — tránh chữ bị co quá nhỏ
              () {
                final v = card['v'] as String;
                final color = hexColor(card['c']) ?? (card['ac'] != null ? const Color(0xFF1A202C) : Brand.cardText);
                final long = v.length > 22 || v.contains('\n');
                final text = Text(v,
                    textAlign: TextAlign.center,
                    style: TextStyle(
                        color: color,
                        fontWeight: FontWeight.w800,
                        fontSize: long ? 14 : 20,
                        height: long ? 1.35 : null,
                        fontFeatures: const [FontFeature.tabularFigures()]));
                return long ? text : FittedBox(fit: BoxFit.scaleDown, child: text);
              }(),
              for (final s in (card['s'] as List? ?? const []))
                Padding(
                  padding: const EdgeInsets.only(top: 2),
                  child: Text(s as String,
                      textAlign: TextAlign.center, style: const TextStyle(fontSize: 11.5, color: Brand.muted)),
                ),
            ]),
          ),
      ]);
    });
  }
}
