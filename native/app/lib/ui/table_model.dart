import 'dart:math' as math;

import 'package:flutter/widgets.dart' show StringCharacters;

import 'text_norm.dart';

/// Bảng từ report_doc.py ({h: dòng tiêu đề, b: dòng dữ liệu, fz: số cột cố định}):
/// đặt ô theo colspan/rowspan, tên cột, lọc dòng, tính kích thước theo màn hình.
class TableModel {
  final List<List<Map<String, dynamic>>> head;
  final List<List<Map<String, dynamic>>> body;
  final int fzWanted;
  late final List<bool> isTotal; // dòng Tổng / Total (không bị lọc)
  late final bool bodyHasRowspan;
  late final int cols;
  late final List<String> colNames;
  late final List<Map<int, String>> rowValues; // body row → {cột: chữ}

  TableModel(Map<String, dynamic> d)
      : head = [for (final r in d['h'] as List) (r as List).cast<Map<String, dynamic>>()],
        body = [for (final r in d['b'] as List) (r as List).cast<Map<String, dynamic>>()],
        fzWanted = (d['fz'] as int?) ?? 0 {
    final totalRe = RegExp(r'TỔNG|TOTAL', caseSensitive: false);
    isTotal = [
      for (final r in body)
        r.take(3).any((c) => totalRe.hasMatch(c['x'] as String? ?? '')) ||
            (r.isNotEmpty && r.every((c) => (c['bg'] as String?)?.toLowerCase() == '#1a365d'))
    ];
    bodyHasRowspan = body.any((r) => r.any((c) => ((c['rs'] as int?) ?? 1) > 1));
    final full = Layout.place(head, body);
    cols = full.cols;

    // Tên cột: ghép các tầng tiêu đề phủ cột đó (bỏ trùng), vd "Kênh OFF › Plan VT"
    final hl = Layout.place(head, const []);
    colNames = List.generate(cols, (c) {
      final parts = <String>[];
      for (var r = 0; r < hl.rows; r++) {
        final p = c < hl.cols ? hl.at[r][c] : null;
        final t = (p?.c['x'] as String? ?? '').replaceAll('\n', ' ').trim();
        if (t.isNotEmpty && (parts.isEmpty || parts.last != t)) parts.add(t);
      }
      return parts.isEmpty ? 'Cột ${c + 1}' : parts.join(' › ');
    });

    rowValues = [
      for (final r in body)
        () {
          final m = <int, String>{};
          var c = 0;
          for (final cell in r) {
            m[c] = (cell['x'] as String? ?? '').replaceAll('\n', ' ');
            c += math.max(1, (cell['cs'] as int?) ?? 1);
          }
          return m;
        }()
    ];
  }

  bool get filterable => !bodyHasRowspan && body.length > 1;

  /// Cột hợp để lọc theo giá trị (tên, mã, thứ, nhóm, kênh...).
  List<int> get filterColumns {
    if (!filterable) return const [];
    final nameHint = RegExp(r'ten|ma |ma$|thu|nhom|nvbh|ddkd|kenh|l1|vip|loai|trang thai|chuong trinh|cat|brand|member|nhan vien|tuyen');
    final numRe = RegExp(r'^[-+]?[\d.,\s]+(%|tr|đ|k)?$');
    final out = <int>[];
    for (var c = 0; c < cols; c++) {
      final vals = <String>{};
      var numeric = 0, n = 0;
      for (var i = 0; i < body.length; i++) {
        if (isTotal[i]) continue;
        final v = rowValues[i][c];
        if (v == null || v.isEmpty) continue;
        n++;
        vals.add(v);
        if (numRe.hasMatch(v)) numeric++;
      }
      if (vals.length < 2 || n == 0) continue;
      final name = fold(colNames[c]);
      if (name.contains('stt')) continue;
      final hinted = nameHint.hasMatch(name);
      if ((numeric / n < 0.5 && vals.length <= 120) || (hinted && vals.length <= 60)) out.add(c);
    }
    return out;
  }

  List<String> valuesOf(int col) {
    final s = <String>{};
    for (var i = 0; i < body.length; i++) {
      if (isTotal[i]) continue;
      final v = rowValues[i][col];
      if (v != null && v.isNotEmpty) s.add(v);
    }
    final l = s.toList()..sort((a, b) => fold(a).compareTo(fold(b)));
    return l;
  }

  /// Tìm cột theo tên (không dấu), vd 'ten nvbh', 'thu vt'.
  int? findCol(List<String> keys) {
    for (var c = 0; c < cols; c++) {
      final n = fold(colNames[c].split(' › ').last);
      if (keys.any(n.contains)) return c;
    }
    return null;
  }
}

/// Bộ lọc dòng của 1 bảng (hoặc cả trang).
class RowFilter {
  final Map<int, Set<String>> byCol; // cột → giá trị được chọn
  final String query;
  const RowFilter({this.byCol = const {}, this.query = ''});

  bool get active => byCol.values.any((s) => s.isNotEmpty) || query.trim().isNotEmpty;
  int get count => byCol.values.where((s) => s.isNotEmpty).length + (query.trim().isEmpty ? 0 : 1);
}

/// Lọc theo tên cột cho cả trang (ĐDKD, Thứ VT, tìm kiếm) — áp lên mọi bảng có cột đó.
class PageFilter {
  final Set<String> nv; // nhiều ĐDKD (lọc dòng)
  final Set<String> thu;
  final String query;
  const PageFilter({this.nv = const {}, this.thu = const {}, this.query = ''});
  bool get active => nv.isNotEmpty || thu.isNotEmpty || query.trim().isNotEmpty;
}

/// Chỉ số các dòng body hiển thị sau khi lọc (dòng Tổng luôn giữ).
List<int> visibleRows(TableModel m, RowFilter f, PageFilter p) {
  if (!m.filterable) return List.generate(m.body.length, (i) => i);
  final nvCol = p.nv.isEmpty ? null : m.findCol(const ['ten nvbh', 'ten nv', 'ddkd', 'nhan vien']);
  final thuCol = p.thu.isEmpty ? null : m.findCol(const ['thu vt']);
  final queries = [
    for (final q in [f.query, p.query])
      if (q.trim().isNotEmpty) fold(q.trim())
  ];
  final out = <int>[];
  for (var i = 0; i < m.body.length; i++) {
    if (m.isTotal[i]) {
      out.add(i);
      continue;
    }
    final v = m.rowValues[i];
    var ok = true;
    f.byCol.forEach((c, sel) {
      if (sel.isNotEmpty && !sel.contains(v[c])) ok = false;
    });
    if (ok && nvCol != null && !p.nv.contains(v[nvCol])) ok = false;
    if (ok && thuCol != null) {
      final t = v[thuCol] ?? '';
      // Thứ VT có thể là "2", "25", "2,5"... → khớp nếu chứa thứ được chọn
      if (!p.thu.any((x) => t == x || t.replaceAll(RegExp(r'\D'), '').contains(x))) ok = false;
    }
    if (ok && queries.isNotEmpty) {
      final row = fold(v.values.join(' | '));
      if (!queries.every(row.contains)) ok = false;
    }
    if (ok) out.add(i);
  }
  return out;
}

class Placed {
  final Map<String, dynamic> c;
  final int r, col, rs, cs, bodyIndex;
  final bool head, total;
  Placed(this.c, this.r, this.col, this.rs, this.cs, this.head, this.total, this.bodyIndex);
}

/// Lưới đã đặt ô + kích thước.
class Layout {
  int rows = 0, cols = 0, headRows = 0, frozen = 0;
  final placed = <Placed>[];
  late List<List<Placed?>> at;
  List<double> colW = const [], rowH = const [];
  double fontScale = 1;

  static Layout place(List<List<Map<String, dynamic>>> head, List<List<Map<String, dynamic>>> body,
      {List<bool>? totals, int fz = 0}) {
    final g = Layout();
    final all = [...head, ...body];
    g.headRows = head.length;
    g.rows = all.length;
    final occ = <int, Set<int>>{};
    for (var r = 0; r < all.length; r++) {
      final isHead = r < head.length;
      final bi = r - head.length;
      final total = !isHead && totals != null && bi < totals.length && totals[bi];
      var c = 0;
      for (final cell in all[r]) {
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
        g.placed.add(Placed(cell, r, c, rs, cs, isHead, total, bi));
        c += cs;
      }
    }
    for (final s in occ.values) {
      for (final c in s) {
        g.cols = math.max(g.cols, c + 1);
      }
    }
    g.at = List.generate(g.rows, (_) => List<Placed?>.filled(g.cols, null));
    for (final p in g.placed) {
      for (var i = 0; i < p.rs; i++) {
        for (var j = 0; j < p.cs; j++) {
          if (p.r + i < g.rows && p.col + j < g.cols) g.at[p.r + i][p.col + j] = p;
        }
      }
    }
    var f = math.min(fz, math.max(0, g.cols - 1));
    bool crosses(int x) => g.placed.any((p) => p.col < x && p.col + p.cs > x);
    while (f > 0 && crosses(f)) {
      f--;
    }
    g.frozen = f;
    if (g.placed.any((p) => p.r < g.headRows && p.r + p.rs > g.headRows)) g.headRows = 0;
    return g;
  }

  /// Kích thước cột/dòng.
  /// [zoom]: tỷ lệ chung của app; [avail]: bề ngang có sẵn (null = không co);
  /// [manual]: tỷ lệ thêm của bảng (toàn màn hình). Bảng hẹp → giãn cột cho vừa;
  /// bảng rộng → co chữ tối thiểu tới [minFit] (1 = giữ cỡ chữ, phần thừa cuộn ngang).
  void size({required double zoom, double? avail, double manual = 1, double minFit = 1}) {
    double charW(bool bold) => (bold ? 7.4 : 7.0);
    double textW(String s, bool bold) {
      final longest = s.split('\n').fold<int>(0, (m, l) => math.max(m, l.characters.length));
      return longest * charW(bold) + 16;
    }

    final base = List<double>.filled(cols, 40.0);
    for (final p in placed.where((p) => p.cs == 1)) {
      final cap = p.head ? 140.0 : 260.0;
      base[p.col] = math.max(base[p.col], math.min(textW(p.c['x'] as String, p.c['b'] == 1 || p.head), cap));
      if (p.c['bar'] != null) base[p.col] = math.max(base[p.col], 150.0); // thanh tiến độ
    }
    for (final p in placed.where((p) => p.cs > 1)) {
      final need = math.min(textW(p.c['x'] as String, true), 300.0);
      var have = 0.0;
      for (var j = 0; j < p.cs; j++) {
        have += base[p.col + j];
      }
      if (need > have) {
        for (var j = 0; j < p.cs; j++) {
          base[p.col + j] += (need - have) / p.cs;
        }
      }
    }

    final natural = base.fold<double>(0, (a, b) => a + b) * zoom * manual;
    var f = manual;
    var stretch = 1.0;
    if (avail != null && avail > 0) {
      if (natural > avail) {
        f = manual * math.max(minFit, avail / natural);
      } else {
        stretch = avail / natural;
      }
    }
    fontScale = f;
    colW = [for (final w in base) w * zoom * f * stretch];

    rowH = List.filled(rows, 30.0 * zoom * f);
    for (final p in placed.where((p) => p.rs == 1)) {
      var w = 0.0;
      for (var j = 0; j < p.cs; j++) {
        w += colW[p.col + j];
      }
      var lines = 0;
      for (final l in (p.c['x'] as String).split('\n')) {
        lines += math.max(1, ((l.characters.length * 6.3 * zoom * f + 10) / w).ceil());
      }
      rowH[p.r] = math.max(rowH[p.r], (math.min(lines, 4) * 15.0 + 12) * zoom * f);
    }
  }

  /// Số cột cố định vừa với màn hình: phần cố định không chiếm quá [maxShare] bề ngang
  /// (điện thoại hẹp mà cố định 4 cột thì không còn chỗ cho số liệu).
  int frozenFor(double maxWidth, {double maxShare = 0.55}) {
    var k = frozen;
    double fx(int n) => colW.take(n).fold<double>(0, (a, b) => a + b);
    bool crosses(int x) => placed.any((p) => p.col < x && p.col + p.cs > x);
    while (k > 0 && (fx(k) > maxWidth * maxShare || crosses(k))) {
      k--;
    }
    return k;
  }

  double get width => colW.fold<double>(0, (a, b) => a + b);
  double get height => rowH.fold<double>(0, (a, b) => a + b);
}
