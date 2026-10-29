"""Kiểm chứng bộ lọc của app == App.py thật, trên các tổ hợp ô lọc ngẫu nhiên.

  python parity_filters.py --app ../../App.py --json out/ --dart-app ../app [--cases 12]

Mỗi báo cáo (ngày mặc định, Tất cả ĐDKD): sinh tổ hợp ô lọc (từng ô + từng cặp ô), chạy
App.py với tổ hợp đó → bảng/thẻ/biểu đồ; chạy filter_engine (Dart) trên bản gốc → so từng
dòng từng bảng (kể cả dòng Tổng tính lại), thẻ, hạng mục biểu đồ. Lệch → exit 1.
"""
import argparse
import datetime as dt
import json
import os
import random
import re
import subprocess
import sys

import export_kpi
import filters_probe as fp
import report_doc
from headless import HeadlessApp


def summarize(items):
    tbls = fp.tables(items)
    return {
        'tables': [{'cols': fp.col_names(t), 'rows': fp.body_cells(t)} for t in tbls],
        'cards': fp.cards(items),
        'cats': fp.chart_cats(items),
    }


def _nonempty(tables):
    out = []
    for t in tables:
        data = [r for r in t['rows'] if not fp.is_total(r)]
        if data:
            out.append(t)
    return out


def compare(exp, got):
    diffs = []
    et, gt = _nonempty(exp['tables']), _nonempty(got['tables'])
    if len(et) != len(gt):
        return [f'số bảng có dữ liệu: App.py={len(et)} app={len(gt)}']
    for i, (a, b) in enumerate(zip(et, gt)):
        if a['cols'] != b['cols']:
            diffs.append(f'bảng {i + 1} cột khác: {set(a["cols"]) ^ set(b["cols"])}')
            continue
        if a['rows'] != b['rows']:
            ra, rb = a['rows'], b['rows']
            if len(ra) != len(rb):
                diffs.append(f'bảng {i + 1} số dòng App.py={len(ra)} app={len(rb)}')
            else:
                for j, (x, y) in enumerate(zip(ra, rb)):
                    if x != y:
                        diffs.append(f'bảng {i + 1} dòng {j + 1}: App.py={x[:8]} app={y[:8]}')
                        break
    if sorted(exp['cards']) != sorted(got['cards']):
        diffs.append(f'thẻ: App.py={exp["cards"]} app={got["cards"]}')
    if exp['cats'] != got['cats'] and [sorted(c) for c in exp['cats']] != [sorted(c) for c in got['cats']]:
        diffs.append('hạng mục biểu đồ khác')
    return diffs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--app', required=True)
    ap.add_argument('--json', required=True)
    ap.add_argument('--dart-app', required=True)
    ap.add_argument('--month', default=None)
    ap.add_argument('--cases', type=int, default=10, help='số tổ hợp ngẫu nhiên mỗi báo cáo')
    ap.add_argument('--only', nargs='*')
    ap.add_argument('--budget', type=float, default=150, help='giây tối đa chạy App.py mỗi màn hình')
    a = ap.parse_args()
    rnd = random.Random(7)
    json_dir = os.path.abspath(a.json)
    man = json.load(open(os.path.join(json_dir, 'manifest.json'), encoding='utf-8'))
    mk = a.month or man['kpi_months'][-1]['key']
    kdir = os.path.join(json_dir, 'kpi', mk)
    idx = json.load(open(os.path.join(kdir, 'index.json'), encoding='utf-8'))
    day = dt.date.fromisoformat(idx['default_date'])
    app = HeadlessApp(os.path.abspath(a.app))
    export_kpi._app = app

    all_cases, expected, labels = [], [], []
    for r in idx['reports']:
        code = r['code']
        if a.only and code not in a.only:
            continue
        nav = r['name'] if r['group'] == 'tab' else export_kpi.NAV_KPI
        path = os.path.join(kdir, code, idx['default_date'] + '.json')
        doc = json.load(open(path, encoding='utf-8'))
        widgets = [w for it in fp._walk(doc['items']) if it['t'] == 'filters' for w in it['w']]
        widgets += list((doc.get('main') or {}).values())
        usable = [w for w in widgets if (w.get('f') or {}).get('mode') in ('select', 'eq', 'cols', 'contains', 'date', 'calc')]
        if not usable:
            continue
        export_kpi._reset_widgets()
        st = export_kpi._state(mk, day, None, r['name'], nav)
        blocks, _, _ = app.run(st)
        raw = {b['key']: dict(zip(b.get('options') or [], b.get('_raw_options') or []))
               for b in blocks if b['kind'] == 'widget' and b.get('key')}
        tbls = fp.tables(doc['items'])

        def gen(w):
            f, kind = w['f'], w['kind']
            opts = w.get('options') or []
            if f['mode'] == 'cols':
                k = rnd.randint(1, max(1, len(opts) - 1))
                return sorted(rnd.sample(opts, k), key=opts.index)
            if f['mode'] in ('select', 'eq'):
                k = rnd.randint(1, min(3, len(opts)))
                return sorted(rnd.sample(opts, k), key=opts.index)
            if f['mode'] == 'calc':
                keys = [k for k in f['variants'] if k != '[]']
                return [json.loads(rnd.choice(keys))] if kind == 'multiselect' else json.loads(rnd.choice(keys))
            if f['mode'] == 'contains':
                tg = f['targets'][0]
                t = tbls[tg['t']]
                ci = fp.col_names(t).index(tg['col'])
                vals = [row[ci] for row in fp.body_cells(t)
                        if ci < len(row) and row[ci].strip() and not fp.is_total(row)]
                pick = rnd.sample(vals, min(2 if f.get('multi') else 1, len(vals)))
                # đôi khi gõ một phần (chữ thường) như người dùng
                pick = [p if rnd.random() < 0.6 else p[: max(2, len(p) // 2)].lower() for p in pick]
                return ','.join(pick)
            if f['mode'] == 'date':
                lo, hi = (dt.date.fromisoformat(x[:10]) for x in w['value'])
                s = rnd.randint(0, (hi - lo).days)
                e = rnd.randint(s, (hi - lo).days)
                return [(lo + dt.timedelta(days=s)).isoformat(), (lo + dt.timedelta(days=e)).isoformat()]

        def to_state(w, v):
            if w['f']['mode'] == 'date':
                return tuple(dt.date.fromisoformat(x) for x in v)
            if isinstance(v, list):
                m = raw.get(w['key'], {})
                return [m.get(x, x) for x in v]
            return v

        cases = []
        for w in usable:
            cases.append({w['key']: gen(w)})
        non_calc = [w for w in usable if w['f']['mode'] != 'calc']
        for _ in range(a.cases):
            if len(non_calc) >= 2:
                ws = rnd.sample(non_calc, 2)
                cases.append({w['key']: gen(w) for w in ws})
        byk = {w['key']: w for w in usable}
        import time
        t_rep = time.time()
        for c in cases:
            if time.time() - t_rep > a.budget:
                break  # màn hình nặng (MCP): đủ thời gian thì thôi
            # như người dùng thật: mở báo cáo trước (App.py tự đặt mặc định, vd Thứ theo ngày),
            # rồi mới chọn ô lọc
            export_kpi._reset_widgets()
            app.run(dict(st))
            state = dict(st)
            for k, v in c.items():
                state[k] = to_state(byk[k], v)
            blocks, _, status = app.run(state)
            expected.append(summarize(report_doc.convert(blocks)))
            all_cases.append({'doc': path, 'values': c})
            labels.append(f'{code} {json.dumps(c, ensure_ascii=False)[:160]}')
        print(f'✓ {code}: {sum(1 for l in labels if l.startswith(code + " "))} tổ hợp', file=sys.stderr)

    proc = subprocess.run(['dart', 'run', 'tool/filter_cli.dart'], cwd=os.path.abspath(a.dart_app),
                          input=json.dumps({'cases': all_cases}, ensure_ascii=False) + '\n',
                          capture_output=True, text=True)
    if proc.returncode != 0:
        print(proc.stderr[-3000:], file=sys.stderr)
        sys.exit(2)
    got = json.loads(proc.stdout)
    bad = 0
    for lab, e, g in zip(labels, expected, got):
        if g.get('note'):
            continue  # app báo rõ không áp dụng được (vd 2 ô tính lại cùng lúc)
        d = compare(e, g)
        if d:
            bad += 1
            print('✗', lab)
            for x in d[:3]:
                print('     ', x)
    print(f'\nĐã so {len(labels)} tổ hợp ô lọc. Lệch: {bad}')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
