"""Xuất toàn bộ báo cáo tab "📊 BÁO CÁO KPI" của App.py ra JSON cho app native.

Chạy chính App.py (headless.py) với từng lựa chọn Ngày × ĐDKD × Báo cáo, ghi lại
bảng/thẻ/nhận xét (report_doc.py). Không viết lại logic báo cáo nào.

Biến thể xuất sẵn (mỗi tháng):
  - Tất cả ĐDKD: mọi ngày từ đầu tháng → ngày có data mới nhất
  - Từng ĐDKD (1 người): ngày mặc định (T-1 giờ VN, giống Streamlit)

  out/kpi/<Thang>/index.json
  out/kpi/<Thang>/<CODE>/<yyyy-mm-dd>.json             (Tất cả)
  out/kpi/<Thang>/<CODE>/<yyyy-mm-dd>__<nv-slug>.json  (1 ĐDKD)
"""
import calendar
import datetime as dt
import hashlib
import json
import multiprocessing as mp
import os
import re
import shutil
import sys
import time
import unicodedata
import warnings

NAV_KPI = '📊 BÁO CÁO KPI'
_app = None  # HeadlessApp riêng mỗi tiến trình


def slug(name):
    s = unicodedata.normalize('NFD', name.replace('Đ', 'D').replace('đ', 'd'))
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-zA-Z0-9]+', '-', s).strip('-').lower()


def _init(app_path):
    global _app
    if _app is not None and _app.app_path == os.path.abspath(app_path):
        return  # đã nạp sẵn ở tiến trình cha (fork kế thừa cache data)
    warnings.filterwarnings('ignore')
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from headless import HeadlessApp
    _app = HeadlessApp(app_path)


def _state(mk, day, nv, label=None):
    s = {'report_month_key': mk, 'ddkd': [nv] if nv else [], 'main_nav_section': NAV_KPI}
    if day is not None:
        s['ngay'] = day
    if label is not None:
        s[f'kpi_{mk}'] = label
    return s


def _task(args):
    """1 tháng × 1 ngày × 1 bộ lọc → JSON của tất cả báo cáo KPI."""
    import report_doc
    mk, iso, nv, reports, out_dir = args
    day = dt.date.fromisoformat(iso)
    written, errors = [], []
    t0 = time.time()
    for code, label in reports:
        blocks, _ns, status = _app.run(_state(mk, day, nv, label))
        try:
            items = report_doc.convert(blocks)
        except Exception as e:
            items, status = [], f'error: convert {type(e).__name__}: {e}'
        if status.startswith('error'):
            errors.append(f'{mk} {iso} {nv or "Tất cả"} {code}: {status}')
            items.append({'t': 'msg', 'lv': 'error', 'x': 'Báo cáo lỗi khi xuất: ' + status[7:]})
        doc = {'code': code, 'name': label, 'month_key': mk, 'date': iso,
               'filter': [nv] if nv else [], 'items': items}
        fn = f'{iso}__{slug(nv)}.json' if nv else f'{iso}.json'
        path = os.path.join(out_dir, code, fn)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as fh:
            json.dump(doc, fh, ensure_ascii=False, separators=(',', ':'))
        written.append(code)
    return mk, iso, nv, len(written), errors, time.time() - t0


def month_fingerprint(repo, app_path, folder):
    h = hashlib.sha256()
    h.update(open(app_path, 'rb').read())
    for f in ('headless.py', 'report_doc.py', 'export_kpi.py'):
        h.update(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f), 'rb').read())
    d = os.path.join(repo, 'data', folder)
    for root, _, files in sorted(os.walk(d)):
        for fn in sorted(files):
            p = os.path.join(root, fn)
            h.update(fn.encode())
            h.update(open(p, 'rb').read())
    return h.hexdigest()[:16]


def plan_month(app_path, mk, now_utc):
    """Chạy App.py 1 lần để lấy danh sách báo cáo, ĐDKD, ngày có data."""
    _init(app_path)
    blocks, ns, status = _app.run(_state(mk, None, None))
    cfg = ns['MONTH_OPTIONS'][mk]
    y, m = cfg['year'], cfg['month']
    start = dt.date(y, m, 1)
    end = dt.date(y, m, calendar.monthrange(y, m)[1])
    vn = (now_utc + dt.timedelta(hours=7)).date()
    default = min(max(vn - dt.timedelta(days=1), start), end)
    df = ns.get('df')
    data_max = None
    if df is not None and 'date' in df.columns and df['date'].notna().any():
        data_max = max(df['date'].dropna())
    last = min(end, max(default, data_max or start))
    dates = [start + dt.timedelta(days=i) for i in range((last - start).days + 1)]
    reports = [(code, label) for label, code in ns['kpi_map'].items()]
    nv = list(ns.get('nv_list') or [])
    return {
        'month_key': mk, 'month_label': cfg['label'], 'year': y, 'month': m,
        'dates': [d.isoformat() for d in dates], 'default_date': default.isoformat(),
        'data_max_date': data_max.isoformat() if data_max else None,
        'reports': reports, 'nv': nv,
    }


def _default_date(y, m, now_utc):
    start = dt.date(y, m, 1)
    end = dt.date(y, m, calendar.monthrange(y, m)[1])
    vn = (now_utc + dt.timedelta(hours=7)).date()
    return min(max(vn - dt.timedelta(days=1), start), end)


def export_month(app_path, mk, out_root, workers, prev_root=None, now_utc=None, mode='full'):
    """mode:
      'default' — chỉ ngày mặc định (Tất cả + từng ĐDKD); các ngày khác giữ từ lần trước
      'history' — các ngày còn lại của tháng (Tất cả), dùng sau khi đã publish 'default'
      'full'    — cả hai
    Tháng đã qua: chỉ ngày cuối tháng. Tháng không đổi (fingerprint) → dùng lại bản trước."""
    now_utc = now_utc or dt.datetime.utcnow()
    repo = os.path.dirname(os.path.abspath(app_path))
    out_dir = os.path.join(out_root, 'kpi', mk)

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from app_logic import load as _load_ns  # đọc MONTH_OPTIONS
    cfg = _load_ns(app_path, log=lambda m: None)['MONTH_OPTIONS'][mk]
    fp = month_fingerprint(repo, app_path, cfg.get('folder', mk))
    default = _default_date(cfg['year'], cfg['month'], now_utc).isoformat()
    month_end = dt.date(cfg['year'], cfg['month'], calendar.monthrange(cfg['year'], cfg['month'])[1])
    past_month = month_end < (now_utc + dt.timedelta(hours=7)).date() - dt.timedelta(days=1)

    prev_dir = os.path.join(prev_root, 'kpi', mk) if prev_root else None
    pidx = None
    if prev_dir and os.path.isfile(os.path.join(prev_dir, 'index.json')):
        pidx = json.load(open(os.path.join(prev_dir, 'index.json'), encoding='utf-8'))
    same = bool(pidx and pidx.get('fingerprint') == fp and pidx.get('default_date') == default)

    if same and (past_month or pidx.get('complete')):
        if os.path.abspath(prev_dir) != os.path.abspath(out_dir):
            shutil.rmtree(out_dir, ignore_errors=True)
            shutil.copytree(prev_dir, out_dir)
        print(f'↺ {mk}: không đổi, dùng lại bản trước', file=sys.stderr)
        return pidx, []

    plan = plan_month(app_path, mk, now_utc)
    others = [d for d in plan['dates'] if d != plan['default_date']]
    if past_month:
        others = []

    # Giữ các file ngày cũ từ lần trước (sẽ ghi đè phần tính lại)
    if prev_dir and os.path.isdir(prev_dir) and os.path.abspath(prev_dir) != os.path.abspath(out_dir) \
            and mode == 'default':
        shutil.rmtree(out_dir, ignore_errors=True)
        shutil.copytree(prev_dir, out_dir)
    elif mode != 'history':
        shutil.rmtree(out_dir, ignore_errors=True)
    os.makedirs(out_dir, exist_ok=True)

    tasks = []
    if mode in ('default', 'full'):
        tasks.append((mk, plan['default_date'], None, plan['reports'], out_dir))
        tasks += [(mk, plan['default_date'], nv, plan['reports'], out_dir) for nv in plan['nv']]
    if mode in ('history', 'full'):
        tasks += [(mk, d, None, plan['reports'], out_dir) for d in reversed(others)]

    errors = []
    t0 = time.time()

    def _log(i, res):
        m, iso, nv, n, errs, sec = res
        errors.extend(errs)
        print(f'  {mk} [{i}/{len(tasks)}] {iso} {nv or "Tất cả"}: {n} báo cáo, {sec:.0f}s', file=sys.stderr)

    if tasks:
        # Tiến trình cha chạy ca đầu (nạp Excel + làm nóng cache của mọi báo cáo),
        # rồi fork: tiến trình con kế thừa cache, không phải đọc lại data.
        _log(1, _task(tasks[0]))
        rest = tasks[1:]
        if rest:
            ctx = mp.get_context('fork' if sys.platform != 'win32' else 'spawn')
            with ctx.Pool(min(workers, len(rest)), initializer=_init, initargs=(app_path,)) as pool:
                for i, res in enumerate(pool.imap_unordered(_task, rest), 2):
                    _log(i, res)
    print(f'✓ {mk} ({mode}): {len(tasks)} biến thể × {len(plan["reports"])} báo cáo trong '
          f'{time.time() - t0:.0f}s', file=sys.stderr)

    # Ngày đang có file "Tất cả" (kể cả giữ lại từ lần trước)
    have = sorted(d for d in plan['dates'] if os.path.isfile(os.path.join(out_dir, 'TURNOVER', f'{d}.json')))
    if past_month:
        have = [plan['default_date']]
    index = {
        'schema': 1, 'fingerprint': fp,
        **{k: plan[k] for k in ('month_key', 'month_label', 'year', 'month',
                                'default_date', 'data_max_date', 'nv')},
        'dates': have,
        # các ngày cũ giữ lại ở lượt 'default' có thể là số cũ → chưa 'complete'
        'complete': mode in ('history', 'full') or past_month or not others,
        'reports': [{'code': c, 'name': l} for c, l in plan['reports']],
        'nv_slugs': {nv: slug(nv) for nv in plan['nv']},
        'nv_dates': [plan['default_date']],
        'errors': errors,
    }
    with open(os.path.join(out_dir, 'index.json'), 'w', encoding='utf-8') as fh:
        json.dump(index, fh, ensure_ascii=False, indent=1)
    return index, errors
