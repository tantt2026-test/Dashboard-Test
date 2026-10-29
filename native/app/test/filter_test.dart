// Logic lọc dòng trên dữ liệu thật: REPORTS_DIR=<out>/kpi/Thang10 flutter test test/filter_test.dart
import 'dart:convert';
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:kpi_native/ui/table_model.dart';

void main() {
  final dir = Platform.environment['REPORTS_DIR'];
  if (dir == null) {
    test('REPORTS_DIR chưa đặt', () {}, skip: 'Đặt REPORTS_DIR');
    return;
  }
  List<TableModel> tables(String code) {
    final d = jsonDecode(File('$dir/$code/2026-10-28.json').readAsStringSync()) as Map<String, dynamic>;
    return [for (final i in (d['items'] as List).cast<Map<String, dynamic>>()) if (i['t'] == 'tbl') TableModel(i)];
  }

  test('Turnover-like bảng Hiệu suất: lọc nhiều ĐDKD, giữ dòng Tổng', () {
    final m = tables('PERFORMANCE').first;
    final nvCol = m.findCol(const ['ten nvbh'])!;
    final rows = visibleRows(m, const RowFilter(), const PageFilter(nv: {'Mai Thị Linh', 'Lê Thị Thơm'}));
    final names = rows.where((i) => !m.isTotal[i]).map((i) => m.rowValues[i][nvCol]).toSet();
    expect(names, {'Mai Thị Linh', 'Lê Thị Thơm'});
    expect(rows.where((i) => m.isTotal[i]).length, m.isTotal.where((t) => t).length);
  });

  test('Tìm không dấu', () {
    final m = tables('PERFORMANCE').first;
    final rows = visibleRows(m, const RowFilter(query: 'le thi thom'), const PageFilter());
    expect(rows.where((i) => !m.isTotal[i]).length, 1);
  });

  test('MBS CAT: lọc Thứ VT + lọc theo cột', () {
    final m = tables('MBS_CAT').first;
    final thuCol = m.findCol(const ['thu vt']);
    expect(thuCol, isNotNull, reason: 'bảng chi tiết MBS phải có cột Thứ VT');
    final rows = visibleRows(m, const RowFilter(), const PageFilter(thu: {'3'}));
    expect(rows, isNotEmpty);
    for (final i in rows.where((i) => !m.isTotal[i])) {
      expect(m.rowValues[i][thuCol]!.contains('3'), isTrue);
    }
    expect(m.filterColumns, isNotEmpty);
    final c = m.filterColumns.first;
    final v = m.valuesOf(c).first;
    final r2 = visibleRows(m, RowFilter(byCol: {c: {v}}), const PageFilter());
    for (final i in r2.where((i) => !m.isTotal[i])) {
      expect(m.rowValues[i][c], v);
    }
    // ignore: avoid_print
    print('MBS_CAT cột lọc được: ${m.filterColumns.map((c) => m.colNames[c]).join(' | ')}');
  });
}
