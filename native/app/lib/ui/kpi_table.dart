import 'package:flutter/material.dart';

import '../logic/turnover_logic.dart';
import 'theme.dart';

/// Bảng KPI kiểu render_html_table: STT + Tên NVBH cố định bên trái,
/// các cột số cuộn ngang; dòng Tổng nền navy; cột % tô màu theo mốc.
class TurnoverTable extends StatelessWidget {
  final TurnoverReport report;
  const TurnoverTable({super.key, required this.report});

  static const _rowH = 40.0;
  static const _cols = <(String, double, TextAlign)>[
    ('Chỉ Tiêu Doanh Số', 140, TextAlign.right),
    ('Thực Hiện Ngày', 124, TextAlign.right),
    ('Doanh Số MTD', 136, TextAlign.right),
    ('% MTD', 82, TextAlign.center),
    ('GAP', 136, TextAlign.right),
    ('Bình quân ngày', 136, TextAlign.right),
  ];

  @override
  Widget build(BuildContext context) {
    final rows = [...report.rows, report.total];
    final display = [for (final r in rows) r.display()];
    // Giống _col_width: max(150, min(260, len*9+24)) — thu nhỏ chút cho điện thoại.
    final maxName = rows.fold<int>(12, (m, r) => r.name.length > m ? r.name.length : m);
    final nameW = (maxName * 8.0 + 24).clamp(150.0, 240.0);
    final moc = report.colorMoc;

    Widget header(String text, double w, {bool shadow = false}) => Container(
          width: w,
          height: _rowH,
          alignment: Alignment.center,
          padding: const EdgeInsets.symmetric(horizontal: 6),
          decoration: BoxDecoration(
            color: Brand.navy,
            border: Border.all(color: Brand.border, width: 0.5),
          ),
          child: Text(text,
              textAlign: TextAlign.center,
              maxLines: 2,
              style: const TextStyle(
                  color: Colors.white, fontWeight: FontWeight.w800, fontSize: 11.5, height: 1.1)),
        );

    Color rowBg(int i, bool total) => total ? Brand.navy : (i % 2 == 0 ? Brand.zebra : Colors.white);
    Color rowFg(bool total) => total ? Colors.white : const Color(0xFF1A202C);

    Widget cell(String text, double w, TextAlign align, int i, TurnoverRow r,
        {bool bold = false, Color? bg, Color? fg}) {
      return Container(
        width: w,
        height: _rowH,
        padding: const EdgeInsets.symmetric(horizontal: 8),
        alignment: switch (align) {
          TextAlign.center => Alignment.center,
          TextAlign.right => Alignment.centerRight,
          _ => Alignment.centerLeft,
        },
        decoration: BoxDecoration(
          color: bg ?? rowBg(i, r.isTotal),
          border: Border.all(
              color: r.isTotal ? Brand.border : Brand.cellBorder, width: 0.5),
        ),
        child: Text(
          text,
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
          style: TextStyle(
            fontSize: 12.5,
            color: fg ?? rowFg(r.isTotal),
            fontWeight: r.isTotal ? FontWeight.w900 : (bold ? FontWeight.w700 : FontWeight.w500),
            fontFeatures: const [FontFeature.tabularFigures()],
          ),
        ),
      );
    }

    final frozen = Column(
      children: [
        Row(children: [header('STT', 44), header('Tên NVBH', nameW)]),
        for (var i = 0; i < rows.length; i++)
          Row(children: [
            cell(display[i]['STT']!, 44, TextAlign.center, i, rows[i]),
            cell(display[i]['Tên NVBH']!, nameW, TextAlign.left, i, rows[i], bold: true),
          ]),
      ],
    );

    final scrollable = Column(
      children: [
        Row(children: [for (final c in _cols) header(c.$1, c.$2)]),
        for (var i = 0; i < rows.length; i++)
          Row(children: [
            for (final c in _cols)
              if (c.$1 == '% MTD')
                () {
                  final (bg, fg) = pctColors(pctColor(rows[i].pct, moc));
                  return cell(display[i][c.$1]!, c.$2, c.$3, i, rows[i],
                      bold: true, bg: bg, fg: fg);
                }()
              else
                cell(display[i][c.$1]!, c.$2, c.$3, i, rows[i]),
          ]),
      ],
    );

    return ClipRRect(
      borderRadius: BorderRadius.circular(6),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          DecoratedBox(
            decoration: const BoxDecoration(boxShadow: [
              BoxShadow(color: Color(0x38000000), blurRadius: 5, offset: Offset(3, 0), spreadRadius: -2)
            ]),
            child: frozen,
          ),
          Expanded(
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: scrollable,
            ),
          ),
        ],
      ),
    );
  }
}
