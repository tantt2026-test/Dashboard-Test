// Dựng giao diện mọi báo cáo đã xuất (JSON thật) để bắt lỗi layout / ngoại lệ,
// bấm thử nút toàn màn hình + lọc.
//   REPORTS_DIR=<thư mục out>/kpi/Thang10 flutter test test/report_render_test.dart
//   ALL=1 → mọi file (mọi ngày + mọi ĐDKD) ở cỡ điện thoại
import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:kpi_native/ui/app_scale.dart';
import 'package:kpi_native/ui/report_table.dart';
import 'package:kpi_native/ui/report_view.dart';
import 'package:kpi_native/ui/table_model.dart';

void main() {
  final dir = Platform.environment['REPORTS_DIR'];
  if (dir == null || !Directory(dir).existsSync()) {
    test('REPORTS_DIR chưa đặt', () {}, skip: 'Đặt REPORTS_DIR để chạy');
    return;
  }
  final idx = jsonDecode(File('$dir/index.json').readAsStringSync()) as Map<String, dynamic>;
  final date = idx['default_date'] as String;
  final all = Platform.environment['ALL'] == '1';
  final sizes = all ? const [Size(390, 844)] : const [Size(390, 844), Size(1280, 800)];

  for (final r in (idx['reports'] as List).cast<Map>()) {
    final code = r['code'] as String;
    final files = all
        ? (Directory('$dir/$code').listSync().whereType<File>().map((f) => f.path).toList()..sort())
        : ['$dir/$code/$date.json'];
    for (final path in files) {
      for (final size in sizes) {
        for (final zoom in all ? const [1.0] : const [0.7, 1.0, 1.5]) {
          testWidgets('$code ${path.split('/').last} @ ${size.width.toInt()}px x$zoom', (tester) async {
            final doc = jsonDecode(File(path).readAsStringSync()) as Map<String, dynamic>;
            tester.view.physicalSize = size;
            tester.view.devicePixelRatio = 1;
            addTearDown(tester.view.reset);
            final scale = AppScale()..value = zoom;
            await tester.pumpWidget(MaterialApp(
              builder: (ctx, child) => ScaledApp(scale: scale, child: child!),
              home: Scaffold(
                body: PageFilterScope(
                  filter: const PageFilter(thu: {'2'}, query: 'a'),
                  child: ListView(padding: const EdgeInsets.all(12), children: [
                    ReportItems(items: (doc['items'] as List).cast<Map<String, dynamic>>(), wide: size.width >= 720),
                  ]),
                ),
              ),
            ));
            await tester.pumpAndSettle();
            expect(tester.takeException(), isNull);
            await tester.drag(find.byType(ListView).first, const Offset(0, -20000));
            await tester.pumpAndSettle();
            expect(tester.takeException(), isNull);
            // mở toàn màn hình bảng đầu tiên đang thấy, cuộn trong đó rồi đóng
            final full = find.byTooltip('Toàn màn hình');
            if (!all && full.evaluate().isNotEmpty) {
              await tester.ensureVisible(full.first);
              await tester.pumpAndSettle();
              await tester.tap(full.first);
              await tester.pumpAndSettle();
              expect(tester.takeException(), isNull);
              await tester.tap(find.byTooltip('Phóng to'));
              await tester.pumpAndSettle();
              await tester.tap(find.byTooltip('Vừa màn hình').evaluate().isNotEmpty
                  ? find.byTooltip('Vừa màn hình')
                  : find.byTooltip('Bỏ vừa màn hình'));
              await tester.pumpAndSettle();
              expect(tester.takeException(), isNull);
            }
          });
        }
      }
    }
  }
}
