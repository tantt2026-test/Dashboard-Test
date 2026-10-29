import 'dart:async';
import 'dart:convert';
import 'dart:io';

import 'package:http/http.dart' as http;

import '../logic/turnover_logic.dart';

/// JSON do GitHub Action xuất ra branch `reports` của repo Dashboard-Test.
/// Build thử với server local:  --dart-define=DATA_BASE_URL=http://10.0.2.2:8000/
const dataBaseUrl = String.fromEnvironment(
  'DATA_BASE_URL',
  defaultValue: 'https://raw.githubusercontent.com/tantt2026-test/Dashboard-Test/reports/',
);

class MonthInfo {
  final String key, label;
  MonthInfo(this.key, this.label);
}

class Manifest {
  final DateTime? generatedAt;
  final String? sourceCommit;
  final List<MonthInfo> months;
  Manifest(this.generatedAt, this.sourceCommit, this.months);

  factory Manifest.fromJson(Map<String, dynamic> j) => Manifest(
        DateTime.tryParse((j['generated_at'] ?? '') as String),
        j['source_commit'] as String?,
        [
          for (final m in j['months'] as List)
            MonthInfo((m as Map<String, dynamic>)['key'] as String, m['label'] as String)
        ],
      );
}

class Loaded<T> {
  final T value;
  final bool fromCache; // true = mất mạng, đang xem bản lưu trên máy
  Loaded(this.value, this.fromCache);
}

class ReportRepository {
  final http.Client _client = http.Client();
  final Map<String, TurnoverMonth> _turnover = {};

  /// Thư mục lưu bản offline — không dùng plugin (path_provider/shared_preferences
  /// cần biên dịch NDK). Android: thư mục cache của app → dùng thư mục cha;
  /// macOS (sandbox): HOME là thư mục container của app.
  Future<File> _cacheFile(String rel) async {
    final String base;
    if (Platform.isAndroid) {
      base = '${Directory.systemTemp.parent.path}/files/reports';
    } else {
      base = '${Platform.environment['HOME'] ?? Directory.systemTemp.path}/Library/Application Support/kpi_reports';
    }
    final f = File('$base/$rel');
    await f.parent.create(recursive: true);
    return f;
  }

  /// Tải từ GitHub; lỗi mạng → dùng bản đã lưu lần trước.
  Future<Loaded<String>> _get(String rel) async {
    final cache = await _cacheFile(rel);
    try {
      // ?v= tránh CDN của raw.githubusercontent giữ bản cũ quá lâu
      final v = DateTime.now().millisecondsSinceEpoch ~/ 60000;
      final res = await _client
          .get(Uri.parse('$dataBaseUrl$rel?v=$v'))
          .timeout(const Duration(seconds: 20));
      if (res.statusCode != 200) {
        throw HttpException('HTTP ${res.statusCode}');
      }
      final body = utf8.decode(res.bodyBytes);
      await cache.writeAsString(body);
      return Loaded(body, false);
    } catch (e) {
      if (await cache.exists()) {
        return Loaded(await cache.readAsString(), true);
      }
      rethrow;
    }
  }

  Future<Loaded<Manifest>> manifest() async {
    final r = await _get('manifest.json');
    return Loaded(Manifest.fromJson(jsonDecode(r.value) as Map<String, dynamic>), r.fromCache);
  }

  Future<Loaded<TurnoverMonth>> turnover(String monthKey, {bool refresh = false}) async {
    if (!refresh && _turnover.containsKey(monthKey)) {
      return Loaded(_turnover[monthKey]!, false);
    }
    final r = await _get('turnover/$monthKey.json');
    final m = TurnoverMonth.fromJson(jsonDecode(r.value) as Map<String, dynamic>);
    _turnover[monthKey] = m;
    return Loaded(m, r.fromCache);
  }

  void clearMemory() => _turnover.clear();
}
