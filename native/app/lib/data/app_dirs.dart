import 'dart:io';

/// Thư mục lưu dữ liệu của app (không dùng plugin path_provider):
/// Android: thư mục files của app; Windows: %APPDATA%\KPI Dashboard;
/// macOS (sandbox): HOME là thư mục container của app.
String appDataDir() {
  if (Platform.isAndroid) return '${Directory.systemTemp.parent.path}/files';
  if (Platform.isWindows) {
    final root = Platform.environment['APPDATA'] ?? Platform.environment['LOCALAPPDATA'] ?? Directory.systemTemp.path;
    return '$root\\KPI Dashboard\\kpi_reports';
  }
  return '${Platform.environment['HOME'] ?? Directory.systemTemp.path}/Library/Application Support/kpi_reports';
}

/// Tên đăng nhập sinh trắc theo hệ máy (Touch ID / Windows Hello / vân tay).
String bioName() => Platform.isMacOS ? 'Touch ID' : (Platform.isWindows ? 'Windows Hello' : 'vân tay');
