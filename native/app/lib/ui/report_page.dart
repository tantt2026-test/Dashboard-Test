import 'dart:async';

import 'package:flutter/material.dart';

import '../data/report_repository.dart';
import '../logic/turnover_logic.dart' show allNvLabel, isoDate;
import 'app_scale.dart';
import 'report_table.dart';
import 'report_view.dart';
import 'table_model.dart';
import 'theme.dart';

/// Màn hình chung cho 17 báo cáo tab KPI: nội dung do App.py xuất sẵn.
/// Bộ lọc như Streamlit: Tháng, Ngày, ĐDKD (chọn nhiều), Thứ VT, tìm Mã KH / Tên KH;
/// mỗi bảng có thêm nút lọc theo cột + toàn màn hình.
class KpiReportPage extends StatefulWidget {
  final ReportRepository repo;
  final Manifest manifest;
  final String code;
  final String monthKey;
  final ValueChanged<String> onMonthChanged;
  final Widget? leading;

  const KpiReportPage({
    super.key,
    required this.repo,
    required this.manifest,
    required this.code,
    required this.monthKey,
    required this.onMonthChanged,
    this.leading,
  });

  @override
  State<KpiReportPage> createState() => _KpiReportPageState();
}

const _thuOptions = ['2', '3', '4', '5', '6', '7', '25', '36', '47']; // như Streamlit

class _KpiReportPageState extends State<KpiReportPage> {
  KpiIndex? _idx;
  ReportDoc? _doc;
  String? _date;
  List<String> _nvs = []; // giữ thứ tự chọn
  Set<String> _thu = {};
  String _query = '';
  final _queryCtl = TextEditingController();
  Timer? _debounce;
  bool _loading = true;
  bool _offline = false;
  String? _error;

  /// 1 ĐDKD → bản xuất riêng (số chính xác); 0 hoặc ≥2 → bản Tất cả + lọc dòng.
  String? get _exactNv => _nvs.length == 1 ? _nvs.first : null;

  @override
  void initState() {
    super.initState();
    _loadIndex();
  }

  @override
  void dispose() {
    _debounce?.cancel();
    _queryCtl.dispose();
    super.dispose();
  }

  @override
  void didUpdateWidget(KpiReportPage old) {
    super.didUpdateWidget(old);
    if (old.monthKey != widget.monthKey) {
      _date = null;
      _loadIndex();
    } else if (old.code != widget.code) {
      _loadDoc();
    }
  }

  Future<void> _loadIndex() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final r = await widget.repo.kpiIndex(widget.monthKey);
      _idx = r.value;
      _offline = r.fromCache;
      if (_date == null || !_idx!.dates.contains(_date)) _date = _idx!.defaultDate;
      _nvs = _nvs.where(_idx!.nv.contains).toList();
      await _loadDoc();
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _error = '$e';
        _loading = false;
      });
    }
  }

  Future<void> _loadDoc() async {
    final idx = _idx;
    if (idx == null) return;
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final nv = _exactNv;
      final date = nv != null ? idx.nvDates.first : _date!;
      final r = await widget.repo.kpiDoc(idx, widget.code, date, nv);
      if (!mounted) return;
      setState(() {
        _doc = r.value;
        _offline = _offline || r.fromCache;
        _loading = false;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _error = 'Không tải được báo cáo: $e';
        _loading = false;
      });
    }
  }

  String _ddmm(String iso) {
    final d = DateTime.parse(iso);
    return '${d.day.toString().padLeft(2, '0')}/${d.month.toString().padLeft(2, '0')}/${d.year}';
  }

  Future<void> _pickDate() async {
    final idx = _idx!;
    if (_exactNv != null) {
      final ok = await showDialog<bool>(
        context: context,
        builder: (ctx) => AlertDialog(
          title: const Text('Đổi ngày'),
          content: Text('Số liệu riêng của 1 ĐDKD hiện chỉ có cho ngày ${_ddmm(idx.nvDates.first)}.\n'
              'Bỏ lọc ĐDKD để xem ngày khác?'),
          actions: [
            TextButton(onPressed: () => Navigator.pop(ctx, false), child: const Text('Huỷ')),
            FilledButton(onPressed: () => Navigator.pop(ctx, true), child: const Text('Bỏ lọc')),
          ],
        ),
      );
      if (ok != true || !mounted) return;
      _nvs = [];
    }
    final dates = idx.dates.map(DateTime.parse).toList();
    final picked = await showDatePicker(
      context: context,
      initialDate: DateTime.parse(_date!),
      firstDate: dates.first,
      lastDate: dates.last,
      selectableDayPredicate: (d) => idx.dates.contains(isoDate(d)),
      helpText: 'Ngày báo cáo',
    );
    if (picked != null) _date = isoDate(picked);
    _loadDoc();
  }

  Future<List<String>?> _multiPick(String title, List<String> options, List<String> current, {String? note}) {
    final sel = [...current];
    return showModalBottomSheet<List<String>>(
      context: context,
      isScrollControlled: true,
      showDragHandle: true,
      builder: (ctx) => StatefulBuilder(
        builder: (ctx, setS) => SafeArea(
          child: ConstrainedBox(
            constraints: BoxConstraints(maxHeight: MediaQuery.of(ctx).size.height * 0.8),
            child: Column(mainAxisSize: MainAxisSize.min, children: [
              Padding(
                padding: const EdgeInsets.fromLTRB(20, 0, 12, 4),
                child: Row(children: [
                  Expanded(child: Text(title, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w700))),
                  TextButton(onPressed: () => setS(sel.clear), child: const Text('Tất cả')),
                  FilledButton(onPressed: () => Navigator.pop(ctx, sel), child: const Text('Xong')),
                ]),
              ),
              if (note != null)
                Padding(
                  padding: const EdgeInsets.fromLTRB(20, 0, 20, 8),
                  child: Text(note, style: const TextStyle(fontSize: 12, color: Brand.muted)),
                ),
              const Divider(height: 1),
              Flexible(
                child: ListView(shrinkWrap: true, children: [
                  for (final o in options)
                    CheckboxListTile(
                      dense: true,
                      value: sel.contains(o),
                      title: Text(o),
                      onChanged: (v) => setS(() => v! ? sel.add(o) : sel.remove(o)),
                    ),
                ]),
              ),
            ]),
          ),
        ),
      ),
    );
  }

  Future<void> _pickNv() async {
    final idx = _idx!;
    final r = await _multiPick('ĐDKD (chọn nhiều)', idx.nv, _nvs,
        note: 'Chọn 1 người: số liệu riêng ngày ${_ddmm(idx.nvDates.first)}. '
            'Chọn nhiều: lọc dòng theo người trong mọi bảng.');
    if (r == null) return;
    final wasExact = _exactNv;
    setState(() => _nvs = r);
    if (wasExact != _exactNv) _loadDoc();
  }

  Future<void> _pickThu() async {
    final r = await _multiPick('Thứ VT', _thuOptions, _thu.toList());
    if (r != null) setState(() => _thu = r.toSet());
  }

  @override
  Widget build(BuildContext context) {
    final name = _idx?.reports.where((r) => r.code == widget.code).map((r) => r.name).firstOrNull ?? widget.code;
    final upd = widget.manifest.generatedAt?.toUtc().add(const Duration(hours: 7));
    final wide = MediaQuery.of(context).size.width >= 720;
    final page = PageFilter(nv: _nvs.length >= 2 ? _nvs.toSet() : const {}, thu: _thu, query: _query);
    return Scaffold(
      appBar: AppBar(
        leading: widget.leading,
        title: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(name,
              maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 16)),
          if (upd != null)
            Text(
              'Cập nhật ${upd.day.toString().padLeft(2, '0')}/${upd.month.toString().padLeft(2, '0')} '
              '${upd.hour.toString().padLeft(2, '0')}:${upd.minute.toString().padLeft(2, '0')}'
              '${_offline ? ' · ngoại tuyến' : ''}',
              style: TextStyle(fontSize: 12, color: _offline ? Brand.accent : Colors.white70),
            ),
        ]),
        actions: [
          const ScaleButton(),
          IconButton(tooltip: 'Tải lại', onPressed: _loading ? null : _loadIndex, icon: const Icon(Icons.refresh)),
        ],
        bottom: _loading
            ? const PreferredSize(
                preferredSize: Size.fromHeight(3), child: LinearProgressIndicator(minHeight: 3, color: Brand.accent))
            : null,
      ),
      body: RefreshIndicator(
        onRefresh: _loadIndex,
        child: ListView(
          padding: EdgeInsets.symmetric(horizontal: wide ? 24 : 10, vertical: 12),
          children: [
            if (_idx != null) _filters(),
            if (_nvs.length >= 2)
              const Padding(
                padding: EdgeInsets.only(top: 8),
                child: Text(
                  'Đang lọc dòng theo nhiều ĐDKD: thẻ số, biểu đồ và dòng Tổng vẫn là số của cả team.',
                  style: TextStyle(fontSize: 12, color: Brand.salary),
                ),
              ),
            const SizedBox(height: 8),
            if (_error != null)
              Padding(
                padding: const EdgeInsets.all(24),
                child: Column(children: [
                  const Icon(Icons.cloud_off, size: 40, color: Brand.navy),
                  const SizedBox(height: 8),
                  Text(_error!, textAlign: TextAlign.center, style: const TextStyle(color: Brand.muted)),
                  const SizedBox(height: 12),
                  FilledButton(onPressed: _loadIndex, child: const Text('Thử lại')),
                ]),
              )
            else if (_doc != null)
              PageFilterScope(filter: page, child: ReportItems(items: _doc!.items, wide: wide)),
            const SizedBox(height: 24),
          ],
        ),
      ),
    );
  }

  Widget _filters() {
    final idx = _idx!;
    final months = widget.manifest.kpiMonths;
    final date = _exactNv != null ? idx.nvDates.first : _date!;
    final nvText = _nvs.isEmpty ? allNvLabel : (_nvs.length == 1 ? _nvs.first : '${_nvs.length} ĐDKD');
    return Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
      Wrap(spacing: 8, runSpacing: 8, crossAxisAlignment: WrapCrossAlignment.center, children: [
        if (months.length > 1)
          SegmentedButton<String>(
            showSelectedIcon: false,
            segments: [for (final m in months) ButtonSegment(value: m.key, label: Text(m.label))],
            selected: {widget.monthKey},
            onSelectionChanged: (s) => widget.onMonthChanged(s.first),
          ),
        OutlinedButton.icon(
          onPressed: _pickDate,
          icon: const Icon(Icons.calendar_today, size: 18),
          label: Text(_ddmm(date)),
        ),
        OutlinedButton.icon(
          onPressed: _pickNv,
          icon: const Icon(Icons.people_alt_outlined, size: 18),
          label: Text(nvText),
        ),
        OutlinedButton.icon(
          onPressed: _pickThu,
          icon: const Icon(Icons.event_note_outlined, size: 18),
          label: Text(_thu.isEmpty ? 'Tất cả các thứ' : 'Thứ ${_thu.join(', ')}'),
        ),
        if (_nvs.isNotEmpty || _thu.isNotEmpty || _query.isNotEmpty)
          TextButton.icon(
            onPressed: () {
              final reload = _exactNv != null;
              setState(() {
                _nvs = [];
                _thu = {};
                _query = '';
                _queryCtl.clear();
              });
              if (reload) _loadDoc();
            },
            icon: const Icon(Icons.clear, size: 18),
            label: const Text('Bỏ lọc'),
          ),
      ]),
      const SizedBox(height: 8),
      TextField(
        controller: _queryCtl,
        decoration: InputDecoration(
          isDense: true,
          prefixIcon: const Icon(Icons.search),
          hintText: 'Tìm Mã KH / Tên KH / tên NV trong mọi bảng',
          border: const OutlineInputBorder(),
          suffixIcon: _query.isEmpty
              ? null
              : IconButton(
                  icon: const Icon(Icons.close),
                  onPressed: () => setState(() {
                    _queryCtl.clear();
                    _query = '';
                  }),
                ),
        ),
        onChanged: (t) {
          _debounce?.cancel();
          _debounce = Timer(const Duration(milliseconds: 350), () => setState(() => _query = t));
        },
      ),
    ]);
  }
}
