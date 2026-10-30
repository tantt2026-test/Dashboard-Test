"""Tự tìm hiểu từng ô lọc của App.py bằng cách chạy thử, để app làm y hệt Streamlit.

Với mỗi ô lọc (sau thanh tab + các ô chung Thứ VT / Mã KH / Tên KH), chạy App.py với
vài giá trị rồi so với bản mặc định:
  select  : mỗi lựa chọn chỉ GIỮ LẠI một phần dòng/cột/thẻ/hạng mục biểu đồ, số không đổi
            → lưu "mặt nạ" từng lựa chọn; nhiều lựa chọn = hợp (đã kiểm chứng)
  eq      : danh sách lựa chọn quá dài → lọc dòng theo 1 cột (giá trị bằng)
  contains: ô gõ chữ → dòng có cột chứa chữ (nhiều giá trị cách nhau dấu phẩy = hoặc)
  date    : ô chọn khoảng ngày → cột ngày nằm trong khoảng
  calc    : số bị TÍNH LẠI → xuất sẵn bản App.py cho từng giá trị (chọn 1 giá trị)
  none    : không đổi gì ở bảng (vd chỉ đổi URL)
Kết quả gắn vào item widget ('f') và doc['main'] (ô chung đầu trang).
"""
import json
import re
import zlib

import report_doc

MAX_SELECT_OPTS = 60    # thử từng lựa chọn nếu danh sách ≤ ngưỡng này
MAX_CALC_OPTS = 40      # xuất sẵn bản tính lại cho từng lựa chọn nếu ≤ ngưỡng này
PROBE_BUDGET_S = 240    # mỗi màn hình đo tối đa ~4 phút; quá thì suy ra từ dữ liệu (guess)
MAIN_KEYS = ('mbs_cat_thu_filter', 'filter_ma_kh', 'filter_ten_kh')


def is_total(cells):
    """Dòng Tổng: 1 trong 3 ô đầu BẮT ĐẦU bằng TỔNG/TOTAL hoặc KẾT THÚC bằng 'Total'
    (vd "TỔNG CỘNG", "SS Trương Thanh Tân Total") — KHÔNG phải tên CH "Cửa Hàng Tổng Hợp"."""
    for c in list(cells)[:3]:
        x = (c or '').strip().upper()
        if x.startswith('TỔNG') or x.startswith('TOTAL') or x.endswith(' TOTAL'):
            return True
    return False


def rkey(cells):
    """Mã dòng: hash các ô (bỏ cột STT) — app tính lại y hệt (FNV-1a 32 bit)."""
    s = '␟'.join(cells)
    h = 0x811c9dc5
    for b in s.encode('utf-8'):
        h ^= b
        h = (h * 0x01000193) & 0xffffffff
    return '%08x' % h


def _walk(items):
    for it in items:
        yield it
        if it['t'] == 'box':
            yield from _walk(it['ch'])


def tables(items):
    return [it for it in _walk(items) if it['t'] == 'tbl']


def col_names(t):
    """Tên cột = đường dẫn tiêu đề "Nhóm › Cột" (giống TableModel.colNames bên app),
    tính theo colspan/rowspan — để phân biệt các cột trùng tên ở nhóm khác nhau."""
    occ, grid = {}, {}
    nrows = len(t['h'])
    for r, row in enumerate(t['h']):
        c = 0
        for cell in row:
            while c in occ.get(r, ()):
                c += 1
            cs, rs = int(cell.get('cs', 1)), int(cell.get('rs', 1))
            for i in range(rs):
                for j in range(cs):
                    occ.setdefault(r + i, set()).add(c + j)
                    if r + i < nrows:
                        grid[(r + i, c + j)] = cell['x'].replace('\n', ' ').strip()
            c += cs
    ncols = max((c for (_, c) in grid), default=-1) + 1
    out = []
    for c in range(ncols):
        parts = []
        for r in range(nrows):
            x = grid.get((r, c), '')
            if x and (not parts or parts[-1] != x):
                parts.append(x)
        out.append(' › '.join(parts) if parts else f'Cột {c + 1}')
    return out


def _sig(t):
    return tuple(col_names(t))


def align(d, v):
    """Ghép bảng của bản thử với bản mặc định theo tiêu đề (App.py có thể ẩn bảng rỗng).
    → list chỉ số bảng v cho từng bảng d (None = bảng bị ẩn)."""
    out, j = [], 0
    vs = [_sig(t) for t in v.tbls]
    for t in d.tbls:
        sig = _sig(t)
        k = next((i for i in range(j, len(vs)) if vs[i] == sig), None)
        if k is None:
            # bảng giữ nguyên vị trí nhưng bớt cột (ẩn cột) → khớp theo tập con tên cột
            k = next((i for i in range(j, len(vs)) if set(vs[i]) < set(sig) and len(vs[i]) > 1), None)
        out.append(k)
        if k is not None:
            j = k + 1
    return out


def body_cells(t):
    """Mỗi dòng body → list chữ theo vị trí cột (bỏ qua bảng có rowspan ở body)."""
    out = []
    for row in t['b']:
        cells, c = {}, 0
        for cell in row:
            cells[c] = cell['x'].replace('\n', ' ')
            c += int(cell.get('cs', 1))
        out.append([cells.get(i, '') for i in range(max(cells) + 1 if cells else 0)])
    return out


def has_rowspan(t):
    return any(int(c.get('rs', 1)) > 1 for r in t['b'] for c in r)


def row_keys(t):
    names = col_names(t)
    skip = {i for i, n in enumerate(names) if n.strip().upper() == 'STT'}
    return [rkey([v for i, v in enumerate(r) if i not in skip]) for r in body_cells(t)]


def cards(items):
    return [c['l'] for it in _walk(items) if it['t'] == 'cards' for c in it['it']]


def chart_cats(items):
    out = []
    for it in _walk(items):
        if it['t'] == 'bar':
            tr = it['tr'][0]
            out.append([str(x) for x in (tr['y'] if tr.get('h') else tr['x'])])
        elif it['t'] == 'pie':
            out.append([str(x) for x in it['tr'][0]['labels']])
    return out


def _other_sig(items):
    """[(chỉ số item, chữ ký)] cho phần không phải bảng/thẻ/biểu đồ/ô lọc. Số được thay bằng #
    (dòng chú thích kiểu "Tổng 619 dòng" đổi số theo bộ lọc — app tự đếm lại)."""
    sig = []
    for idx, it in enumerate(_walk(items)):
        if it['t'] in ('tbl', 'cards', 'bar', 'pie', 'filters', 'box'):
            continue
        if it['t'] == 'p':
            txt = ''.join(r['x'] for r in it['r'])
        elif it['t'] in ('h', 'msg'):
            txt = json.dumps(it, ensure_ascii=False, sort_keys=True)
        else:
            continue
        sig.append((idx, re.sub(r'\d[\d.,]*', '#', txt)))
    return sig


def _hidden_others(d_other, v_other):
    """v là dãy con của d (chỉ bớt mục)? → chỉ số các mục bị ẩn, hoặc None.
    Thông báo "Không có ... phù hợp" khi bảng rỗng không tính là khác (app tự báo bảng rỗng)."""
    hidden, j = [], 0
    vs = [s for _, s in v_other if not re.search(r'"t": "msg".*(Không có|không có)', s)]
    for idx, sg in d_other:
        if j < len(vs) and vs[j] == sg:
            j += 1
        else:
            hidden.append(idx)
    return hidden if j == len(vs) else None


def _strip_filters(items):
    return [it for it in items if it['t'] != 'filters']


class Snapshot:
    def __init__(self, items):
        self.items = items
        self.tbls = tables(items)
        self.cols = [col_names(t) for t in self.tbls]
        self.rows = [row_keys(t) for t in self.tbls]
        # giá trị từng dòng (theo mã dòng) để biết số có bị tính lại không
        self.vals = [{k: json.dumps(t['b'][i], ensure_ascii=False, sort_keys=True)
                      for i, k in enumerate(ks)} for t, ks in zip(self.tbls, self.rows)]
        self.cards = cards(items)
        self.cats = chart_cats(items)
        self.other = _other_sig(items)
        self.tbl_idx = [i for i, it in enumerate(_walk(items)) if it['t'] == 'tbl']
        self.plain = json.dumps(_strip_filters(items), ensure_ascii=False, sort_keys=True)


WHY = []


def _subset_hit(label, unsel):
    s = str(label).strip()
    return any(s == o or s.startswith(o + ' ') or s.startswith(o + '(') for o in unsel)


def _place(rows):
    """Vị trí cột của từng ô (tính rowspan/colspan) → [[(c0, c1), ...] theo dòng]."""
    occ, out = {}, []
    for r, row in enumerate(rows):
        c, pos = 0, []
        for cell in row:
            while occ.get((r, c)):
                c += 1
            cs, rs = int(cell.get('cs') or 1), int(cell.get('rs') or 1)
            for dr in range(rs):
                for dc in range(cs):
                    occ[(r + dr, c + dc)] = True
            pos.append((c, c + cs))
            c += cs
        out.append(pos)
    return out


def _plain(items):
    def clean(x):
        if isinstance(x, dict):
            return {k: clean(v) for k, v in x.items() if k != 'tot'}
        if isinstance(x, list):
            return [clean(v) for v in x]
        return x
    return json.dumps(clean(items), ensure_ascii=False, sort_keys=True)


def apply_subset(items, opts, sel):
    """Ô 'chọn chỉ số hiển thị' (mode subset): bỏ thẻ / nhóm cột bảng / cột biểu đồ của chỉ số
    không chọn. Chọn rỗng = tất cả (như App.py). Dart: filter_engine.dart applySubset."""
    unsel = [o for o in opts if o not in set(sel)]
    if not sel or not unsel:
        return items
    out = []
    for it in items:
        t = it.get('t')
        if t == 'cards':
            it = {**it, 'it': [c for c in it['it'] if not _subset_hit(c.get('l'), unsel)]}
            if not it['it']:
                continue
        elif t == 'tbl' and it.get('h'):
            ph = _place(it['h'])
            drop = set()
            for row, pos in zip(it['h'], ph):
                for cell, (c0, c1) in zip(row, pos):
                    if row is it['h'][0] and _subset_hit(cell.get('x', ''), unsel):
                        drop.update(range(c0, c1))
            if drop:
                def cut(rows):
                    res = []
                    for row, pos in zip(rows, _place(rows)):
                        nr = []
                        for cell, (c0, c1) in zip(row, pos):
                            keep = sum(1 for c in range(c0, c1) if c not in drop)
                            if keep == 0:
                                continue
                            if keep != c1 - c0:
                                cell = {**cell, 'cs': keep}
                            nr.append(cell)
                        res.append(nr)
                    return res
                ncol = max((p[-1][1] for p in ph if p), default=0)
                remap = {}
                for c in range(ncol):
                    if c not in drop:
                        remap[c] = len(remap)
                it = {**it, 'h': cut(it['h']), 'b': cut(it['b'])}
                if it.get('tot'):
                    tot = {}
                    for k, f in it['tot'].items():
                        refs = [int(k)] + [f[x] for x in ('a', 'b') if x in f]
                        if all(r in remap for r in refs):
                            f = dict(f)
                            for x in ('a', 'b'):
                                if x in f:
                                    f[x] = remap[f[x]]
                            tot[str(remap[int(k)])] = f
                    it['tot'] = tot
        elif t == 'bar':
            trs = []
            for tr in it['tr']:
                cats = tr.get('y') if tr.get('h') else tr.get('x')
                if isinstance(cats, list):
                    n = len(cats)
                    keep = [i for i, c in enumerate(cats) if not _subset_hit(c, unsel)]
                    # màu theo vị trí cột (bảng màu lặp lại từ đầu) → giữ màu đầu danh sách
                    tr = {k: ((v[:len(keep)] if k == 'color' else [v[i] for i in keep])
                              if isinstance(v, list) and len(v) == n else v) for k, v in tr.items()}
                trs.append(tr)
            it = {**it, 'tr': trs}
        elif t == 'box':
            it = {**it, 'ch': apply_subset(it['ch'], opts, sel)}
        out.append(it)
    return out


def _no(reason):
    WHY.append(reason)
    return None


def _subselection(d: Snapshot, v: Snapshot):
    """v có phải chỉ là phần giữ lại của d (không tính lại số)? → mặt nạ hoặc None."""
    hidden = _hidden_others(d.other, v.other)
    if hidden is None or len(v.cats) > len(d.cats):
        return _no('other/cats')
    al = align(d, v)
    if sum(1 for x in al if x is not None) != len(v.tbls):
        return _no('bảng mới')  # có bảng mới / lạ → không phải chọn bớt
    mask = {'rows': [], 'cols': [], 'cards': None, 'cats': [], 'hide': hidden}
    for ti, vi in enumerate(al):
        dc = d.cols[ti]
        if vi is None:  # bảng bị ẩn vì rỗng
            mask['rows'].append([])
            mask['cols'].append(None)
            continue
        vc = v.cols[vi]
        dt_, vt_ = d.tbls[ti], v.tbls[vi]
        if vc != dc:
            if not set(vc) <= set(dc):
                return _no('cột lạ')
            mask['cols'].append(vc)
            dmap = [dict(zip(dc, r)) for r in body_cells(dt_)]
            vmap = [dict(zip(vc, r)) for r in body_cells(vt_)]
            if len(dmap) != len(vmap) or any(
                    {c: a.get(c) for c in vc if c.upper() != 'STT'} != {c: b.get(c) for c in vc if c.upper() != 'STT'}
                    for a, b in zip(dmap, vmap)):
                return _no('giá trị cột')
            mask['rows'].append(None)
            continue
        mask['cols'].append(None)
        if v.rows[vi] == d.rows[ti]:
            mask['rows'].append(None)
            continue
        if not set(v.rows[vi]) <= set(d.rows[ti]):
            # dòng Tổng tính lại cho phần đã lọc → bỏ qua dòng tổng khi so
            extra = set(v.rows[vi]) - set(d.rows[ti])
            vcells = body_cells(vt_)
            if any(not is_total(vcells[v.rows[vi].index(k)]) for k in extra):
                return _no('dòng mới')
        mask['rows'].append(sorted(set(v.rows[vi]) & set(d.rows[ti])))
    if v.cards != d.cards:
        if not set(v.cards) <= set(d.cards):
            return _no('thẻ lạ')
        mask['cards'] = v.cards
    if len(v.cats) < len(d.cats):
        return _no('biểu đồ ẩn')  # biểu đồ bị ẩn cả cái: chưa hỗ trợ ghép
    for ci in range(len(d.cats)):
        if v.cats[ci] != d.cats[ci]:
            if not set(v.cats[ci]) <= set(d.cats[ci]):
                return _no('hạng mục lạ')
            mask['cats'].append(v.cats[ci])
        else:
            mask['cats'].append(None)
    return mask


def _union(masks):
    out = {'rows': [], 'cols': [], 'cards': None, 'cats': []}
    n = len(masks[0]['rows'])
    for ti in range(n):
        rs = [m['rows'][ti] for m in masks]
        out['rows'].append(None if any(r is None for r in rs) else sorted(set().union(*rs)))
        cs = [m['cols'][ti] for m in masks]
        out['cols'].append(None if any(c is None for c in cs) else sorted(set().union(*cs)))
    cds = [m['cards'] for m in masks]
    out['cards'] = None if any(c is None for c in cds) else sorted(set().union(*cds))
    for ci in range(len(masks[0]['cats'])):
        cs = [m['cats'][ci] for m in masks]
        out['cats'].append(None if any(c is None for c in cs) else sorted(set().union(*cs)))
    out['hide'] = sorted(set.intersection(*[set(m.get('hide') or []) for m in masks]))
    return out


def _same_mask(a, b):
    """So 2 mặt nạ không tính thứ tự (thẻ/hạng mục/dòng/cột là tập hợp)."""
    def norm(x):
        if isinstance(x, list):
            items = [norm(y) for y in x]
            if all(isinstance(y, str) for y in items):
                return sorted(items)
            return items
        if isinstance(x, dict):
            return {k: norm(v) for k, v in x.items()}
        return x
    return json.dumps(norm(a), sort_keys=True) == json.dumps(norm(b), sort_keys=True)


def _find_col(d: Snapshot, v: Snapshot, pred):
    """Tìm các (bảng, cột) mà dòng giữ lại của v == các dòng của d thoả pred(giá trị ô)."""
    found = []
    al = align(d, v)
    for ti, t in enumerate(d.tbls):
        vi = al[ti]
        kept = set(v.rows[vi]) if vi is not None else set()
        if (vi is not None and v.rows[vi] == d.rows[ti]) or has_rowspan(t):
            continue
        cells = body_cells(t)
        nontotal_keep = {k for k in kept if k in set(d.rows[ti]) and not _is_total_key(d, ti, k)}
        for ci, name in enumerate(d.cols[ti]):
            want = {d.rows[ti][ri] for ri, r in enumerate(cells)
                    if ci < len(r) and pred(r[ci]) and not is_total(r)}
            # chỉ tin lần thử CÓ dữ liệu: 0 dòng thì cột nào cũng "khớp" (đo nhầm)
            if want and want == nontotal_keep:
                found.append((ti, name))
                break
    return found


def _only_targets_changed(d, v, targets):
    """Ngoài các bảng bị lọc, mọi thứ khác (bảng khác, thẻ, biểu đồ, chữ) có giữ nguyên không?
    Nếu App.py tính lại bảng tổng hợp → không phải lọc dòng thuần."""
    if v.cards != d.cards or v.cats != d.cats or _hidden_others(d.other, v.other) is None:
        return False
    tset = {t for t, _ in targets}
    al = align(d, v)
    for ti, vi in enumerate(al):
        if ti in tset:
            continue
        if vi is None or v.rows[vi] != d.rows[ti] or v.cols[vi] != d.cols[ti]:
            return False
    return True


def _is_total_key(d, ti, k):
    try:
        i = d.rows[ti].index(k)
    except ValueError:
        return False
    return is_total(body_cells(d.tbls[ti])[i])


class _Budget(Exception):
    pass


class Prober:
    def __init__(self, app, base_state, log=lambda m: None):
        import time
        self.app = app
        self.base = dict(base_state)
        self.log = log
        self.t0 = time.time()

    def over_budget(self):
        import time
        return time.time() - self.t0 > PROBE_BUDGET_S

    def guess(self, w, default):
        """Hết thời gian đo (màn hình nặng như MCP VISIT): suy cách lọc từ dữ liệu, không chạy App.py.
        Kết quả được parity_filters.py kiểm chứng lại bằng App.py."""
        kind, opts = w['kind'], [str(o).strip() for o in (w.get('options') or [])]
        if kind == 'multiselect' and opts:
            best = None
            for ti, t in enumerate(default.tbls):
                if has_rowspan(t):
                    continue
                cells = body_cells(t)
                for ci, name in enumerate(default.cols[ti]):
                    vals = {r[ci].strip() for r in cells if ci < len(r) and r[ci].strip()}
                    if not vals:
                        continue
                    cover = len(vals & set(opts)) / len(vals)
                    if cover >= 0.95 and len(vals & set(opts)) >= min(2, len(opts)) and (best is None or cover > best[0]):
                        best = (cover, ti, name)
            if best:
                return {'mode': 'partial', 'inner': {'mode': 'eq', 'targets': [{'t': best[1], 'col': best[2]}]}, 'guess': True}
            # ô chọn cột: bảng có tập tên cột giống danh sách lựa chọn nhất (Jaccard)
            so = set(opts)
            scored = []
            for ti, names in enumerate(default.cols):
                sh = {n.split(' › ')[-1] for n in names}
                inter = len(so & sh)
                if inter >= max(2, len(opts) * 0.8):
                    scored.append((inter / len(so | sh), ti, sh))
            if scored:
                _, ti, sh = max(scored)
                fixed = sorted(sh - so)
                return {'mode': 'cols', 'targets': [ti], 'always': fixed, 'guess': True}
        if kind in ('text_input', 'text_area'):
            lab = (w.get('label') or '') + ' ' + (w.get('placeholder') or '')
            want = 'ma' if re.search(r'mã|ma kh|code', lab, re.I) else 'ten'
            for ti, names in enumerate(default.cols):
                for n in names:
                    nl = n.lower()
                    if (want == 'ma' and re.search(r'outlet_code|outlet code|mã kh|mã ch', nl)) or \
                            (want == 'ten' and re.search(r'outlet_name|outlet name|tên kh|tên ch', nl)):
                        return {'mode': 'partial', 'inner': {'mode': 'contains', 'multi': False, 'targets': [{'t': ti, 'col': n}]}, 'guess': True}
        return {'mode': 'unsupported', 'err': 'quá thời gian đo'}

    def snap(self, extra):
        if self.over_budget():
            raise _Budget()
        blocks, _ns, status = self.app.run({**self.base, **extra})
        if status.startswith('error'):
            raise RuntimeError(status)
        return Snapshot(report_doc.convert(blocks)), blocks

    def probe(self, w, default: Snapshot, variant_cb):
        """→ spec dict cho widget w (item 't':'w')."""
        key, kind = w['key'], w['kind']
        dflt = w.get('value')
        opts = w.get('options') or []
        if self.over_budget():
            return self.guess(w, default)
        try:
            return self._probe(w, default, variant_cb)
        except _Budget:
            return self.guess(w, default)
        finally:
            # trả ô lọc về mặc định (xoá khỏi session → App.py dùng giá trị mặc định của nó)
            self.app.rec.session_state.pop(key, None)

    def _probe(self, w, default, variant_cb):
        key, kind = w['key'], w['kind']
        dflt = w.get('value')
        opts = w.get('options') or []
        if True:
            if kind == 'multiselect':
                return self._multi(w, default, variant_cb)
            if kind in ('selectbox', 'radio'):
                R = dict(zip(opts, w.get('_raw_options') or opts))
                return self._calc_each(w, opts, lambda o: R[o], variant_cb, default)
            if kind in ('checkbox', 'toggle'):
                return self._calc_each(w, [not bool(dflt)], lambda o: o, variant_cb, default, raw=True)
            if kind in ('text_input', 'text_area'):
                return self._text(w, default)
            if kind == 'date_input':
                return self._date(w, default)
        return {'mode': 'none'}

    def _multi(self, w, default, variant_cb):
        key = w['key']
        sopts = w.get('options') or []
        raw = w.get('_raw_options') or sopts
        R = dict(zip(sopts, raw))          # chữ (JSON) → giá trị gốc (chạy App.py)
        opts = sopts
        dflt = w.get('value') or []
        if not opts:
            return {'mode': 'none'}
        # thử nhanh: 2 lựa chọn mà nội dung không đổi → ô này không ảnh hưởng báo cáo này
        same = 0
        for o in opts[:1] + opts[-1:]:
            v, _ = self.snap({key: [R[o]]})
            if v.plain == default.plain:
                same += 1
        if same == min(2, len(opts)) and not dflt:
            return {'mode': 'none'}
        # Ô chọn chỉ số hiển thị (mặc định chọn hết): chỉ bỏ thẻ / nhóm cột / cột biểu đồ
        sub = self._subset(w, default, R)
        if sub:
            return sub
        # Ô ẩn/hiện cột (lựa chọn = tên cột): chọn 1 cột → bảng còn cột đó + các cột cố định
        cols_spec = self._cols(w, default, R)
        if cols_spec:
            return cols_spec
        # Nhiều lựa chọn: thử kiểu "lọc theo giá trị 1 cột" trước (2 lần chạy thay vì N lần)
        if len(opts) > 12:
            eq = self._eq(w, default, R)
            if eq:
                return eq
        if len(opts) <= MAX_SELECT_OPTS:
            masks, ok = {}, True
            for o in opts:
                v, _ = self.snap({key: [R[o]]})
                m = _subselection(default, v)
                if m is None:
                    ok = False
                    break
                masks[o] = m
            if ok:
                # kiểm chứng "chọn nhiều = hợp" bằng 1 tổ hợp 2 lựa chọn
                if len(opts) >= 2:
                    pair = [opts[0], opts[-1]]
                    v, _ = self.snap({key: [R[o] for o in pair]})
                    m = _subselection(default, v)
                    if m is None or not _same_mask(m, _union([masks[o] for o in pair])):
                        ok = False
                if ok:
                    return {'mode': 'select', 'masks': masks}
            # không phải chọn bớt → tính lại
            return self._calc_each(w, opts, lambda o: [R[o]], variant_cb, default)
        return self._eq(w, default, R) or {'mode': 'unsupported'}

    def _eq(self, w, default, R):
        """Lọc dòng theo 1 cột bằng giá trị chọn; kiểm chứng bằng 2 giá trị + 1 cặp (hợp)."""
        key, opts = w['key'], w.get('options') or []
        labels = w.get('labels') or opts
        targets = None
        pure = True
        for idx in sorted({0, len(opts) // 2, len(opts) - 1}):
            o, lab = opts[idx], labels[idx]
            v, _ = self.snap({key: [R[o]]})
            found = _find_col(default, v, lambda x, o=o, lab=lab: x.strip() in (str(o).strip(), str(lab).strip()))
            if not found:
                return None
            if targets is None:
                targets = found
            elif sorted(found) != sorted(targets):
                return None
            if not _only_targets_changed(default, v, found):
                pure = False
        if not targets:
            return None
        spec = {'mode': 'eq', 'targets': [{'t': ti, 'col': c} for ti, c in targets]}
        return spec if pure else {'mode': 'partial', 'inner': spec}

    def _subset(self, w, default, R):
        """Mặc định chọn hết; chọn bớt → App.py chỉ bỏ phần của chỉ số không chọn (kiểm chứng 3 tổ hợp)."""
        key, opts = w['key'], w.get('options') or []
        if len(opts) < 2 or set(w.get('value') or []) != set(opts):
            return None
        tests = [[opts[0]], [opts[-1]], [o for i, o in enumerate(opts) if i % 2]]
        base = _strip_filters(default.items)
        for sel in tests:
            v, _ = self.snap({key: [R[o] for o in sel]})
            if _plain(apply_subset(base, opts, sel)) != _plain(_strip_filters(v.items)):
                return None
        return {'mode': 'subset'}

    def _cols(self, w, default, R):
        """Ô chọn cột hiển thị: lựa chọn trùng tên cột bảng; chọn 1 cột → còn cột đó + cột cố định."""
        key, opts = w['key'], w.get('options') or []
        for ti, names in enumerate(default.cols):
            short = [n.split(' › ')[-1] for n in names]
            if len(set(opts) & set(short)) < max(2, len(opts) * 0.8):
                continue
            always = None
            for o in (opts[0], opts[-1]):
                v, _ = self.snap({key: [R[o]]})
                al = align(default, v)
                vi = al[ti] if ti < len(al) else None
                if vi is None or v.rows[vi] != default.rows[ti] and len(v.rows[vi]) != len(default.rows[ti]):
                    return None
                vc = [n.split(' › ')[-1] for n in v.cols[vi]]
                if o not in vc:
                    return None
                rest = set(vc) - {o}
                if always is None:
                    always = rest
                elif rest != always:
                    return None
            return {'mode': 'cols', 'targets': [ti], 'always': sorted(always or [])}
        return None

    def _calc_each(self, w, values, to_state, variant_cb, default, raw=False):
        key = w['key']
        values = list(values)[:MAX_CALC_OPTS]
        variants = {}
        changed = False
        for o in values:
            v, blocks = self.snap({key: to_state(o)})
            if v.plain != default.plain:
                changed = True
            variants[json.dumps(o if raw else o, ensure_ascii=False)] = variant_cb(key, o, v.items)
        if w['kind'] == 'multiselect':
            v, blocks = self.snap({key: []})
            variants['[]'] = variant_cb(key, '__empty__', v.items)
        if not changed:
            return {'mode': 'none'}
        return {'mode': 'calc', 'variants': variants}

    def _text(self, w, default):
        """Ô gõ chữ: tìm cột lọc (chứa chữ, không phân biệt hoa thường) bằng nhiều giá trị mẫu,
        rồi kiểm tra gõ 2 giá trị cách dấu phẩy là 'hoặc' hay là nguyên chuỗi."""
        key = w['key']
        lab = (w.get('label') or '') + ' ' + (w.get('placeholder') or '')
        want = 'ma' if re.search(r'mã|ma kh|code', lab, re.I) else 'ten'
        safe = re.compile(r'^[\w\s/.-]+$')  # tránh ký tự đặc biệt của regex (App.py dùng str.contains)
        cand = []
        for ti, t in enumerate(default.tbls):
            if has_rowspan(t) or len(t['b']) < 2:
                continue
            for ci, n in enumerate(default.cols[ti]):
                nl = n.lower()
                if (want == 'ma' and re.search(r'mã|outlet code|outlet_code|code', nl)) or \
                        (want == 'ten' and re.search(r'tên ?(kh|ch)|outlet name|outlet_name|tên khách|tên cửa', nl)):
                    cells = body_cells(t)
                    vals = [r[ci] for r in cells if ci < len(r) and r[ci].strip() and safe.match(r[ci])
                            and not is_total(r)]
                    if len(vals) >= 2:
                        cand.append((ti, n, vals))
        for ti, n, vals in cand:
            for probe in vals[:3]:
                v, _ = self.snap({key: probe})
                found = _find_col(default, v, lambda x, p=probe: p.lower() in x.lower())
                if not found:
                    continue
                # 2 giá trị cách dấu phẩy: 'hoặc' (ô chung) hay nguyên chuỗi (ô ở các tab)?
                multi = False
                other = next((x for x in vals if x != probe and probe.lower() not in x.lower()
                              and x.lower() not in probe.lower()), None)
                if other:
                    v2, _ = self.snap({key: f'{probe},{other}'})
                    f2 = _find_col(default, v2, lambda x, a=probe, b=other: a.lower() in x.lower() or b.lower() in x.lower())
                    multi = bool(f2)
                spec = {'mode': 'contains', 'multi': multi, 'targets': [{'t': t_, 'col': c} for t_, c in found]}
                # App.py có bỏ dấu cách đầu/cuối chữ gõ không? (vd "anh " ở tab Combo OFF: không bỏ)
                vt, _ = self.snap({key: f' {probe} '})
                if vt.plain != v.plain:
                    spec['raw'] = True
                if not _only_targets_changed(default, v, found):
                    # App.py lọc dữ liệu gốc rồi tính lại báo cáo (vd ô Mã KH/Tên KH chung)
                    return {'mode': 'partial', 'inner': spec}
                return spec
        return {'mode': 'none'}

    def _date(self, w, default):
        key = w['key']
        val = w.get('value')
        if not isinstance(val, list) or len(val) != 2:
            return {'mode': 'none'}
        import datetime as dt
        lo, hi = dt.date.fromisoformat(val[0][:10]), dt.date.fromisoformat(val[1][:10])
        day = hi
        v, _ = self.snap({key: (day, day)})
        ddmm = day.strftime('%d/%m/%Y')
        found = _find_col(default, v, lambda x, d=ddmm: x.startswith(d))
        if found:
            spec = {'mode': 'date', 'targets': [{'t': ti, 'col': c} for ti, c in found]}
            return spec if _only_targets_changed(default, v, found) else {'mode': 'partial', 'inner': spec}
        return {'mode': 'none'}


def main_widgets(blocks):
    """Ô lọc chung đầu trang (trước thanh tab) có ảnh hưởng tuỳ báo cáo: Thứ VT, Mã KH, Tên KH."""
    out = []
    for b in blocks:
        if b['kind'] == 'nav':
            break
        if b['kind'] == 'widget' and b.get('key') in MAIN_KEYS:
            w = {'t': 'w', 'key': b['key'], 'kind': b.get('wkind'), 'label': b.get('label') or '',
                 'value': b.get('value'), 'placeholder': b.get('placeholder')}
            for f in ('options', 'labels'):
                if b.get(f) is not None:
                    w[f] = b[f]
            out.append(w)
    return out


def annotate(app, base_state, items, blocks, variant_cb, log=lambda m: None):
    """Gắn spec vào các ô lọc trong items (tại chỗ); trả về dict spec các ô chung đầu trang."""
    pr = Prober(app, base_state, log)
    default = Snapshot(items)
    for it in _walk(items):
        if it['t'] != 'filters':
            continue
        for w in it['w']:
            try:
                w['f'] = pr.probe(w, default, variant_cb)
            except Exception as e:
                w['f'] = {'mode': 'unsupported', 'err': str(e)[:200]}
            log(f"    {w['key']}: {w['f']['mode']}")
    main = {}
    for w in main_widgets(blocks):
        try:
            w['f'] = pr.probe(w, default, variant_cb)
        except Exception as e:
            w['f'] = {'mode': 'unsupported', 'err': str(e)[:200]}
        if w['f']['mode'] not in ('none',):
            main[w['key']] = w
        log(f"    [chung] {w['key']}: {w['f']['mode']}")
    return main


# ---------------- Dòng Tổng: tìm công thức để app tính lại khi lọc ----------------
_STYLES = [('.', ','), (',', '.')]  # (ngăn nghìn, thập phân)


def _num(x, style):
    t, dec = style
    s = (x or '').strip().replace(' ', '').replace(' ', '')
    s = re.sub(r'(tr|Tr|đ|k|VNĐ)$', '', s)
    pct = s.endswith('%')
    s = s.rstrip('%')
    if not re.fullmatch(r'[-+]?[\d.,]+', s or 'x'):
        return None, pct
    if t in s and dec in s and s.rfind(t) > s.rfind(dec):
        return None, pct
    s2 = s.replace(t, '').replace(dec, '.')
    try:
        return float(s2), pct
    except ValueError:
        return None, pct


def _decimals(x, style):
    s = (x or '').strip().rstrip('%')
    return len(s.split(style[1])[1]) if style[1] in s else 0


def total_formulas(t):
    """Bảng có đúng 1 dòng Tổng ở cuối → {cột: công thức} để app tính lại khi lọc dòng."""
    if has_rowspan(t) or len(t['b']) < 3:
        return None
    cells = body_cells(t)
    is_tot = [is_total(r) for r in cells]
    if sum(is_tot) != 1 or not is_tot[-1]:
        return None
    body, tot = cells[:-1], cells[-1]
    ncol = len(col_names(t))
    out = {}
    sums = {}
    for c in range(ncol):
        tv = tot[c] if c < len(tot) else ''
        for style in _STYLES:
            total, pct = _num(tv, style)
            if total is None or pct:
                continue
            vals = [_num(r[c] if c < len(r) else '', style)[0] for r in body]
            if any(v is None for v in vals if v is not None) or not any(v is not None for v in vals):
                continue
            ssum = sum(v for v in vals if v is not None)
            d = _decimals(tv, style)
            if abs(round(ssum, d) - total) <= 0.5 * 10 ** -d + 1e-9:
                out[c] = {'op': 'sum', 't': style[0], 'd': style[1], 'n': d}
                sums[c] = (ssum, style)
                break
    # % = tỷ lệ của 2 cột tổng (a/b*100)
    for c in range(ncol):
        if c in out:
            continue
        tv = tot[c] if c < len(tot) else ''
        for style in _STYLES:
            total, pct = _num(tv, style)
            if total is None or not pct:
                continue
            d = _decimals(tv, style)
            hit = None
            for a in sums:
                for b in sums:
                    if a == b or sums[b][0] == 0:
                        continue
                    if abs(round(sums[a][0] / sums[b][0] * 100, d) - total) <= 0.5 * 10 ** -d + 1e-9:
                        hit = (a, b)
                        break
                if hit:
                    break
            if hit:
                out[c] = {'op': 'ratio', 'a': hit[0], 'b': hit[1], 't': style[0], 'd': style[1], 'n': d}
                break
    return {str(k): v for k, v in out.items()} or None


def annotate_totals(items):
    for t in tables(items):
        f = total_formulas(t)
        if f:
            t['tot'] = f
