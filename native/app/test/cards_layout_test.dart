// Thẻ số (metric card): chia đều số thẻ / hàng, không tràn chữ trên màn hình rộng và điện thoại.
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:kpi_native/ui/report_view.dart';

List<Map<String, dynamic>> cards(int n) => [
      for (var i = 0; i < n; i++)
        {
          'l': i.isEven ? 'HV TẾT - BRAND_VIPDAISU\nĐẠT NHIỆM VỤ' : 'PC ON',
          'v': '123/122/231/53%',
          's': ['TH ngày/MTD/CT/%MTD', if (i % 3 == 0) ...['28,9/288,2/10%', 'DS Combo/DS Ngày/% (Triệu đồng)']],
          if (i % 3 == 0) 'sv': [1], // dòng số phụ: cùng cỡ dòng số chính
          'ac': '#d53f8c',
        }
    ];

final catCard = {
  'l': 'SELL OUT BY CAT (Triệu đồng)',
  'v': '',
  'full': 1,
  'ac': '#2c5282',
  's': ['TH/CT/%TH'],
  'grid': [
    [for (final c in ['Seasoning', 'Refreshment Drinks', 'Convenience Foods', 'Coffee']) [c, '155,1/148,3/105%']],
    [for (final c in ['Processed Meats', 'Home Care', 'Nutrition', 'Personal Care']) [c, '22,1/25,2/88%']],
  ],
};

Future<void> pump(WidgetTester t, double w, int n, bool wide) async {
  t.view.physicalSize = Size(w, 1600);
  t.view.devicePixelRatio = 1;
  addTearDown(t.view.reset);
  await t.pumpWidget(MaterialApp(
      home: Scaffold(
          body: SingleChildScrollView(
              child: ReportItems(items: [
    {'t': 'cards', 'it': [...cards(n), catCard]}
  ], wide: wide)))));
}

void main() {
  for (final (w, wide, n) in [(1960.0, true, 18), (1960.0, true, 16), (1280.0, true, 18), (390.0, false, 18), (1960.0, true, 2)]) {
    testWidgets('w=$w n=$n không tràn', (t) async {
      await pump(t, w, n, wide);
      expect(t.takeException(), isNull);
      if (n > 2) expect(find.text('ĐẠT NHIỆM VỤ'), findsWidgets); // tiêu đề 2 dòng
      // thẻ SELL OUT BY CAT: rộng cả hàng, dưới cùng
      final cat = t.getRect(find.text('SELL OUT BY CAT (Triệu đồng)'));
      final first = t.getRect(find.text('123/122/231/53%').first);
      expect(cat.top, greaterThan(first.top));
      expect(find.text('Personal Care'), findsOneWidget);
      final main = t.widget<Text>(find.text('123/122/231/53%').first).style!.fontSize;
      expect(t.widget<Text>(find.text('28,9/288,2/10%').first).style!.fontSize, main);
      final rows = find.byType(IntrinsicHeight).evaluate().length;
      // ignore: avoid_print
      print('w=$w n=$n → $rows hàng');
    });
  }
}
