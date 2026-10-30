import 'dart:convert';

import 'package:flutter/material.dart';

import '../data/filter_cache.dart';
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
  // Bộ lọc kiểu "tính lại": kết quả App.py do GitHub Actions tính & lưu (branch filters)
  static final _cache = FilterCache();
  FilterJob? _job;
  // Ghi nhớ kết quả lọc: chỉ tính lại khi đổi lựa chọn / dữ liệu (tránh treo máy khi vẽ lại)
  String? _memoKey;
  FilterResult? _memo;
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
    } else if (old.manifest.sourceCommit != widget.manifest.sourceCommit ||
        old.manifest.generatedAt != widget.manifest.generatedAt) {
      // có data mới → tải lại, giữ nguyên các ô đang lọc
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
      final wasDefault = _idx == null || _date == _idx!.defaultDate;
      final r = await widget.repo.kpiIndex(widget.monthKey);
      _idx = r.value;
      _offline = r.fromCache;
      if (wasDefault || _date == null || !_idx!.dates.contains(_date)) _date = _idx!.defaultDate;
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

  /// Ngày đang chọn chưa có bản tính sẵn theo data mới nhất (ngày còn số cũ, hoặc chưa tính)
  /// → hiện khung báo cáo của ngày gần nhất, số do App.py tính lại cho đúng ngày đó.
  bool get _staleDay {
    final idx = _idx!;
    if (_isTab || _exactNv != null) return false;
    return idx.staleDates.contains(_date) || !idx.dates.contains(_date);
  }

  String get _fileDate => _staleDay && !_idx!.dates.contains(_date) ? _idx!.defaultDate : _docDate;

  Future<void> _loadDoc() async {
    final idx = _idx;
    if (idx == null) return;
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final r = await widget.repo.kpiDoc(idx, widget.code, _fileDate, _isTab ? null : _exactNv);
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
    // chọn được cả tháng như Streamlit; ngày chưa tính sẵn thì App.py tính lại
    final picked = await showDatePicker(
      context: context,
      initialDate: DateTime.parse(_date!),
      firstDate: DateTime(idx.year, idx.month, 1),
      lastDate: DateTime(idx.year, idx.month + 1, 0),
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

  /// Lựa chọn hiện tại có cần App.py tính lại không (app không tự tính chính xác được)?
  bool _needServer(List<Map<String, dynamic>> widgets, String? variantNote) {
    if (_nvs.length >= 2) return true;
    if (variantNote != null) return true;
    if (_staleDay) return true;
    // bản Mac tự tính từ data mới: chưa đo cách áp ô lọc → lọc gì cũng tính lại bằng App.py
    if (_doc?.local == true && widgets.any((w) => isActive(w, _values[w['key']]))) return true;
    for (final w in widgets) {
      final mode = (w['f'] as Map?)?['mode'];
      if ((mode == 'partial' || mode == 'unsupported') && isActive(w, _values[w['key']])) return true;
    }
    return false;
  }

  /// Lấy kết quả App.py cho lựa chọn hiện tại (đã lưu sẵn trên GitHub, hoặc nhờ GitHub tính).
  FilterJob? _requestGithub(List<Map<String, dynamic>> widgets) {
    final idx = _idx!, doc = _doc!;
    final sc = widget.manifest.sourceCommit;
    if (sc == null) return null;
    final name = idx.reports.where((r) => r.code == widget.code).map((r) => r.name).firstOrNull ?? doc.name;
    final active = {for (final w in widgets) w['key']: w};
    final req = {
      'month_key': idx.monthKey,
      'date': _docDate,
      'code': widget.code,
      'name': name,
      'nav': _isTab ? name : null,
      'ddkd': _nvs,
      'values': {
        for (final e in _values.entries)
          if (active[e.key] != null && isActive(active[e.key]!, e.value)) e.key: e.value
      },
      'sc': sc,
    };
    return _cache.get(req, () {
      if (mounted) setState(() {});
    });
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
    var fromServer = false;
    if (_doc != null) {
      final widgets = [...collectWidgets(_doc!.items), ..._mainWidgets()];
      final (file, note) = pickVariant(widgets, _values);
      // Lựa chọn app không tự tính chính xác → kết quả App.py do GitHub tính & lưu (đúng như Streamlit)
      final useServer = _needServer(widgets, note);
      _job = useServer ? _requestGithub(widgets) : null;
      final job = _job;
      if (job?.items != null) {
        items = job!.items;
        fromServer = true;
      }
      if (job != null && job.items == null && job.error == null) {
        notes.add(job.local
            ? 'Máy đang tính lại bằng App.py… ${job.waitedSeconds}s (lần đầu sau mỗi lần sync phải tải data về máy, '
                'lâu hơn chút; sau đó chỉ vài giây)'
            : job.dispatched
            ? 'GitHub đang tính lại theo bộ lọc bằng App.py… ${job.waitedSeconds}s (thường 1,5–3 phút; '
                'xong sẽ tự hiện, lần sau mở tổ hợp này là có ngay)'
            : 'Đang tìm kết quả đã tính sẵn cho bộ lọc này…');
      }
      if (job?.error != null) {
        notes.add('Chưa lấy được kết quả tính lại (${job!.error}) — đang hiện kết quả lọc trên máy.');
      }
      if (note != null && !fromServer && !useServer) notes.add(note);
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
      if (!fromServer) {
        final mk = '${identityHashCode(base)}|${jsonEncode(_values)}|${_nvs.join(',')}|$file|$waitingVariant';
        if (mk != _memoKey) {
          _memo = applyFilters(base, widgets, _values,
              onVariant: file != null && !waitingVariant, multiNv: _nvs.length >= 2 ? _nvs.toSet() : null);
          _memoKey = mk;
        }
        final res = _memo!;
        items = res.items;
        if (!useServer || job?.error != null) notes.addAll(res.notes);
        // ngày chưa có số theo data mới: không hiện số cũ trong lúc chờ tính lại
        if (_staleDay) items = const [];
      }
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
        bottom: (_loading || waitingVariant || (_job != null && _job!.items == null && _job!.error == null))
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
              if (fromServer)
                const Padding(
                  padding: EdgeInsets.only(top: 6),
                  child: Text('✓ Kết quả tính lại theo bộ lọc bằng App.py (giống Streamlit) — lưu sẵn trên GitHub',
                      style: TextStyle(fontSize: 12, color: Color(0xFF2F855A), fontWeight: FontWeight.w600)),
                ),
              if (_nvs.length >= 2 && !fromServer)
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
