import 'package:flutter/material.dart';

import '../data/report_repository.dart';
import '../logic/pyfmt.dart';
import '../logic/turnover_logic.dart';
import 'app_scale.dart';
import 'kpi_table.dart';
import 'report_table.dart';
import 'theme.dart';

class TurnoverPage extends StatefulWidget {
  final ReportRepository repo;
  final Widget? leading; // nút mở menu báo cáo
  final String? dataKey; // đổi khi có data mới → tải lại, giữ NV đang lọc
  const TurnoverPage({super.key, required this.repo, this.leading, this.dataKey});

  @override
  State<TurnoverPage> createState() => _TurnoverPageState();
}

class _TurnoverPageState extends State<TurnoverPage> {
  Manifest? _manifest;
  TurnoverMonth? _month;
  String? _monthKey;
  String? _date;
  List<String> _filter = []; // giữ thứ tự chọn như multiselect của Streamlit
  bool _loading = true;
  bool _offline = false;
  String? _error;

  @override
  void initState() {
    super.initState();
    _load();
  }

  @override
  void didUpdateWidget(TurnoverPage old) {
    super.didUpdateWidget(old);
    if (old.dataKey != widget.dataKey && old.dataKey != null) _load(refresh: true);
  }

  Future<void> _load({bool refresh = false}) async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      if (refresh) widget.repo.clearMemory();
      final man = await widget.repo.manifest();
      final months = man.value.months;
      if (months.isEmpty) throw StateError('Chưa có dữ liệu tháng nào');
      final key = months.any((m) => m.key == _monthKey) ? _monthKey! : months.last.key;
      final tm = await widget.repo.turnover(key, refresh: true);
      final wasDefault = _month == null || _date == defaultReportDate(_month!, DateTime.now().toUtc());
      setState(() {
        _manifest = man.value;
        _monthKey = key;
        _month = tm.value;
        _offline = man.fromCache || tm.fromCache;
        if (wasDefault || _date == null || !tm.value.days.containsKey(_date)) {
          _date = defaultReportDate(tm.value, DateTime.now().toUtc());
        }
        _filter = _filter.where(tm.value.nv.contains).toList();
      });
    } catch (e) {
      setState(() => _error = '$e');
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  Future<void> _switchMonth(String key) async {
    if (key == _monthKey) return;
    setState(() => _loading = true);
    try {
      final tm = await widget.repo.turnover(key);
      setState(() {
        _monthKey = key;
        _month = tm.value;
        _date = defaultReportDate(tm.value, DateTime.now().toUtc());
        _filter = _filter.where(tm.value.nv.contains).toList();
      });
    } catch (e) {
      _snack('Không tải được tháng: $e');
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  void _snack(String m) => ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(m)));

  Future<void> _pickDate() async {
    final m = _month!;
    final cur = DateTime.parse(_date!);
    final picked = await showDatePicker(
      context: context,
      initialDate: cur,
      firstDate: DateTime(m.year, m.month, 1),
      lastDate: DateTime(m.year, m.month + 1, 0),
      helpText: 'Ngày báo cáo',
      locale: const Locale('vi'),
    );
    if (picked != null) setState(() => _date = isoDate(picked));
  }

  Future<void> _pickNv() async {
    final m = _month!;
    final sel = [..._filter];
    final result = await showModalBottomSheet<List<String>>(
      context: context,
      isScrollControlled: true,
      showDragHandle: true,
      builder: (ctx) => StatefulBuilder(
        builder: (ctx, setS) => SafeArea(
          child: ConstrainedBox(
            constraints: BoxConstraints(maxHeight: MediaQuery.of(ctx).size.height * 0.8),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Padding(
                  padding: const EdgeInsets.fromLTRB(20, 0, 12, 8),
                  child: Row(children: [
                    const Expanded(
                        child: Text('ĐDKD (chọn nhiều)',
                            style: TextStyle(fontSize: 16, fontWeight: FontWeight.w700))),
                    TextButton(onPressed: () => setS(sel.clear), child: const Text('Tất cả')),
                    FilledButton(
                        onPressed: () => Navigator.pop(ctx, sel), child: const Text('Xong')),
                  ]),
                ),
                const Divider(height: 1),
                Flexible(
                  child: ListView(
                    shrinkWrap: true,
                    children: [
                      for (final n in m.nv)
                        CheckboxListTile(
                          dense: true,
                          value: sel.contains(n),
                          title: Text(n),
                          onChanged: (v) => setS(() => v! ? sel.add(n) : sel.remove(n)),
                        ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
    if (result != null) setState(() => _filter = result);
  }

  String _ddmmyyyy(String iso) {
    final d = DateTime.parse(iso);
    return '${d.day.toString().padLeft(2, '0')}/${d.month.toString().padLeft(2, '0')}/${d.year}';
  }

  @override
  Widget build(BuildContext context) {
    final man = _manifest;
    // generated_at có múi +07:00; DateTime.parse trả về UTC → đổi lại giờ VN
    final upd = man?.generatedAt?.toUtc().add(const Duration(hours: 7));
    return Scaffold(
      appBar: AppBar(
        leading: widget.leading,
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('1. TURNOVER', style: TextStyle(fontWeight: FontWeight.w800, fontSize: 18)),
            if (upd != null)
              Text(
                'Cập nhật ${upd.day.toString().padLeft(2, '0')}/${upd.month.toString().padLeft(2, '0')} '
                '${upd.hour.toString().padLeft(2, '0')}:${upd.minute.toString().padLeft(2, '0')}'
                '${_offline ? ' · ngoại tuyến' : ''}',
                style: TextStyle(fontSize: 12, color: _offline ? Brand.accent : Colors.white70),
              ),
          ],
        ),
        actions: [
          const ScaleButton(),
          IconButton(
            tooltip: 'Tải lại',
            onPressed: _loading ? null : () => _load(refresh: true),
            icon: const Icon(Icons.refresh),
          ),
        ],
        bottom: _loading
            ? const PreferredSize(
                preferredSize: Size.fromHeight(3),
                child: LinearProgressIndicator(minHeight: 3, color: Brand.accent))
            : null,
      ),
      body: _body(),
    );
  }

  Widget _body() {
    if (_month == null) {
      if (_error != null) {
        return Center(
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: Column(mainAxisSize: MainAxisSize.min, children: [
              const Icon(Icons.cloud_off, size: 48, color: Brand.navy),
              const SizedBox(height: 12),
              const Text('Không tải được dữ liệu',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.w700)),
              const SizedBox(height: 6),
              Text(_error!, textAlign: TextAlign.center, style: const TextStyle(color: Brand.muted)),
              const SizedBox(height: 16),
              FilledButton(onPressed: _load, child: const Text('Thử lại')),
            ]),
          ),
        );
      }
      return const Center(child: CircularProgressIndicator());
    }

    final m = _month!;
    final TurnoverReport rep;
    try {
      rep = buildTurnover(m, _date!, _filter);
    } catch (e) {
      return Center(child: Text('$e'));
    }
    final wide = MediaQuery.of(context).size.width >= 720;

    return RefreshIndicator(
      onRefresh: () => _load(refresh: true),
      child: ListView(
        padding: EdgeInsets.symmetric(horizontal: wide ? 24 : 12, vertical: 12),
        children: [
          _filters(m),
          const SizedBox(height: 10),
          _timegone(rep.timegone),
          const SizedBox(height: 14),
          Text(
            '${m.title} - THÁNG ${m.month.toString().padLeft(2, '0')}/${m.year}',
            textAlign: TextAlign.center,
            style: const TextStyle(color: Brand.blue, fontWeight: FontWeight.w800, fontSize: 16),
          ),
          const SizedBox(height: 4),
          Text('⚡ Ngày: ${_ddmmyyyy(_date!)} | Lọc: ${rep.filterLabel}',
              textAlign: TextAlign.center, style: const TextStyle(color: Brand.muted, fontSize: 12.5)),
          if (m.salaryLabel.isNotEmpty) ...[
            const SizedBox(height: 4),
            Text('💰 Mức lương KPI: ${m.salaryLabel}',
                textAlign: TextAlign.center,
                style: const TextStyle(color: Brand.salary, fontSize: 12, fontWeight: FontWeight.w700)),
          ],
          const SizedBox(height: 10),
          _cards(rep, wide),
          const SizedBox(height: 12),
          ReportTable(data: turnoverTableData(rep), title: m.title),
          const SizedBox(height: 12),
          _notes(m, rep),
          const SizedBox(height: 24),
        ],
      ),
    );
  }

  Widget _filters(TurnoverMonth m) {
    final months = _manifest?.months ?? [];
    final nvText = _filter.isEmpty
        ? allNvLabel
        : (_filter.length == 1 ? _filter.first : '${_filter.length} ĐDKD đã chọn');
    return Wrap(
      spacing: 8,
      runSpacing: 8,
      children: [
        if (months.length > 1)
          SegmentedButton<String>(
            showSelectedIcon: false,
            segments: [for (final mi in months) ButtonSegment(value: mi.key, label: Text(mi.label))],
            selected: {_monthKey!},
            onSelectionChanged: (s) => _switchMonth(s.first),
          ),
        OutlinedButton.icon(
          onPressed: _pickDate,
          icon: const Icon(Icons.calendar_today, size: 18),
          label: Text(_ddmmyyyy(_date!)),
        ),
        OutlinedButton.icon(
          onPressed: _pickNv,
          icon: const Icon(Icons.people_alt_outlined, size: 18),
          label: Text(nvText),
        ),
        if (_filter.isNotEmpty)
          IconButton(
            tooltip: 'Bỏ lọc',
            onPressed: () => setState(() => _filter = []),
            icon: const Icon(Icons.clear),
          ),
      ],
    );
  }

  Widget _timegone(Timegone t) {
    Widget item(String k, String v) => Column(children: [
          Text(v, style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 16, color: Brand.navy)),
          Text(k, style: const TextStyle(fontSize: 11, color: Brand.muted)),
        ]);
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 8),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: Brand.cardBorder),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          item('Tổng làm việc', '${t.total}'),
          item('Đã trôi qua', '${t.elapsed}'),
          item('Còn lại', '${t.remain}'),
          item('% Timegone', '${pyStr(t.pct)}%'),
        ],
      ),
    );
  }

  Widget _cards(TurnoverReport rep, bool wide) {
    final cards = [
      ('🎯 Chỉ Tiêu DS', vnNumber(rep.teamTarget)),
      ('📈 Doanh Số MTD', vnNumber(rep.total.mtd)),
      ('📊 % MTD', rep.total.pctLabel),
      ('🆕 Thực Hiện Ngày', vnNumber(rep.total.today)),
    ];
    return LayoutBuilder(builder: (ctx, c) {
      final perRow = wide ? 4 : 2;
      final w = (c.maxWidth - 8 * (perRow - 1)) / perRow;
      return Wrap(
        spacing: 8,
        runSpacing: 8,
        children: [
          for (final (label, value) in cards)
            Container(
              width: w,
              padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 6),
              decoration: BoxDecoration(
                color: Brand.cardBg,
                borderRadius: BorderRadius.circular(6),
                border: Border.all(color: Brand.cardBorder),
              ),
              child: Column(children: [
                Text(label,
                    textAlign: TextAlign.center,
                    style: const TextStyle(color: Brand.cardText, fontWeight: FontWeight.w800, fontSize: 13)),
                const SizedBox(height: 4),
                FittedBox(
                  fit: BoxFit.scaleDown,
                  child: Text(value,
                      style: const TextStyle(
                          color: Brand.cardText,
                          fontWeight: FontWeight.w800,
                          fontSize: 22,
                          fontFeatures: [FontFeature.tabularFigures()])),
                ),
              ]),
            ),
        ],
      );
    });
  }

  Widget _notes(TurnoverMonth m, TurnoverReport rep) {
    Widget li(String b, String t) => Padding(
          padding: const EdgeInsets.only(bottom: 6),
          child: Text.rich(TextSpan(children: [
            const TextSpan(text: '•  '),
            TextSpan(text: '$b ', style: const TextStyle(fontWeight: FontWeight.w700)),
            TextSpan(text: t),
          ])),
        );
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: const Color(0xFFF0F7FF),
        borderRadius: BorderRadius.circular(8),
        border: const Border(left: BorderSide(color: Brand.blue, width: 4)),
      ),
      child: DefaultTextStyle.merge(
        style: const TextStyle(fontSize: 13, height: 1.45, color: Color(0xFF1A202C)),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text('NHẬN XÉT & ĐÁNH GIÁ ${m.title}:',
              style: const TextStyle(fontWeight: FontWeight.w800, color: Brand.blue, fontSize: 13.5)),
          const SizedBox(height: 8),
          li('Kết Quả Thực Hiện:', rep.resultText),
          li('Top 3 ĐDKD Dẫn Đầu:', '${rep.top3Text}.'),
          li('Bottom 3 ĐDKD Cần Cải Thiện:', '${rep.bottom3Text}.'),
          li('Đề Xuất Hành Động Cho 3 Bạn Bottom:',
              'Tập trung rà soát doanh số khách hàng trọng điểm, thúc đẩy đơn hàng lớn và SS hỗ trợ trực tiếp tại tuyến.'),
        ]),
      ),
    );
  }
}
