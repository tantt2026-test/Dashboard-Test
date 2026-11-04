// Sale Sup 'Cả 2': bảng tách theo team ('seg') — lọc ĐDKD tính lại dòng Tổng từng team + Total chung.
import 'package:flutter_test/flutter_test.dart';
import 'package:kpi_native/logic/filter_engine.dart';
import 'package:kpi_native/logic/turnover_logic.dart';

List<Map<String, String>> row(String stt, String name, String v) =>
    [{'x': stt}, {'x': name}, {'x': v}];

Map<String, dynamic> table() => {
      't': 'tbl',
      'h': [
        [{'x': 'STT'}, {'x': 'Tên NVBH'}, {'x': 'Số'}]
      ],
      'b': [
        row('1', 'A', '1.000'),
        row('2', 'B', '2.000'),
        row('-', 'SS Tân Total', '3.000'),
        row('1', 'C', '10.000'),
        row('2', 'D', '20.000'),
        row('-', 'SS Vy Total', '30.000'),
        row('-', 'TOTAL 2 SALE SUP', '33.000'),
      ],
      'tot': {
        '2': {'op': 'sum', 't': '.', 'd': ',', 'n': 0}
      },
      'seg': [3, 6],
    };

List<List<String>> cells(FilterResult r) =>
    [for (final row in (r.items.first['b'] as List)) [for (final c in row as List) '${(c as Map)['x']}']];

void main() {
  test('lọc 2 NV ở 2 team: Tổng từng team + Total chung tính lại', () {
    final r = applyFilters([table()], const [], const {}, multiNv: {'B', 'C'});
    expect(cells(r), [
      ['1', 'B', '2.000'],
      ['-', 'SS Tân Total', '2.000'],
      ['1', 'C', '10.000'],
      ['-', 'SS Vy Total', '10.000'],
      ['-', 'TOTAL 2 SALE SUP', '12.000'],
    ]);
    expect(r.items.first['seg'], [2, 4]);
  });

  test('lọc NV 1 team: bỏ dòng Tổng team không còn dòng', () {
    final r = applyFilters([table()], const [], const {}, multiNv: {'D'});
    expect(cells(r), [
      ['1', 'D', '20.000'],
      ['-', 'SS Vy Total', '20.000'],
      ['-', 'TOTAL 2 SALE SUP', '20.000'],
    ]);
    expect(r.items.first['seg'], [0, 2]);
  });

  test('Turnover: NV theo team + dòng Tổng team, dòng cuối = Total chung', () {
    final m = TurnoverMonth.fromJson({
      'month_key': 'Thang11', 'month_label': 'T11', 'title': 'TURNOVER', 'total_label': 'TOTAL 2 SALE SUP',
      'year': 2026, 'month': 11, 'nv': ['A', 'B', 'C'],
      'teams': [
        {'label': 'SS Tân Total', 'nv': ['A', 'B']},
        {'label': 'SS Vy Total', 'nv': ['C']},
      ],
      'days': {
        '2026-11-03': {
          'timegone': {'total': 26, 'elapsed': 3, 'remain': 23, 'pct': 11.5},
          'rows': [
            {'code': '1', 'name': 'A', 'target': 100, 'today': 1, 'mtd': 10},
            {'code': '2', 'name': 'B', 'target': 100, 'today': 2, 'mtd': 20},
            {'code': '3', 'name': 'C', 'target': 200, 'today': 3, 'mtd': 30},
          ],
        }
      },
    });
    final r = buildTurnover(m, '2026-11-03', const []);
    expect([for (final x in r.tableRows) '${x.stt}|${x.name}|${x.mtd}'],
        ['1|A|10.0', '2|B|20.0', '-|SS Tân Total|30.0', '1|C|30.0', '-|SS Vy Total|30.0']);
    expect(r.total.name, 'TOTAL 2 SALE SUP');
    expect(r.total.mtd, 60);
  });
}
