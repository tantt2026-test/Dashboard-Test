import 'dart:math' as math;

import 'package:flutter/material.dart';
import 'package:two_dimensional_scrollables/two_dimensional_scrollables.dart';

import 'report_view.dart' show hexColor;
import 'theme.dart';

/// Bảng từ report_doc.py: dòng tiêu đề + cột đầu cố định, gộp ô (colspan/rowspan),
/// màu từng ô như Streamlit. Vẽ lười (chỉ phần đang thấy) nên bảng 600+ dòng vẫn mượt.
class ReportTable extends StatelessWidget {
  final Map<String, dynamic> data;
  const ReportTable({super.key, required this.data});

  @override
  Widget build(BuildContext context) {
    final g = _Grid.build(data);
    if (g.rows == 0 || g.cols == 0) return const SizedBox.shrink();
    final total = g.rowH.fold<double>(0, (a, b) => a + b);
    // Bảng vừa: hiện đủ chiều cao (vuốt là cuộn cả trang). Bảng dài (>60 dòng):
    // khung cao ~75% màn hình, cuộn bên trong, dòng tiêu đề đứng yên.
    final screen = MediaQuery.of(context).size.height;
    final height = g.rows <= 60 ? total + 2 : math.min(total + 2, screen * 0.75);

    return Container(
      height: height,
      decoration: BoxDecoration(
        border: Border.all(color: Brand.cellBorder),
        borderRadius: BorderRadius.circular(6),
      ),
      clipBehavior: Clip.antiAlias,
      child: TableView.builder(
        pinnedRowCount: g.headRows,
        pinnedColumnCount: g.frozen,
        rowCount: g.rows,
        columnCount: g.cols,
        diagonalDragBehavior: DiagonalDragBehavior.free,
        columnBuilder: (i) => TableSpan(extent: FixedTableSpanExtent(g.colW[i])),
        rowBuilder: (i) => TableSpan(extent: FixedTableSpanExtent(g.rowH[i])),
        cellBuilder: (ctx, v) => g.cell(v.row, v.column),
      ),
    );
  }
}

class _Placed {
  final Map<String, dynamic> c;
  final int r, col, rs, cs;
  final bool head, total;
  final int bodyIndex;
  _Placed(this.c, this.r, this.col, this.rs, this.cs, this.head, this.total, this.bodyIndex);
}

class _Grid {
  int rows = 0, cols = 0, headRows = 0, frozen = 0;
  late List<double> colW, rowH;
  late List<List<_Placed?>> at; // ô gốc phủ (r, c)

  static _Grid build(Map<String, dynamic> d) {
    final g = _Grid();
    final head = (d['h'] as List).cast<List>();
    final body = (d['b'] as List).cast<List>();
    final all = [...head, ...body];
    g.headRows = head.length;
    g.rows = all.length;

    // Đặt ô theo colspan/rowspan như trình duyệt
    final occ = <int, Set<int>>{};
    final placed = <_Placed>[];
    for (var r = 0; r < all.length; r++) {
      final isHead = r < head.length;
      final row = all[r].cast<Map<String, dynamic>>();
      final firstText = row.isNotEmpty ? '${row.first['x']} ${row.length > 1 ? row[1]['x'] : ''}' : '';
      final total = !isHead && RegExp(r'TỔNG|TOTAL', caseSensitive: false).hasMatch(firstText);
      var c = 0;
      for (final cell in row) {
        while (occ[r]?.contains(c) ?? false) {
          c++;
        }
        final rs = math.max(1, math.min((cell['rs'] as int?) ?? 1, all.length - r));
        final cs = math.max(1, (cell['cs'] as int?) ?? 1);
        for (var i = 0; i < rs; i++) {
          for (var j = 0; j < cs; j++) {
            (occ[r + i] ??= {}).add(c + j);
          }
        }
        placed.add(_Placed(cell, r, c, rs, cs, isHead, total, r - head.length));
        c += cs;
      }
      g.cols = math.max(g.cols, c);
    }
    for (final s in occ.values) {
      for (final c in s) {
        g.cols = math.max(g.cols, c + 1);
      }
    }
    g.at = List.generate(g.rows, (_) => List<_Placed?>.filled(g.cols, null));
    for (final p in placed) {
      for (var i = 0; i < p.rs; i++) {
        for (var j = 0; j < p.cs; j++) {
          if (p.r + i < g.rows && p.col + j < g.cols) g.at[p.r + i][p.col + j] = p;
        }
      }
    }

    // Cột cố định: không cho ô gộp vắt qua ranh giới; ô gộp dọc không được vắt qua dòng tiêu đề
    var fz = (d['fz'] as int?) ?? 0;
    fz = math.min(fz, g.cols - 1);
    bool crosses(int f) => placed.any((p) => p.col < f && p.col + p.cs > f);
    while (fz > 0 && crosses(fz)) {
      fz--;
    }
    g.frozen = math.max(0, fz);
    if (placed.any((p) => p.r < g.headRows && p.r + p.rs > g.headRows)) g.headRows = 0;

    // Độ rộng cột theo nội dung (ô không gộp ngang)
    double textW(String s, bool bold) {
      final longest = s.split('\n').fold<int>(0, (m, l) => math.max(m, l.characters.length));
      return longest * (bold ? 7.6 : 7.0) + 18;
    }

    g.colW = List.filled(g.cols, 44.0);
    for (final p in placed.where((p) => p.cs == 1)) {
      final cap = p.head ? 150.0 : 280.0; // tiêu đề dài thì xuống dòng
      final w = math.min(textW(p.c['x'] as String, p.c['b'] == 1), cap);
      g.colW[p.col] = math.max(g.colW[p.col], w);
    }
    // ô gộp ngang rộng hơn tổng cột → chia đều phần thiếu
    for (final p in placed.where((p) => p.cs > 1)) {
      final need = math.min(textW(p.c['x'] as String, true), 320.0);
      var have = 0.0;
      for (var j = 0; j < p.cs; j++) {
        have += g.colW[p.col + j];
      }
      if (need > have) {
        for (var j = 0; j < p.cs; j++) {
          g.colW[p.col + j] += (need - have) / p.cs;
        }
      }
    }

    // Chiều cao dòng: số dòng chữ lớn nhất (tiêu đề tự xuống dòng theo độ rộng)
    g.rowH = List.filled(g.rows, 34.0);
    for (final p in placed.where((p) => p.rs == 1)) {
      final text = p.c['x'] as String;
      var w = 0.0;
      for (var j = 0; j < p.cs; j++) {
        w += g.colW[p.col + j];
      }
      var lines = 0;
      for (final l in text.split('\n')) {
        lines += math.max(1, ((l.characters.length * 7.4 + 14) / w).ceil());
      }
      g.rowH[p.r] = math.max(g.rowH[p.r], math.min(lines, 4) * 16.0 + 14);
    }
    return g;
  }

  TableViewCell cell(int r, int c) {
    final p = at[r][c];
    if (p == null) {
      return const TableViewCell(child: SizedBox.shrink());
    }
    final cell = p.c;
    final bgDefault = p.head
        ? Brand.navy
        : (p.total ? Brand.navy : (p.bodyIndex.isEven ? Brand.zebra : Colors.white));
    final fgDefault = (p.head || p.total) ? Colors.white : const Color(0xFF1A202C);
    final bg = hexColor(cell['bg']) ?? bgDefault;
    final fg = hexColor(cell['fg']) ?? (cell['bg'] != null ? _contrast(bg) : fgDefault);
    // Ô tiêu đề gộp nhiều cột: căn trái để chữ không trôi khỏi màn hình
    final al = (p.head && p.cs > 2)
        ? 'l'
        : cell['al'] ?? (p.head ? 'c' : (_numeric(cell['x'] as String) ? 'r' : 'l'));
    final child = Container(
      padding: const EdgeInsets.symmetric(horizontal: 7, vertical: 4),
      alignment: switch (al) {
        'c' => Alignment.center,
        'r' => Alignment.centerRight,
        _ => Alignment.centerLeft,
      },
      decoration: BoxDecoration(
        color: bg,
        border: Border.all(color: (p.head || p.total) ? Brand.border : Brand.cellBorder, width: 0.5),
      ),
      child: Text(
        cell['x'] as String,
        maxLines: 4,
        overflow: TextOverflow.ellipsis,
        textAlign: switch (al) {
          'c' => TextAlign.center,
          'r' => TextAlign.right,
          _ => TextAlign.left,
        },
        style: TextStyle(
          color: fg,
          fontSize: p.head ? 11.5 : 12.5,
          height: 1.2,
          fontWeight: (cell['b'] == 1 || p.total) ? FontWeight.w700 : FontWeight.w500,
          fontFeatures: const [FontFeature.tabularFigures()],
        ),
      ),
    );
    if (p.rs == 1 && p.cs == 1) return TableViewCell(child: child);
    return TableViewCell(
      rowMergeStart: p.rs > 1 ? p.r : null,
      rowMergeSpan: p.rs > 1 ? p.rs : null,
      columnMergeStart: p.cs > 1 ? p.col : null,
      columnMergeSpan: p.cs > 1 ? p.cs : null,
      child: child,
    );
  }

  static final _num = RegExp(r'^[-+]?[\d.,]+\s*(%|tr|Tr|đ|k)?$');
  static bool _numeric(String s) => _num.hasMatch(s.trim());

  static Color _contrast(Color bg) =>
      bg.computeLuminance() < 0.35 ? Colors.white : const Color(0xFF1A202C);
}
