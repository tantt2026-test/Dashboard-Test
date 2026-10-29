import 'package:flutter/material.dart';

import '../logic/filter_engine.dart';
import 'text_norm.dart';
import 'theme.dart';

/// Giá trị hiện tại của các ô lọc + hàm đổi giá trị (do màn hình báo cáo giữ).
class FilterScope extends InheritedWidget {
  final FilterValues values;
  final void Function(String key, Object? value) onChanged;
  const FilterScope({super.key, required this.values, required this.onChanged, required super.child});

  static FilterScope? of(BuildContext context) => context.dependOnInheritedWidgetOfExactType<FilterScope>();

  @override
  bool updateShouldNotify(FilterScope old) => old.values != values;
}

const _labelColor = Color(0xFFC53030); // nhãn ô lọc màu đỏ như .filter-label của App.py

/// Một nhóm ô lọc như trên Streamlit: tiêu đề nhóm (nếu có) + các ô, nhãn phía trên.
class StreamlitFilterGroup extends StatelessWidget {
  final Map<String, dynamic> item;
  const StreamlitFilterGroup({super.key, required this.item});

  @override
  Widget build(BuildContext context) {
    final ws = (item['w'] as List).cast<Map<String, dynamic>>();
    final title = item['title'] as String?;
    return Container(
      margin: const EdgeInsets.symmetric(vertical: 8),
      padding: const EdgeInsets.fromLTRB(10, 8, 10, 10),
      decoration: BoxDecoration(
        color: const Color(0xFFF7FAFC),
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: const Color(0xFFE2E8F0)),
      ),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        if (title != null && title.isNotEmpty)
          Padding(
            padding: const EdgeInsets.only(bottom: 6),
            child: Text(title, style: const TextStyle(fontWeight: FontWeight.w800, color: Brand.navy, fontSize: 13.5)),
          ),
        FilterRow(widgets: ws),
      ]),
    );
  }
}

/// Hàng ô lọc tự xuống dòng; mỗi ô rộng ~260 (máy tính) hoặc cả hàng (điện thoại hẹp).
class FilterRow extends StatelessWidget {
  final List<Map<String, dynamic>> widgets;
  const FilterRow({super.key, required this.widgets});

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(builder: (ctx, c) {
      final per = c.maxWidth >= 1100 ? 4 : (c.maxWidth >= 700 ? 3 : (c.maxWidth >= 460 ? 2 : 1));
      final w = (c.maxWidth - 10 * (per - 1)) / per;
      return Wrap(spacing: 10, runSpacing: 8, children: [
        for (final wd in widgets) SizedBox(width: w, child: StreamlitWidget(w: wd)),
      ]);
    });
  }
}

class StreamlitWidget extends StatelessWidget {
  final Map<String, dynamic> w;
  const StreamlitWidget({super.key, required this.w});

  @override
  Widget build(BuildContext context) {
    final scope = FilterScope.of(context);
    final key = w['key'] as String;
    final value = scope?.values.containsKey(key) == true ? scope!.values[key] : w['value'];
    final mode = (w['f'] as Map?)?['mode'];
    void set(Object? v) => scope?.onChanged(key, v);
    final label = (w['label'] as String? ?? '').trim();
    final kind = w['kind'] as String?;

    Widget control;
    switch (kind) {
      case 'multiselect':
        control = _MultiSelect(w: w, value: ((value as List?) ?? const []).map((e) => '$e').toList(), onChanged: set);
        break;
      case 'selectbox':
      case 'radio':
        final opts = (w['options'] as List? ?? const []).cast<String>();
        final labels = (w['labels'] as List? ?? opts).cast<String>();
        control = DropdownButtonFormField<String>(
          isExpanded: true,
          initialValue: opts.contains(value) ? value as String : null,
          decoration: _deco(),
          items: [
            for (var i = 0; i < opts.length; i++)
              DropdownMenuItem(value: opts[i], child: Text(labels[i], overflow: TextOverflow.ellipsis))
          ],
          onChanged: set,
        );
        break;
      case 'checkbox':
      case 'toggle':
        final on = value == true;
        return InkWell(
          onTap: () => set(!on),
          child: Padding(
            padding: const EdgeInsets.only(top: 18),
            child: Row(children: [
              kind == 'toggle' ? Switch(value: on, onChanged: set) : Checkbox(value: on, onChanged: (v) => set(v == true)),
              Expanded(child: Text(label, style: const TextStyle(fontSize: 13))),
            ]),
          ),
        );
      case 'text_input':
      case 'text_area':
        control = _TextFilter(
            initial: (value as String?) ?? '', placeholder: w['placeholder'] as String? ?? '', onSubmit: set);
        break;
      case 'date_input':
        control = _DateRange(value: value, onChanged: set);
        break;
      default:
        control = const SizedBox.shrink();
    }
    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      if (label.isNotEmpty)
        Padding(
          padding: const EdgeInsets.only(bottom: 4),
          child: Text(label,
              style: const TextStyle(color: _labelColor, fontWeight: FontWeight.w700, fontSize: 12.5)),
        ),
      Opacity(opacity: mode == 'unsupported' ? 0.5 : 1, child: control),
    ]);
  }
}

InputDecoration _deco({String? hint}) => InputDecoration(
      isDense: true,
      hintText: hint,
      hintStyle: const TextStyle(fontSize: 13, color: Brand.muted),
      filled: true,
      fillColor: Colors.white,
      contentPadding: const EdgeInsets.symmetric(horizontal: 10, vertical: 10),
      border: OutlineInputBorder(borderRadius: BorderRadius.circular(6)),
    );

class _MultiSelect extends StatelessWidget {
  final Map<String, dynamic> w;
  final List<String> value;
  final ValueChanged<Object?> onChanged;
  const _MultiSelect({required this.w, required this.value, required this.onChanged});

  @override
  Widget build(BuildContext context) {
    final opts = (w['options'] as List? ?? const []).cast<String>();
    final labels = (w['labels'] as List? ?? opts).cast<String>();
    final lab = {for (var i = 0; i < opts.length && i < labels.length; i++) opts[i]: labels[i]};
    final placeholder = (w['placeholder'] as String?) ?? 'Choose options';
    return InkWell(
      borderRadius: BorderRadius.circular(6),
      onTap: () async {
        final r = await showModalBottomSheet<List<String>>(
          context: context,
          isScrollControlled: true,
          showDragHandle: true,
          builder: (_) => _MultiSheet(title: (w['label'] as String?) ?? '', opts: opts, labels: labels, initial: value),
        );
        if (r != null) onChanged(r);
      },
      child: InputDecorator(
        decoration: _deco().copyWith(suffixIcon: const Icon(Icons.arrow_drop_down)),
        child: value.isEmpty
            ? Text(placeholder, style: const TextStyle(fontSize: 13, color: Brand.muted), overflow: TextOverflow.ellipsis)
            : Wrap(spacing: 4, runSpacing: 4, children: [
                for (final v in value.take(6))
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                    decoration: BoxDecoration(color: const Color(0xFFFF4B4B), borderRadius: BorderRadius.circular(4)),
                    child: Text(lab[v] ?? v, style: const TextStyle(color: Colors.white, fontSize: 12)),
                  ),
                if (value.length > 6)
                  Text('+${value.length - 6}', style: const TextStyle(fontSize: 12, color: Brand.muted)),
              ]),
      ),
    );
  }
}

class _MultiSheet extends StatefulWidget {
  final String title;
  final List<String> opts, labels;
  final List<String> initial;
  const _MultiSheet({required this.title, required this.opts, required this.labels, required this.initial});

  @override
  State<_MultiSheet> createState() => _MultiSheetState();
}

class _MultiSheetState extends State<_MultiSheet> {
  late final List<String> _sel = [...widget.initial];
  String _q = '';

  @override
  Widget build(BuildContext context) {
    final q = fold(_q);
    final idx = [
      for (var i = 0; i < widget.opts.length; i++)
        if (q.isEmpty || fold(widget.labels[i]).contains(q)) i
    ];
    return SafeArea(
      child: Padding(
        padding: EdgeInsets.only(bottom: MediaQuery.of(context).viewInsets.bottom),
        child: ConstrainedBox(
          constraints: BoxConstraints(maxHeight: MediaQuery.of(context).size.height * 0.85),
          child: Column(mainAxisSize: MainAxisSize.min, children: [
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 0, 12, 6),
              child: Row(children: [
                Expanded(
                    child: Text(widget.title, style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w700))),
                TextButton(onPressed: () => setState(_sel.clear), child: const Text('Bỏ chọn')),
                FilledButton(onPressed: () => Navigator.pop(context, _sel), child: const Text('Xong')),
              ]),
            ),
            if (widget.opts.length > 8)
              Padding(
                padding: const EdgeInsets.fromLTRB(16, 0, 16, 6),
                child: TextField(
                  decoration: _deco(hint: 'Tìm...').copyWith(prefixIcon: const Icon(Icons.search, size: 20)),
                  onChanged: (t) => setState(() => _q = t),
                ),
              ),
            const Divider(height: 1),
            Flexible(
              child: ListView.builder(
                shrinkWrap: true,
                itemCount: idx.length,
                itemBuilder: (ctx, k) {
                  final i = idx[k];
                  final o = widget.opts[i];
                  return CheckboxListTile(
                    dense: true,
                    value: _sel.contains(o),
                    title: Text(widget.labels[i]),
                    onChanged: (v) => setState(() {
                      // giữ đúng thứ tự như danh sách gốc (giống multiselect của Streamlit)
                      if (v == true) {
                        _sel.add(o);
                        _sel.sort((a, b) => widget.opts.indexOf(a).compareTo(widget.opts.indexOf(b)));
                      } else {
                        _sel.remove(o);
                      }
                    }),
                  );
                },
              ),
            ),
          ]),
        ),
      ),
    );
  }
}

class _TextFilter extends StatefulWidget {
  final String initial, placeholder;
  final ValueChanged<Object?> onSubmit;
  const _TextFilter({required this.initial, required this.placeholder, required this.onSubmit});

  @override
  State<_TextFilter> createState() => _TextFilterState();
}

class _TextFilterState extends State<_TextFilter> {
  late final _c = TextEditingController(text: widget.initial);
  final _focus = FocusNode();

  @override
  void initState() {
    super.initState();
    // như Streamlit: áp dụng khi Enter hoặc rời ô
    _focus.addListener(() {
      if (!_focus.hasFocus) widget.onSubmit(_c.text);
    });
  }

  @override
  void didUpdateWidget(_TextFilter old) {
    super.didUpdateWidget(old);
    if (widget.initial != _c.text && !_focus.hasFocus) _c.text = widget.initial;
  }

  @override
  void dispose() {
    _c.dispose();
    _focus.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => TextField(
        controller: _c,
        focusNode: _focus,
        style: const TextStyle(fontSize: 13),
        decoration: _deco(hint: widget.placeholder),
        textInputAction: TextInputAction.search,
        onSubmitted: widget.onSubmit,
      );
}

class _DateRange extends StatelessWidget {
  final Object? value;
  final ValueChanged<Object?> onChanged;
  const _DateRange({required this.value, required this.onChanged});

  @override
  Widget build(BuildContext context) {
    final v = (value is List && (value as List).length == 2) ? (value as List).cast<String>() : null;
    String fmt(String iso) {
      final d = DateTime.parse(iso);
      return '${d.year}/${d.month.toString().padLeft(2, '0')}/${d.day.toString().padLeft(2, '0')}';
    }

    return InkWell(
      onTap: v == null
          ? null
          : () async {
              final lo = DateTime.parse(v[0]), hi = DateTime.parse(v[1]);
              final r = await showDateRangePicker(
                context: context,
                firstDate: DateTime(lo.year, lo.month, 1),
                lastDate: DateTime(hi.year, hi.month + 1, 0),
                initialDateRange: DateTimeRange(start: lo, end: hi),
              );
              if (r != null) {
                String iso(DateTime d) =>
                    '${d.year}-${d.month.toString().padLeft(2, '0')}-${d.day.toString().padLeft(2, '0')}';
                onChanged([iso(r.start), iso(r.end)]);
              }
            },
      child: InputDecorator(
        decoration: _deco().copyWith(suffixIcon: const Icon(Icons.date_range, size: 18)),
        child: Text(v == null ? '' : '${fmt(v[0])} – ${fmt(v[1])}', style: const TextStyle(fontSize: 13)),
      ),
    );
  }
}
