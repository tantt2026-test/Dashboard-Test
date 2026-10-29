import 'dart:math' as math;

import 'package:flutter/material.dart';
import 'package:two_dimensional_scrollables/two_dimensional_scrollables.dart';

import 'app_scale.dart';
import 'report_view.dart' show hexColor;
import 'table_model.dart';
import 'text_norm.dart';
import 'theme.dart';

/// Bộ lọc cấp trang (ĐDKD nhiều người, Thứ VT, tìm kiếm) — mọi bảng bên dưới đều áp dụng.
class PageFilterScope extends InheritedWidget {
  final PageFilter filter;
  const PageFilterScope({super.key, required this.filter, required super.child});

  static PageFilter of(BuildContext context) =>
      context.dependOnInheritedWidgetOfExactType<PageFilterScope>()?.filter ?? const PageFilter();

  @override
  bool updateShouldNotify(PageFilterScope old) => old.filter != filter;
}

/// Bảng trong trang báo cáo: tự vừa bề ngang màn hình, chữ căn giữa, vuốt dọc là cuộn cả
/// trang. Bảng dài hiện [inlineRows] dòng đầu + nút xem đủ. Nút 🔍 lọc, ⛶ toàn màn hình.
class ReportTable extends StatefulWidget {
  final Map<String, dynamic> data;
  final String? title;
  final int inlineRows;
  const ReportTable({super.key, required this.data, this.title, this.inlineRows = 30});

  @override
  State<ReportTable> createState() => _ReportTableState();
}

class _ReportTableState extends State<ReportTable> {
  late TableModel _model;
  RowFilter _filter = const RowFilter();

  @override
  void initState() {
    super.initState();
    _model = TableModel(widget.data);
  }

  @override
  void didUpdateWidget(ReportTable old) {
    super.didUpdateWidget(old);
    if (!identical(old.data, widget.data)) {
      _model = TableModel(widget.data);
      _filter = const RowFilter();
    }
  }

  Future<void> _openFilter() async {
    final f = await showTableFilter(context, _model, _filter);
    if (f != null) setState(() => _filter = f);
  }

  Future<void> _openFull() async {
    final f = await Navigator.of(context).push<RowFilter>(MaterialPageRoute(
      builder: (_) => FullscreenTable(
        model: _model,
        title: widget.title,
        filter: _filter,
        page: PageFilterScope.of(context),
      ),
    ));
    if (f != null && mounted) setState(() => _filter = f);
  }

  @override
  Widget build(BuildContext context) {
    final page = PageFilterScope.of(context);
    final zoom = AppScale.of(context).value;
    final m = _model;
    if (m.head.isEmpty && m.body.isEmpty) return const SizedBox.shrink();
    final vis = visibleRows(m, _filter, page);
    final dataRows = vis.where((i) => !m.isTotal[i]).length;
    final allData = m.isTotal.where((t) => !t).length;

    // Trong trang: tối đa inlineRows dòng dữ liệu + các dòng Tổng
    final shown = <int>[];
    var n = 0;
    for (final i in vis) {
      if (m.isTotal[i]) {
        shown.add(i);
      } else if (n < widget.inlineRows) {
        shown.add(i);
        n++;
      }
    }
    final hidden = dataRows - n;
    final filtering = _filter.active || (page.active && m.filterable);

    return LayoutBuilder(builder: (ctx, c) {
      final layout = Layout.place(m.head, [for (final i in shown) m.body[i]],
          totals: [for (final i in shown) m.isTotal[i]], fz: m.fzWanted)
        ..size(zoom: zoom, avail: c.maxWidth - 2);
      return Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
        _Toolbar(
          text: filtering ? 'Hiển thị $dataRows / $allData dòng' : '$allData dòng',
          filterCount: _filter.count,
          onFilter: m.filterable ? _openFilter : null,
          onFull: _openFull,
        ),
        DecoratedBox(
          decoration: BoxDecoration(
            border: Border.all(color: Brand.cellBorder),
            borderRadius: BorderRadius.circular(6),
          ),
          child: ClipRRect(borderRadius: BorderRadius.circular(6), child: StaticGrid(layout: layout)),
        ),
        if (hidden > 0)
          Align(
            alignment: Alignment.center,
            child: TextButton.icon(
              onPressed: _openFull,
              icon: const Icon(Icons.open_in_full, size: 18),
              label: Text('Xem đủ $dataRows dòng'),
            ),
          ),
        if (filtering && m.isTotal.contains(true))
          const Padding(
            padding: EdgeInsets.only(top: 4),
            child: Text('* Dòng Tổng là số của cả bảng (chưa tính lại theo bộ lọc).',
                textAlign: TextAlign.center, style: TextStyle(fontSize: 11, color: Brand.muted)),
          ),
      ]);
    });
  }
}

class _Toolbar extends StatelessWidget {
  final String text;
  final int filterCount;
  final VoidCallback? onFilter;
  final VoidCallback onFull;
  const _Toolbar({required this.text, required this.filterCount, required this.onFilter, required this.onFull});

  @override
  Widget build(BuildContext context) {
    return Row(children: [
      Expanded(child: Text(text, style: const TextStyle(fontSize: 11.5, color: Brand.muted))),
      if (onFilter != null)
        IconButton(
          visualDensity: VisualDensity.compact,
          tooltip: 'Lọc bảng',
          onPressed: onFilter,
          icon: Badge(
            isLabelVisible: filterCount > 0,
            label: Text('$filterCount'),
            child: Icon(Icons.filter_alt_outlined, color: filterCount > 0 ? Brand.blue : Brand.muted),
          ),
        ),
      IconButton(
        visualDensity: VisualDensity.compact,
        tooltip: 'Toàn màn hình',
        onPressed: onFull,
        icon: const Icon(Icons.fullscreen, color: Brand.muted),
      ),
    ]);
  }
}

/// Ô bảng: màu như Streamlit, chữ căn giữa.
Widget tableCell(Placed p, Layout l) {
  final cell = p.c;
  final bgDefault = (p.head || p.total) ? Brand.navy : (p.bodyIndex.isEven ? Brand.zebra : Colors.white);
  final bg = hexColor(cell['bg']) ?? bgDefault;
  final fg = hexColor(cell['fg']) ??
      ((cell['bg'] != null)
          ? (bg.computeLuminance() < 0.35 ? Colors.white : const Color(0xFF1A202C))
          : ((p.head || p.total) ? Colors.white : const Color(0xFF1A202C)));
  final f = l.fontScale;
  return Container(
    padding: EdgeInsets.symmetric(horizontal: 5 * f, vertical: 3 * f),
    alignment: Alignment.center,
    decoration: BoxDecoration(
      color: bg,
      border: Border.all(color: (p.head || p.total) ? Brand.border : Brand.cellBorder, width: 0.5),
    ),
    child: Text(
      cell['x'] as String,
      maxLines: 4,
      overflow: TextOverflow.ellipsis,
      textAlign: TextAlign.center,
      style: TextStyle(
        color: fg,
        fontSize: (p.head ? 11.5 : 12.5) * f,
        height: 1.2,
        fontWeight: (cell['b'] == 1 || p.total) ? FontWeight.w700 : FontWeight.w500,
        fontFeatures: const [FontFeature.tabularFigures()],
      ),
    ),
  );
}

/// Lưới tĩnh (không tự cuộn dọc): vừa màn hình thì vẽ thẳng; rộng hơn thì giữ cột cố định
/// bên trái, phần còn lại cuộn ngang.
class StaticGrid extends StatelessWidget {
  final Layout layout;
  const StaticGrid({super.key, required this.layout});

  @override
  Widget build(BuildContext context) {
    final l = layout;
    final xs = <double>[0];
    for (final w in l.colW) {
      xs.add(xs.last + w);
    }
    final ys = <double>[0];
    for (final h in l.rowH) {
      ys.add(ys.last + h);
    }
    Widget stack(Iterable<Placed> cells, double x0, double width) => SizedBox(
          width: width,
          height: ys.last,
          child: Stack(children: [
            for (final p in cells)
              Positioned(
                left: xs[p.col] - x0,
                top: ys[p.r],
                width: xs[math.min(p.col + p.cs, l.cols)] - xs[p.col],
                height: ys[math.min(p.r + p.rs, l.rows)] - ys[p.r],
                child: tableCell(p, l),
              ),
          ]),
        );

    return LayoutBuilder(builder: (ctx, c) {
      final frozen = l.frozenFor(c.maxWidth);
      if (l.width <= c.maxWidth + 0.5 || frozen == 0) {
        final grid = stack(l.placed, 0, l.width);
        return l.width <= c.maxWidth + 0.5
            ? Center(child: grid)
            : SingleChildScrollView(scrollDirection: Axis.horizontal, child: grid);
      }
      final fx = xs[frozen];
      return Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
        DecoratedBox(
          decoration: const BoxDecoration(boxShadow: [
            BoxShadow(color: Color(0x30000000), blurRadius: 4, offset: Offset(2, 0), spreadRadius: -2)
          ]),
          child: stack(l.placed.where((p) => p.col < frozen), 0, fx),
        ),
        Expanded(
          child: SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: stack(l.placed.where((p) => p.col >= frozen), fx, l.width - fx),
          ),
        ),
      ]);
    });
  }
}

/// Bảng toàn màn hình: cuộn dọc + ngang, dòng tiêu đề & cột tên cố định, phóng to/thu nhỏ,
/// lọc. Trả về bộ lọc khi đóng để bảng trong trang dùng tiếp.
class FullscreenTable extends StatefulWidget {
  final TableModel model;
  final String? title;
  final RowFilter filter;
  final PageFilter page;
  const FullscreenTable({super.key, required this.model, this.title, required this.filter, required this.page});

  @override
  State<FullscreenTable> createState() => _FullscreenTableState();
}

class _FullscreenTableState extends State<FullscreenTable> {
  late RowFilter _filter = widget.filter;
  double _manual = 1.0;
  bool _fit = true;
  final _v = ScrollController();
  final _h = ScrollController();

  @override
  void dispose() {
    _v.dispose();
    _h.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final m = widget.model;
    final zoom = AppScale.of(context).value;
    final vis = visibleRows(m, _filter, widget.page);
    final dataRows = vis.where((i) => !m.isTotal[i]).length;

    return PopScope(
      canPop: false,
      onPopInvokedWithResult: (didPop, _) {
        if (!didPop) Navigator.of(context).pop(_filter);
      },
      child: Scaffold(
        appBar: AppBar(
          title: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(widget.title ?? 'Bảng dữ liệu',
                maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w700)),
            Text('$dataRows dòng · ${(_manual * 100).round()}%${_fit ? ' · vừa màn hình' : ''}',
                style: const TextStyle(fontSize: 12, color: Colors.white70)),
          ]),
          actions: [
            if (m.filterable)
              IconButton(
                tooltip: 'Lọc',
                onPressed: () async {
                  final f = await showTableFilter(context, m, _filter);
                  if (f != null) setState(() => _filter = f);
                },
                icon: Badge(
                  isLabelVisible: _filter.count > 0,
                  label: Text('${_filter.count}'),
                  child: const Icon(Icons.filter_alt_outlined),
                ),
              ),
            IconButton(
                tooltip: 'Thu nhỏ',
                onPressed: () => setState(() => _manual = math.max(0.4, _manual - 0.1)),
                icon: const Icon(Icons.zoom_out)),
            IconButton(
                tooltip: 'Phóng to',
                onPressed: () => setState(() => _manual = math.min(3.0, _manual + 0.1)),
                icon: const Icon(Icons.zoom_in)),
            IconButton(
              tooltip: _fit ? 'Bỏ vừa màn hình' : 'Vừa màn hình',
              onPressed: () => setState(() {
                _fit = !_fit;
                _manual = 1.0;
              }),
              icon: Icon(_fit ? Icons.fit_screen : Icons.fit_screen_outlined),
            ),
          ],
        ),
        body: SafeArea(
          child: LayoutBuilder(builder: (ctx, c) {
            final l = Layout.place(m.head, [for (final i in vis) m.body[i]],
                totals: [for (final i in vis) m.isTotal[i]], fz: m.fzWanted)
              ..size(zoom: zoom, avail: _fit ? c.maxWidth - 12 : null, manual: _manual, minFit: 0.4);
            if (l.rows == 0 || l.cols == 0) return const Center(child: Text('Không có dòng nào khớp bộ lọc'));
            return Scrollbar(
              controller: _v,
              thumbVisibility: true,
              notificationPredicate: (n) => n.metrics.axis == Axis.vertical,
              child: Scrollbar(
                controller: _h,
                thumbVisibility: true,
                notificationPredicate: (n) => n.metrics.axis == Axis.horizontal,
                child: Padding(
                  padding: const EdgeInsets.only(right: 10, bottom: 10),
                  child: TableView.builder(
                    verticalDetails: ScrollableDetails.vertical(controller: _v),
                    horizontalDetails: ScrollableDetails.horizontal(controller: _h),
                    diagonalDragBehavior: DiagonalDragBehavior.free,
                    pinnedRowCount: math.min(l.headRows, l.rows),
                    pinnedColumnCount: l.frozenFor(c.maxWidth - 12, maxShare: 0.6),
                    rowCount: l.rows,
                    columnCount: l.cols,
                    columnBuilder: (i) => TableSpan(extent: FixedTableSpanExtent(l.colW[i])),
                    rowBuilder: (i) => TableSpan(extent: FixedTableSpanExtent(l.rowH[i])),
                    cellBuilder: (ctx, v) {
                      final p = l.at[v.row][v.column];
                      if (p == null) return const TableViewCell(child: SizedBox.shrink());
                      final child = tableCell(p, l);
                      if (p.rs == 1 && p.cs == 1) return TableViewCell(child: child);
                      return TableViewCell(
                        rowMergeStart: p.rs > 1 ? p.r : null,
                        rowMergeSpan: p.rs > 1 ? p.rs : null,
                        columnMergeStart: p.cs > 1 ? p.col : null,
                        columnMergeSpan: p.cs > 1 ? p.cs : null,
                        child: child,
                      );
                    },
                  ),
                ),
              ),
            );
          }),
        ),
      ),
    );
  }
}

/// Hộp lọc bảng: tìm kiếm + chọn giá trị theo từng cột (như các ô lọc trên Streamlit).
Future<RowFilter?> showTableFilter(BuildContext context, TableModel m, RowFilter current) {
  return showModalBottomSheet<RowFilter>(
    context: context,
    isScrollControlled: true,
    showDragHandle: true,
    builder: (ctx) => _FilterSheet(model: m, initial: current),
  );
}

class _FilterSheet extends StatefulWidget {
  final TableModel model;
  final RowFilter initial;
  const _FilterSheet({required this.model, required this.initial});

  @override
  State<_FilterSheet> createState() => _FilterSheetState();
}

class _FilterSheetState extends State<_FilterSheet> {
  late final Map<int, Set<String>> _sel = {
    for (final e in widget.initial.byCol.entries) e.key: {...e.value}
  };
  late final _q = TextEditingController(text: widget.initial.query);
  final Map<int, String> _colSearch = {};

  @override
  void dispose() {
    _q.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final m = widget.model;
    final cols = m.filterColumns;
    return SafeArea(
      child: Padding(
        padding: EdgeInsets.only(bottom: MediaQuery.of(context).viewInsets.bottom),
        child: ConstrainedBox(
          constraints: BoxConstraints(maxHeight: MediaQuery.of(context).size.height * 0.85),
          child: Column(mainAxisSize: MainAxisSize.min, children: [
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 0, 12, 8),
              child: Row(children: [
                const Expanded(
                    child: Text('Lọc bảng', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w700))),
                TextButton(
                  onPressed: () => setState(() {
                    _sel.clear();
                    _q.clear();
                  }),
                  child: const Text('Xoá lọc'),
                ),
                FilledButton(
                  onPressed: () => Navigator.pop(context, RowFilter(byCol: {..._sel}, query: _q.text)),
                  child: const Text('Áp dụng'),
                ),
              ]),
            ),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: TextField(
                controller: _q,
                decoration: const InputDecoration(
                  prefixIcon: Icon(Icons.search),
                  hintText: 'Tìm trong bảng (mã KH, tên KH, tên NV...)',
                  isDense: true,
                  border: OutlineInputBorder(),
                ),
              ),
            ),
            const SizedBox(height: 8),
            const Divider(height: 1),
            Flexible(
              child: ListView(shrinkWrap: true, children: [
                for (final c in cols)
                  () {
                    final values = m.valuesOf(c);
                    final sel = _sel[c] ?? {};
                    final q = fold(_colSearch[c] ?? '');
                    final shownVals = q.isEmpty ? values : values.where((v) => fold(v).contains(q)).toList();
                    return ExpansionTile(
                      title: Text(m.colNames[c], style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600)),
                      subtitle: sel.isEmpty
                          ? Text('Tất cả (${values.length})', style: const TextStyle(fontSize: 12))
                          : Text('Đã chọn ${sel.length}: ${sel.take(3).join(', ')}${sel.length > 3 ? '…' : ''}',
                              style: const TextStyle(fontSize: 12, color: Brand.blue)),
                      childrenPadding: const EdgeInsets.fromLTRB(16, 0, 16, 12),
                      children: [
                        if (values.length > 12)
                          Padding(
                            padding: const EdgeInsets.only(bottom: 8),
                            child: TextField(
                              decoration: const InputDecoration(
                                  isDense: true, hintText: 'Tìm giá trị...', prefixIcon: Icon(Icons.search, size: 18)),
                              onChanged: (t) => setState(() => _colSearch[c] = t),
                            ),
                          ),
                        Wrap(spacing: 6, runSpacing: 4, children: [
                          for (final v in shownVals.take(200))
                            FilterChip(
                              label: Text(v, style: const TextStyle(fontSize: 12)),
                              selected: sel.contains(v),
                              visualDensity: VisualDensity.compact,
                              onSelected: (on) => setState(() {
                                final s = _sel.putIfAbsent(c, () => {});
                                on ? s.add(v) : s.remove(v);
                                if (s.isEmpty) _sel.remove(c);
                              }),
                            ),
                        ]),
                      ],
                    );
                  }(),
                if (cols.isEmpty)
                  const Padding(
                    padding: EdgeInsets.all(16),
                    child: Text('Bảng này chỉ lọc được bằng ô tìm kiếm.', style: TextStyle(color: Brand.muted)),
                  ),
              ]),
            ),
          ]),
        ),
      ),
    );
  }
}
