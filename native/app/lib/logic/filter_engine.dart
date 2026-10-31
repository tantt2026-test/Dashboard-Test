// Áp các ô lọc của Streamlit lên báo cáo đã xuất — y hệt cách App.py lọc, dựa trên "spec"
// mà pipeline/filters_probe.py đã tìm ra bằng cách chạy thử App.py:
//   select   : mặt nạ từng lựa chọn (dòng/cột/thẻ/hạng mục biểu đồ/mục bị ẩn); nhiều lựa chọn = hợp
//   eq       : dòng có cột == giá trị chọn          contains: cột chứa chữ (phẩy = hoặc)
//   date     : cột ngày nằm trong khoảng            calc    : tải bản App.py tính sẵn (1 giá trị)
// Sau khi bớt dòng: tính lại dòng Tổng theo công thức ('tot') và đếm lại "Hiển thị x / y".
// Không import Flutter: test bằng `dart test` được.
import 'dart:convert';
import 'dart:math' as math;

/// Mã dòng giống filters_probe.rkey (FNV-1a 32 bit trên UTF-8, nối bằng U+241F, bỏ cột STT).
String rowKey(List<String> cells) {
  final bytes = utf8.encode(cells.join('␟'));
  var h = 0x811c9dc5;
  for (final b in bytes) {
    h ^= b;
    h = (h * 0x01000193) & 0xffffffff;
  }
  return h.toRadixString(16).padLeft(8, '0');
}

/// Tên cột = đường dẫn tiêu đề "Nhóm › Cột" (giống filters_probe.col_names).
List<String> colPaths(Map<String, dynamic> t) {
  final head = (t['h'] as List).cast<List>();
  final grid = <int, Map<int, String>>{};
  final occ = <int, Set<int>>{};
  for (var r = 0; r < head.length; r++) {
    var c = 0;
    for (final cell in head[r].cast<Map>()) {
      while (occ[r]?.contains(c) ?? false) {
        c++;
      }
      final cs = (cell['cs'] as int?) ?? 1, rs = (cell['rs'] as int?) ?? 1;
      for (var i = 0; i < rs; i++) {
        for (var j = 0; j < cs; j++) {
          (occ[r + i] ??= {}).add(c + j);
          if (r + i < head.length) (grid[r + i] ??= {})[c + j] = (cell['x'] as String).replaceAll('\n', ' ').trim();
        }
      }
      c += cs;
    }
  }
  var n = 0;
  for (final m in grid.values) {
    for (final c in m.keys) {
      n = math.max(n, c + 1);
    }
  }
  return List.generate(n, (c) {
    final parts = <String>[];
    for (var r = 0; r < head.length; r++) {
      final x = grid[r]?[c] ?? '';
      if (x.isNotEmpty && (parts.isEmpty || parts.last != x)) parts.add(x);
    }
    return parts.isEmpty ? 'Cột ${c + 1}' : parts.join(' › ');
  });
}

/// Dòng body → chữ theo vị trí cột (như filters_probe.body_cells).
List<String> bodyCells(List row) {
  final m = <int, String>{};
  var c = 0;
  for (final cell in row.cast<Map>()) {
    m[c] = (cell['x'] as String).replaceAll('\n', ' ');
    c += (cell['cs'] as int?) ?? 1;
  }
  if (m.isEmpty) return const [];
  final n = m.keys.reduce(math.max) + 1;
  return List.generate(n, (i) => m[i] ?? '');
}

final _totalRe = RegExp(r'^(TỔNG|TOTAL)|\sTOTAL$', caseSensitive: false);

/// Dòng Tổng: 1 trong 3 ô đầu bắt đầu bằng TỔNG/TOTAL hoặc kết thúc bằng " Total"
/// (không nhầm tên CH như "Cửa Hàng Tổng Hợp") — giống filters_probe.is_total.
bool isTotalRow(List<String> cells) => cells.take(3).any((c) => _totalRe.hasMatch(c.trim()));

/// Bản tính sẵn chỉ đổi THỨ TỰ dòng so với bản gốc (vd Sort Tên NVBH A→Z): cùng bảng, cùng cột,
/// cùng tập dòng → mặt nạ dòng đo trên bản gốc vẫn áp được (các ô lọc phối hợp với nhau).
bool sameRowsAs(List<Map<String, dynamic>> base, List<Map<String, dynamic>> variant) {
  List<Map<String, dynamic>> tbls(List<Map<String, dynamic>> l) => [
        for (final it in l)
          if (it['t'] == 'tbl') it else if (it['t'] == 'box') ...tbls((it['ch'] as List).cast<Map<String, dynamic>>())
      ];
  Set<String> keys(Map<String, dynamic> t) {
    final names = colPaths(t);
    final skip = {for (var i = 0; i < names.length; i++) if (names[i].trim().toUpperCase() == 'STT') i};
    return {
      for (final r in (t['b'] as List).cast<List>())
        rowKey([for (final (i, c) in bodyCells(r).indexed) if (!skip.contains(i)) c])
    };
  }

  final a = tbls(base), b = tbls(variant);
  if (a.length != b.length) return false;
  for (var i = 0; i < a.length; i++) {
    if (jsonEncode(colPaths(a[i])) != jsonEncode(colPaths(b[i]))) return false;
    final ka = keys(a[i]), kb = keys(b[i]);
    if (ka.length != kb.length || !ka.containsAll(kb)) return false;
  }
  return true;
}

/// Ghi chỉ số duyệt (giống _walk của Python: item, rồi con của box) vào '_i', bảng thứ mấy vào '_ti'.
void indexItems(List<Map<String, dynamic>> items) {
  var i = 0, ti = 0;
  void walk(List<Map<String, dynamic>> l) {
    for (final it in l) {
      it['_i'] = i++;
      if (it['t'] == 'tbl') it['_ti'] = ti++;
      if (it['t'] == 'box') walk((it['ch'] as List).cast<Map<String, dynamic>>());
    }
  }
  walk(items);
}

/// Giá trị ô lọc: multiselect → `List<String>`, text → String, checkbox → bool,
/// date → [yyyy-mm-dd, yyyy-mm-dd], selectbox → String.
typedef FilterValues = Map<String, Object?>;

bool sameValue(Object? a, Object? b) => jsonEncode(a) == jsonEncode(b);

/// Ô lọc đang khác mặc định?
bool isActive(Map<String, dynamic> w, Object? v) {
  if (v == null) return false;
  if (sameValue(v, w['value'])) return false;
  if (v is List && v.isEmpty) return (w['value'] as List?)?.isNotEmpty ?? false;
  if (v is String && v.trim().isEmpty) return false;
  return true;
}

class _RowRule {
  final int table; // _ti
  final bool Function(List<String> cells, List<String> names, String key) keep;
  _RowRule(this.table, this.keep);
}

class FilterResult {
  final List<Map<String, dynamic>> items;
  final List<String> notes; // ghi chú (ô lọc tính lại chọn nhiều giá trị...)
  FilterResult(this.items, this.notes);
}

/// Chọn bản tính sẵn cho ô lọc kiểu "tính lại" (null = dùng bản gốc).
/// Trả về (tên file, ghi chú nếu không có bản phù hợp).
(String?, String?) pickVariant(List<Map<String, dynamic>> widgets, FilterValues values) {
  final active = [
    for (final w in widgets)
      if ((w['f'] as Map?)?['mode'] == 'calc' && isActive(w, values[w['key']])) w
  ];
  if (active.isEmpty) return (null, null);
  if (active.length > 1) {
    return (null,
        'Các ô "${active.map((w) => _clean(w['label'])).join('", "')}" cần tính lại số — app chỉ áp dụng được 1 ô loại này mỗi lần. Đang hiện kết quả mặc định.');
  }
  final w = active.first;
  final v = values[w['key']];
  final variants = ((w['f'] as Map)['variants'] as Map).cast<String, String>();
  String? k;
  if (v is List) {
    if (v.isEmpty) {
      k = '[]';
    } else if (v.length == 1) {
      k = jsonEncode(v.first);
    }
  } else {
    k = jsonEncode(v);
  }
  final fn = k == null ? null : variants[k];
  if (fn == null) {
    return (null,
        'Ô "${_clean(w['label'])}" cần tính lại số — app có sẵn kết quả khi chọn 1 giá trị. Đang hiện kết quả mặc định.');
  }
  return (fn, null);
}

String _clean(Object? s) => (s as String? ?? '').replaceAll(RegExp(r'^[^\p{L}\d]+', unicode: true), '').trim();

/// Áp mọi ô lọc (trừ "tính lại" — đã chọn bản ở pickVariant) lên [base].
/// [onVariant]: true khi base là bản tính sẵn (mặt nạ dòng tính theo bản gốc → bỏ qua).
FilterResult applyFilters(
  List<Map<String, dynamic>> base,
  List<Map<String, dynamic>> widgets,
  FilterValues values, {
  bool onVariant = false,
  Set<String>? multiNv, // ĐDKD chọn nhiều → lọc dòng theo cột tên NV
}) {
  final notes = <String>[];
  var items = (jsonDecode(jsonEncode(base)) as List).cast<Map<String, dynamic>>();
  // Ô chọn chỉ số hiển thị: bỏ thẻ / nhóm cột / cột biểu đồ trước, rồi mới lọc dòng
  for (final w in widgets) {
    if ((w['f'] as Map?)?['mode'] == 'subset' && isActive(w, values[w['key']])) {
      items = applySubset(items, [for (final o in (w['options'] as List)) '$o'],
          [for (final o in (values[w['key']] as List)) '$o']);
    }
  }
  indexItems(items);

  final rowRules = <_RowRule>[];
  Set<int>? hideItems;
  final keepRows = <int, Set<String>>{}; // _ti → mã dòng giữ (giao các ô lọc)
  final keepCols = <int, Set<String>>{};
  Set<String>? keepCards;
  final keepCats = <int, Set<String>>{};

  for (final w in widgets) {
    var f = (w['f'] as Map?)?.cast<String, dynamic>() ?? const {};
    final v = values[w['key']];
    if (!isActive(w, v)) continue;
    if (f['mode'] == 'partial') {
      // App.py lọc dữ liệu gốc rồi tính lại cả báo cáo (vd ô Mã KH/Tên KH chung):
      // app chỉ lọc được bảng chi tiết → báo rõ, không im lặng hiện số khác Streamlit
      notes.add('Ô "${_clean(w['label'])}": app lọc các dòng của bảng chi tiết; '
          'các bảng/thẻ tổng hợp chưa tính lại theo ô này như trên Streamlit.');
      f = (f['inner'] as Map).cast<String, dynamic>();
    }
    switch (f['mode']) {
      case 'select':
        final sel = (v as List).map((e) => '$e').toList();
        if (sel.isEmpty) break;
        final masks = (f['masks'] as Map).cast<String, dynamic>();
        final ms = [for (final s in sel) if (masks[s] != null) (masks[s] as Map).cast<String, dynamic>()];
        if (ms.isEmpty) break;
        // hợp các lựa chọn
        final nT = (ms.first['rows'] as List).length;
        for (var t = 0; t < nT; t++) {
          final rs = [for (final m in ms) (m['rows'] as List)[t]];
          if (!onVariant && rs.every((r) => r != null)) {
            final u = {for (final r in rs) ...(r as List).cast<String>()};
            keepRows[t] = keepRows.containsKey(t) ? keepRows[t]!.intersection(u) : u;
          }
          final cs = [for (final m in ms) (m['cols'] as List)[t]];
          if (cs.every((c) => c != null)) {
            final u = {for (final c in cs) ...(c as List).cast<String>()};
            keepCols[t] = keepCols.containsKey(t) ? keepCols[t]!.intersection(u) : u;
          }
        }
        final cds = [for (final m in ms) m['cards']];
        if (cds.every((c) => c != null)) {
          final u = {for (final c in cds) ...(c as List).cast<String>()};
          keepCards = keepCards == null ? u : keepCards.intersection(u);
        }
        final nC = (ms.first['cats'] as List).length;
        for (var c = 0; c < nC; c++) {
          final cs = [for (final m in ms) (m['cats'] as List)[c]];
          if (cs.every((x) => x != null)) {
            final u = {for (final x in cs) ...(x as List).cast<String>()};
            keepCats[c] = keepCats.containsKey(c) ? keepCats[c]!.intersection(u) : u;
          }
        }
        final hides = [for (final m in ms) {...((m['hide'] as List?) ?? const []).cast<int>()}];
        final h = hides.reduce((a, b) => a.intersection(b));
        hideItems = {...?hideItems, ...h};
        break;
      case 'cols':
        // ô "chọn cột hiển thị": cột cố định + các cột được chọn
        final sel = (v as List).map((e) => '$e').toSet();
        if (sel.isEmpty) break;
        final keep = {...((f['always'] as List?) ?? const []).cast<String>(), ...sel};
        for (final t in (f['targets'] as List).cast<int>()) {
          keepCols[t] = keepCols.containsKey(t) ? keepCols[t]!.intersection(keep) : keep;
        }
        break;
      case 'eq':
        final sel = (v as List).map((e) => '$e'.trim()).toSet();
        final labels = (w['labels'] as List?)?.cast<String>();
        final opts = (w['options'] as List?)?.cast<String>();
        if (labels != null && opts != null) {
          for (var i = 0; i < opts.length && i < labels.length; i++) {
            if (sel.contains(opts[i])) sel.add(labels[i].trim());
          }
        }
        for (final tg in (f['targets'] as List).cast<Map>()) {
          final col = tg['col'] as String;
          rowRules.add(_RowRule(tg['t'] as int, (cells, names, _) {
            final ci = names.indexOf(col);
            return ci < 0 || (ci < cells.length && sel.contains(cells[ci].trim()));
          }));
        }
        break;
      case 'contains':
        // raw: App.py tìm nguyên chữ gõ, không bỏ dấu cách đầu/cuối (filters_probe dò từng ô)
        final keep = f['raw'] == true;
        final raw = keep ? '$v' : '$v'.trim();
        final terms = (f['multi'] == true ? raw.split(',') : [raw])
            .map((e) => (keep ? e : e.trim()).toLowerCase())
            .where((e) => e.isNotEmpty)
            .toList();
        if (terms.isEmpty) break;
        for (final tg in (f['targets'] as List).cast<Map>()) {
          final col = tg['col'] as String;
          rowRules.add(_RowRule(tg['t'] as int, (cells, names, _) {
            final ci = names.indexOf(col);
            if (ci < 0) return true;
            final x = ci < cells.length ? cells[ci].toLowerCase() : '';
            return terms.any(x.contains);
          }));
        }
        break;
      case 'date':
        final r = (v as List).cast<String>();
        if (r.length != 2) break;
        final lo = DateTime.parse(r[0]), hi = DateTime.parse(r[1]);
        for (final tg in (f['targets'] as List).cast<Map>()) {
          final col = tg['col'] as String;
          rowRules.add(_RowRule(tg['t'] as int, (cells, names, _) {
            final ci = names.indexOf(col);
            if (ci < 0 || ci >= cells.length) return true;
            final m = RegExp(r'^(\d{2})/(\d{2})/(\d{4})').firstMatch(cells[ci]);
            if (m == null) return false;
            final d = DateTime(int.parse(m[3]!), int.parse(m[2]!), int.parse(m[1]!));
            return !d.isBefore(lo) && !d.isAfter(hi);
          }));
        }
        break;
      case 'unsupported':
        notes.add('Ô "${_clean(w['label'])}" chưa áp dụng được trên app.');
        break;
    }
  }

  // ---- áp lên từng mục ----
  final out = <Map<String, dynamic>>[];
  var catIdx = 0;

  List<Map<String, dynamic>> process(List<Map<String, dynamic>> list) {
    final res = <Map<String, dynamic>>[];
    for (var k = 0; k < list.length; k++) {
      final it = list[k];
      if (hideItems?.contains(it['_i']) ?? false) {
        if (it['t'] == 'bar' || it['t'] == 'pie') catIdx++;
        continue;
      }
      switch (it['t']) {
        case 'box':
          it['ch'] = process((it['ch'] as List).cast<Map<String, dynamic>>());
          if ((it['ch'] as List).isEmpty) continue;
          break;
        case 'cards':
          if (keepCards != null) {
            it['it'] = [for (final c in (it['it'] as List).cast<Map>()) if (keepCards.contains(c['l'])) c];
            if ((it['it'] as List).isEmpty) continue;
          }
          break;
        case 'bar':
        case 'pie':
          final keep = keepCats[catIdx];
          catIdx++;
          if (keep != null) _filterChart(it, keep);
          break;
        case 'tbl':
          _filterTable(it, it['_ti'] as int, keepRows, rowRules, multiNv);
          if (keepCols.containsKey(it['_ti'])) _keepColumns(it, keepCols[it['_ti']]!);
          break;
      }
      res.add(it);
    }
    return res;
  }

  out.addAll(process(items));
  _updateCountCaptions(out);
  return FilterResult(out, notes);
}

void _filterChart(Map<String, dynamic> it, Set<String> keep) {
  for (final tr in (it['tr'] as List).cast<Map<String, dynamic>>()) {
    if (it['t'] == 'pie') {
      final labels = (tr['labels'] as List).map((e) => '$e').toList();
      final idx = [for (var i = 0; i < labels.length; i++) if (keep.contains(labels[i])) i];
      for (final f in ['labels', 'values', 'colors']) {
        if (tr[f] is List) tr[f] = [for (final i in idx) (tr[f] as List)[i]];
      }
    } else {
      final catKey = tr['h'] == 1 ? 'y' : 'x';
      final cats = ((tr[catKey] as List?) ?? const []).map((e) => '$e').toList();
      final idx = [for (var i = 0; i < cats.length; i++) if (keep.contains(cats[i])) i];
      for (final f in ['x', 'y', 'text', 'color']) {
        if (tr[f] is List && (tr[f] as List).length == cats.length) tr[f] = [for (final i in idx) (tr[f] as List)[i]];
      }
    }
  }
}

void _filterTable(Map<String, dynamic> t, int ti, Map<int, Set<String>> keepRows, List<_RowRule> rules,
    Set<String>? multiNv) {
  final body = (t['b'] as List).cast<List>();
  if (body.any((r) => r.any((c) => ((c as Map)['rs'] as int? ?? 1) > 1))) return;
  final names = colPaths(t);
  final skip = {for (var i = 0; i < names.length; i++) if (names[i].trim().toUpperCase() == 'STT') i};
  int? nvCol;
  if (multiNv != null && multiNv.isNotEmpty) {
    for (var i = 0; i < names.length; i++) {
      final n = names[i].split(' › ').last.toLowerCase();
      if (n == 'tên nvbh' || n == 'tên nv' || n == 'tên đdkd' || n == 'sm name' || n == 'nhân viên') {
        nvCol = i;
        break;
      }
    }
  }
  final myRules = rules.where((r) => r.table == ti).toList();
  final mask = keepRows[ti];
  if (mask == null && myRules.isEmpty && nvCol == null) return;

  final kept = <List>[];
  var dataBefore = 0, dataAfter = 0;
  for (final row in body) {
    final cells = bodyCells(row);
    if (isTotalRow(cells)) {
      kept.add(row);
      continue;
    }
    dataBefore++;
    final key = rowKey([for (var i = 0; i < cells.length; i++) if (!skip.contains(i)) cells[i]]);
    var ok = mask == null || mask.contains(key);
    if (ok && nvCol != null) ok = nvCol < cells.length && multiNv!.contains(cells[nvCol].trim());
    if (ok) ok = myRules.every((r) => r.keep(cells, names, key));
    if (ok) {
      kept.add(row);
      dataAfter++;
    }
  }
  if (dataAfter == dataBefore) return;
  // đánh lại STT
  var n = 0;
  for (final row in kept) {
    final cells = bodyCells(row);
    if (isTotalRow(cells) || skip.isEmpty) continue;
    n++;
    final first = (row.first as Map);
    if (skip.contains(0) && RegExp(r'^\d+$').hasMatch('${first['x']}'.trim())) first['x'] = '$n';
  }
  t['b'] = kept;
  t['_before'] = dataBefore;
  t['_after'] = dataAfter;
  _recomputeTotals(t);
}

/// Tính lại dòng Tổng cho các dòng còn lại theo công thức pipeline đã kiểm chứng ('tot').
/// Cột không có công thức → để trống (không hiện số sai).
void _recomputeTotals(Map<String, dynamic> t) {
  final body = (t['b'] as List).cast<List>();
  final totIdx = body.indexWhere((r) => isTotalRow(bodyCells(r)));
  if (totIdx < 0) return;
  final tot = (t['tot'] as Map?)?.cast<String, dynamic>();
  final data = [for (final r in body) if (!isTotalRow(bodyCells(r))) bodyCells(r)];
  final sums = <int, double>{};
  double? parse(String s, String th, String dec) {
    var x = s.trim().replaceAll(' ', '').replaceAll(' ', '');
    x = x.replaceAll(RegExp(r'(tr|Tr|đ|k|VNĐ|%)$'), '');
    if (!RegExp(r'^[-+]?[\d.,]+$').hasMatch(x)) return null;
    return double.tryParse(x.replaceAll(th, '').replaceAll(dec, '.'));
  }

  String fmt(double v, Map spec, {bool pct = false}) {
    final n = spec['n'] as int;
    final neg = v < 0;
    final s = v.abs().toStringAsFixed(n);
    final parts = s.split('.');
    final ip = parts[0];
    final buf = StringBuffer();
    for (var i = 0; i < ip.length; i++) {
      if (i > 0 && (ip.length - i) % 3 == 0) buf.write(spec['t']);
      buf.write(ip[i]);
    }
    var out = '${neg ? '-' : ''}$buf${n > 0 ? '${spec['d']}${parts[1]}' : ''}';
    if (pct) out = '$out%';
    return out;
  }

  final row = body[totIdx];
  final cellAt = <int, Map>{};
  var c = 0;
  for (final cell in row.cast<Map>()) {
    cellAt[c] = cell;
    c += (cell['cs'] as int?) ?? 1;
  }
  if (tot != null) {
    tot.forEach((k, spec) {
      final ci = int.parse(k);
      if (spec['op'] == 'sum') {
        var s = 0.0;
        for (final r in data) {
          s += (ci < r.length ? parse(r[ci], spec['t'], spec['d']) : null) ?? 0;
        }
        sums[ci] = s;
      }
    });
  }
  cellAt.forEach((ci, cell) {
    final x = '${cell['x']}'.trim();
    if (x.isEmpty || x == '-' || x == '—' || _totalRe.hasMatch(x)) return; // ô STT / nhãn "TỔNG CỘNG"
    final spec = tot?['$ci'];
    if (spec == null) {
      if (RegExp(r'\d').hasMatch('${cell['x']}')) cell['x'] = '';
      return;
    }
    if (spec['op'] == 'sum') {
      cell['x'] = fmt(sums[ci] ?? 0, spec);
    } else if (spec['op'] == 'ratio') {
      final a = sums[spec['a']] ?? 0, b = sums[spec['b']] ?? 0;
      cell['x'] = b == 0 ? '0%' : fmt(a / b * 100, spec, pct: true);
    }
  });
}

void _keepColumns(Map<String, dynamic> t, Set<String> keep) {
  final names = colPaths(t);
  // khớp theo tên đầy đủ "Nhóm › Cột" hoặc tên cột cuối (ô chọn cột của các tab dùng tên ngắn)
  final keepIdx = {
    for (var i = 0; i < names.length; i++)
      if (keep.contains(names[i]) || keep.contains(names[i].split(' › ').last)) i
  };
  if (keepIdx.length == names.length) return;
  List<List> rebuild(List rows, {required bool head}) {
    final occ = <int, Set<int>>{};
    final out = <List>[];
    for (var r = 0; r < rows.length; r++) {
      final nr = [];
      var c = 0;
      for (final cell in (rows[r] as List).cast<Map>()) {
        while (head && (occ[r]?.contains(c) ?? false)) {
          c++;
        }
        final cs = (cell['cs'] as int?) ?? 1, rs = (cell['rs'] as int?) ?? 1;
        if (head) {
          for (var i = 0; i < rs; i++) {
            for (var j = 0; j < cs; j++) {
              (occ[r + i] ??= {}).add(c + j);
            }
          }
        }
        final kept = [for (var j = 0; j < cs; j++) if (keepIdx.contains(c + j)) 1].length;
        if (kept > 0) {
          final nc = Map<String, dynamic>.from(cell);
          if (kept > 1) {
            nc['cs'] = kept;
          } else {
            nc.remove('cs');
          }
          nr.add(nc);
        }
        c += cs;
      }
      out.add(nr);
    }
    return out;
  }

  t['h'] = rebuild(t['h'] as List, head: true);
  t['b'] = rebuild(t['b'] as List, head: false);
  if (t['fz'] is int) {
    t['fz'] = [for (var i = 0; i < (t['fz'] as int); i++) if (keepIdx.contains(i)) 1].length;
  }
  t.remove('tot');
}

/// Đoạn chú thích ngay sau/trước bảng có số dòng ("Hiển thị: 102 / 102 KH", "Tổng 619 dòng",
/// "· 619 đơn hàng") → thay bằng số dòng sau khi lọc.
void _updateCountCaptions(List<Map<String, dynamic>> items) {
  for (var i = 0; i < items.length; i++) {
    final t = items[i];
    if (t['t'] != 'tbl' || t['_before'] == null) continue;
    final before = t['_before'] as int, after = t['_after'] as int;
    for (final j in [i + 1, i + 2, i + 3, i - 1]) {
      if (j < 0 || j >= items.length || items[j]['t'] != 'p') continue;
      for (final r in (items[j]['r'] as List).cast<Map>()) {
        final x = r['x'] as String;
        var y = x.replaceAllMapped(RegExp('Hiển thị: ?$before ?/'), (m) => m[0]!.replaceFirst('$before', '$after'));
        y = y.replaceAll(RegExp('(?<![\\d.,])${_fmtVariants(before)}(?= (dòng|đơn hàng|KH|cửa hàng|CH))'), '$after');
        r['x'] = y;
      }
    }
  }
}

String _fmtVariants(int n) {
  final plain = '$n';
  final comma = plain.replaceAllMapped(RegExp(r'\B(?=(\d{3})+(?!\d))'), (_) => ',');
  final dot = plain.replaceAllMapped(RegExp(r'\B(?=(\d{3})+(?!\d))'), (_) => '.');
  return '(?:${RegExp.escape(plain)}|${RegExp.escape(comma)}|${RegExp.escape(dot)})';
}

/// Mọi ô lọc trong báo cáo (theo thứ tự xuất hiện).
List<Map<String, dynamic>> collectWidgets(List<Map<String, dynamic>> items) {
  final out = <Map<String, dynamic>>[];
  void walk(List l) {
    for (final it in l.cast<Map<String, dynamic>>()) {
      if (it['t'] == 'filters') out.addAll((it['w'] as List).cast<Map<String, dynamic>>());
      if (it['t'] == 'box') walk(it['ch'] as List);
    }
  }
  walk(items);
  return out;
}

bool _subsetHit(Object? label, List<String> unsel) {
  final s = '${label ?? ''}'.trim();
  return unsel.any((o) => s == o || s.startsWith('$o ') || s.startsWith('$o('));
}

/// Vị trí cột (c0, c1) của từng ô theo dòng, tính rowspan/colspan.
List<List<(int, int)>> _place(List<List> rows) {
  final occ = <(int, int)>{};
  final out = <List<(int, int)>>[];
  for (var r = 0; r < rows.length; r++) {
    var c = 0;
    final pos = <(int, int)>[];
    for (final cell in rows[r].cast<Map>()) {
      while (occ.contains((r, c))) {
        c++;
      }
      final cs = (cell['cs'] as num?)?.toInt() ?? 1, rs = (cell['rs'] as num?)?.toInt() ?? 1;
      for (var dr = 0; dr < rs; dr++) {
        for (var dc = 0; dc < cs; dc++) {
          occ.add((r + dr, c + dc));
        }
      }
      pos.add((c, c + cs));
      c += cs;
    }
    out.add(pos);
  }
  return out;
}

/// Ô 'chọn chỉ số hiển thị' (mode subset) — y hệt pipeline/filters_probe.py apply_subset
/// (đã kiểm chứng bằng App.py): bỏ thẻ / nhóm cột bảng / cột biểu đồ của chỉ số không chọn.
List<Map<String, dynamic>> applySubset(List<Map<String, dynamic>> items, List<String> opts, List<String> sel) {
  final unsel = [for (final o in opts) if (!sel.contains(o)) o];
  if (sel.isEmpty || unsel.isEmpty) return items;
  final out = <Map<String, dynamic>>[];
  for (var it in items) {
    switch (it['t']) {
      case 'cards':
        it = {...it, 'it': [for (final c in (it['it'] as List).cast<Map>()) if (!_subsetHit(c['l'], unsel)) c]};
        if ((it['it'] as List).isEmpty) continue;
        break;
      case 'tbl':
        final head = (it['h'] as List?)?.cast<List>();
        if (head == null || head.isEmpty) break;
        final ph = _place(head);
        final drop = <int>{};
        final row0 = head.first.cast<Map>();
        for (var i = 0; i < row0.length; i++) {
          if (_subsetHit(row0[i]['x'], unsel)) {
            for (var c = ph.first[i].$1; c < ph.first[i].$2; c++) {
              drop.add(c);
            }
          }
        }
        if (drop.isEmpty) break;
        List<List> cut(List<List> rows) {
          final pos = _place(rows);
          return [
            for (var r = 0; r < rows.length; r++)
              [
                for (var i = 0; i < rows[r].length; i++)
                  if (() {
                    final (c0, c1) = pos[r][i];
                    var keep = 0;
                    for (var c = c0; c < c1; c++) {
                      if (!drop.contains(c)) keep++;
                    }
                    return keep;
                  }() case final keep when keep > 0)
                    keep == pos[r][i].$2 - pos[r][i].$1 ? rows[r][i] : {...(rows[r][i] as Map), 'cs': keep}
              ]
          ];
        }
        var ncol = 0;
        for (final p in ph) {
          if (p.isNotEmpty && p.last.$2 > ncol) ncol = p.last.$2;
        }
        final remap = <int, int>{};
        for (var c = 0; c < ncol; c++) {
          if (!drop.contains(c)) remap[c] = remap.length;
        }
        it = {...it, 'h': cut(head), 'b': cut((it['b'] as List).cast<List>())};
        final tot = (it['tot'] as Map?)?.cast<String, dynamic>();
        if (tot != null) {
          final nt = <String, dynamic>{};
          tot.forEach((k, f0) {
            final f = Map<String, dynamic>.from(f0 as Map);
            final refs = [int.parse(k), for (final x in ['a', 'b']) if (f[x] != null) (f[x] as num).toInt()];
            if (refs.every(remap.containsKey)) {
              for (final x in ['a', 'b']) {
                if (f[x] != null) f[x] = remap[(f[x] as num).toInt()];
              }
              nt['${remap[int.parse(k)]}'] = f;
            }
          });
          it['tot'] = nt;
        }
        break;
      case 'bar':
        it = {
          ...it,
          'tr': [
            for (final tr in (it['tr'] as List).cast<Map>())
              () {
                final cats = (tr['h'] == true || tr['h'] == 1) ? tr['y'] : tr['x'];
                if (cats is! List) return tr;
                final n = cats.length;
                final keep = [for (var i = 0; i < n; i++) if (!_subsetHit(cats[i], unsel)) i];
                return {
                  for (final e in tr.entries)
                    e.key: (e.value is List && (e.value as List).length == n)
                        // màu theo vị trí cột (bảng màu lặp lại từ đầu) → giữ màu đầu danh sách
                        ? (e.key == 'color'
                            ? (e.value as List).sublist(0, keep.length)
                            : [for (final i in keep) (e.value as List)[i]])
                        : e.value
                };
              }()
          ]
        };
        break;
      case 'box':
        it = {...it, 'ch': applySubset((it['ch'] as List).cast<Map<String, dynamic>>(), opts, sel)};
        break;
    }
    out.add(it);
  }
  return out;
}
