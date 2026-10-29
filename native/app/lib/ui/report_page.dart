import 'package:flutter/material.dart';

import '../data/report_repository.dart';
import '../logic/turnover_logic.dart' show allNvLabel, isoDate;
import 'report_view.dart';
import 'theme.dart';

/// Màn hình chung cho 17 báo cáo tab KPI (giai đoạn 2): nội dung do App.py xuất sẵn.
/// Lọc: Tháng, Ngày (Tất cả ĐDKD), hoặc 1 ĐDKD (ngày mặc định).
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

class _KpiReportPageState extends State<KpiReportPage> {
  KpiIndex? _idx;
  ReportDoc? _doc;
  String? _date;
  String? _nv;
  bool _loading = true;
  bool _offline = false;
  String? _error;

  @override
  void initState() {
    super.initState();
    _loadIndex();
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
      if (_nv != null && !_idx!.nv.contains(_nv)) _nv = null;
      await _loadDoc();
    } catch (e) {
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
      final date = _nv != null ? idx.nvDates.first : _date!;
      final r = await widget.repo.kpiDoc(idx, widget.code, date, _nv);
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
    if (_nv != null) {
      final ok = await showDialog<bool>(
        context: context,
        builder: (ctx) => AlertDialog(
          title: const Text('Đổi ngày'),
          content: Text('Báo cáo lọc theo 1 ĐDKD hiện chỉ có cho ngày ${_ddmm(idx.nvDates.first)}.\n'
              'Bỏ lọc ĐDKD để xem ngày khác?'),
          actions: [
            TextButton(onPressed: () => Navigator.pop(ctx, false), child: const Text('Huỷ')),
            FilledButton(onPressed: () => Navigator.pop(ctx, true), child: const Text('Bỏ lọc')),
          ],
        ),
      );
      if (ok != true || !mounted) return;
      _nv = null;
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
    if (picked != null) {
      _date = isoDate(picked);
    }
    _loadDoc();
  }

  Future<void> _pickNv() async {
    final idx = _idx!;
    final picked = await showModalBottomSheet<String>(
      context: context,
      showDragHandle: true,
      isScrollControlled: true,
      builder: (ctx) => SafeArea(
        child: ConstrainedBox(
          constraints: BoxConstraints(maxHeight: MediaQuery.of(ctx).size.height * 0.8),
          child: Column(mainAxisSize: MainAxisSize.min, children: [
            Padding(
              padding: const EdgeInsets.fromLTRB(20, 0, 20, 8),
              child: Text('ĐDKD (ngày ${_ddmm(idx.nvDates.first)})',
                  style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w700)),
            ),
            const Divider(height: 1),
            Flexible(
              child: ListView(shrinkWrap: true, children: [
                ListTile(
                  dense: true,
                  leading: Icon(_nv == null ? Icons.radio_button_checked : Icons.radio_button_off,
                      color: Brand.navy),
                  title: const Text(allNvLabel),
                  onTap: () => Navigator.pop(ctx, ''),
                ),
                for (final n in idx.nv)
                  ListTile(
                    dense: true,
                    leading: Icon(_nv == n ? Icons.radio_button_checked : Icons.radio_button_off,
                        color: Brand.navy),
                    title: Text(n),
                    onTap: () => Navigator.pop(ctx, n),
                  ),
              ]),
            ),
          ]),
        ),
      ),
    );
    if (picked == null) return;
    _nv = picked.isEmpty ? null : picked;
    _loadDoc();
  }

  @override
  Widget build(BuildContext context) {
    final name = _idx?.reports.where((r) => r.code == widget.code).map((r) => r.name).firstOrNull ?? widget.code;
    final upd = widget.manifest.generatedAt?.toUtc().add(const Duration(hours: 7));
    final wide = MediaQuery.of(context).size.width >= 720;
    return Scaffold(
      appBar: AppBar(
        leading: widget.leading,
        title: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(name, maxLines: 1, overflow: TextOverflow.ellipsis,
              style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 16)),
          if (upd != null)
            Text(
              'Cập nhật ${upd.day.toString().padLeft(2, '0')}/${upd.month.toString().padLeft(2, '0')} '
              '${upd.hour.toString().padLeft(2, '0')}:${upd.minute.toString().padLeft(2, '0')}'
              '${_offline ? ' · ngoại tuyến' : ''}',
              style: TextStyle(fontSize: 12, color: _offline ? Brand.accent : Colors.white70),
            ),
        ]),
        actions: [
          IconButton(tooltip: 'Tải lại', onPressed: _loading ? null : _loadIndex, icon: const Icon(Icons.refresh)),
        ],
        bottom: _loading
            ? const PreferredSize(
                preferredSize: Size.fromHeight(3),
                child: LinearProgressIndicator(minHeight: 3, color: Brand.accent))
            : null,
      ),
      body: RefreshIndicator(
        onRefresh: _loadIndex,
        child: ListView(
          padding: EdgeInsets.symmetric(horizontal: wide ? 24 : 12, vertical: 12),
          children: [
            if (_idx != null) _filters(),
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
              ReportItems(items: _doc!.items, wide: wide),
            const SizedBox(height: 24),
          ],
        ),
      ),
    );
  }

  Widget _filters() {
    final idx = _idx!;
    final months = widget.manifest.kpiMonths;
    final date = _nv != null ? idx.nvDates.first : _date!;
    return Wrap(spacing: 8, runSpacing: 8, crossAxisAlignment: WrapCrossAlignment.center, children: [
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
        icon: const Icon(Icons.person_outline, size: 18),
        label: Text(_nv ?? allNvLabel),
      ),
    ]);
  }
}
