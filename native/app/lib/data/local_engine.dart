import 'dart:async';
import 'dart:convert';
import 'dart:io';

import 'package:http/http.dart' as http;

import 'filter_cache.dart' show ghRepo, ghToken;

/// App Mac: tự chạy App.py trên máy (Python 3.12 + pandas như Streamlit Cloud đóng gói trong
/// "KPI Dashboard.app/Contents/Resources/py", xem native/macpy/build_mac.sh) thay vì nhờ GitHub.
///   - tải App.py + data/ đúng commit dữ liệu app đang xem về ~/Library/Application Support
///     (file nào đã có — cùng mã blob — thì không tải lại)
///   - giữ 1 tiến trình Python chạy nền (pipeline/local_engine.py): data đọc 1 lần, lọc sau vài giây
class LocalEngine {
  LocalEngine._();
  static final instance = LocalEngine._();

  static String? get _pyDir {
    if (!Platform.isMacOS) return null;
    final res = File(Platform.resolvedExecutable).parent.parent.uri.resolve('Resources/py/').toFilePath();
    return File('${res}python/bin/python3').existsSync() ? res : null;
  }

  /// Có máy tính tại chỗ (chỉ bản Mac build bằng build_mac.sh).
  bool get available => _pyDir != null;

  final http.Client _client = http.Client();
  final Map<String, Future<String>> _snaps = {};
  Process? _proc;
  Future<void>? _starting;
  final Map<int, Completer<Map<String, dynamic>>> _wait = {};
  int _nextId = 0;
  String _buf = '';

  String get _home => '${Platform.environment['HOME']}/Library/Application Support/KPI Dashboard';

  /// Chuẩn bị sẵn (gọi khi app có manifest): tải data + bật Python để lần lọc đầu đỡ chờ.
  void warmUp(String sc) {
    if (!available) return;
    snapshot(sc).then((_) => _ensureProc()).then((_) => _selfTest(sc)).catchError((_) {});
  }

  /// Kiểm tra khi build: `open --env KPI_SELFTEST=<req JSON> "KPI Dashboard.app"`
  /// → ghi kết quả vào `Application Support/KPI Dashboard/selftest.txt`
  Future<void> _selfTest(String sc) async {
    final q = Platform.environment['KPI_SELFTEST'];
    if (q == null || q.isEmpty) return;
    final f = File('$_home/selftest.txt');
    final t = DateTime.now();
    try {
      final items = await compute({...(jsonDecode(q) as Map<String, dynamic>), 'sc': sc});
      f.writeAsStringSync('ok ${items.length} items ${DateTime.now().difference(t).inMilliseconds}ms\n'
          '${jsonEncode(items).substring(0, 300)}');
    } catch (e) {
      f.writeAsStringSync('error $e');
    }
  }

  /// Thư mục App.py + data/ của commit [sc] (tải phần còn thiếu).
  Future<String> snapshot(String sc) => _snaps[sc] ??= _download(sc).catchError((Object e) {
        _snaps.remove(sc);
        throw e;
      });

  Map<String, String> get _headers => {
        'Accept': 'application/vnd.github+json',
        if (ghToken.isNotEmpty) 'Authorization': 'Bearer $ghToken',
      };

  Future<String> _download(String sc) async {
    final dir = Directory('$_home/snap/${sc.substring(0, 12)}');
    final done = File('${dir.path}/.ok');
    if (done.existsSync()) return dir.path;
    final res = await _client
        .get(Uri.parse('https://api.github.com/repos/$ghRepo/git/trees/$sc?recursive=1'), headers: _headers)
        .timeout(const Duration(seconds: 60));
    if (res.statusCode != 200) throw HttpException('GitHub ${res.statusCode} (danh sách file)');
    final tree = ((jsonDecode(res.body) as Map)['tree'] as List).cast<Map>();
    final files = [
      for (final t in tree)
        if (t['type'] == 'blob' && (t['path'] == 'App.py' || '${t['path']}'.startsWith('data/'))) t
    ];
    final blobs = Directory('$_home/blobs')..createSync(recursive: true);
    if (dir.existsSync()) dir.deleteSync(recursive: true);
    for (final f in files) {
      final path = '${f['path']}', sha = '${f['sha']}';
      final blob = File('${blobs.path}/$sha');
      if (!blob.existsSync()) {
        final url = Uri.https('raw.githubusercontent.com', '/$ghRepo/$sc/$path');
        http.Response? r;
        for (var attempt = 1; attempt <= 3; attempt++) {
          try {
            r = await _client.get(url).timeout(const Duration(minutes: 3));
            if (r.statusCode == 200) break;
          } catch (_) {
            if (attempt == 3) rethrow;
          }
          await Future<void>.delayed(Duration(seconds: 2 * attempt));
        }
        if (r == null || r.statusCode != 200) throw HttpException('Tải $path lỗi ${r?.statusCode}');
        final tmp = File('${blob.path}.part');
        await tmp.writeAsBytes(r.bodyBytes, flush: true);
        await tmp.rename(blob.path);
      }
      final dst = File('${dir.path}/$path');
      dst.parent.createSync(recursive: true);
      await Link(dst.path).create(blob.path);
    }
    done.writeAsStringSync(sc);
    _prune(sc);
    return dir.path;
  }

  /// Giữ 2 commit gần nhất + các file chúng dùng; xoá phần cũ.
  void _prune(String keepSc) {
    try {
      final snaps = Directory('$_home/snap').listSync().whereType<Directory>().toList()
        ..sort((a, b) => b.statSync().modified.compareTo(a.statSync().modified));
      for (final d in snaps.skip(2)) {
        d.deleteSync(recursive: true);
      }
      final used = <String>{};
      for (final d in snaps.take(2)) {
        for (final e in d.listSync(recursive: true, followLinks: false)) {
          if (e is Link) used.add(e.targetSync().split('/').last);
        }
      }
      for (final b in Directory('$_home/blobs').listSync().whereType<File>()) {
        if (!used.contains(b.uri.pathSegments.last)) b.deleteSync();
      }
    } catch (_) {}
  }

  Future<void> _ensureProc() => _starting ??= () async {
        final py = _pyDir!;
        final p = await Process.start('${py}python/bin/python3', ['-u', '${py}engine/local_engine.py'],
            environment: {'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONIOENCODING': 'utf-8'});
        final ready = Completer<void>();
        p.stdout.transform(utf8.decoder).listen((chunk) {
          _buf += chunk;
          int nl;
          while ((nl = _buf.indexOf('\n')) >= 0) {
            final line = _buf.substring(0, nl);
            _buf = _buf.substring(nl + 1);
            if (line.trim().isEmpty) continue;
            final m = jsonDecode(line) as Map<String, dynamic>;
            if (m['ready'] == true) {
              if (!ready.isCompleted) ready.complete();
              continue;
            }
            _wait.remove(m['id'])?.complete(m);
          }
        });
        p.stderr.drain<void>();
        p.exitCode.then((code) {
          _proc = null;
          _starting = null;
          _buf = '';
          for (final c in _wait.values) {
            c.completeError(StateError('Python tại chỗ dừng (mã $code)'));
          }
          _wait.clear();
          if (!ready.isCompleted) ready.completeError(StateError('Không khởi động được Python tại chỗ'));
        });
        await ready.future.timeout(const Duration(seconds: 60));
        _proc = p;
      }();

  /// Nhật ký bộ lọc (Application Support/KPI Dashboard/filter.log, giữ ~1 MB gần nhất):
  /// yêu cầu, nơi tính, và dòng đầu + dòng tổng bảng đầu tiên → dò khi số khác Streamlit.
  void log(String what, Map<String, dynamic> req, List<Map<String, dynamic>>? items) {
    if (!Platform.isMacOS) return;
    try {
      String brief = '';
      if (items != null) {
        final t = items.where((i) => i['t'] == 'tbl').firstOrNull;
        final b = (t?['b'] as List?) ?? const [];
        String row(Object? r) => [for (final c in (r as List).take(6)) (c as Map)['x']].join(' | ');
        if (b.isNotEmpty) brief = ' ⇒ ${row(b.first)} … ${row(b.last)}';
      }
      final f = File('$_home/filter.log')..parent.createSync(recursive: true);
      if (f.existsSync() && f.lengthSync() > 1 << 20) f.writeAsStringSync('');
      f.writeAsStringSync('${DateTime.now().toIso8601String().substring(0, 19)} [$what] ${jsonEncode(req)}$brief\n',
          mode: FileMode.append);
    } catch (_) {}
  }

  Future<Map<String, dynamic>> _call(String sc, Map<String, dynamic> msg) async {
    final root = await snapshot(sc);
    await _ensureProc();
    final id = ++_nextId;
    final c = _wait[id] = Completer<Map<String, dynamic>>();
    _proc!.stdin.writeln(jsonEncode({...msg, 'id': id, 'root': root}));
    final res = await c.future.timeout(const Duration(minutes: 5));
    if (res['error'] != null) throw StateError('${res['error']}');
    return res;
  }

  /// Tính 1 yêu cầu bộ lọc (như GitHub filter-run) → items.
  Future<List<Map<String, dynamic>>> compute(Map<String, dynamic> req) async {
    final res = await _call(req['sc'] as String, {'req': req});
    return [for (final i in res['items'] as List) (i as Map).cast<String, dynamic>()];
  }

  /// Danh sách báo cáo / ngày / ĐDKD của tháng (như `kpi/<Thang>/index.json`).
  Future<Map<String, dynamic>> plan(String sc, String monthKey) async =>
      ((await _call(sc, {'op': 'plan', 'month_key': monthKey}))['plan'] as Map).cast<String, dynamic>();

  /// Số liệu Turnover cả tháng (như `turnover/<Thang>.json`).
  Future<Map<String, dynamic>> turnover(String sc, String monthKey) async =>
      ((await _call(sc, {'op': 'turnover', 'month_key': monthKey}))['turnover'] as Map).cast<String, dynamic>();

  // ---------- Data mới trên GitHub chưa xuất xong JSON → Mac tự tính ----------

  /// Commit dữ liệu Mac đang tự tính (null = dùng bản GitHub đã xuất).
  String? liveSc;
  DateTime? liveAt;
  String? liveMonth;
  Map<String, dynamic>? livePlan;
  String? _lastHead;
  bool _checking = false;

  /// Kiểm tra main trên GitHub: có commit đổi data/App.py mới hơn bản đã xuất ([remoteSc])
  /// → tải về + lấy danh sách báo cáo của tháng [monthKey]. Trả về true nếu đổi trạng thái.
  Future<bool> checkLive(String? remoteSc, String monthKey) async {
    if (!available || _checking) return false;
    _checking = true;
    try {
      final res = await _client
          .get(Uri.parse('https://api.github.com/repos/$ghRepo/commits/main'), headers: _headers)
          .timeout(const Duration(seconds: 20));
      if (res.statusCode != 200) return false;
      final j = jsonDecode(res.body) as Map;
      final head = j['sha'] as String;
      if (head == remoteSc) {
        // GitHub đã xuất xong bản mới nhất → bỏ bản tự tính
        final had = liveSc != null;
        liveSc = null;
        livePlan = null;
        liveMonth = null;
        liveAt = null;
        _lastHead = head;
        return had;
      }
      if (head == _lastHead && (liveSc == null || liveMonth == monthKey)) return false;
      if (remoteSc != null) {
        final cmp = await _client
            .get(Uri.parse('https://api.github.com/repos/$ghRepo/compare/$remoteSc...$head'), headers: _headers)
            .timeout(const Duration(seconds: 20));
        if (cmp.statusCode != 200) return false;
        final files = [for (final f in ((jsonDecode(cmp.body) as Map)['files'] as List? ?? const [])) '${(f as Map)['filename']}'];
        if (!files.any((f) => f == 'App.py' || f.startsWith('data/'))) {
          _lastHead = head;
          return false; // chỉ đổi code app, data như cũ
        }
      }
      final plan = await this.plan(head, monthKey);
      liveSc = head;
      liveMonth = monthKey;
      livePlan = plan;
      liveAt = DateTime.tryParse('${((j['commit'] as Map)['committer'] as Map)['date']}');
      _lastHead = head;
      log('live $head', {'month_key': monthKey}, null);
      return true;
    } catch (e) {
      log('live lỗi $e', {'month_key': monthKey}, null);
      return false;
    } finally {
      _checking = false;
    }
  }
}
