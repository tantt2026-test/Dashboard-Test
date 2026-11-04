"""Sale Sup 'Cả 2' (all): mỗi bảng tách theo team như khi xem riêng từng Sale Sup + 1 dòng Total chung.

  Bảng = dòng team Vy (+ dòng Tổng Vy) → dòng team Tân (+ dòng Tổng Tân) → dòng Tổng cả 2 team
  (lấy từ App.py chạy trên data ghép). Thẻ / biểu đồ / nhận xét giữ bản data ghép.

  python team_merge.py --tan _reports --vy _reports/t/vy --all _reports/t/all
      → ghi đè các file Tất cả ĐDKD của t/all (kpi/<Thang>/<CODE>/<ngày>.json + biến thể __wN)
        + turnover/<Thang>.json (thêm 'teams' để app chia nhóm)

Ghép lại nhiều lần không sao: bảng đã ghép có 'seg' → dòng Tổng chung = các dòng sau đoạn cuối.
"""
import argparse
import copy
import json
import os
import re

import filters_probe as fp

ALL_TOTAL = 'TOTAL 2 SALE SUP'
_DAY = re.compile(r'^\d{4}-\d{2}-\d{2}(__w\d+)?\.json$')


def _tables(items):
    return fp.tables(items)


def _grand_rows(t):
    """Dòng Tổng chung của bảng bản data ghép (bảng đã ghép: các dòng sau đoạn cuối)."""
    if t.get('seg'):
        return t['b'][t['seg'][-1]:]
    rows = fp.body_cells(t) if not fp.has_rowspan(t) else None
    if rows is None:
        return []
    stt = fp.col_names(t)[:1] == ['STT']
    # dòng Tổng: chữ TỔNG/Total, tô nền xanh đậm, hoặc ô STT '-' (vd '25 Nhân viên' của MCP VISIT)
    return [r for r, c in zip(t['b'], rows)
            if fp.is_total(c) or _navy(r) or (stt and c and c[0].strip() in ('-', '—'))]


def _navy(row):
    """Dòng tô nền xanh đậm cả dòng — app cũng coi là dòng Tổng."""
    return bool(row) and all((c.get('bg') or '').lower() == '#1a365d' for c in row)


def _team_rows(t):
    """Phần của 1 team (bảng có thể đã ghép ở lần trước → bỏ dòng Tổng chung)."""
    if t.get('seg'):
        return t['b'][:t['seg'][0]]
    return t['b']


def _relabel(rows):
    out = copy.deepcopy(rows)
    for r in out:
        for c in r[:3]:
            x = (c.get('x') or '').strip()
            u = x.upper()
            if u.endswith(' TOTAL') or u.startswith('TOTAL'):
                c['x'] = ALL_TOTAL
                break
            if u.startswith('TỔNG'):
                c['x'] = 'TỔNG CỘNG 2 SALE SUP'
                break
    return out


def _label_row(text, ncol):
    return [{'x': text, 'cs': ncol, 'b': 1, 'al': 'l', 'bg': '#e2e8f0', 'fg': '#1a365d'}]


def merge_table(tt, tv, ta, labels=None):
    """None nếu 3 bảng không cùng cột (giữ bảng data ghép)."""
    names = fp.col_names(ta)
    if fp.col_names(tt) != names or fp.col_names(tv) != names:
        return None
    a, b = _team_rows(tt), _team_rows(tv)
    if labels and not _grand_rows(tt) and not _grand_rows(tv) and not fp.has_rowspan(ta):
        # bảng không có dòng Tổng (vd bảng chỉ số LPPC) → dòng tên Sale Sup đầu phần mỗi team
        a = [_label_row(labels[0], len(names))] + a
        b = [_label_row(labels[1], len(names))] + b
    g = _relabel(_grand_rows(ta))
    out = dict(ta)
    # Vy trước, Tân sau (theo mẫu); app tính lại dòng Tổng từng đoạn khi lọc dòng
    out['b'] = copy.deepcopy(b) + copy.deepcopy(a) + g
    out['seg'] = [len(b), len(b) + len(a)]
    out.pop('_before', None)
    out.pop('_after', None)
    return out


def _widgets(items):
    for it in fp._walk(items):
        if it['t'] == 'filters':
            yield from it['w']


def _merge_masks(wa, wt, wv, tmap):
    """Ô lọc kiểu 'select' (mặt nạ dòng theo từng lựa chọn): dòng giữ = dòng giữ của Tân ∪ Vy."""
    fa = wa.get('f') or {}
    if fa.get('mode') != 'select' or not isinstance(fa.get('masks'), dict):
        return
    mt = ((wt or {}).get('f') or {}).get('masks') or {}
    mv = ((wv or {}).get('f') or {}).get('masks') or {}
    for val, m in fa['masks'].items():
        rows = m.get('rows')
        if not isinstance(rows, list):
            continue
        for ti, merged in tmap.items():
            if ti >= len(rows):
                continue
            keep = []
            for src in (mt.get(val), mv.get(val)):
                r = (src or {}).get('rows') or []
                if ti < len(r) and r[ti]:
                    keep += r[ti]
            if rows[ti] is None and not keep:
                continue
            rows[ti] = sorted(set(keep))


def team_label(items, default):
    """Tên Sale Sup của 1 bản: dòng Tổng 'SS … Total' đầu tiên."""
    for t in _tables(items):
        if fp.has_rowspan(t):
            continue
        for c in fp.body_cells(t):
            for x in c[:3]:
                x = (x or '').strip()
                if x.upper().endswith(' TOTAL') and x.upper().startswith('SS '):
                    return x[:-6].strip()
    return default


def merge_items(tan, vy, al, labels=None):
    """Gộp nội dung (list item) của 3 bản. tan/vy None → giữ bản data ghép.
    labels: tên 2 Sale Sup (dòng tên đầu phần mỗi team ở bảng không có dòng Tổng)."""
    out = copy.deepcopy(al)
    if tan is None or vy is None:
        return out
    labels = labels or (team_label(tan, 'Team Tân'), team_label(vy, 'Team Vy'))
    ta, tt, tv = _tables(out), _tables(tan), _tables(vy)
    if not (len(ta) == len(tt) == len(tv)):
        return out
    tmap = {}
    for i, (a, t, v) in enumerate(zip(ta, tt, tv)):
        m = merge_table(t, v, a, labels)
        if m is None:
            continue
        a.clear()
        a.update(m)
        tmap[i] = a
    if tmap:
        wt = {w.get('key'): w for w in _widgets(tan)}
        wv = {w.get('key'): w for w in _widgets(vy)}
        for w in _widgets(out):
            _merge_masks(w, wt.get(w.get('key')), wv.get(w.get('key')), tmap)
    return out


def _load(p):
    try:
        with open(p, encoding='utf-8') as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


def _variant_files(doc):
    """{(ô lọc, giá trị): tên file biến thể} của 1 bản."""
    out = {}
    for w in _widgets(doc.get('items') or []):
        for val, fn in ((w.get('f') or {}).get('variants') or {}).items():
            out[(w.get('key'), val)] = fn
    return out


def merge_report_dir(dt, dv, da, labels=None):
    """1 thư mục báo cáo (kpi/<Thang>/<CODE>): ghép file Tất cả ĐDKD + biến thể của nó."""
    n = 0
    for fn in sorted(os.listdir(da)):
        if not re.match(r'^\d{4}-\d{2}-\d{2}\.json$', fn):
            continue
        pa = os.path.join(da, fn)
        A, T, V = _load(pa), _load(os.path.join(dt, fn)), _load(os.path.join(dv, fn))
        if A is None or T is None or V is None:
            continue
        pairs = [(fn, fn, fn)]
        vt, vv = _variant_files(T), _variant_files(V)
        for k, f in _variant_files(A).items():
            if k in vt and k in vv:
                pairs.append((f, vt[k], vv[k]))
        for fa, ft, fv in pairs:
            A2 = A if fa == fn else _load(os.path.join(da, fa))
            T2 = T if ft == fn else _load(os.path.join(dt, ft))
            V2 = V if fv == fn else _load(os.path.join(dv, fv))
            if A2 is None or T2 is None or V2 is None:
                continue
            A2['items'] = merge_items(T2.get('items') or [], V2.get('items') or [], A2.get('items') or [],
                                      labels)
            with open(os.path.join(da, fa), 'w', encoding='utf-8') as fh:
                json.dump(A2, fh, ensure_ascii=False, separators=(',', ':'))
            n += 1
    return n


def merge_turnover(pt, pv, pa):
    """Turnover: app tự dựng bảng từ số từng NV → chỉ cần biết NV thuộc team nào + tên dòng Tổng team."""
    T, V, A = _load(pt), _load(pv), _load(pa)
    if T is None or V is None or A is None:
        return False
    A['teams'] = [  # Vy trước, Tân sau (giống bảng báo cáo)
        {'label': V.get('total_label') or 'Team Vy', 'nv': V.get('nv') or []},
        {'label': T.get('total_label') or 'Team Tân', 'nv': T.get('nv') or []},
    ]
    A['total_label'] = ALL_TOTAL
    with open(pa, 'w', encoding='utf-8') as fh:
        json.dump(A, fh, ensure_ascii=False, separators=(',', ':'))
    return True


def _label_of(team_dir):
    """Tên Sale Sup từ Turnover của team ('SS Trương Thanh Tân Total' → 'SS Trương Thanh Tân')."""
    tdir = os.path.join(team_dir, 'turnover')
    for fn in sorted(os.listdir(tdir), reverse=True) if os.path.isdir(tdir) else []:
        lab = ((_load(os.path.join(tdir, fn)) or {}).get('total_label') or '').strip()
        if lab:
            return re.sub(r'\s+total$', '', lab, flags=re.I)
    return None


def merge_tree(tan, vy, al):
    n = 0
    lt, lv = _label_of(tan), _label_of(vy)
    labels = (lt, lv) if lt and lv else None
    kpi = os.path.join(al, 'kpi')
    for mk in sorted(os.listdir(kpi)) if os.path.isdir(kpi) else []:
        for code in sorted(os.listdir(os.path.join(kpi, mk))):
            da = os.path.join(kpi, mk, code)
            dt, dv = os.path.join(tan, 'kpi', mk, code), os.path.join(vy, 'kpi', mk, code)
            if os.path.isdir(da) and os.path.isdir(dt) and os.path.isdir(dv):
                n += merge_report_dir(dt, dv, da, labels)
    tdir = os.path.join(al, 'turnover')
    for fn in sorted(os.listdir(tdir)) if os.path.isdir(tdir) else []:
        if fn.endswith('.json'):
            merge_turnover(os.path.join(tan, 'turnover', fn), os.path.join(vy, 'turnover', fn),
                           os.path.join(tdir, fn))
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tan', required=True)
    ap.add_argument('--vy', required=True)
    ap.add_argument('--all', required=True)
    a = ap.parse_args()
    n = merge_tree(a.tan, a.vy, a.all)
    print(f'Cả 2 Sale Sup: tách bảng theo team ({n} file)')


if __name__ == '__main__':
    main()
