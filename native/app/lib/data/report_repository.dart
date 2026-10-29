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
  final List<MonthInfo> kpiMonths; // tháng có báo cáo tab KPI (giai đoạn 2)
  Manifest(this.generatedAt, this.sourceCommit, this.months, this.kpiMonths);

  factory Manifest.fromJson(Map<String, dynamic> j) => Manifest(
        DateTime.tryParse((j['generated_at'] ?? '') as String),
        j['source_commit'] as String?,
        [
          for (final m in j['months'] as List)
            MonthInfo((m as Map<String, dynamic>)['key'] as String, m['label'] as String)
        ],
        [
          for (final m in (j['kpi_months'] ?? const []) as List)
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
  Future<Loaded<String>> _getPublic(String rel) => _get(rel);

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

// ===================== Giai đoạn 2: báo cáo tab KPI =====================

class KpiReportInfo {
  final String code, name, group; // group: 'kpi' (tab Báo cáo KPI) | 'tab' (tab khác)
  KpiReportInfo(this.code, this.name, [this.group = 'kpi']);
}

/// `kpi/<Thang>/index.json`
class KpiIndex {
  final String monthKey, monthLabel, defaultDate;
  final int year, month;
  final List<String> dates; // có bản "Tất cả ĐDKD"
  final List<String> nvDates; // có bản lọc từng ĐDKD
  final List<String> tabDates; // các tab khác (MCP, Tracking...) chỉ có ngày mặc định
  final List<String> nv;
  final Map<String, String> nvSlugs;
  final List<KpiReportInfo> reports;

  KpiIndex.fromJson(Map<String, dynamic> j)
      : monthKey = j['month_key'] as String,
        monthLabel = j['month_label'] as String,
        defaultDate = j['default_date'] as String,
        year = j['year'] as int,
        month = j['month'] as int,
        dates = [for (final d in j['dates'] as List) d as String],
        nvDates = [for (final d in (j['nv_dates'] ?? const []) as List) d as String],
        tabDates = [for (final d in (j['tab_dates'] ?? const []) as List) d as String],
        nv = [for (final n in j['nv'] as List) n as String],
        nvSlugs = {for (final e in (j['nv_slugs'] as Map).entries) e.key as String: e.value as String},
        reports = [
          for (final r in j['reports'] as List)
            KpiReportInfo((r as Map)['code'] as String, r['name'] as String, (r['group'] as String?) ?? 'kpi')
        ];
}

/// 1 báo cáo đã xuất: danh sách item (tiêu đề, bảng, thẻ, biểu đồ...).
class ReportDoc {
  final String code, name, date;
  final List<String> filter;
  final List<Map<String, dynamic>> items;
  final Map<String, Map<String, dynamic>> main; // ô lọc chung (Thứ VT, Mã KH, Tên KH) + cách áp
  ReportDoc.fromJson(Map<String, dynamic> j)
      : code = j['code'] as String,
        name = j['name'] as String,
        date = j['date'] as String,
        filter = [for (final f in j['filter'] as List) f as String],
        items = [for (final i in j['items'] as List) i as Map<String, dynamic>],
        main = {
          for (final e in ((j['main'] as Map?) ?? const {}).entries)
            e.key as String: (e.value as Map).cast<String, dynamic>()
        };
}

extension KpiRepository on ReportRepository {
  Future<Loaded<KpiIndex>> kpiIndex(String monthKey) async {
    final r = await _getPublic('kpi/$monthKey/index.json');
    return Loaded(KpiIndex.fromJson(jsonDecode(r.value) as Map<String, dynamic>), r.fromCache);
  }

  /// Bản App.py tính sẵn cho 1 giá trị ô lọc kiểu "tính lại".
  Future<List<Map<String, dynamic>>> kpiVariant(KpiIndex idx, String code, String file) async {
    final r = await _getPublic('kpi/${idx.monthKey}/$code/$file');
    return [for (final i in (jsonDecode(r.value) as Map)['items'] as List) i as Map<String, dynamic>];
  }

  Future<Loaded<ReportDoc>> kpiDoc(KpiIndex idx, String code, String date, String? nv) async {
    final name = nv == null ? '$date.json' : '${date}__${idx.nvSlugs[nv]}.json';
    final r = await _getPublic('kpi/${idx.monthKey}/$code/$name');
    return Loaded(ReportDoc.fromJson(jsonDecode(r.value) as Map<String, dynamic>), r.fromCache);
  }
}
