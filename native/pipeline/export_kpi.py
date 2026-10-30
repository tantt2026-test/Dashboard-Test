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
# Giai đoạn cuối: các tab còn lại của App.py (code app → tên tab trên Streamlit)
TAB_CODES = {'🗺️ MCP VISIT': 'TAB_MCP', '📦 TRACKING MBS - CAT': 'TAB_CAT',
             '🏷️ TRACKING MBS - BRAND': 'TAB_BRAND', '📋 DSKH_Combo OFF': 'TAB_OFF',
             '📋 DSKH_Combo ON': 'TAB_ON'}
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
    print(f'  [worker {os.getpid()}] sẵn sàng', file=sys.stderr, flush=True)


def _state(mk, day, nv, label=None, nav=NAV_KPI):
    # month_select_box = None: ô chọn tháng của App.py nhớ tháng của lần chạy trước → nếu không
    # xoá, App.py tự đổi về tháng cũ (lỗi báo cáo 4-7 ra Turnover khi xuất tháng 9 rồi tháng 10)
    s = {'report_month_key': mk, 'month_select_box': None, 'ddkd': [nv] if nv else [],
         'main_nav_section': nav}
    if day is not None:
        s['ngay'] = day
    if label is not None and nav == NAV_KPI:
        s[f'kpi_{mk}'] = label
    return s


def _reset_widgets():
    """Xoá giá trị các ô lọc phụ của lần chạy trước (giữ ô chính) → mỗi báo cáo bắt đầu mặc định."""
    keep = {'report_month_key', 'month_select_box', 'ddkd', 'main_nav_section', 'ngay'}
    for k in list(_app.rec.session_state):
        if k not in keep and not str(k).startswith('kpi_') and not str(k).startswith('_'):
            _app.rec.session_state.pop(k, None)


def _task(args):
    """1 tháng × 1 ngày × 1 bộ lọc → JSON các báo cáo. probe=True (ngày mặc định, Tất cả):
    chạy thử từng ô lọc (filters_probe) + xuất sẵn bản tính lại cho ô lọc kiểu tính lại."""
    import filters_probe
    import report_doc
    mk, iso, nv, reports, out_dir, probe = args
    day = dt.date.fromisoformat(iso)
    written, errors = [], []
    t0 = time.time()
    for code, label, nav in reports:
        _reset_widgets()
        st = _state(mk, day, nv, label, nav)
        blocks, _ns, status = _app.run(st)
        if any(b['kind'] == 'widget_miss' and str(b.get('key', '')).startswith('kpi_') for b in blocks):
            status = f'error: SELECT_MISS không chọn được báo cáo "{label}" (App.py hiện báo cáo khác)'
        base = f'{iso}__{slug(nv)}' if nv else iso
        main = {}
        try:
            items = report_doc.convert(blocks)
            filters_probe.annotate_totals(items)
            if probe and not status.startswith('error'):
                nvar = [0]

                def variant_cb(key, opt, v_items, code=code):
                    nvar[0] += 1
                    fn = f'{base}__w{nvar[0]}.json'
                    filters_probe.annotate_totals(v_items)
                    with open(os.path.join(out_dir, code, fn), 'w', encoding='utf-8') as fh:
                        json.dump({'items': report_doc.strip_private(v_items)}, fh,
                                  ensure_ascii=False, separators=(',', ':'))
                    return fn
                os.makedirs(os.path.join(out_dir, code), exist_ok=True)
                main = filters_probe.annotate(_app, st, items, blocks, variant_cb)
        except Exception as e:
            items, status = [], f'error: convert {type(e).__name__}: {e}'
        if status.startswith('error'):
            errors.append(f'{mk} {iso} {nv or "Tất cả"} {code}: {status}')
            items.append({'t': 'msg', 'lv': 'error', 'x': 'Báo cáo lỗi khi xuất: ' + status[7:]})
        doc = {'code': code, 'name': label, 'month_key': mk, 'date': iso,
               'filter': [nv] if nv else [], 'items': report_doc.strip_private(items)}
        if main:
            doc['main'] = report_doc.strip_private(main)
        path = os.path.join(out_dir, code, base + '.json')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as fh:
            json.dump(doc, fh, ensure_ascii=False, separators=(',', ':'))
        written.append(code)
    return mk, iso, nv, len(written), errors, time.time() - t0, _task_id(nv, reports, probe)


def _task_id(nv, reports, probe):
    """Tên tác vụ để ghi thời gian chạy (chia việc cho các máy song song ở lần sau)."""
    return f'nv:{nv}' if nv else (reports[0][0] if probe and len(reports) == 1 else 'day')


def month_fingerprint(repo, app_path, folder):
    h = hashlib.sha256()
    h.update(open(app_path, 'rb').read())
    for f in ('headless.py', 'report_doc.py', 'export_kpi.py', 'filters_probe.py'):
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
    reports = [(code, label, NAV_KPI) for label, code in ns['kpi_map'].items()]
    # các tab còn lại (giai đoạn cuối): MCP VISIT, TRACKING MBS CAT/BRAND, DSKH Combo OFF/ON
    for nav in ns.get('_nav_opts') or []:
        if nav in TAB_CODES:
            reports.append((TAB_CODES[nav], nav, nav))
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


def _split(tasks, shard, weights):
    """Chia tác vụ cho máy số i/n: tác vụ nặng trước, mỗi tác vụ vào máy đang nhẹ nhất
    (thời gian lấy từ lần chạy trước; chưa có thì coi như 60s)."""
    i, n = shard
    load = [0.0] * n
    mine = []
    order = sorted(tasks, key=lambda t: -weights.get(_task_id(t[2], t[3], t[5]), 60.0))
    for t in order:
        k = min(range(n), key=lambda j: load[j])
        load[k] += weights.get(_task_id(t[2], t[3], t[5]), 60.0)
        if k == i:
            mine.append(t)
    return mine


def export_month(app_path, mk, out_root, workers, prev_root=None, now_utc=None, mode='full', shard=None):
    """mode:
      'default' — chỉ ngày mặc định (Tất cả + từng ĐDKD); các ngày khác giữ từ lần trước
      'history' — các ngày còn lại của tháng (Tất cả), dùng sau khi đã publish 'default'
      'full'    — cả hai
    shard=(i, n): chỉ tính phần việc của máy i trong n máy chạy song song (lượt 'default');
      không chép bản cũ vào — merge_shards.py ghép bản cũ + phần của các máy.
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

    # Tháng đã qua ở lượt nhanh: dùng lại bản cũ (dù App.py đổi) — lượt 2 mới tính lại
    if past_month and mode == 'default' and pidx is not None and not same:
        if os.path.abspath(prev_dir) != os.path.abspath(out_dir):
            shutil.rmtree(out_dir, ignore_errors=True)
            shutil.copytree(prev_dir, out_dir)
        pidx['complete'] = False
        with open(os.path.join(out_dir, 'index.json'), 'w', encoding='utf-8') as fh:
            json.dump(pidx, fh, ensure_ascii=False, indent=1)
        print(f'↺ {mk}: tháng đã qua — tạm dùng bản trước, lượt 2 sẽ tính lại', file=sys.stderr)
        return pidx, []
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
            and mode == 'default' and shard is None:
        shutil.rmtree(out_dir, ignore_errors=True)
        shutil.copytree(prev_dir, out_dir)
    elif mode != 'history':
        shutil.rmtree(out_dir, ignore_errors=True)
    os.makedirs(out_dir, exist_ok=True)

    kpi_reports = [r for r in plan['reports'] if r[2] == NAV_KPI]
    tasks = []
    if mode in ('default', 'full'):
        # ngày mặc định, Tất cả: mỗi báo cáo/tab 1 tác vụ (có chạy thử ô lọc) → chạy song song
        tasks += [(mk, plan['default_date'], None, [r], out_dir, True) for r in plan['reports']]
        tasks += [(mk, plan['default_date'], nv, kpi_reports, out_dir, False) for nv in plan['nv']]
    if mode in ('history', 'full'):
        tasks += [(mk, d, None, kpi_reports, out_dir, False) for d in reversed(others)]
    if mode == 'history' and past_month:
        # tháng đã qua được tính ở lượt 2 (ngày cuối tháng, có đo ô lọc)
        tasks += [(mk, plan['default_date'], None, [r], out_dir, True) for r in plan['reports']]
        tasks += [(mk, plan['default_date'], nv, kpi_reports, out_dir, False) for nv in plan['nv']]

    weights = {}
    for d in (prev_dir, out_dir):
        try:
            weights.update(json.load(open(os.path.join(d, 'timing.json'), encoding='utf-8')))
        except Exception:
            pass
    if shard is not None:
        tasks = _split(tasks, shard, weights)
    errors = []
    t0 = time.time()
    timing = {}

    def _log(i, res):
        m, iso, nv, n, errs, sec, tid = res
        errors.extend(errs)
        if tid != 'day':
            timing[tid] = round(sec, 1)
        print(f'  {mk} [{i}/{len(tasks)}] {iso} {nv or "Tất cả"}: {n} báo cáo, {sec:.0f}s', file=sys.stderr)

    if tasks:
        # 'spawn' (không dùng fork): pandas 3 dùng pyarrow có luồng chạy ngầm, fork tiến trình
        # đang có luồng → tiến trình con treo (deadlock) trên Linux. Mỗi tiến trình con tự nạp data.
        ctx = mp.get_context('spawn')
        with ctx.Pool(min(workers, len(tasks)), initializer=_init, initargs=(app_path,)) as pool:
            for i, res in enumerate(pool.imap_unordered(_task, tasks), 1):
                _log(i, res)
    print(f'✓ {mk} ({mode}): {len(tasks)} biến thể × {len(plan["reports"])} báo cáo trong '
          f'{time.time() - t0:.0f}s', file=sys.stderr)

    # Ngày đang có file "Tất cả" (kể cả giữ lại từ lần trước)
    have = sorted(d for d in plan['dates'] if os.path.isfile(os.path.join(out_dir, 'TURNOVER', f'{d}.json')))
    if past_month:
        have = [plan['default_date']]
    if timing:
        with open(os.path.join(out_dir, 'timing.json'), 'w', encoding='utf-8') as fh:
            json.dump({**weights, **timing}, fh, ensure_ascii=False, indent=0)
    index = {
        'schema': 1, 'fingerprint': fp,
        'plan_dates': [] if past_month else plan['dates'],  # merge_shards.py tính lại 'dates'
        **{k: plan[k] for k in ('month_key', 'month_label', 'year', 'month',
                                'default_date', 'data_max_date', 'nv')},
        'dates': have,
        # các ngày cũ giữ lại ở lượt 'default' có thể là số cũ → chưa 'complete'
        'complete': mode in ('history', 'full') or past_month or not others,
        'reports': [{'code': c, 'name': l, 'group': 'kpi' if n == NAV_KPI else 'tab'}
                    for c, l, n in plan['reports']],
        'tab_dates': [plan['default_date']],
        'nv_slugs': {nv: slug(nv) for nv in plan['nv']},
        'nv_dates': [plan['default_date']],
        'errors': errors,
    }
    with open(os.path.join(out_dir, 'index.json'), 'w', encoding='utf-8') as fh:
        json.dump(index, fh, ensure_ascii=False, indent=1)
    return index, errors
