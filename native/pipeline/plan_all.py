"""Liệt kê mọi tổ hợp bộ lọc cần GitHub tính (app không tự tính được), theo thứ tự ưu tiên.

Khớp đúng yêu cầu app gửi (lib/ui/report_page.dart _needServer/_requestGithub):
  - ô 'partial' / 'unsupported' đang bật
  - ô 'calc' chọn ≥ 2 giá trị (1 giá trị đã có bản tính sẵn trong reports)
  - ĐDKD chọn ≥ 2 người
Ngày = ngày mặc định của tháng. Ô gõ chữ / chọn ngày: vô hạn giá trị → không liệt kê.
"""
import itertools
import json
import os

import filters_probe

MAX_ONE = 300     # ô có quá nhiều lựa chọn (vd. Mã KH) → bỏ
ALL_SUBSETS = 9   # ≤ 9 lựa chọn → đủ mọi tổ hợp (≤ 511)
PAIRS = 40        # ≤ 40 lựa chọn → mọi cặp


def _subsets(opts, lo=2):
    return [list(c) for n in range(lo, len(opts) + 1) for c in itertools.combinations(opts, n)]


def _pairs(opts):
    return [list(c) for c in itertools.combinations(opts, 2)]


def plan(reports_dir):
    man = json.load(open(os.path.join(reports_dir, 'manifest.json'), encoding='utf-8'))
    sc = man['source_commit']
    months = list(reversed(man.get('kpi_months') or []))  # tháng mới trước
    tiers = [[] for _ in range(6)]
    for mi, m in enumerate(months):
        kdir = os.path.join(reports_dir, 'kpi', m['key'])
        idx = json.load(open(os.path.join(kdir, 'index.json'), encoding='utf-8'))
        date = idx['default_date']
        nvs = list(idx.get('nv') or [])
        old = 3 if mi else 0  # tháng trước: ưu tiên thấp hơn
        for r in idx['reports']:
            path = os.path.join(kdir, r['code'], date + '.json')
            if r['code'] == 'TURNOVER' or not os.path.isfile(path):  # Turnover: app tự tính
                continue
            doc = json.load(open(path, encoding='utf-8'))
            ws = [w for it in filters_probe._walk(doc['items']) if it['t'] == 'filters' for w in it['w']]
            ws += list((doc.get('main') or {}).values())
            base = {'month_key': m['key'], 'date': date, 'code': r['code'], 'name': r['name'],
                    'nav': r['name'] if r.get('group') == 'tab' else None, 'ddkd': [], 'sc': sc}
            add = lambda t, values=None, ddkd=None: tiers[min(t + old, 5)].append(
                {**base, 'values': values or {}, 'ddkd': ddkd or []})
            for w in ws:
                mode = (w.get('f') or {}).get('mode')
                kind, opts, dv = w.get('kind'), w.get('options') or [], w.get('value')
                if mode not in ('calc', 'partial', 'unsupported') or len(opts) > MAX_ONE:
                    if not (mode in ('partial', 'unsupported') and kind in ('checkbox', 'toggle')):
                        continue
                k = w['key']
                if kind == 'multiselect':
                    if mode != 'calc':
                        for o in opts:
                            if [o] != dv:
                                add(0, {k: [o]})
                        if dv:
                            add(0, {k: []})
                    many = _subsets(opts) if len(opts) <= ALL_SUBSETS else _pairs(opts) if len(opts) <= PAIRS else []
                    for v in many:
                        if v != dv:
                            add(1 if len(opts) <= ALL_SUBSETS else 2, {k: v})
                elif kind in ('selectbox', 'radio') and mode != 'calc':
                    for o in opts:
                        if o != dv:
                            add(0, {k: o})
                elif kind in ('checkbox', 'toggle') and mode != 'calc':
                    add(0, {k: not bool(dv)})
            if r.get('group') != 'tab' and len(nvs) >= 2:
                for v in _pairs(nvs):
                    add(2, ddkd=v)
                for v in itertools.combinations(nvs, 3):
                    add(5, ddkd=list(v))
    return sc, [q for t in tiers for q in t]


if __name__ == '__main__':
    import sys
    from collections import Counter
    sc, p = plan(sys.argv[1])
    print(sc[:12], len(p))
    print(Counter((q['month_key'], q['code']) for q in p).most_common(40))
