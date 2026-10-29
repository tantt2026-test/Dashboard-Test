// Dựng giao diện mọi báo cáo đã xuất (JSON thật) để bắt lỗi layout / ngoại lệ.
//   REPORTS_DIR=<thư mục out>/kpi/Thang10 flutter test test/report_render_test.dart
import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:kpi_native/ui/report_view.dart';

void main() {
  final dir = Platform.environment['REPORTS_DIR'];
  if (dir == null || !Directory(dir).existsSync()) {
    test('REPORTS_DIR chưa đặt', () {}, skip: 'Đặt REPORTS_DIR để chạy');
    return;
  }
  final idx = jsonDecode(
    File('$dir/index.json').readAsStringSync(),
  ) as Map<String, dynamic>;
  final date = idx['default_date'] as String;
  // ALL=1: mọi file (mọi ngày + mọi ĐDKD) ở cỡ điện thoại; mặc định: ngày mặc định × 2 cỡ màn hình
  final all = Platform.environment['ALL'] == '1';
  for (final r in (idx['reports'] as List).cast<Map>()) {
    final code = r['code'] as String;
    final files = all
        ? (Directory('$dir/$code')
              .listSync()
              .whereType<File>()
              .map((f) => f.path)
              .toList()
            ..sort())
        : ['$dir/$code/$date.json'];
    for (final path in files)
      for (final size
          in all
              ? const [Size(390, 844)]
              : const [Size(390, 844), Size(1280, 800)]) {
        testWidgets('$code ${path.split('/').last} @ ${size.width.toInt()}px', (
          tester,
        ) async {
          final doc =
              jsonDecode(File(path).readAsStringSync()) as Map<String, dynamic>;
          tester.view.physicalSize = size;
          tester.view.devicePixelRatio = 1;
          addTearDown(tester.view.reset);
          await tester.pumpWidget(
            MaterialApp(
              home: Scaffold(
                body: ListView(
                  padding: const EdgeInsets.all(12),
                  children: [
                    ReportItems(
                      items: (doc['items'] as List)
                          .cast<Map<String, dynamic>>(),
                      wide: size.width >= 720,
                    ),
                  ],
                ),
              ),
            ),
          );
          await tester.pumpAndSettle();
          // cuộn hết trang để dựng mọi phần
          await tester.drag(
            find.byType(ListView).first,
            const Offset(0, -20000),
          );
          await tester.pumpAndSettle();
          expect(tester.takeException(), isNull);
        });
      }
  }
}
