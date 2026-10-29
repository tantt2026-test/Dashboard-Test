// Dùng bởi pipeline/parity_check.py: chạy logic Dart của app trên các ca test,
// in kết quả dạng JSON để Python so với build_turnover_report.
//   dart run tool/parity_cli.dart <Thang10.json> < cases.json
import 'dart:convert';
import 'dart:io';

import 'package:kpi_native/logic/pyfmt.dart';
import 'package:kpi_native/logic/turnover_logic.dart';

void main(List<String> args) {
  final month = TurnoverMonth.fromJson(
      jsonDecode(File(args[0]).readAsStringSync()) as Map<String, dynamic>);
  final input = jsonDecode(stdin.readLineSync(encoding: utf8) ?? '{}') as Map<String, dynamic>;

  final out = <String, dynamic>{};
  out['cases'] = [
    for (final c in input['cases'] as List)
      () {
        final r = buildTurnover(month, c['date'] as String,
            [for (final n in c['filter'] as List) n as String]);
        return {
          'rows': [
            for (final row in r.rows) {'code': row.code, ...row.display()}
          ],
          'total': r.total.display(),
          'top3': r.top3Text,
          'bottom3': r.bottom3Text,
          'result_text': r.resultText,
        };
      }()
  ];
  out['fmt'] = [
    for (final f in input['fmt'] as List)
      {
        'fixed': pyFixed((f[0] as num).toDouble(), f[1] as int),
        'thousands': pyThousands((f[0] as num).toDouble(), f[1] as int),
        'round_str': pyStr(pyRound((f[0] as num).toDouble(), f[1] as int)),
      }
  ];
  stdout.write(jsonEncode(out));
}
