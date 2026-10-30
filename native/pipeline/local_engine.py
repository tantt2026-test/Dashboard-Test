"""Máy tính tại chỗ cho app Mac: chạy App.py (headless) theo bộ lọc, y như GitHub filter-run.

App Mac khởi động 1 lần (Python đóng gói trong app) rồi gửi từng yêu cầu qua stdin, mỗi dòng 1 JSON:
  {"id": 1, "root": "<thư mục có App.py + data/ đúng commit>", "req": {...như run_request}}
Trả về stdout, mỗi dòng 1 JSON: {"id": 1, "status": "ok", "items": [...]} hoặc {"id": 1, "error": "..."}
Giữ App.py + data đã đọc trong bộ nhớ (theo root) → lần lọc sau chỉ vài giây.
"""
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


def _app(root):
    app = _apps.get(root)
    if app is None:
        _apps.clear()  # commit dữ liệu mới → bỏ bản cũ cho nhẹ bộ nhớ
        app = _apps[root] = HeadlessApp(os.path.join(root, 'App.py'))
    return app


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
            req = msg['req']
            app = _app(msg['root'])
            export_kpi._app = app
            items, status = run_request.compute(app, export_kpi, report_doc, filters_probe, req,
                                                req['name'], req.get('nav'))
            res = {'id': msg.get('id'), 'status': status, 'items': items, 'secs': round(time.time() - t, 1)}
        except Exception as e:  # noqa: BLE001
            traceback.print_exc()
            res = {'id': msg.get('id'), 'error': f'{type(e).__name__}: {e}'[:500]}
        out.write(json.dumps(res, ensure_ascii=False) + '\n')
        out.flush()


if __name__ == '__main__':
    main()
