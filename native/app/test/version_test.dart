// Số phiên bản hiện trong app (appVersion) phải khớp version trong pubspec.yaml.
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:kpi_native/ui/home_shell.dart';

void main() {
  test('appVersion khớp pubspec.yaml', () {
    final m = RegExp(r'^version:\s*([0-9.]+)', multiLine: true).firstMatch(File('pubspec.yaml').readAsStringSync());
    expect(appVersion, m!.group(1));
  });
}
