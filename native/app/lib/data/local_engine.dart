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
    final res = File(Platform.resolvedExecutable).parent.parent.uri
        .resolve('Resources/py/')
        .toFilePath();
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

  String get _home =>
      '${Platform.environment['HOME']}/Library/Application Support/KPI Dashboard';

  /// Chuẩn bị sẵn (gọi khi app có manifest): tải data + bật Python để lần lọc đầu đỡ chờ.
  void warmUp(String sc) {
    if (!available) return;
    snapshot(sc)
        .then((_) => _ensureProc())
        .then((_) => _selfTest(sc))
        .catchError((_) {});
  }

  /// Kiểm tra khi build: `open --env KPI_SELFTEST=<req JSON> "KPI Dashboard.app"`
  /// → ghi kết quả vào `Application Support/KPI Dashboard/selftest.txt`
  Future<void> _selfTest(String sc) async {
    final q = Platform.environment['KPI_SELFTEST'];
    if (q == null || q.isEmpty) return;
    final f = File('$_home/selftest.txt');
    final t = DateTime.now();
    try {
      final items = await compute({
        ...(jsonDecode(q) as Map<String, dynamic>),
        'sc': sc,
      });
      f.writeAsStringSync(
        'ok ${items.length} items ${DateTime.now().difference(t).inMilliseconds}ms\n'
        '${jsonEncode(items).substring(0, 300)}',
      );
    } catch (e) {
      f.writeAsStringSync('error $e');
    }
  }

  /// Thư mục App.py + data/ của commit [sc] (tải phần còn thiếu).
  Future<String> snapshot(String sc) async {
    final dir = await (_snaps[sc] ??= _download(sc).catchError((Object e) {
      _snaps.remove(sc);
      throw e;
    }));
    // _prune() có thể đã xoá thư mục này trong lúc Future trên vẫn còn cache (vd. bị
    // đẩy ra khỏi 6 bộ "gần dùng nhất" bởi các bộ khác) → tải lại thay vì trả đường dẫn chết.
    if (File('$dir/.ok').existsSync()) return dir;
    _snaps.remove(sc);
    return snapshot(sc);
  }

  Map<String, String> get _headers => {
    'Accept': 'application/vnd.github+json',
    if (ghToken.isNotEmpty) 'Authorization': 'Bearer $ghToken',
  };

  Future<String> _download(String sc) async {
    final dir = Directory('$_home/snap/${sc.substring(0, 12)}');
    final done = File('${dir.path}/.ok');
    if (done.existsSync()) return dir.path;
    if (dir.existsSync()) dir.deleteSync(recursive: true);
    await _fetchTree(
      ghRepo,
      sc,
      dir.path,
      (p) => p == 'App.py' || p.startsWith('data/'),
    );
    done.writeAsStringSync(sc);
    _prune(sc);
    return dir.path;
  }

  /// Repo data team Vy (Sale Sup 'vy' và phần Vy của 'all').
  static const vyRepo = 'Tantt2026/Vyntt_Dashboard';

  final Map<String, Future<String>> _appPy = {};

  /// Chỉ App.py của commit [sc] (KHÔNG kéo theo data/ team Tân) — dùng cho team 'vy', vì team
  /// này không đụng tới data Tân. Nếu [sc] đã có sẵn bộ data đầy đủ (snapshot/snapshotFor khác
  /// đã tải) thì dùng lại luôn, không tải lại.
  Future<String> _appPyOnly(String sc) async {
    final root = await (_appPy[sc] ??=
        () async {
          final done = File('$_home/snap/${sc.substring(0, 12)}/.ok');
          if (done.existsSync()) return done.parent.path;
          final dir = Directory('$_home/apppy/${sc.substring(0, 12)}');
          final doneAp = File('${dir.path}/.ok');
          if (doneAp.existsSync()) return dir.path;
          await _fetchTree(ghRepo, sc, dir.path, (p) => p == 'App.py');
          doneAp.writeAsStringSync(sc);
          return dir.path;
        }().catchError((Object e) {
          _appPy.remove(sc);
          throw e;
        }));
    // như snapshot(): _prune() có thể đã xoá thư mục cache trong lúc Future còn nhớ.
    if (File('$root/App.py').existsSync()) return root;
    _appPy.remove(sc);
    return _appPyOnly(sc);
  }

  /// Thư mục App.py + data/ cho Sale Sup của [req] (team tan: [snapshot]; vy: App.py commit [sc] +
  /// data repo Vyntt commit 'dsc'; all: data 2 team ghép bằng team_data.py — như GitHub).
  Future<String> snapshotFor(Map<String, dynamic> req) async {
    final team = (req['team'] as String?) ?? 'tan';
    final sc = req['sc'] as String;
    if (team == 'tan') return snapshot(sc);
    final dsc = (req['dsc'] as String?) ?? 'HEAD';
    final key =
        '${team}_${sc.substring(0, 12)}_${dsc.length > 12 ? dsc.substring(0, 12) : dsc}';
    final dir = await (_snaps[key] ??= _snapshotFor(team, sc, dsc, key));
    if (File('$dir/.ok').existsSync()) return dir;
    _snaps.remove(key);
    return snapshotFor(req);
  }

  Future<String> _snapshotFor(String team, String sc, String dsc, String key) {
    return () async {
          final dir = Directory('$_home/snap/$key');
          final done = File('${dir.path}/.ok');
          if (done.existsSync()) return dir.path;
          final vyDir = Directory(
            '$_home/snap/vydata_${dsc.length > 12 ? dsc.substring(0, 12) : dsc}',
          );
          Future<void> ensureVyDir() async {
            if (File('${vyDir.path}/.ok').existsSync()) return;
            if (vyDir.existsSync()) vyDir.deleteSync(recursive: true);
            await _fetchTree(
              vyRepo,
              dsc,
              vyDir.path,
              (p) => p.startsWith('data/'),
            );
            File('${vyDir.path}/.ok').writeAsStringSync(dsc);
          }

          // team 'vy' chỉ cần App.py của Tân, không cần data/ của Tân → khỏi tải cho đỡ chậm.
          // snapshot()/_appPyOnly() tự kiểm tra lại & tải lại nếu bị _prune() xoá giữa chừng,
          // nên gọi lại (rẻ nếu còn nguyên) ngay trước lúc dùng để tránh đường dẫn đã chết.
          Future<String> tanRoot() => team == 'vy' ? _appPyOnly(sc) : snapshot(sc);

          await ensureVyDir();
          await tanRoot();
          if (dir.existsSync()) dir.deleteSync(recursive: true);
          dir.createSync(recursive: true);
          await ensureVyDir();
          final tan = await tanRoot();
          await Link('${dir.path}/App.py')
              .create(File('$tan/App.py').resolveSymbolicLinksSync());
          if (team == 'vy') {
            await Link('${dir.path}/data').create('${vyDir.path}/data');
          } else {
            await _ensureProc();
            await _call(null, {
              'op': 'combine',
              'a': '$tan/data',
              'b': '${vyDir.path}/data',
              'out': '${dir.path}/data',
            }, root: dir.path);
          }
          done.writeAsStringSync(key);
          _prune(key);
          return dir.path;
        }().catchError((Object e) {
          _snaps.remove(key);
          throw e;
        });
  }

  Future<void> _fetchTree(
    String repo,
    String ref,
    String dirPath,
    bool Function(String) want,
  ) async {
    final res = await _client
        .get(
          Uri.parse(
            'https://api.github.com/repos/$repo/git/trees/$ref?recursive=1',
          ),
          headers: _headers,
        )
        .timeout(const Duration(seconds: 60));
    if (res.statusCode != 200)
      throw HttpException('GitHub ${res.statusCode} (danh sách file $repo)');
    final tree = ((jsonDecode(res.body) as Map)['tree'] as List).cast<Map>();
    final files = [
      for (final t in tree)
        if (t['type'] == 'blob' && want('${t['path']}')) t,
    ];
    final blobs = Directory('$_home/blobs')..createSync(recursive: true);
    for (final f in files) {
      final path = '${f['path']}', sha = '${f['sha']}';
      final blob = File('${blobs.path}/$sha');
      if (!blob.existsSync()) {
        final url = Uri.https('raw.githubusercontent.com', '/$repo/$ref/$path');
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
        if (r == null || r.statusCode != 200)
          throw HttpException('Tải $path lỗi ${r?.statusCode}');
        final tmp = File('${blob.path}.part');
        await tmp.writeAsBytes(r.bodyBytes, flush: true);
        await tmp.rename(blob.path);
      }
      final dst = File('$dirPath/$path');
      dst.parent.createSync(recursive: true);
      await Link(dst.path).create(blob.path);
    }
  }

  /// Giữ 6 bộ data gần nhất (các Sale Sup) + các file chúng dùng; xoá phần cũ.
  // snap/ giờ chứa nhiều loại thư mục dùng chung 1 quota (tan gốc, vy_*, all_*, vydata_*)
  // — mỗi lần xem nhiều Sale Sup/ngày khác nhau có thể tạo >6 thư mục trong vài phút, nên
  // để 6 thì sẽ xoá nhầm thư mục đang được dùng dở (vd. vydata_ vừa qua bước kiểm tra .ok
  // nhưng chưa kịp đọc xong data/ trong 1 lần build khác) → lỗi "No such file or directory".
  // Vì file nặng thật sự nằm ở blobs/ (dùng chung qua symlink, không nhân bản), giữ nhiều
  // thư mục snap/apppy hơn gần như không tốn ổ đĩa thêm.
  static const _keepSnaps = 30;

  void _prune(String keepSc) {
    try {
      final snaps =
          Directory('$_home/snap').listSync().whereType<Directory>().toList()
            ..sort(
              (a, b) => b.statSync().modified.compareTo(a.statSync().modified),
            );
      for (final d in snaps.skip(_keepSnaps)) {
        d.deleteSync(recursive: true);
      }
      final apDir = Directory('$_home/apppy');
      final apSnaps = apDir.existsSync()
          ? apDir.listSync().whereType<Directory>().toList()
          : <Directory>[];
      apSnaps.sort(
        (a, b) => b.statSync().modified.compareTo(a.statSync().modified),
      );
      for (final d in apSnaps.skip(_keepSnaps)) {
        d.deleteSync(recursive: true);
      }
      final used = <String>{};
      for (final d in [...snaps.take(_keepSnaps), ...apSnaps.take(_keepSnaps)]) {
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
    final p = await Process.start(
      '${py}python/bin/python3',
      ['-u', '${py}engine/local_engine.py'],
      environment: {
        'PYTHONDONTWRITEBYTECODE': '1',
        'PYTHONIOENCODING': 'utf-8',
      },
    );
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
      log('python dừng (mã $code)', const {}, null);
      _proc = null;
      _starting = null;
      _buf = '';
      for (final c in _wait.values) {
        c.completeError(StateError('Python tại chỗ dừng (mã $code)'));
      }
      _wait.clear();
      if (!ready.isCompleted)
        ready.completeError(StateError('Không khởi động được Python tại chỗ'));
    });
    await ready.future.timeout(const Duration(seconds: 60));
    _proc = p;
  }();

  /// Nhật ký bộ lọc (Application Support/KPI Dashboard/filter.log, giữ ~1 MB gần nhất):
  /// yêu cầu, nơi tính, và dòng đầu + dòng tổng bảng đầu tiên → dò khi số khác Streamlit.
  void log(
    String what,
    Map<String, dynamic> req,
    List<Map<String, dynamic>>? items,
  ) {
    if (!Platform.isMacOS) return;
    try {
      String brief = '';
      if (items != null) {
        final t = items.where((i) => i['t'] == 'tbl').firstOrNull;
        final b = (t?['b'] as List?) ?? const [];
        String row(Object? r) =>
            [for (final c in (r as List).take(6)) (c as Map)['x']].join(' | ');
        if (b.isNotEmpty) brief = ' ⇒ ${row(b.first)} … ${row(b.last)}';
      }
      final f = File('$_home/filter.log')..parent.createSync(recursive: true);
      if (f.existsSync() && f.lengthSync() > 1 << 20) f.writeAsStringSync('');
      f.writeAsStringSync(
        '${DateTime.now().toIso8601String().substring(0, 19)} [$what] ${jsonEncode(req)}$brief\n',
        mode: FileMode.append,
      );
    } catch (_) {}
  }

  Future<Map<String, dynamic>> _call(
    String? sc,
    Map<String, dynamic> msg, {
    String? root,
  }) async {
    root ??= await snapshot(sc!);
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
    final root = await snapshotFor(req);
    // Sale Sup 'Cả 2': tính thêm từng team → bảng tách theo team + dòng Total chung (team_merge.py)
    final parts = req['team'] == 'all'
        ? {
            'tan': await snapshotFor({...req, 'team': 'tan'}),
            'vy': await snapshotFor({...req, 'team': 'vy'}),
          }
        : null;
    final res = await _call(null, {'req': req, 'parts': ?parts}, root: root);
    return [
      for (final i in res['items'] as List) (i as Map).cast<String, dynamic>(),
    ];
  }

  /// Danh sách báo cáo / ngày / ĐDKD của tháng (như `kpi/<Thang>/index.json`).
  Future<Map<String, dynamic>> plan(String sc, String monthKey) async =>
      ((await _call(sc, {'op': 'plan', 'month_key': monthKey}))['plan'] as Map)
          .cast<String, dynamic>();

  /// Số liệu Turnover cả tháng (như `turnover/<Thang>.json`).
  Future<Map<String, dynamic>> turnover(String sc, String monthKey) async =>
      ((await _call(sc, {'op': 'turnover', 'month_key': monthKey}))['turnover']
              as Map)
          .cast<String, dynamic>();

  /// Như [turnover] nhưng cho Sale Sup khác team Tân (team 'vy'/'all' — dùng [snapshotFor]
  /// để lấy đúng data repo Vyntt commit 'dsc' thay vì chỉ data Tân).
  Future<Map<String, dynamic>> turnoverFor(Map<String, dynamic> req) async {
    final root = await snapshotFor(req);
    final res = await _call(null, {
      'op': 'turnover',
      'month_key': req['month_key'],
    }, root: root);
    return (res['turnover'] as Map).cast<String, dynamic>();
  }

  // ---------- Data mới trên GitHub chưa xuất xong JSON → Mac tự tính ----------

  /// Repo Vyntt có data mới hơn bản GitHub đã xuất ([remoteDsc]) → dùng commit này làm 'dsc'
  /// khi tính tại chỗ (null = dùng bản GitHub đã xuất). Không cần tải trước gì ở đây —
  /// [snapshotFor] tự tải khi có yêu cầu dùng tới commit này.
  String? liveVyDsc;
  String? _lastVyHead;
  bool _checkingVy = false;

  /// Kiểm tra repo Vyntt: có commit mới hơn bản GitHub đã xuất ([remoteDsc]) không.
  /// Trả về true nếu đổi trạng thái (có bản mới hơn, hoặc GitHub đã xuất kịp nên bỏ bản tự tính).
  Future<bool> checkLiveVy(String? remoteDsc) async {
    if (!available || _checkingVy) return false;
    _checkingVy = true;
    try {
      final res = await _client
          .get(
            Uri.parse('https://api.github.com/repos/$vyRepo/commits/main'),
            headers: _headers,
          )
          .timeout(const Duration(seconds: 20));
      if (res.statusCode != 200) {
        log('checkLiveVy http ${res.statusCode}', {
          'remoteDsc': remoteDsc,
        }, null);
        return false;
      }
      final head = (jsonDecode(res.body) as Map)['sha'] as String;
      if (head == remoteDsc) {
        final had = liveVyDsc != null;
        liveVyDsc = null;
        _lastVyHead = head;
        log('checkLiveVy đã khớp', {
          'remoteDsc': remoteDsc,
          'head': head,
        }, null);
        return had;
      }
      if (head == _lastVyHead) return false;
      liveVyDsc = head;
      _lastVyHead = head;
      log('checkLiveVy có bản mới', {
        'remoteDsc': remoteDsc,
        'head': head,
      }, null);
      return true;
    } catch (e) {
      log('checkLiveVy lỗi: $e', {'remoteDsc': remoteDsc}, null);
      return false;
    } finally {
      _checkingVy = false;
    }
  }

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
          .get(
            Uri.parse('https://api.github.com/repos/$ghRepo/commits/main'),
            headers: _headers,
          )
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
      if (head == _lastHead && (liveSc == null || liveMonth == monthKey))
        return false;
      if (remoteSc != null) {
        final cmp = await _client
            .get(
              Uri.parse(
                'https://api.github.com/repos/$ghRepo/compare/$remoteSc...$head',
              ),
              headers: _headers,
            )
            .timeout(const Duration(seconds: 20));
        if (cmp.statusCode != 200) return false;
        final files = [
          for (final f
              in ((jsonDecode(cmp.body) as Map)['files'] as List? ?? const []))
            '${(f as Map)['filename']}',
        ];
        if (!files.any((f) => f == 'App.py' || f.startsWith('data/'))) {
          _lastHead = head;
          return false; // chỉ đổi code app, data như cũ
        }
      }
      final plan = await this.plan(head, monthKey);
      liveSc = head;
      liveMonth = monthKey;
      livePlan = plan;
      liveAt = DateTime.tryParse(
        '${((j['commit'] as Map)['committer'] as Map)['date']}',
      );
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
