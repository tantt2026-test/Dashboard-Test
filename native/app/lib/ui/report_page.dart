import 'package:flutter/material.dart';

import '../data/report_repository.dart';
import '../logic/filter_engine.dart';
import '../logic/turnover_logic.dart' show allNvLabel, isoDate;
import 'app_scale.dart';
import 'filter_widgets.dart';
import 'report_view.dart';
import 'theme.dart';

/// Màn hình chung cho các báo cáo tab KPI + các tab khác: nội dung do App.py xuất sẵn.
/// Ô lọc y như Streamlit: hàng lọc chung (Ngày, ĐDKD, Thứ VT, Mã KH, Tên KH) + các nhóm
/// ô lọc của từng báo cáo đúng vị trí. Cách lọc do pipeline đo từ App.py (filter_engine).
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

// Ô lọc chung đầu trang của App.py (nhãn/placeholder/lựa chọn y như Streamlit)
const _mainDefs = <Map<String, dynamic>>[
  {
    'key': 'mbs_cat_thu_filter',
    'kind': 'multiselect',
    'label': '📅 Thứ VT (MBS CAT/BRAND)',
    'placeholder': 'Tất cả các thứ',
    'options': ['2', '3', '4', '5', '6', '7', '25', '36', '47'],
    'value': <String>[],
  },
  {
    'key': 'filter_ma_kh',
    'kind': 'text_input',
    'label': '🆔 Mã Khách Hàng',
    'placeholder': 'Nhập mã KH rồi Enter (nhiều mã cách nhau bởi dấu phẩy)',
    'value': '',
  },
  {
    'key': 'filter_ten_kh',
    'kind': 'text_input',
    'label': '🏪 Tên Khách Hàng',
    'placeholder': 'Nhập tên KH rồi Enter (nhiều tên cách nhau bởi dấu phẩy)',
    'value': '',
  },
];

class _KpiReportPageState extends State<KpiReportPage> {
  KpiIndex? _idx;
  ReportDoc? _doc;
  String? _date;
  List<String> _nvs = []; // ĐDKD (chọn nhiều, giữ thứ tự)
  FilterValues _values = {};
  final Map<String, List<Map<String, dynamic>>> _variants = {};
  final Set<String> _loadingVariants = {};
  bool _loading = true;
  bool _offline = false;
  String? _error;

  String? get _exactNv => _nvs.length == 1 ? _nvs.first : null;
  bool get _isTab => widget.code.startsWith('TAB_');

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
      _values = {};
      _variants.clear();
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

  String get _docDate {
    final idx = _idx!;
    if (_isTab) return idx.tabDates.isNotEmpty ? idx.tabDates.first : idx.defaultDate;
    if (_exactNv != null) return idx.nvDates.first;
    return _date!;
  }

  Future<void> _loadDoc() async {
    final idx = _idx;
    if (idx == null) return;
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final r = await widget.repo.kpiDoc(idx, widget.code, _docDate, _isTab ? null : _exactNv);
      if (!mounted) return;
      setState(() {
        _doc = r.value;
        _variants.clear();
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

  void _loadVariant(String file) {
    if (_variants.containsKey(file) || _loadingVariants.contains(file)) return;
    _loadingVariants.add(file);
    widget.repo.kpiVariant(_idx!, widget.code, file).then((items) {
      if (!mounted) return;
      setState(() {
        _variants[file] = items;
        _loadingVariants.remove(file);
      });
    }).catchError((Object e) {
      _loadingVariants.remove(file);
    });
  }

  String _ddmm(String iso) {
    final d = DateTime.parse(iso);
    return '${d.year}/${d.month.toString().padLeft(2, '0')}/${d.day.toString().padLeft(2, '0')}';
  }

  Future<void> _pickDate() async {
    final idx = _idx!;
    if (_isTab) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          content: Text('Tab này hiện có số liệu ngày ${_ddmm(_docDate)} (ngày mới nhất).')));
      return;
    }
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
      helpText: 'NGÀY',
    );
    if (picked != null) _date = isoDate(picked);
    _loadDoc();
  }

  void _setValue(String key, Object? v) {
    if (key == 'ddkd') {
      final wasExact = _exactNv;
      setState(() => _nvs = ((v as List?) ?? const []).map((e) => '$e').toList());
      if (wasExact != _exactNv && !_isTab) _loadDoc();
      return;
    }
    setState(() => _values = {..._values, key: v});
  }

  /// Ô lọc chung: lấy cách áp (spec) của báo cáo này nếu có.
  List<Map<String, dynamic>> _mainWidgets() => [
        for (final d in _mainDefs)
          {...d, if (_doc?.main[d['key']] != null) 'f': _doc!.main[d['key']]!['f']}
      ];

  @override
  Widget build(BuildContext context) {
    final name = _idx?.reports.where((r) => r.code == widget.code).map((r) => r.name).firstOrNull ?? widget.code;
    final upd = widget.manifest.generatedAt?.toUtc().add(const Duration(hours: 7));
    final wide = MediaQuery.of(context).size.width >= 720;

    List<Map<String, dynamic>>? items;
    final notes = <String>[];
    var waitingVariant = false;
    if (_doc != null) {
      final widgets = [...collectWidgets(_doc!.items), ..._mainWidgets()];
      final (file, note) = pickVariant(widgets, _values);
      if (note != null) notes.add(note);
      var base = _doc!.items;
      if (file != null) {
        final v = _variants[file];
        if (v == null) {
          _loadVariant(file);
          waitingVariant = true;
        } else {
          base = v;
        }
      }
      final res = applyFilters(base, widgets, _values,
          onVariant: file != null && !waitingVariant, multiNv: _nvs.length >= 2 ? _nvs.toSet() : null);
      items = res.items;
      notes.addAll(res.notes);
    }

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
        bottom: (_loading || waitingVariant)
            ? const PreferredSize(
                preferredSize: Size.fromHeight(3), child: LinearProgressIndicator(minHeight: 3, color: Brand.accent))
            : null,
      ),
      body: FilterScope(
        values: {..._values, 'ddkd': _nvs},
        onChanged: _setValue,
        child: RefreshIndicator(
          onRefresh: _loadIndex,
          child: ListView(
            padding: EdgeInsets.symmetric(horizontal: wide ? 24 : 10, vertical: 12),
            children: [
              if (_idx != null) _mainBar(),
              if (_nvs.length >= 2)
                const Padding(
                  padding: EdgeInsets.only(top: 6),
                  child: Text('Nhiều ĐDKD: bảng lọc theo người, dòng Tổng tính lại theo các dòng còn lại; '
                      'thẻ số và biểu đồ là của cả team.',
                      style: TextStyle(fontSize: 12, color: Brand.salary)),
                ),
              for (final n in notes)
                Container(
                  margin: const EdgeInsets.only(top: 8),
                  padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(color: const Color(0xFFFEFCBF), borderRadius: BorderRadius.circular(6)),
                  child: Text(n, style: const TextStyle(fontSize: 12.5, color: Color(0xFF744210))),
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
              else if (items != null)
                ReportItems(items: items, wide: wide),
              const SizedBox(height: 24),
            ],
          ),
        ),
      ),
    );
  }

  /// Hàng lọc chung như Streamlit: Tháng · NGÀY · ĐDKD · Thứ VT · Mã KH · Tên KH
  Widget _mainBar() {
    final idx = _idx!;
    final months = widget.manifest.kpiMonths;
    const label = TextStyle(color: Color(0xFFC53030), fontWeight: FontWeight.w700, fontSize: 12.5);
    final nvDef = {
      'key': 'ddkd',
      'kind': 'multiselect',
      'label': 'ĐDKD (Nhân viên - Chọn nhiều)',
      'placeholder': allNvLabel,
      'options': idx.nv,
      'value': <String>[],
    };
    return Container(
      padding: const EdgeInsets.all(10),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: const Color(0xFFE2E8F0)),
      ),
      child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
        Wrap(spacing: 10, runSpacing: 8, crossAxisAlignment: WrapCrossAlignment.end, children: [
          if (months.length > 1)
            Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              const Padding(padding: EdgeInsets.only(bottom: 4), child: Text('📅 Tháng báo cáo', style: label)),
              SegmentedButton<String>(
                showSelectedIcon: false,
                segments: [for (final m in months) ButtonSegment(value: m.key, label: Text(m.label))],
                selected: {widget.monthKey},
                onSelectionChanged: (s) => widget.onMonthChanged(s.first),
              ),
            ]),
          Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            const Padding(padding: EdgeInsets.only(bottom: 4), child: Text('NGÀY', style: label)),
            OutlinedButton.icon(
              onPressed: _pickDate,
              icon: const Icon(Icons.calendar_today, size: 16),
              label: Text(_ddmm(_docDate)),
            ),
          ]),
        ]),
        const SizedBox(height: 8),
        FilterRow(widgets: [nvDef, ..._mainWidgets()]),
      ]),
    );
  }
}
