import 'dart:async';
import 'dart:convert';
import 'dart:io';

import 'package:crypto/crypto.dart';
import 'package:http/http.dart' as http;

import 'local_engine.dart';

/// Kết quả bộ lọc kiểu "tính lại" do GitHub Actions chạy App.py rồi lưu ở branch `filters`:
///   `<source_commit[:12]>/<mã tổ hợp>.json`   (pipeline/run_request.py tính mã y hệt)
/// Chưa có → kích hoạt workflow filter-run.yml (token giới hạn: Actions R/W + Contents R),
/// chờ vài phút rồi tải. Đã có → tải ngay (lần sau mọi máy đều nhanh).
const ghRepo = 'tantt2026-test/Dashboard-Test';

/// Token GitHub giới hạn, đưa vào lúc build: --dart-define=GH_TOKEN=...
/// (không lưu trong code / repo).
const ghToken = String.fromEnvironment('GH_TOKEN');

/// JSON chuẩn hoá giống Python: khoá sắp xếp, không khoảng trắng, giữ Unicode.
String canonicalJson(Object? v) {
  Object? sortDeep(Object? x) {
    if (x is Map) {
      final keys = x.keys.map((k) => '$k').toList()..sort();
      return {for (final k in keys) k: sortDeep(x[k])};
    }
    if (x is List) return [for (final e in x) sortDeep(e)];
    return x;
  }

  return jsonEncode(sortDeep(v));
}

Map<String, dynamic> canonicalReq(Map<String, dynamic> req) => {
      'month_key': req['month_key'],
      'date': (req['date'] as String).substring(0, 10),
      'code': req['code'],
      'ddkd': req['ddkd'] ?? const [],
      'values': {
        for (final e in ((req['values'] as Map?) ?? const {}).entries)
          if (e.value != null && e.value != '' && !(e.value is List && (e.value as List).isEmpty)) '${e.key}': e.value
      },
    };

String comboKey(Map<String, dynamic> req) =>
    sha1.convert(utf8.encode(canonicalJson(canonicalReq(req)))).toString().substring(0, 20);

class FilterJob {
  final String key;
  final DateTime started = DateTime.now();
  List<Map<String, dynamic>>? items;
  String? error;
  bool dispatched = false;
  bool local = false; // app Mac tự tính bằng App.py trên máy
  FilterJob(this.key);
  int get waitedSeconds => DateTime.now().difference(started).inSeconds;
}

class FilterCache {
  final http.Client _client = http.Client();
  final Map<String, FilterJob> _jobs = {};

  Map<String, String> get _headers => {
        'Accept': 'application/vnd.github.raw+json',
        'X-GitHub-Api-Version': '2022-11-28',
        if (ghToken.isNotEmpty) 'Authorization': 'Bearer $ghToken',
      };

  /// Đọc kết quả đã lưu (API, không qua CDN → thấy file mới ngay). null = chưa có.
  Future<List<Map<String, dynamic>>?> _read(String sc, String key) async {
    final path = '${sc.substring(0, sc.length < 12 ? sc.length : 12)}/$key.json';
    final res = await _client
        .get(Uri.parse('https://api.github.com/repos/$ghRepo/contents/$path?ref=filters'), headers: _headers)
        .timeout(const Duration(seconds: 30));
    if (res.statusCode == 404) return null;
    if (res.statusCode != 200) throw HttpException('GitHub ${res.statusCode}');
    final j = jsonDecode(utf8.decode(res.bodyBytes)) as Map<String, dynamic>;
    return [for (final i in j['items'] as List) i as Map<String, dynamic>];
  }

  Future<void> _dispatch(Map<String, dynamic> req) async {
    if (ghToken.isEmpty) throw StateError('App chưa có token GitHub để nhờ tính');
    final res = await _client
        .post(
          Uri.parse('https://api.github.com/repos/$ghRepo/actions/workflows/filter-run.yml/dispatches'),
          headers: {..._headers, 'Content-Type': 'application/json'},
          body: jsonEncode({
            'ref': 'main',
            'inputs': {'req': jsonEncode(req)},
          }),
        )
        .timeout(const Duration(seconds: 30));
    if (res.statusCode != 204) throw HttpException('Không kích hoạt được GitHub (${res.statusCode})');
  }

  /// Lấy kết quả cho [req] (cần 'sc' = commit dữ liệu đang xem). [onUpdate] gọi khi có tiến triển.
  FilterJob get(Map<String, dynamic> req, void Function() onUpdate) {
    final key = comboKey(req);
    final existing = _jobs[key];
    if (existing != null && existing.error == null) return existing;
    final job = FilterJob(key);
    _jobs[key] = job;
    () async {
      // App Mac: tự chạy App.py trên máy (vài giây); lỗi thì quay về GitHub như điện thoại
      if (LocalEngine.instance.available) {
        job.local = true;
        onUpdate();
        try {
          job.items = await LocalEngine.instance.compute(req);
          LocalEngine.instance.log('local ok', req, job.items);
          onUpdate();
          return;
        } catch (e) {
          LocalEngine.instance.log('local lỗi: $e', req, null);
          job.local = false;
        }
      }
      try {
        final sc = req['sc'] as String;
        var items = await _read(sc, key);
        if (items == null) {
          await _dispatch(req);
          job.dispatched = true;
          onUpdate();
          // GitHub cần ~1,5–3 phút: bật máy, cài thư viện, chạy App.py, lưu
          final deadline = DateTime.now().add(const Duration(minutes: 8));
          await Future.delayed(const Duration(seconds: 45));
          while (items == null && DateTime.now().isBefore(deadline)) {
            await Future.delayed(const Duration(seconds: 10));
            items = await _read(sc, key);
            onUpdate();
          }
          if (items == null) throw TimeoutException('GitHub chưa tính xong sau 8 phút');
        }
        job.items = items;
        LocalEngine.instance.log(job.dispatched ? 'github tính' : 'github có sẵn', req, items);
      } catch (e) {
        LocalEngine.instance.log('github lỗi: $e', req, null);
        job.error = '$e';
      }
      onUpdate();
    }();
    return job;
  }
}
