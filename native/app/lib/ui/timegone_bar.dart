import 'dart:math' as math;

import 'package:flutter/material.dart';

import '../logic/turnover_logic.dart';
import 'theme.dart';

/// Ngày nghỉ lễ theo tháng — giống get_timegone_stats() của App.py (trừ Chủ nhật + lễ).
const _holidays = {
  (2026, 9): {1, 2},
};

/// (tổng ngày bán, đã qua, còn lại, % timegone) của tháng chứa [d] tính tới hết ngày [d].
(int, int, int, double) timegoneStats(DateTime d) {
  final hol = _holidays[(d.year, d.month)] ?? const <int>{};
  final last = DateTime(d.year, d.month + 1, 0).day;
  var total = 0, elapsed = 0;
  for (var day = 1; day <= last; day++) {
    final cur = DateTime(d.year, d.month, day);
    if (cur.weekday == DateTime.sunday || hol.contains(day)) continue;
    total++;
    if (day <= d.day) elapsed++;
  }
  final pct = total == 0 ? 0.0 : (elapsed / total * 1000).round() / 10;
  return (total, elapsed, total - elapsed, pct);
}

String _pct(double v) {
  final s = v.toStringAsFixed(1).replaceAll('.', ',');
  return s.endsWith(',0') ? s.substring(0, s.length - 2) : s;
}

/// % MTD tổng của báo cáo: thẻ số đầu tiên có nhãn "% MTD" (Turnover, PC BT, ASO, LPPC…).
double? reportPctMtd(List<Map<String, dynamic>> items) {
  double? found;
  void walk(List<dynamic> list) {
    for (final i in list) {
      if (found != null || i is! Map) return;
      if (i['t'] == 'cards') {
        for (final c in (i['it'] as List? ?? const [])) {
          final l = '${(c as Map)['l'] ?? ''}'.replaceAll(' ', '').toUpperCase();
          if (!l.contains('%MTD')) continue;
          final m = RegExp(r'-?\d+(?:[.,]\d+)?').firstMatch('${c['v'] ?? ''}');
          if (m != null) {
            found = double.tryParse(m.group(0)!.replaceAll(',', '.'));
            return;
          }
        }
      }
      for (final k in ['ch', 'items']) {
        if (i[k] is List) walk(i[k] as List);
      }
    }
  }

  walk(items);
  return found;
}

/// Thanh tiến độ thời gian (mẫu C): % MTD của báo cáo so với timegone của ngày báo cáo.
class TimegoneBar extends StatelessWidget {
  final DateTime date;
  final double? pctMtd;
  const TimegoneBar({super.key, required this.date, this.pctMtd});

  static const _red = Color(0xFFE53E3E), _green = Color(0xFF38A169), _purple = Color(0xFF805AD5);
  static const _orange = Color(0xFFED8936), _yellow = Color(0xFFD69E2E);

  @override
  Widget build(BuildContext context) {
    final dark = isDark(context);
    final (total, elapsed, remain, tg) = timegoneStats(date);
    final moc = math.min(tg, 95.0); // mốc tô màu như App: theo timegone, tối đa 95%
    final p = pctMtd;
    final c = p == null ? null : pctColor(p, moc);
    final fill = switch (c) {
      PctColor.red => _red,
      PctColor.green => _green,
      PctColor.purple => _purple,
      null => _orange,
    };
    final text = dark ? Brand.darkText : Brand.navy;
    final muted = mutedText(context);
    final diff = p == null ? 0.0 : p - tg;
    final status = p == null
        ? null
        : (diff < 0
            ? '· chậm ${_pct(-diff)}% so với timegone'
            : '· vượt ${_pct(diff)}% so với timegone');
    final statusColor = p == null
        ? muted
        : (diff < 0 ? (dark ? const Color(0xFFFC8181) : _red) : (dark ? const Color(0xFF9AE6B4) : _green));
    final tgColor = dark ? const Color(0xFFF6E05E) : _yellow;
    final width = (p ?? tg).clamp(0, 100) / 100;

    return Container(
      margin: const EdgeInsets.only(top: 10),
      padding: const EdgeInsets.fromLTRB(12, 10, 12, 9),
      decoration: BoxDecoration(
        color: dark ? Brand.darkTileBg : Colors.white,
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: dark ? Brand.darkTileBorder : Brand.cardBorder),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            crossAxisAlignment: CrossAxisAlignment.end,
            children: [
              Expanded(
                child: Text.rich(
                  TextSpan(children: [
                    TextSpan(
                      text: p == null ? 'Tiến độ thời gian tháng ${date.month}' : '% MTD ${_pct(p)}%  ',
                      style: TextStyle(color: text, fontWeight: FontWeight.w700),
                    ),
                    if (status != null)
                      TextSpan(text: status, style: TextStyle(color: statusColor, fontWeight: FontWeight.w600)),
                  ]),
                  style: const TextStyle(fontSize: 13),
                ),
              ),
              Text(
                'Timegone ${_pct(tg)}%',
                style: TextStyle(color: tgColor, fontWeight: FontWeight.w800, fontSize: 13.5),
              ),
            ],
          ),
          const SizedBox(height: 7),
          LayoutBuilder(builder: (ctx, box) {
            final w = box.maxWidth;
            return SizedBox(
              height: 16,
              child: Stack(clipBehavior: Clip.none, children: [
                Positioned(
                  left: 0, right: 0, top: 3, height: 10,
                  child: Container(
                    decoration: BoxDecoration(
                      color: dark ? Brand.darkTileBorder : const Color(0xFFE2E8F0),
                      borderRadius: BorderRadius.circular(5),
                    ),
                  ),
                ),
                Positioned(
                  left: 0, top: 3, height: 10, width: w * width,
                  child: Container(decoration: BoxDecoration(color: fill, borderRadius: BorderRadius.circular(5))),
                ),
                if (p != null)
                  Positioned(
                    left: (w * tg / 100).clamp(0, w - 2),
                    top: -1, width: 2.5, height: 18,
                    child: Container(color: dark ? Colors.white : Brand.navy),
                  ),
              ]),
            );
          }),
          const SizedBox(height: 5),
          Text(
            'Đã qua $elapsed / $total ngày bán · còn $remain ngày '
            '(tính tới ${date.day.toString().padLeft(2, '0')}/${date.month.toString().padLeft(2, '0')})',
            style: TextStyle(color: muted, fontSize: 12),
          ),
        ],
      ),
    );
  }
}
