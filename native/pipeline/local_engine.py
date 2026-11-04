"""Máy tính tại chỗ cho app Mac: chạy App.py (headless) theo bộ lọc, y như GitHub filter-run.

App Mac khởi động 1 lần (Python đóng gói trong app) rồi gửi từng yêu cầu qua stdin, mỗi dòng 1 JSON:
  {"id": 1, "root": "<thư mục có App.py + data/ đúng commit>", "req": {...như run_request}}
Trả về stdout, mỗi dòng 1 JSON: {"id": 1, "status": "ok", "items": [...]} hoặc {"id": 1, "error": "..."}
Thêm "op" (khi GitHub có data mới mà chưa xuất xong JSON cho app, app Mac tự tính):
  "plan"     + "month_key" → danh sách báo cáo/ngày/ĐDKD như index.json
  "turnover" + "month_key" → JSON Turnover như turnover/<Thang>.json
  "combine" + "a", "b", "out" → ghép data 2 Sale Sup (team_data.combine_dirs)
Giữ App.py + data đã đọc trong bộ nhớ (theo root) → lần lọc sau chỉ vài giây.
"""
import datetime as dt
import json
import os
import sys
import time
import traceback
import warnings

warnings.filterwarnings('ignore')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import export_kpi  # noqa: E402
import filters_probe  # noqa: E402
import report_doc  # noqa: E402
import run_request  # noqa: E402
from headless import HeadlessApp  # noqa: E402

_apps = {}
_ns = {}


def _app(root, keep=1):
    """keep: số bản giữ trong bộ nhớ (Sale Sup 'Cả 2' cần 3: data ghép + Tân + Vy)."""
    app = _apps.pop(root, None)
    if app is None:
        while len(_apps) >= keep:  # commit dữ liệu mới → bỏ bản cũ cho nhẹ bộ nhớ
            _apps.pop(next(iter(_apps)))
            _ns.clear()
        app = HeadlessApp(os.path.join(root, 'App.py'))
    _apps[root] = app  # cuối dict = dùng gần nhất
    return app


def _plan(app, root, mk):
    export_kpi._app = app
    p = export_kpi.plan_month(os.path.join(root, 'App.py'), mk, dt.datetime.utcnow())
    return {**{k: p[k] for k in ('month_key', 'month_label', 'year', 'month', 'dates', 'default_date',
                                 'data_max_date', 'nv')},
            'reports': [{'code': c, 'name': lab, 'group': export_kpi.report_group(nav)}
                        for c, lab, nav in p['reports']]}


def _turnover(root, mk):
    import app_logic
    import export_reports
    ns = _ns.get(root)
    if ns is None:
        ns = _ns[root] = app_logic.load(os.path.join(root, 'App.py'), log=lambda m: None)
    return export_reports.export_turnover(ns, mk)


def main():
    out = sys.stdout
    sys.stdout = sys.stderr  # print() của App.py không lẫn vào kênh trả lời
    out.write(json.dumps({'ready': True}) + '\n')
    out.flush()
    for line in sys.stdin:
        if not line.strip():
            continue
        msg = json.loads(line)
        t = time.time()
        try:
            op = msg.get('op')
            if op == 'combine':
                # Sale Sup 'Cả 2': ghép data 2 team (team_data.py — giống GitHub)
                import team_data
                team_data.combine_dirs(msg['a'], msg['b'], msg['out'], workers=1)
                out.write(json.dumps({'id': msg.get('id'), 'ok': True, 'secs': round(time.time() - t, 1)}) + '\n')
                out.flush()
                continue
            parts = msg.get('parts') or {}
            keep = 3 if parts else 1
            app = _app(msg['root'], keep)
            export_kpi._app = app
            if op == 'plan':
                res = {'id': msg.get('id'), 'plan': _plan(app, msg['root'], msg['month_key'])}
            elif op == 'turnover':
                res = {'id': msg.get('id'), 'turnover': _turnover(msg['root'], msg['month_key'])}
            else:
                req = msg['req']
                if parts:  # Sale Sup 'Cả 2': tách bảng theo team + Total chung
                    apps = {'all': app, **{k: _app(r, 3) for k, r in parts.items()}}
                    items, status = run_request.compute_team(apps, export_kpi, report_doc, filters_probe,
                                                             req, req['name'], req.get('nav'))
                else:
                    items, status = run_request.compute(app, export_kpi, report_doc, filters_probe, req,
                                                        req['name'], req.get('nav'))
                res = {'id': msg.get('id'), 'status': status, 'items': items}
            res['secs'] = round(time.time() - t, 1)
        except Exception as e:  # noqa: BLE001
            traceback.print_exc()
            res = {'id': msg.get('id'), 'error': f'{type(e).__name__}: {e}'[:500]}
        out.write(json.dumps(res, ensure_ascii=False) + '\n')
        out.flush()


if __name__ == '__main__':
    main()
