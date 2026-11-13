import 'dart:math' as math;

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

List<InlineSpan> runSpans(List runs, {Color? color, double? size, BuildContext? ctx}) => [
      for (final r in runs.cast<Map>())
        TextSpan(
          text: r['x'] as String,
          style: TextStyle(
            fontWeight: r['b'] == 1 ? FontWeight.w700 : null,
            fontStyle: r['i'] == 1 ? FontStyle.italic : null,
            color: (ctx != null ? adaptFg(ctx, hexColor(r['c'])) : hexColor(r['c'])) ?? color,
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
            TextSpan(children: runSpans(it['r'] as List, color: adaptFg(context, Brand.blue), ctx: context)),
            textAlign: lv <= 3 ? TextAlign.center : _align(it['al']),
            style: TextStyle(
              fontSize: lv <= 2 ? 18 : (lv == 3 ? 16 : 14),
              fontWeight: FontWeight.w800,
              color: adaptFg(context, Brand.blue),
            ),
          ),
        );
      case 'p':
        final cap = it['cap'] == 1;
        final li = it['li'] == 1;
        final text = Text.rich(
          TextSpan(children: runSpans(it['r'] as List, ctx: context)),
          textAlign: cap ? TextAlign.center : _align(it['al']),
          style: TextStyle(
            fontSize: cap ? 12 : 13,
            height: 1.45,
            color: cap ? mutedText(context) : (isDark(context) ? Brand.darkText : const Color(0xFF1A202C)),
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
        final boxBg = adaptBg(context, hexColor(it['bg']), dark: Brand.darkPanelBg) ??
            (isDark(context) ? Brand.darkPanelBg : const Color(0xFFF0F7FF));
        return Container(
          margin: const EdgeInsets.symmetric(vertical: 8),
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: boxBg,
            borderRadius: BorderRadius.circular(8),
            border: Border(left: BorderSide(color: bd, width: 4)),
          ),
          child: keepLight(
            context,
            boxBg,
            DefaultTextStyle.merge(
              style: TextStyle(color: isDark(context) ? Brand.darkText : const Color(0xFF1A202C)),
              child: ReportItems(items: (it['ch'] as List).cast<Map<String, dynamic>>(), wide: wide),
            ),
          ),
        );
      case 'exp':
        // Mục thu gọn (st.expander của App.py, vd Kết quả ngày theo từng NV): mặc định chỉ hiện tiêu đề
        final expDark = isDark(context);
        return Container(
          margin: const EdgeInsets.symmetric(vertical: 4),
          decoration: BoxDecoration(
            color: expDark ? Brand.darkPanelBg : Colors.white,
            borderRadius: BorderRadius.circular(8),
            border: Border.all(color: expDark ? Brand.darkTileBorder : const Color(0xFFCBD5E0)),
          ),
          child: Theme(
            data: Theme.of(context).copyWith(dividerColor: Colors.transparent),
            child: ExpansionTile(
              initiallyExpanded: it['open'] == true,
              tilePadding: const EdgeInsets.symmetric(horizontal: 12),
              childrenPadding: const EdgeInsets.fromLTRB(8, 0, 8, 8),
              iconColor: expDark ? Brand.darkText : null,
              collapsedIconColor: expDark ? Brand.darkText : null,
              title: Text(it['title'] as String? ?? '',
                  style: TextStyle(
                      fontSize: 14, fontWeight: FontWeight.w700, color: expDark ? Brand.darkText : const Color(0xFF1A365D))),
              children: [ReportItems(items: (it['ch'] as List).cast<Map<String, dynamic>>(), wide: wide)],
            ),
          ),
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

  /// Số thẻ / hàng: chia đều các hàng (16 thẻ → 2 hàng × 8, 18 → 3 × 6, 2 → 2 thẻ rộng nửa màn hình),
  /// mỗi thẻ rộng tối thiểu ~170px; điện thoại 2 thẻ / hàng.
  static int perRowFor(int n, double width, bool wide) {
    if (n <= 1) return 1;
    final maxCols = wide ? (width / 170).floor().clamp(2, 8) : 2;
    final rows = (n / maxCols).ceil();
    return (n / rows).ceil();
  }

  @override
  Widget build(BuildContext context) {
    // thẻ 'full' (vd SELL OUT BY CAT): rộng cả hàng, nằm dưới cùng
    final cards = [for (final c in this.cards) if (c['full'] == null) c];
    final full = [for (final c in this.cards) if (c['full'] != null) c];
    return LayoutBuilder(builder: (ctx, c) {
      final perRow = perRowFor(cards.length, c.maxWidth, wide);
      final w = (c.maxWidth - 8 * (perRow - 1)) / perRow;
      return Column(children: [
        for (var i = 0; i < cards.length; i += perRow)
          Padding(
            padding: EdgeInsets.only(top: i == 0 ? 0 : 8),
            // cùng hàng cao bằng nhau; hàng thiếu thẻ: giữ độ rộng, căn giữa
            child: IntrinsicHeight(
              child: Row(mainAxisAlignment: MainAxisAlignment.center, crossAxisAlignment: CrossAxisAlignment.stretch, children: [
                for (var j = i; j < math.min(i + perRow, cards.length); j++) ...[
                  if (j > i) const SizedBox(width: 8),
                  SizedBox(width: w, child: _card(context, cards[j])),
                ],
              ]),
            ),
          ),
        for (final (k, f) in full.indexed)
          Padding(
            padding: EdgeInsets.only(top: cards.isEmpty && k == 0 ? 0 : 8),
            child: SizedBox(width: c.maxWidth, child: _card(context, f)),
          ),
      ]);
    });
  }

  Widget _card(BuildContext context, Map<String, dynamic> card) {
    // giao diện Tối mà thẻ giữ nền màu nhạt mang nghĩa (vd xanh lá "Đã đạt") → vẽ cả thẻ như giao diện Sáng
    final rawBg = hexColor(card['bg']);
    if (isDark(context) && rawBg != null && rawBg.computeLuminance() > 0.6 && adaptBg(context, rawBg) == rawBg) {
      return Theme(data: buildTheme(Brightness.light), child: Builder(builder: (c) => _card(c, card)));
    }
    final dark = isDark(context);
    // 1 dòng, tự co chữ cho vừa thẻ (tiêu đề / dòng phụ ngắn)
    Widget fit(Widget t) => FittedBox(fit: BoxFit.scaleDown, child: t);
    final sv = {for (final i in (card['sv'] as List? ?? const [])) (i as num).toInt()};
    // số ngắn: to, tự co cho vừa thẻ; nội dung dài (vd "OFF: 458/1188 CH ... ON: ..."):
    // cỡ vừa, xuống dòng — tránh chữ bị co quá nhỏ
    Widget value(String v) {
      final color = adaptFg(context, hexColor(card['c'])) ??
          (card['ac'] != null ? (dark ? Brand.darkText : const Color(0xFF1A202C)) : adaptFg(context, Brand.cardText)!);
      final long = v.length > 22 || v.contains('\n');
      final text = Text(v,
          textAlign: TextAlign.center,
          style: TextStyle(
              color: color,
              fontWeight: FontWeight.w800,
              fontSize: long ? 14 : 20,
              height: long ? 1.35 : null,
              fontFeatures: const [FontFeature.tabularFigures()]));
      return long ? text : fit(text);
    }

    final cardBg = adaptBg(context, hexColor(card['bg'])) ?? (dark ? Brand.darkTileBg : Brand.cardBg);
    return keepLight(context, cardBg, Container(
      padding: EdgeInsets.fromLTRB(8, card['ac'] != null ? 13 : 10, 8, 10),
      decoration: BoxDecoration(
        color: cardBg,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: dark ? Brand.darkTileBorder : Brand.cardBorder),
        // vạch màu nhấn ở mép trên (border-top-color của App.py)
        gradient: card['ac'] != null
            ? LinearGradient(
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
                stops: const [0, 0.035, 0.035],
                colors: [
                  hexColor(card['ac'])!,
                  hexColor(card['ac'])!,
                  cardBg,
                ],
              )
            : null,
      ),
      child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
        if (card['grid'] is List) ...[
          // thẻ nhiều cột: tiêu đề + các cột "nhãn — số" (tự co vừa ô) + chú thích
          fit(Text(card['l'] as String,
              maxLines: 1,
              style: TextStyle(
                  color: adaptFg(context, hexColor(card['ac']) ?? Brand.cardText),
                  fontWeight: FontWeight.w800,
                  fontSize: 12.5))),
          const SizedBox(height: 6),
          Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
            for (final (ci, col) in (card['grid'] as List).indexed) ...[
              if (ci > 0) const SizedBox(width: 20),
              Expanded(
                child: Column(children: [
                  for (final r in (col as List))
                    Container(
                      padding: const EdgeInsets.symmetric(vertical: 3),
                      decoration:
                          BoxDecoration(border: Border(bottom: BorderSide(color: dark ? Brand.darkTileBorder : Brand.cardBorder))),
                      child: Row(children: [
                        Expanded(
                            child: Align(
                                alignment: Alignment.centerLeft,
                                child: fit(Text('${(r as List)[0]}',
                                    style: TextStyle(
                                        fontWeight: FontWeight.w700, color: mutedText(context), fontSize: 13))))),
                        const SizedBox(width: 8),
                        Flexible(
                            child: fit(Text('${r[1]}',
                                style: TextStyle(
                                    fontWeight: FontWeight.w800,
                                    fontSize: 16,
                                    color: dark ? Brand.darkText : const Color(0xFF1A202C), // số TH/CT/%
                                    fontFeatures: const [FontFeature.tabularFigures()])))),
                      ]),
                    ),
                ]),
              ),
            ],
          ]),
          for (final s in (card['s'] as List? ?? const []))
            Padding(
                padding: const EdgeInsets.only(top: 4),
                child: fit(Text('$s', style: TextStyle(fontSize: 11.5, color: mutedText(context))))),
        ] else ...[
        // tiêu đề: mỗi dòng (xuống dòng bằng <br> bên App.py) tự co vừa 1 dòng
        for (final line in (card['l'] as String).split('\n'))
          fit(Text(line,
              textAlign: TextAlign.center,
              maxLines: 1,
              style: TextStyle(
                  color: adaptFg(context, hexColor(card['ac']) ?? hexColor(card['c']) ?? Brand.cardText),
                  fontWeight: FontWeight.w800,
                  fontSize: 12.5))),
        const SizedBox(height: 4),
        value(card['v'] as String),
        for (final (i, s) in (card['s'] as List? ?? const []).indexed)
          if (sv.contains(i))
            // dòng số phụ (vd DS Combo/DS Ngày/%): cùng cỡ/màu dòng số chính, tự co vừa thẻ
            Padding(padding: const EdgeInsets.only(top: 6), child: value(s as String))
          else
            Padding(
              padding: const EdgeInsets.only(top: 2),
              child: () {
                final t = Text(s as String,
                    textAlign: TextAlign.center, style: TextStyle(fontSize: 11.5, color: mutedText(context)));
                return (s.length <= 40 && !s.contains('\n')) ? fit(t) : t;
              }(),
            ),
        ],
      ]),
    ));
  }
}
