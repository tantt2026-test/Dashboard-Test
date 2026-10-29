// Dùng bởi pipeline/parity_filters.py: áp bộ lọc của app (filter_engine) lên báo cáo gốc
// cho từng ca, in kết quả rút gọn (dòng từng bảng, thẻ, hạng mục biểu đồ) để so với App.py.
//   dart run tool/filter_cli.dart < cases.json
import 'dart:convert';
import 'dart:io';

import 'package:kpi_native/logic/filter_engine.dart';

List<Map<String, dynamic>> _walk(List items) {
  final out = <Map<String, dynamic>>[];
  for (final it in items.cast<Map<String, dynamic>>()) {
    out.add(it);
    if (it['t'] == 'box') out.addAll(_walk(it['ch'] as List));
  }
  return out;
}

Map<String, dynamic> summarize(List<Map<String, dynamic>> items) {
  final all = _walk(items);
  return {
    'tables': [
      for (final t in all.where((i) => i['t'] == 'tbl'))
        {
          'cols': colPaths(t),
          'rows': [for (final r in (t['b'] as List)) bodyCells(r as List)],
        }
    ],
    'cards': [for (final c in all.where((i) => i['t'] == 'cards')) for (final x in (c['it'] as List)) (x as Map)['l']],
    'cats': [
      for (final c in all.where((i) => i['t'] == 'bar' || i['t'] == 'pie'))
        c['t'] == 'pie'
            ? ((c['tr'] as List).first['labels'] as List).map((e) => '$e').toList()
            : (((c['tr'] as List).first['h'] == 1 ? (c['tr'] as List).first['y'] : (c['tr'] as List).first['x']) as List)
                .map((e) => '$e')
                .toList()
    ],
  };
}

void main() {
  final input = jsonDecode(stdin.readLineSync(encoding: utf8) ?? '{}') as Map<String, dynamic>;
  final out = <dynamic>[];
  for (final c in (input['cases'] as List).cast<Map<String, dynamic>>()) {
    final doc = jsonDecode(File(c['doc'] as String).readAsStringSync()) as Map<String, dynamic>;
    final items = (doc['items'] as List).cast<Map<String, dynamic>>();
    final widgets = [
      ...collectWidgets(items),
      for (final w in ((doc['main'] as Map?) ?? const {}).values) (w as Map).cast<String, dynamic>(),
    ];
    final values = (c['values'] as Map).cast<String, Object?>();
    final (file, note) = pickVariant(widgets, values);
    var base = items;
    if (file != null) {
      final dir = File(c['doc'] as String).parent.path;
      base = ((jsonDecode(File('$dir/$file').readAsStringSync()) as Map)['items'] as List).cast<Map<String, dynamic>>();
    }
    final res = applyFilters(base, widgets, values, onVariant: file != null);
    final allNotes = [?note, ...res.notes];
    out.add({'note': allNotes.isEmpty ? null : allNotes.join(' | '), 'variant': file, ...summarize(res.items)});
  }
  stdout.write(jsonEncode(out));
}
