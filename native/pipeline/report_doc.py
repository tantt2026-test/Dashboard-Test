"""Chuyển các block ghi được khi chạy App.py (headless.py) thành JSON có cấu trúc
để app native tự vẽ: tiêu đề, đoạn chữ, thẻ số, bảng (gộp ô, màu từng ô), hộp nhận xét,
biểu đồ cột/tròn.

Item (key ngắn cho file nhỏ):
  {"t":"h","lv":3,"r":[run]}                     tiêu đề
  {"t":"p","r":[run],"al":"c","li":1}            đoạn chữ (li = gạch đầu dòng)
  {"t":"box","bg":"#..","bd":"#..","ch":[item]}  hộp màu (nhận xét...)
  {"t":"cards","it":[{"l":..,"v":..,"c":"#.."}]} thẻ số
  {"t":"tbl","fz":2,"h":[[cell]],"b":[[cell]]}   bảng; cell {"x","cs","rs","bg","fg","b","al"}
  {"t":"msg","lv":"warning","x":..}              cảnh báo
  {"t":"bar"|"pie", ...}                         biểu đồ
  run = {"x":text,"b":1,"i":1,"c":"#hex"}
"""
import math
import re

from bs4 import BeautifulSoup, NavigableString, Tag

SKIP_TAGS = {'script', 'style', 'svg', 'button', 'head', 'meta', 'link', 'title', 'noscript', 'input'}
BLOCK_TAGS = {'div', 'p', 'section', 'article', 'header', 'footer', 'center', 'tr', 'ul', 'ol', 'table', 'body', 'html'}
HEADINGS = {'h1': 1, 'h2': 2, 'h3': 3, 'h4': 4, 'h5': 5, 'h6': 6}

# Màu theo class CSS của App.py (khi ô không có style inline)
CLASS_COLORS = {
    'pct-red': ('#fed7d7', '#742a2a'),
    'pct-green': ('#c6f6d5', '#22543d'),
    'pct-purple': ('#e9d8fd', '#553c9a'),
    'row-total-cell': ('#1a365d', '#ffffff'),
}

_named = {'white': '#ffffff', 'black': '#000000', 'red': '#ff0000', 'green': '#008000',
          'blue': '#0000ff', 'transparent': None, 'inherit': None, 'none': None}


def norm_color(v):
    if not v:
        return None
    v = v.strip().lower().replace('!important', '').strip()
    if v in _named:
        return _named[v]
    m = re.search(r'#([0-9a-f]{3,8})\b', v)
    if m:
        h = m.group(1)
        if len(h) == 3:
            h = ''.join(c * 2 for c in h)
        return '#' + h[:6] if len(h) in (6, 8) else None
    m = re.search(r'rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([\d.]+))?\)', v)
    if m:
        if m.group(4) is not None and float(m.group(4)) < 0.2:
            return None
        return '#%02x%02x%02x' % tuple(int(m.group(i)) for i in (1, 2, 3))
    return None


def parse_style(s):
    out = {}
    for part in (s or '').split(';'):
        if ':' in part:
            k, v = part.split(':', 1)
            if ':' in v:
                # Khai báo sai cú pháp (vd "background-color:background-color:#fed7d7" trong
                # App.py) — trình duyệt bỏ qua, nên app cũng bỏ qua để màu giống web
                continue
            out[k.strip().lower()] = v.replace('!important', '').strip()
    return out


def bg_of(st):
    c = norm_color(st.get('background-color'))
    if c:
        return c
    bg = st.get('background', '')
    if 'gradient' in bg:
        cols = re.findall(r'#[0-9a-fA-F]{3,6}', bg)
        return norm_color(cols[0]) if cols else None
    return norm_color(bg)


def is_bold(st):
    fw = st.get('font-weight', '')
    return fw in ('bold', 'bolder') or (fw.isdigit() and int(fw) >= 600)


def align_of(st, tag=None):
    a = (st.get('text-align') or (tag.get('align') if tag is not None else '') or '').lower()
    return {'center': 'c', 'right': 'r', 'left': 'l'}.get(a)


def clean_text(s):
    return re.sub(r'[ \t\r\f\v\n]+', ' ', s)


def tidy(s):
    """Bỏ khoảng trắng thừa khi ghép chữ từ nhiều thẻ: "( 38.6% )" → "(38.6%)"."""
    s = re.sub(r'([(\[]) +', r'\1', s)
    s = re.sub(r' +([)\],.;:%])', r'\1', s)
    return s


def md_runs(text):
    """Markdown đơn giản (**đậm**) → runs."""
    runs = []
    for i, part in enumerate(re.split(r'\*\*', text)):
        if part:
            runs.append({'x': part, 'b': 1} if i % 2 else {'x': part})
    return runs


def _pct(v):
    m = re.match(r'\s*([-\d.]+)\s*%', v or '')
    return float(m.group(1)) if m else None


def progress_bar(td):
    """Thanh tiến độ vẽ bằng div trong ô bảng (vd cột "TIẾN ĐỘ 88.9%" báo cáo Hiệu suất):
    div có width:x% + màu nền = phần đạt; div position:absolute left:y% = vạch mốc."""
    fill = mark = None
    for d in td.find_all('div'):
        st = parse_style(d.get('style'))
        if 'absolute' in st.get('position', '') and _pct(st.get('left')) is not None:
            mark = (_pct(st.get('left')), bg_of(st))
        elif _pct(st.get('width')) is not None and bg_of(st):
            fill = (_pct(st.get('width')), bg_of(st))
    if fill is None:
        return None
    bar = {'p': round(max(0.0, min(fill[0], 100.0)), 2), 'c': fill[1]}
    track = None
    for d in td.find_all('div'):
        st = parse_style(d.get('style'))
        if d.find('div') and bg_of(st):
            track = bg_of(st)
            break
    if track:
        bar['t'] = track
    if mark:
        bar['m'] = mark[0]
        if mark[1]:
            bar['mc'] = mark[1]
    return bar


class _Para:
    def __init__(self):
        self.runs = []
        self.attrs = {}

    def add(self, text, style):
        if not text:
            return
        r = {'x': text}
        if style.get('b'):
            r['b'] = 1
        if style.get('i'):
            r['i'] = 1
        if style.get('c'):
            r['c'] = style['c']
        if self.runs and {k: v for k, v in self.runs[-1].items() if k != 'x'} == {k: v for k, v in r.items() if k != 'x'}:
            self.runs[-1]['x'] += text
        else:
            self.runs.append(r)

    def finish(self):
        # bỏ khoảng trắng thừa đầu/cuối, dòng trống
        while self.runs and not self.runs[0]['x'].strip(' '):
            self.runs.pop(0)
        while self.runs and not self.runs[-1]['x'].strip(' '):
            self.runs.pop()
        if not self.runs:
            return None
        self.runs[0]['x'] = self.runs[0]['x'].lstrip(' ')
        self.runs[-1]['x'] = self.runs[-1]['x'].rstrip(' ')
        if not ''.join(r['x'] for r in self.runs).strip():
            return None
        return {'t': 'p', 'r': self.runs, **self.attrs}


class Converter:
    def __init__(self):
        self.items = []
        self.para = _Para()
        self.stack = [self.items]

    # ---- helpers ----
    @property
    def out(self):
        return self.stack[-1]

    def flush(self, **attrs):
        p = self.para.finish()
        if p:
            self.out.append(p)
        self.para = _Para()
        self.para.attrs.update({k: v for k, v in attrs.items() if v})

    def emit(self, item):
        self.flush()
        if item['t'] == 'cards' and self.out and self.out[-1]['t'] == 'cards':
            self.out[-1]['it'].extend(item['it'])
        else:
            self.out.append(item)

    # ---- detectors ----
    @staticmethod
    def _child_tags(tag):
        return [c for c in tag.children if isinstance(c, Tag)]

    def card_of(self, tag):
        """Thẻ số: render_metric_card (<div bg><div>nhãn</div><div>số</div></div>),
        hoặc div class *card* (mbs-card, hs-day-card) có 2–5 dòng con."""
        if tag.name != 'div' or tag.find('table'):
            return None
        kids = self._child_tags(tag)
        if not 2 <= len(kids) <= 5 or any(k.name != 'div' or k.find('div') for k in kids):
            return None
        st = parse_style(tag.get('style'))
        cls = ' '.join(tag.get('class') or [])
        if 'card' not in cls and not bg_of(st) and 'border' not in st:
            return None
        if 'card' not in cls and len(kids) != 2:
            return None
        def _txt(k):
            for br in k.find_all('br'):
                br.replace_with('\n')
            return '\n'.join(tidy(clean_text(l).strip()) for l in k.get_text(' ').split('\n') if l.strip())
        lines = [_txt(k) for k in kids]
        if not lines[0] or not lines[1] or len(lines[1]) > 90:
            return None
        card = {'l': lines[0], 'v': lines[1]}
        if len(lines) > 2:
            card['s'] = [l for l in lines[2:] if l]
        c = norm_color(parse_style(kids[1].get('style')).get('color')) or \
            norm_color(parse_style(kids[0].get('style')).get('color'))
        if c:
            card['c'] = c
        bg = bg_of(st)
        if bg:
            card['bg'] = bg
        ac = norm_color(st.get('border-top-color'))
        if ac:
            card['ac'] = ac
        return card

    def is_box(self, tag):
        if tag.name != 'div':
            return False
        cls = ' '.join(tag.get('class') or [])
        if 'note-box' in cls:
            return True
        st = parse_style(tag.get('style'))
        has_border = any(k.startswith('border') for k in st)
        return bool(bg_of(st)) and has_border and not tag.find('table') and len(clean_text(tag.get_text()).strip()) > 60

    # ---- table ----
    def table(self, tag):
        def cell(td, in_head):
            st = parse_style(td.get('style'))
            cls = td.get('class') or []
            # chỉ xuống dòng ở <br>, giống trình duyệt
            for br in td.find_all('br'):
                br.replace_with('\n')
            # chỉ gọn khoảng trắng khi chữ ghép từ nhiều thẻ; ô chữ thuần giữ y nguyên như trình duyệt
            # (vd tên KH "Anh Hùng ( Trái Cây )" → ô tìm Tên KH khớp đúng như App.py)
            nested = td.find(lambda t: t.name != 'br') is not None
            raw = td.get_text(' ')
            fix = tidy if nested else (lambda x: x)
            c = {'x': '\n'.join(fix(clean_text(l).strip()) for l in raw.split('\n') if l.strip())}
            cs, rs = int(td.get('colspan', 1) or 1), int(td.get('rowspan', 1) or 1)
            if cs > 1:
                c['cs'] = cs
            if rs > 1:
                c['rs'] = rs
            bg, fg = bg_of(st), norm_color(st.get('color'))
            for k in cls:
                if k in CLASS_COLORS and not bg:
                    bg, fg = CLASS_COLORS[k][0], fg or CLASS_COLORS[k][1]
            # màu chữ đặt ở thẻ con (span/b)
            if not fg:
                for inner in td.find_all(True, style=True):
                    fg = norm_color(parse_style(inner.get('style')).get('color'))
                    if fg:
                        break
            if bg:
                c['bg'] = bg
            if fg:
                c['fg'] = fg
            bar = progress_bar(td)
            if bar:
                c['bar'] = bar
            if is_bold(st) or td.find(['b', 'strong']) or in_head:
                c['b'] = 1
            al = align_of(st, td)
            if al:
                c['al'] = al
            return c

        rows_h, rows_b = [], []
        fz = 0
        for tr in tag.find_all('tr'):
            if tr.find_parent('table') is not tag:
                continue
            tds = [c for c in tr.find_all(['td', 'th'], recursive=False)]
            in_head = tr.find_parent('thead') is not None or (tds and all(c.name == 'th' for c in tds))
            row = [cell(c, in_head) for c in tds]
            tr_st = parse_style(tr.get('style'))
            tr_bg = bg_of(tr_st)
            tr_cls = ' '.join(tr.get('class') or [])
            if tr_bg or 'row-total' in tr_cls:
                for c in row:
                    c.setdefault('bg', tr_bg or '#1a365d')
                    c.setdefault('fg', norm_color(tr_st.get('color')) or ('#ffffff' if not tr_bg else '#1a202c'))
            if in_head and not rows_b:
                rows_h.append(row)
                if len(rows_h) == 1:
                    n = 0
                    for c in tds:
                        if 'sticky' in (c.get('style') or ''):
                            n += int(c.get('colspan', 1) or 1)
                        else:
                            break
                    fz = n
            else:
                rows_b.append(row)
        if not rows_h and not rows_b:
            return None
        if not fz and rows_b:  # sticky ở td body
            n = 0
            for td in tag.find('tbody').find('tr').find_all(['td', 'th'], recursive=False) if tag.find('tbody') and tag.find('tbody').find('tr') else []:
                if 'sticky' in (td.get('style') or ''):
                    n += 1
                else:
                    break
            fz = n
        item = {'t': 'tbl', 'h': rows_h, 'b': rows_b}
        if fz:
            item['fz'] = min(fz, 4)
        return item

    # ---- walker ----
    def walk(self, node, style):
        if isinstance(node, NavigableString):
            if type(node).__name__ in ('Comment', 'Doctype', 'Declaration', 'ProcessingInstruction'):
                return
            self.para.add(clean_text(str(node)), style)
            return
        if not isinstance(node, Tag) or node.name in SKIP_TAGS:
            return
        if 'filter-label' in (node.get('class') or []):
            return  # nhãn bộ lọc của Streamlit
        name = node.name
        st = parse_style(node.get('style'))
        s2 = dict(style)
        if name in ('b', 'strong') or is_bold(st):
            s2['b'] = True
        if name in ('i', 'em'):
            s2['i'] = True
        c = norm_color(st.get('color'))
        if c:
            s2['c'] = c

        if name == 'table':
            t = self.table(node)
            if t:
                self.emit(t)
            return
        card = self.card_of(node)
        if card:
            self.emit({'t': 'cards', 'it': [card]})
            return
        if name in HEADINGS:
            self.flush()
            self.para.attrs = {}
            sub = _Para()
            old, self.para = self.para, sub
            for ch in node.children:
                self.walk(ch, s2)
            p = sub.finish()
            self.para = _Para()
            if p:
                h = {'t': 'h', 'lv': HEADINGS[name], 'r': p['r']}
                al = align_of(st)
                if al:
                    h['al'] = al
                self.out.append(h)
            return
        if self.is_box(node):
            self.flush()
            box = {'t': 'box', 'ch': []}
            bg = bg_of(st)
            if bg:
                box['bg'] = bg
            bd = None
            for k in ('border-left', 'border', 'border-color'):
                if k in st:
                    bd = norm_color(st[k])
                    if bd:
                        break
            if bd:
                box['bd'] = bd
            self.stack.append(box['ch'])
            for ch in node.children:
                self.walk(ch, s2)
            self.flush()
            self.stack.pop()
            if box['ch']:
                self.out.append(box)
            return
        if name == 'br':
            self.para.add('\n', style)
            return
        if name == 'li':
            self.flush()
            self.para.attrs = {'li': 1}
            for ch in node.children:
                self.walk(ch, s2)
            self.flush()
            return
        if name in BLOCK_TAGS:
            self.flush()
            al = align_of(st, node)
            self.para.attrs = {'al': al} if al else {}
            for ch in node.children:
                self.walk(ch, s2)
            self.flush()
            return
        for ch in node.children:  # inline: span, a, font, small...
            self.walk(ch, s2)
        if 'inline-block' in st.get('display', ''):
            self.para.add('   ', style)

    def html(self, body):
        soup = BeautifulSoup(body, 'html.parser')
        for ch in soup.children:
            self.walk(ch, {})
        self.flush()


# ---------- Plotly ----------
def _lst(v):
    if v is None:
        return None
    if hasattr(v, 'tolist'):
        v = v.tolist()
    if isinstance(v, dict) and 'bdata' in v:  # plotly ≥6 typed array
        import base64
        import numpy as np
        arr = np.frombuffer(base64.b64decode(v['bdata']), dtype=v['dtype'])
        if 'shape' in v:
            arr = arr.reshape([int(x) for x in str(v['shape']).split(',')])
        v = arr.tolist()
    if isinstance(v, (list, tuple)):
        out = []
        for x in v:
            if hasattr(x, 'item'):
                x = x.item()
            if isinstance(x, float) and (math.isnan(x) or math.isinf(x)):
                x = None
            out.append(x)
        return out
    return v


def _plain(s):
    return clean_text(re.sub(r'<[^>]+>', ' ', str(s or ''))).strip()


def plotly_item(fig):
    data, layout = fig.get('data', []), fig.get('layout', {})
    title = layout.get('title')
    title = _plain(title.get('text') if isinstance(title, dict) else title)
    if data and all(t.get('type') == 'table' for t in data):
        t = data[0]
        hdr = [_plain(x) for x in (_lst((t.get('header') or {}).get('values')) or [])]
        cols = _lst((t.get('cells') or {}).get('values')) or []
        cols = [_lst(c) or [] for c in cols]
        fill = (t.get('cells') or {}).get('fill', {}).get('color')
        n = max((len(c) for c in cols), default=0)
        body = []
        for i in range(n):
            body.append([{'x': _plain(c[i]) if i < len(c) else ''} for c in cols])
        item = {'t': 'tbl', 'h': [[{'x': h, 'b': 1} for h in hdr]], 'b': body}
        return ([{'t': 'h', 'lv': 4, 'r': [{'x': title}]}] if title else []) + [item]

    traces = []
    kind = 'bar'
    for t in data:
        typ = t.get('type', 'scatter')
        if typ == 'pie':
            kind = 'pie'
            m = t.get('marker') or {}
            traces.append({'labels': [_plain(x) for x in _lst(t.get('labels')) or []],
                           'values': _lst(t.get('values')) or [],
                           'colors': _lst(m.get('colors')) or None,
                           'hole': t.get('hole') or 0})
        elif typ == 'bar':
            m = t.get('marker') or {}
            col = m.get('color')
            traces.append({'name': _plain(t.get('name') or ''),
                           'x': _lst(t.get('x')) or [], 'y': _lst(t.get('y')) or [],
                           'text': [_plain(x) for x in (_lst(t.get('text')) or [])] if isinstance(t.get('text'), (list, tuple)) or hasattr(t.get('text'), 'tolist') or isinstance(t.get('text'), dict) else None,
                           'color': _lst(col) if not isinstance(col, str) else col,
                           'h': 1 if t.get('orientation') == 'h' else 0})
    if not traces:
        return []
    item = {'t': kind, 'title': title, 'tr': traces}
    if kind == 'bar':
        item['mode'] = layout.get('barmode') or 'group'
        shapes = layout.get('shapes') or []
        lines = [s for s in shapes if s.get('type') == 'line']
        if lines:  # đường mốc (Timegone...)
            item['ref'] = [{'x0': s.get('x0'), 'x1': s.get('x1'), 'y0': s.get('y0'), 'y1': s.get('y1'),
                            'c': norm_color((s.get('line') or {}).get('color'))} for s in lines]
    return [item]


def dataframe_item(df):
    try:
        import pandas as pd
        if isinstance(df, pd.io.formats.style.Styler):
            df = df.data
        if not isinstance(df, pd.DataFrame):
            return []
        hdr = [[{'x': str(c), 'b': 1} for c in df.columns]]
        body = [[{'x': '' if (isinstance(v, float) and math.isnan(v)) else str(v)} for v in row]
                for row in df.itertuples(index=False)]
        return [{'t': 'tbl', 'h': hdr, 'b': body}]
    except Exception:
        return []


def strip_private(obj):
    """Bỏ các khoá '_...' (giá trị gốc chỉ dùng khi chạy thử) trước khi ghi JSON."""
    if isinstance(obj, dict):
        return {k: strip_private(v) for k, v in obj.items() if not str(k).startswith('_')}
    if isinstance(obj, list):
        return [strip_private(x) for x in obj]
    return obj


def convert(blocks):
    """blocks (headless.Recorder) → (items, sections). Chỉ lấy phần sau thanh tab chính."""
    start = 0
    for i, b in enumerate(blocks):
        if b['kind'] == 'nav':
            start = i + 1
    blocks = blocks[start:]

    def _short(b):
        return b['kind'] == 'markdown' and len(b['body']) < 300 and '<table' not in b['body']

    def _plain(b):
        return clean_text(re.sub(r'<[^>]+>', ' ', b.get('body') or '')).strip()
    # Nhãn ô lọc = markdown ngắn ngay trước widget (App.py vẽ nhãn bằng <p class=filter-label>);
    # dòng "Bộ lọc ..." ngay trước nhãn = tiêu đề nhóm lọc. Đưa vào item widget, không in thành chữ.
    drop = set()
    wlabel, wgroup = {}, {}
    for i, b in enumerate(blocks):
        if b['kind'] == 'widget' and i > 0 and _short(blocks[i - 1]):
            drop.add(i - 1)
            wlabel[i] = _plain(blocks[i - 1])
            if i > 1 and _short(blocks[i - 2]) and 'lọc' in _plain(blocks[i - 2]).lower():
                drop.add(i - 2)
                wgroup[i] = _plain(blocks[i - 2])
    conv = Converter()
    for i, b in enumerate(blocks):
        if i in drop:
            continue
        k = b['kind']
        if b.get('section') and '__popover__' in b['section'] and k != 'widget':
            continue  # popover: chỉ lấy ô lọc, bỏ nút tải / nội dung phụ
        if k == 'markdown':
            body = b['body']
            if b['html'] or '<' in body:
                conv.html(body)
            else:
                txt = body.strip()
                if txt in ('---', '***', ''):
                    continue
                conv.flush()
                for line in txt.split('\n'):
                    m = re.match(r'^(#{1,6})\s+(.*)', line)
                    if m:
                        conv.out.append({'t': 'h', 'lv': len(m.group(1)), 'r': md_runs(m.group(2))})
                    elif line.strip():
                        li = re.match(r'^\s*[-*•]\s+(.*)', line)
                        conv.out.append({'t': 'p', 'r': md_runs(li.group(1) if li else line.strip()),
                                         **({'li': 1} if li else {})})
        elif k == 'caption':
            conv.flush()
            conv.out.append({'t': 'p', 'r': md_runs(b['body']), 'cap': 1})
        elif k == 'heading':
            conv.flush()
            conv.out.append({'t': 'h', 'lv': b['level'], 'r': md_runs(b['body'])})
        elif k == 'message':
            conv.emit({'t': 'msg', 'lv': b['level'], 'x': re.sub(r'\*\*', '', b['body'])})
        elif k == 'write':
            if b['body'].strip():
                conv.flush()
                conv.out.append({'t': 'p', 'r': md_runs(b['body'])})
        elif k == 'plotly':
            for it in plotly_item(b['figure']):
                conv.emit(it)
        elif k == 'dataframe':
            for it in dataframe_item(b['data']):
                conv.emit(it)
        elif k == 'widget':
            w = {'t': 'w', 'key': b.get('key'), 'kind': b.get('wkind'),
                 'label': wlabel.get(i) or b.get('label') or '', 'value': b.get('value')}
            for f in ('options', 'labels', 'placeholder', 'min_value', 'max_value', '_raw_options'):
                if b.get(f) is not None:
                    w[f] = b[f]
            if i in wgroup:
                w['group'] = wgroup[i]
            conv.flush()
            if conv.out and conv.out[-1]['t'] == 'filters' and not w.get('group'):
                conv.out[-1]['w'].append(w)
            else:
                conv.out.append({'t': 'filters', 'title': w.pop('group', None), 'w': [w]})
        elif k == 'metric':
            conv.emit({'t': 'cards', 'it': [{'l': b['label'], 'v': b['value']}]})
    conv.flush()
    return conv.items
