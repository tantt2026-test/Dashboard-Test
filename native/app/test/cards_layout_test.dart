// Thẻ số (metric card): chia đều số thẻ / hàng, không tràn chữ trên màn hình rộng và điện thoại.
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:kpi_native/ui/report_view.dart';

List<Map<String, dynamic>> cards(int n) => [
      for (var i = 0; i < n; i++)
        {
          'l': i.isEven ? 'HV TẾT · VIP ĐẠI SỨ · MUA HÀNG' : 'PC ON',
          'v': '123/122/231/53%',
          's': ['TH ngày/MTD/CT/%MTD', if (i % 3 == 0) ...['28,9/288,2/10%', 'DS Combo/DS Ngày/% (Triệu đồng)']],
          'ac': '#d53f8c',
        }
    ];

Future<void> pump(WidgetTester t, double w, int n, bool wide) async {
  t.view.physicalSize = Size(w, 1600);
  t.view.devicePixelRatio = 1;
  addTearDown(t.view.reset);
  await t.pumpWidget(MaterialApp(
      home: Scaffold(
          body: SingleChildScrollView(
              child: ReportItems(items: [
    {'t': 'cards', 'it': cards(n)}
  ], wide: wide)))));
}

void main() {
  for (final (w, wide, n) in [(1960.0, true, 18), (1960.0, true, 16), (1280.0, true, 18), (390.0, false, 18), (1960.0, true, 2)]) {
    testWidgets('w=$w n=$n không tràn', (t) async {
      await pump(t, w, n, wide);
      expect(t.takeException(), isNull);
      final rows = find.byType(IntrinsicHeight).evaluate().length;
      // ignore: avoid_print
      print('w=$w n=$n → $rows hàng');
    });
  }
}
