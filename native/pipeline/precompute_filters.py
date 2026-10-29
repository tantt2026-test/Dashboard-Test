"""Tính sẵn kết quả bộ lọc kiểu "tính lại" (App.py) để app mở tức thì.

  python precompute_filters.py --app App.py --reports _reports --out _filters --budget 2700
  python precompute_filters.py --app App.py --req '<json>' --out _filters      (1 yêu cầu từ app)
  python precompute_filters.py --app App.py --req '{"sc":..,"shard":[i,n],"budget":1320}' --out _filters
      (1 phần của "tính tất cả" — plan_all.py; tool/precompute_all.sh trên máy chia phần + gọi lặp)

Tính sẵn (ngày mặc định, Tất cả ĐDKD), cho mọi ô lọc mà app không tự tính được
(calc / partial / unsupported):
  - từng giá trị một (multiselect ≤ 40 lựa chọn, selectbox, checkbox)
  - ô 9 lựa chọn "Thứ / Chu kỳ" ở báo cáo nhẹ: đủ 511 tổ hợp
Ghi: <out>/<source_commit[:12]>/<mã tổ hợp>.json   (mã: run_request.key_of)
"""
import argparse
import itertools
import json
import os
import sys
import time

import export_kpi
import filters_probe
import report_doc
import run_request
from headless import HeadlessApp

THU = ['2', '3', '4', '5', '6', '7', '25', '36', '47']
MAX_SINGLE = 40
CHEAP_S = 3.0  # báo cáo chạy < 3 giây → tính đủ tổ hợp ô Thứ


def _write(out, sc, req, items, status):
    d = os.path.join(out, sc[:12])
    os.makedirs(d, exist_ok=True)
    k = run_request.key_of(req)
    with open(os.path.join(d, k + '.json'), 'w', encoding='utf-8') as fh:
        json.dump({'req': json.loads(run_request.canonical(req)), 'status': status, 'items': items},
                  fh, ensure_ascii=False, separators=(',', ':'))
    return k


def run_shard(app_path, req, out):
    """Phần i/n của danh sách plan_all (bỏ tổ hợp đã có ở branch filters), dừng khi hết ngân sách."""
    import subprocess
    import plan_all
    t0 = time.time()
    budget = float(req.get('budget') or 1320)
    i, n = req['shard']
    url = f"https://github.com/{os.environ.get('REPO', 'tantt2026-test/Dashboard-Test')}.git"
    subprocess.run(['git', 'clone', '-q', '--depth', '1', '-b', 'reports', url, '_reports'], check=True)
    sc, todo = plan_all.plan('_reports')
    if sc != req['sc']:
        print(f'Dữ liệu đã đổi ({sc[:7]} ≠ {req["sc"][:7]}) → bỏ', file=sys.stderr)
        return
    have = set()
    if subprocess.run(['git', 'clone', '-q', '--depth', '1', '--no-checkout', '-b', 'filters', url, '_have']).returncode == 0:
        ls = subprocess.run(['git', '-C', '_have', 'ls-tree', '-r', '--name-only', 'HEAD', sc[:12] + '/'],
                            capture_output=True, text=True).stdout.split()
        have = {os.path.basename(x)[:-5] for x in ls}
    mine = [q for k, q in enumerate(todo) if k % n == i and run_request.key_of(q) not in have]
    print(f'Phần {i}/{n}: {len(mine)} tổ hợp chưa có', file=sys.stderr)
    app = HeadlessApp(app_path)
    export_kpi._app = app
    done = 0
    for q in mine:
        if time.time() - t0 > budget:
            break
        items, status = run_request.compute(app, export_kpi, report_doc, filters_probe, q, q['name'], q.get('nav'))
        _write(out, sc, q, items, status)
        done += 1
    print(f'Phần {i}/{n}: xong {done}/{len(mine)} ({time.time() - t0:.0f}s)', file=sys.stderr)


def run_one(app_path, req, out):
    if 'shard' in req:
        return run_shard(app_path, req, out)
    app = HeadlessApp(app_path)
    export_kpi._app = app
    t = time.time()
    items, status = run_request.compute(app, export_kpi, report_doc, filters_probe, req,
                                        req['name'], req.get('nav'))
    k = _write(out, req['sc'], req, items, status)
    print(f'✓ {req["code"]} {k} ({time.time() - t:.0f}s) {status}', file=sys.stderr)


def precompute(app_path, reports_dir, out, budget):
    man = json.load(open(os.path.join(reports_dir, 'manifest.json'), encoding='utf-8'))
    sc = man.get('source_commit') or 'local'
    app = HeadlessApp(app_path)
    export_kpi._app = app
    t0 = time.time()
    done = 0
    for m in reversed(man.get('kpi_months') or []):  # tháng mới trước
        kdir = os.path.join(reports_dir, 'kpi', m['key'])
        idx = json.load(open(os.path.join(kdir, 'index.json'), encoding='utf-8'))
        date = idx['default_date']
        for r in idx['reports']:
            path = os.path.join(kdir, r['code'], date + '.json')
            if not os.path.isfile(path):
                continue
            doc = json.load(open(path, encoding='utf-8'))
            widgets = [w for it in filters_probe._walk(doc['items']) if it['t'] == 'filters' for w in it['w']]
            widgets += list((doc.get('main') or {}).values())
            nav = r['name'] if r.get('group') == 'tab' else None
            base = {'month_key': m['key'], 'date': date, 'code': r['code'], 'ddkd': [], 'sc': sc}
            # đo tốc độ báo cáo
            ts = time.time()
            run_request.compute(app, export_kpi, report_doc, filters_probe, {**base, 'values': {}}, r['name'], nav)
            cheap = time.time() - ts < CHEAP_S
            for w in widgets:
                mode = (w.get('f') or {}).get('mode')
                if mode not in ('calc', 'partial', 'unsupported'):
                    continue
                kind, opts = w.get('kind'), w.get('options') or []
                if kind == 'multiselect':
                    if not opts or len(opts) > MAX_SINGLE:
                        continue
                    combos = [[o] for o in opts]
                    if cheap and set(opts) == set(THU):
                        # ô Thứ/Chu kỳ ở báo cáo nhẹ: đủ 511 tổ hợp (thứ tự như danh sách gốc)
                        combos = [list(c) for n in range(1, len(THU) + 1) for c in itertools.combinations(THU, n)]
                elif kind in ('selectbox', 'radio'):
                    combos = list(opts)
                elif kind in ('checkbox', 'toggle'):
                    combos = [not bool(w.get('value'))]
                else:
                    continue  # ô gõ chữ: vô hạn giá trị → tính theo yêu cầu
                for v in combos:
                    if time.time() - t0 > budget:
                        print(f'⏱ hết ngân sách sau {done} tổ hợp', file=sys.stderr)
                        return done
                    if v == w.get('value'):
                        continue
                    req = {**base, 'values': {w['key']: v}}
                    if os.path.isfile(os.path.join(out, sc[:12], run_request.key_of(req) + '.json')):
                        continue
                    items, status = run_request.compute(app, export_kpi, report_doc, filters_probe,
                                                        req, r['name'], nav)
                    _write(out, sc, req, items, status)
                    done += 1
            print(f'✓ {m["key"]} {r["code"]}: tổng {done} tổ hợp ({time.time() - t0:.0f}s)', file=sys.stderr)
    return done


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--app', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--reports')
    ap.add_argument('--req', help='JSON 1 yêu cầu từ app (month_key,date,code,name,nav,ddkd,values,sc)')
    ap.add_argument('--budget', type=float, default=2700)
    a = ap.parse_args()
    app_path = os.path.abspath(a.app)
    out = os.path.abspath(a.out)
    if a.req:
        run_one(app_path, json.loads(a.req), out)
    else:
        n = precompute(app_path, os.path.abspath(a.reports), out, a.budget)
        print(f'Đã tính sẵn {n} tổ hợp', file=sys.stderr)


if __name__ == '__main__':
    main()
