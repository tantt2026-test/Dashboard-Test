import 'dart:async';
import 'dart:convert';
import 'dart:io';

import 'package:crypto/crypto.dart';
import 'package:flutter/material.dart';
import 'package:local_auth/local_auth.dart';


import '../data/local_engine.dart';
import '../data/report_repository.dart';
import 'report_page.dart';
import 'theme.dart';
import '../data/app_dirs.dart';
import 'turnover_page.dart';

/// Khung app: danh sách 18 báo cáo tab KPI (menu trượt trên điện thoại,
/// thanh bên cố định trên Mac / màn hình rộng).
/// Hiện ở cuối menu để biết đang dùng bản nào (tăng mỗi lần build bản mới).
const appVersion = '1.7.13';

class HomeShell extends StatefulWidget {
  final ReportRepository repo;
  const HomeShell({super.key, required this.repo});

  @override
  State<HomeShell> createState() => _HomeShellState();
}

class _HomeShellState extends State<HomeShell> with WidgetsBindingObserver {
  final int _refreshTick = 0; // giữ trong khoá trang (tải lại nay giữ nguyên trang + bộ lọc)
  DateTime _lastLoad = DateTime.now();

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    // Mở lại app / quay lại cửa sổ → kiểm tra data mới ngay (giữ nguyên ô đang lọc)
    if (state == AppLifecycleState.resumed && DateTime.now().difference(_lastLoad).inSeconds >= 20) {
      _checkNew();
    }
  }

  Timer? _poll;
  bool _polling = false;

  /// Mỗi phút: GitHub đã xuất data mới chưa (mọi máy); app Mac còn xem main có data mới chưa
  /// xuất xong → tự tính bằng App.py. Có bản mới → các trang tự tải lại, giữ bộ lọc.
  Future<void> _checkNew() async {
    if (_polling || _manifest == null) return;
    _polling = true;
    _lastLoad = DateTime.now();
    try {
      var man = (await widget.repo.manifest()).value;
      final mk = man.kpiMonths.isEmpty ? null : man.kpiMonths.last.key;
      if (ReportRepository.team == 'tan' && mk != null &&
          await LocalEngine.instance.checkLive(widget.repo.remoteSc, mk)) {
        man = (await widget.repo.manifest()).value;
      }
      final old = _manifest;
      if (old == null || (man.sourceCommit == old.sourceCommit && man.generatedAt == old.generatedAt)) return;
      // không lùi về bản cũ hơn bản đang xem
      if (man.generatedAt != null && old.generatedAt != null && man.generatedAt!.isBefore(old.generatedAt!)) return;
      final months = man.kpiMonths;
      final k = months.any((m) => m.key == _kpiMonth) ? _kpiMonth : (months.isEmpty ? null : months.last.key);
      final idx = k == null ? null : (await widget.repo.kpiIndex(k)).value;
      if (man.sourceCommit != null) LocalEngine.instance.warmUp(man.sourceCommit!);
      if (!mounted) return;
      setState(() {
        _manifest = man;
        _kpiMonth = k;
        _idx = idx;
      });
    } catch (_) {
      // mất mạng → thử lại phút sau
    } finally {
      _polling = false;
    }
  }

  @override
  void dispose() {
    _poll?.cancel();
    WidgetsBinding.instance.removeObserver(this);
    super.dispose();
  }

  final _scaffold = GlobalKey<ScaffoldState>();
  Manifest? _manifest;
  KpiIndex? _idx;
  String? _kpiMonth;
  String _code = 'TURNOVER';
  String? _error;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    widget.repo.loadTeam().then((_) => _load()).then((_) => _checkNew());
    _poll = Timer.periodic(const Duration(minutes: 1), (_) => _checkNew());
  }

  Future<void> _load() async {
    setState(() => _error = null);
    try {
      final man = await widget.repo.manifest();
      final months = man.value.kpiMonths;
      final mk = months.any((m) => m.key == _kpiMonth) ? _kpiMonth : (months.isEmpty ? null : months.last.key);
      KpiIndex? idx;
      if (mk != null) idx = (await widget.repo.kpiIndex(mk)).value;
      final sc = man.value.sourceCommit;
      if (sc != null) LocalEngine.instance.warmUp(sc);
      // app Mac: tải sẵn data của Sale Sup đang xem (Vy / Cả 2) để lọc tại máy đỡ chờ
      if (sc != null && man.value.team != 'tan' && LocalEngine.instance.available) {
        LocalEngine.instance
            .snapshotFor({'sc': sc, 'team': man.value.team, 'dsc': man.value.dataSc ?? 'HEAD'})
            .catchError((Object _) => '');
      }
      setState(() {
        _manifest = man.value;
        _kpiMonth = mk;
        _idx = idx;
      });
    } catch (e) {
      setState(() => _error = '$e');
    }
  }

  /// Đổi Sale Sup: tải manifest / báo cáo của bộ data đó, giữ báo cáo đang xem.
  Future<void> _setTeam(String id) async {
    if (id == ReportRepository.team) return;
    await widget.repo.setTeam(id);
    if (!mounted) return;
    setState(() {
      _manifest = null;
      _idx = null;
    });
    await _load();
  }

  void _select(String code) {
    setState(() => _code = code);
    if (_scaffold.currentState?.isDrawerOpen ?? false) Navigator.of(context).pop();
  }

  // Tab 🔒 TRACKING SALE SUP: đăng nhập 1 lần mỗi lần mở app. Chỉ lưu mã băm sha256('ID:mật khẩu').
  static const _supHash = 'fb9cddadb09f9202efde9aa4efe5862694547ff21d31007167bee2d4891c8eb4';
  bool _supOk = false;

  // Vân tay (Android) / Touch ID (Mac): bật sau 1 lần đăng nhập đúng bằng mật khẩu trên máy này
  final _bio = LocalAuthentication();

  File get _bioFlag {
    final base = appDataDir();
    return File('$base/sup_bio_on');
  }

  Future<bool> _bioAvailable() async {
    try {
      return await _bio.isDeviceSupported() && (await _bio.getAvailableBiometrics()).isNotEmpty;
    } catch (_) {
      return false;
    }
  }

  Future<bool> _bioAuth() async {
    try {
      return await _bio.authenticate(
          localizedReason: 'Xác thực để xem Tracking Sale Sup', biometricOnly: true);
    } catch (_) {
      return false;
    }
  }

  Future<void> _openSup(String code) async {
    if (_supOk) return _select(code);
    final bioOk = await _bioAvailable();
    final bioOn = bioOk && _bioFlag.existsSync();
    // đã bật vân tay → quét luôn, không cần mở ô mật khẩu
    if (bioOn && await _bioAuth()) {
      if (!mounted) return;
      setState(() => _supOk = true);
      return _select(code);
    }
    if (!mounted) return;
    final user = TextEditingController(), pass = TextEditingController();
    String? err;
    var show = false;
    final ok = await showDialog<bool>(
      context: context,
      builder: (ctx) => StatefulBuilder(builder: (ctx, setD) {
        void submit() {
          final h = sha256.convert(utf8.encode('${user.text.trim()}:${pass.text}')).toString();
          if (h == _supHash) {
            Navigator.pop(ctx, true);
          } else {
            setD(() => err = 'Sai ID hoặc mật khẩu');
          }
        }

        return AlertDialog(
          title: const Text('🔒 Tracking Sale Sup — Đăng nhập'),
          content: Column(mainAxisSize: MainAxisSize.min, children: [
            TextField(controller: user, autofocus: !bioOn, decoration: const InputDecoration(labelText: 'ID đăng nhập')),
            TextField(
                controller: pass,
                obscureText: !show,
                decoration: InputDecoration(
                  labelText: 'Mật khẩu',
                  errorText: err,
                  suffixIcon: IconButton(
                    tooltip: show ? 'Ẩn mật khẩu' : 'Hiện mật khẩu',
                    icon: Icon(show ? Icons.visibility_off : Icons.visibility),
                    onPressed: () => setD(() => show = !show),
                  ),
                ),
                onSubmitted: (_) => submit()),
            if (bioOn) ...[
              const SizedBox(height: 14),
              OutlinedButton.icon(
                icon: const Icon(Icons.fingerprint),
                label: Text('Đăng nhập bằng ${bioName()}'),
                onPressed: () async {
                  if (await _bioAuth() && ctx.mounted) Navigator.pop(ctx, true);
                },
              ),
            ],
          ]),
          actions: [
            TextButton(onPressed: () => Navigator.pop(ctx, false), child: const Text('Huỷ')),
            FilledButton(onPressed: submit, child: const Text('Đăng nhập')),
          ],
        );
      }),
    );
    if (ok != true || !mounted) return;
    setState(() => _supOk = true);
    _select(code);
    // lần đầu đăng nhập bằng mật khẩu → hỏi bật vân tay cho lần sau
    if (bioOk && !_bioFlag.existsSync()) {
      final yes = await showDialog<bool>(
        context: context,
        builder: (ctx) => AlertDialog(
          title: Text('Dùng ${bioName()}?'),
          content: Text('Lần sau mở Tracking Sale Sup chỉ cần xác thực bằng ${bioName()}.'),
          actions: [
            TextButton(onPressed: () => Navigator.pop(ctx, false), child: const Text('Để sau')),
            FilledButton(onPressed: () => Navigator.pop(ctx, true), child: const Text('Bật')),
          ],
        ),
      );
      if (yes == true && await _bioAuth()) {
        try {
          _bioFlag
            ..parent.createSync(recursive: true)
            ..writeAsStringSync('1');
        } catch (_) {}
      }
    }
  }

  Widget _menu({required bool permanent}) {
    final reports = _idx?.reports ?? [];
    return Container(
      color: panelBg(context),
      child: SafeArea(
        right: false,
        child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
          // cao đúng bằng thanh tiêu đề trang (AppBar) bên phải → 2 dải xanh thẳng hàng
          Container(
            color: Brand.navy,
            height: kToolbarHeight,
            alignment: Alignment.centerLeft,
            padding: const EdgeInsets.symmetric(horizontal: 16),
            child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('KPI Dashboard',
                      style: TextStyle(color: Colors.white, fontSize: 17, fontWeight: FontWeight.w800, height: 1.15)),
                  const SizedBox(height: 2),
                  // Bộ lọc Sale Sup: Tân / Vy / Cả 2 (mỗi lựa chọn là 1 bộ data GitHub xuất riêng)
                  PopupMenuButton<String>(
                    tooltip: 'Chọn Sale Sup',
                    initialValue: ReportRepository.team,
                    onSelected: _setTeam,
                    itemBuilder: (_) => [
                      for (final t in saleSups)
                        PopupMenuItem(
                            value: t.id,
                            child: Text(t.id == 'all' ? '👥 ${t.name}' : 'SS ${t.name}',
                                style: TextStyle(fontWeight: t.id == ReportRepository.team ? FontWeight.w800 : FontWeight.w500))),
                    ],
                    child: Row(mainAxisSize: MainAxisSize.min, children: [
                      Flexible(
                        child: Text(
                            ReportRepository.team == 'all'
                                ? 'Sale Sup: Cả 2 Sup'
                                : 'Sale Sup: SS ${saleSupOf(ReportRepository.team).name}',
                            overflow: TextOverflow.ellipsis,
                            style: const TextStyle(color: Colors.white, fontSize: 11.5, height: 1.15, fontWeight: FontWeight.w600)),
                      ),
                      const Icon(Icons.arrow_drop_down, color: Colors.white70, size: 18),
                    ]),
                  ),
                ]),
          ),
          Expanded(
            child: ListView(padding: const EdgeInsets.fromLTRB(10, 6, 10, 10), children: [
              if (reports.isEmpty) _tile('TURNOVER', '1. TURNOVER - Tổng doanh số bán ra'),
              _section('📊 BÁO CÁO KPI'),
              for (final r in reports.where((r) => r.group == 'kpi')) _tile(r.code, r.name),
              if (reports.any((r) => r.group == 'tab')) ...[
                // đường kẻ cam ngăn phần báo cáo KPI với các tab khác
                Container(
                  height: 2.5,
                  margin: const EdgeInsets.fromLTRB(4, 14, 4, 2),
                  decoration: BoxDecoration(color: const Color(0xFFED8936), borderRadius: BorderRadius.circular(2)),
                ),
                _section('CÁC TAB KHÁC'),
              ],
              for (final r in reports.where((r) => r.group == 'tab')) _tile(r.code, r.name),
              if (reports.any((r) => r.group == 'sup')) ...[
                Container(
                  height: 2.5,
                  margin: const EdgeInsets.fromLTRB(4, 14, 4, 2),
                  decoration: BoxDecoration(color: const Color(0xFF805AD5), borderRadius: BorderRadius.circular(2)),
                ),
                Row(children: [
                  Expanded(child: _section('🔒 TRACKING SALE SUP')),
                  if (_supOk)
                    TextButton(
                      onPressed: () => setState(() {
                        _supOk = false;
                        if (_code.startsWith('SUP_')) _code = 'TURNOVER';
                      }),
                      child: const Text('Đăng xuất', style: TextStyle(fontSize: 11)),
                    ),
                ]),
                // chưa đăng nhập: ẩn danh sách báo cáo, chỉ có nút đăng nhập
                if (_supOk)
                  for (final r in reports.where((r) => r.group == 'sup'))
                    _MenuTile(name: r.name, selected: r.code == _code, onTap: () => _openSup(r.code))
                else
                  _MenuTile(
                      name: '🔒 Đăng nhập để xem',
                      selected: false,
                      onTap: () => _openSup(reports.firstWhere((r) => r.group == 'sup').code)),
              ],
            ]),
          ),
          const Divider(height: 1),
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 8, 16, 10),
            child: Text(
              'Phiên bản $appVersion'
              '${_manifest?.generatedAt != null ? ' · dữ liệu ${_fmtTime(_manifest!.generatedAt!)}' : ''}'
              '${LocalEngine.instance.liveSc != null && LocalEngine.instance.liveSc == _manifest?.sourceCommit ? ' (máy tự tính)' : ''}',
              style: TextStyle(fontSize: 11, color: mutedText(context)),
            ),
          ),
        ]),
      ),
    );
  }

  static String _fmtTime(DateTime t) {
    final v = t.toUtc().add(const Duration(hours: 7));
    String two(int n) => n.toString().padLeft(2, '0');
    return '${two(v.day)}/${two(v.month)} ${two(v.hour)}:${two(v.minute)}';
  }

  Widget _section(String t) => Builder(
        builder: (context) => Padding(
          padding: const EdgeInsets.fromLTRB(6, 12, 6, 6),
          child: Text(t,
              style: TextStyle(
                  fontSize: 11.5,
                  fontWeight: FontWeight.w800,
                  color: isDark(context) ? const Color(0xFF63B3ED) : Brand.blue)),
        ),
      );

  Widget _tile(String code, String name) =>
      _MenuTile(name: name, selected: code == _code, onTap: () => _select(code));

  // Khoá toàn cục cho trang báo cáo: kéo cửa sổ qua mốc 1000px (menu cố định ↔ menu kéo ra) chỉ
  // chuyển trang sang khung mới, không tạo lại → giữ nguyên các ô đang lọc.
  String? _pageId;
  GlobalKey _pageKey = GlobalKey();
  Key _keyFor(String id) {
    if (id != _pageId) {
      _pageId = id;
      _pageKey = GlobalKey();
    }
    return _pageKey;
  }

  @override
  Widget build(BuildContext context) {
    final wide = MediaQuery.of(context).size.width >= 1000;
    final menuButton = wide
        ? null
        : IconButton(icon: const Icon(Icons.menu), onPressed: () => _scaffold.currentState?.openDrawer());

    Widget page;
    // TURNOVER: dùng bản App.py xuất (giống hệt Streamlit: bảng DS theo nhóm VIP, chi tiết ĐH/SP…) khi tháng có;
    // màn Turnover tự tính của app chỉ còn là dự phòng (chưa có data KPI / mất mạng lúc đầu)
    final kpiTurnover = _idx?.reports.any((r) => r.code == 'TURNOVER') ?? false;
    if ((_code == 'TURNOVER' && !kpiTurnover) || _manifest == null || _kpiMonth == null) {
      page = TurnoverPage(
          key: _keyFor('to-$_refreshTick-${ReportRepository.team}'),
          repo: widget.repo,
          leading: menuButton,
          dataKey: '${_manifest?.sourceCommit}|${_manifest?.generatedAt}');
    } else {
      page = KpiReportPage(
        key: _keyFor('kpi-$_kpiMonth-$_refreshTick-${ReportRepository.team}'),
        repo: widget.repo,
        manifest: _manifest!,
        code: _code,
        monthKey: _kpiMonth!,
        leading: menuButton,
        onMonthChanged: (mk) async {
          final idx = (await widget.repo.kpiIndex(mk)).value;
          setState(() {
            _kpiMonth = mk;
            _idx = idx;
          });
        },
      );
    }
    if (_error != null && _manifest == null && _code != 'TURNOVER') {
      page = Center(child: FilledButton(onPressed: _load, child: const Text('Thử lại')));
    }

    if (wide) {
      // Viền ngăn cách khung menu và khung báo cáo
      return Row(children: [
        SizedBox(width: 280, child: Material(elevation: 2, child: _menu(permanent: true))),
        Container(width: 1.5, color: Brand.border.withValues(alpha: 0.55)),
        Expanded(child: page),
      ]);
    }
    return Scaffold(
      key: _scaffold,
      drawer: Drawer(width: 300, child: _menu(permanent: false)),
      body: page,
    );
  }
}


/// Mục KPI ở menu: thẻ trắng viền xanh; đang chọn = nền xanh chữ trắng;
/// rê chuột → nảy lên (nhấc + phóng nhẹ + đổ bóng).
class _MenuTile extends StatefulWidget {
  final String name;
  final bool selected;
  final VoidCallback onTap;
  const _MenuTile({required this.name, required this.selected, required this.onTap});

  @override
  State<_MenuTile> createState() => _MenuTileState();
}

class _MenuTileState extends State<_MenuTile> {
  bool _hover = false;

  @override
  Widget build(BuildContext context) {
    final sel = widget.selected;
    final up = _hover && !sel;
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 3),
      child: MouseRegion(
        cursor: SystemMouseCursors.click,
        onEnter: (_) => setState(() => _hover = true),
        onExit: (_) => setState(() => _hover = false),
        child: GestureDetector(
          onTap: widget.onTap,
          child: AnimatedScale(
            scale: _hover ? 1.03 : 1,
            duration: const Duration(milliseconds: 220),
            curve: Curves.easeOutBack,
            child: AnimatedContainer(
              duration: const Duration(milliseconds: 220),
              curve: Curves.easeOutBack,
              transform: Matrix4.translationValues(0, _hover ? -3 : 0, 0),
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 9),
              decoration: BoxDecoration(
                gradient: sel
                    ? const LinearGradient(colors: [Brand.navy, Brand.blue])
                    : null,
                color: sel ? null : tileBg(context, hover: up),
                borderRadius: BorderRadius.circular(10),
                border: Border.all(color: sel ? Brand.blue : tileBorder(context, hover: up), width: 1.2),
                boxShadow: [
                  BoxShadow(
                    color: Brand.blue.withValues(alpha: _hover ? 0.22 : (sel ? 0.18 : 0.06)),
                    blurRadius: _hover ? 12 : 4,
                    offset: Offset(0, _hover ? 5 : 2),
                  ),
                ],
              ),
              child: Text(
                widget.name,
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
                style: TextStyle(
                  fontSize: 13,
                  height: 1.25,
                  fontWeight: sel ? FontWeight.w800 : FontWeight.w600,
                  color: sel ? Colors.white : tileText(context),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
