import 'package:flutter/material.dart';

import '../data/report_repository.dart';
import 'report_page.dart';
import 'theme.dart';
import 'turnover_page.dart';

/// Khung app: danh sách 18 báo cáo tab KPI (menu trượt trên điện thoại,
/// thanh bên cố định trên Mac / màn hình rộng).
class HomeShell extends StatefulWidget {
  final ReportRepository repo;
  const HomeShell({super.key, required this.repo});

  @override
  State<HomeShell> createState() => _HomeShellState();
}

class _HomeShellState extends State<HomeShell> {
  final _scaffold = GlobalKey<ScaffoldState>();
  Manifest? _manifest;
  KpiIndex? _idx;
  String? _kpiMonth;
  String _code = 'TURNOVER';
  String? _error;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() => _error = null);
    try {
      final man = await widget.repo.manifest();
      final months = man.value.kpiMonths;
      final mk = months.any((m) => m.key == _kpiMonth) ? _kpiMonth : (months.isEmpty ? null : months.last.key);
      KpiIndex? idx;
      if (mk != null) idx = (await widget.repo.kpiIndex(mk)).value;
      setState(() {
        _manifest = man.value;
        _kpiMonth = mk;
        _idx = idx;
      });
    } catch (e) {
      setState(() => _error = '$e');
    }
  }

  void _select(String code) {
    setState(() => _code = code);
    if (_scaffold.currentState?.isDrawerOpen ?? false) Navigator.of(context).pop();
  }

  Widget _menu({required bool permanent}) {
    final reports = _idx?.reports ?? [];
    return Container(
      color: Colors.white,
      child: SafeArea(
        right: false,
        child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
          Container(
            color: Brand.navy,
            padding: const EdgeInsets.fromLTRB(16, 18, 16, 14),
            child: const Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text('KPI Dashboard', style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.w800)),
              SizedBox(height: 2),
              Text('Team SS Trương Thanh Tân', style: TextStyle(color: Colors.white70, fontSize: 12)),
            ]),
          ),
          Expanded(
            child: ListView(padding: const EdgeInsets.symmetric(vertical: 6), children: [
              if (reports.isEmpty) _tile('TURNOVER', '1. TURNOVER - Tổng doanh số bán ra'),
              for (final r in reports) _tile(r.code, r.name),
            ]),
          ),
        ]),
      ),
    );
  }

  Widget _tile(String code, String name) {
    final sel = code == _code;
    return ListTile(
      dense: true,
      selected: sel,
      selectedTileColor: Brand.zebra,
      selectedColor: Brand.navy,
      title: Text(name,
          maxLines: 2,
          overflow: TextOverflow.ellipsis,
          style: TextStyle(fontSize: 13, fontWeight: sel ? FontWeight.w800 : FontWeight.w500)),
      onTap: () => _select(code),
    );
  }

  @override
  Widget build(BuildContext context) {
    final wide = MediaQuery.of(context).size.width >= 1000;
    final menuButton = wide
        ? null
        : IconButton(icon: const Icon(Icons.menu), onPressed: () => _scaffold.currentState?.openDrawer());

    Widget page;
    if (_code == 'TURNOVER' || _manifest == null || _kpiMonth == null) {
      page = TurnoverPage(repo: widget.repo, leading: menuButton);
    } else {
      page = KpiReportPage(
        key: ValueKey('kpi-$_kpiMonth'),
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
      return Row(children: [
        SizedBox(width: 280, child: Material(elevation: 1, child: _menu(permanent: true))),
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
