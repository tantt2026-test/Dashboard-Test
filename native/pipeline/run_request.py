"""Tính 1 báo cáo theo lựa chọn bộ lọc bằng chính App.py — dùng cho:
  - GitHub Action "filter-run" (app nhờ tính tổ hợp chưa có)
  - precompute_filters.py (tính sẵn tổ hợp sau mỗi lần sync)
Kết quả lưu ở branch `filters`: <source_commit[:12]>/<mã tổ hợp>.json

Mã tổ hợp = sha1 của JSON chuẩn hoá (khoá sắp xếp, không khoảng trắng, giữ Unicode) —
app (Dart, lib/data/filter_cache.dart) tính y hệt.
"""
import datetime as dt
import hashlib
import json


def canonical(req):
    """Chỉ giữ phần quyết định kết quả; giá trị list giữ thứ tự (giống multiselect)."""
    r = {
        'month_key': req['month_key'],
        'date': req['date'][:10],
        'code': req['code'],
        'ddkd': list(req.get('ddkd') or []),
        'values': {k: v for k, v in sorted((req.get('values') or {}).items()) if v not in (None, '', [])},
    }
    # Sale Sup khác team Tân: thêm team + commit data Vyntt (mã tổ hợp team Tân giữ như cũ)
    if req.get('team') and req.get('team') != 'tan':
        r['team'] = req['team']
        r['dsc'] = req.get('dsc') or ''
    return json.dumps(r, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def key_of(req):
    return hashlib.sha1(canonical(req).encode('utf-8')).hexdigest()[:20]


def compute(app, export_kpi, report_doc, filters_probe, req, name, nav=None):
    """Mở báo cáo (App.py đặt mặc định) rồi áp lựa chọn — như người dùng thật."""
    nav = nav or export_kpi.NAV_KPI
    if str(name).startswith(getattr(export_kpi, 'SUP_PREFIX', '\0')):
        nav = export_kpi.SUP_NAV
    day = dt.date.fromisoformat(req['date'][:10])
    export_kpi._reset_widgets()
    base = export_kpi._state(req['month_key'], day, None, name, nav)
    base['ddkd'] = list(req.get('ddkd') or [])
    blocks, _, _ = app.run(dict(base))
    raw = {b['key']: dict(zip(b.get('options') or [], b.get('_raw_options') or []))
           for b in blocks if b['kind'] == 'widget' and b.get('key')}
    kinds = {b['key']: b.get('wkind') for b in blocks if b['kind'] == 'widget' and b.get('key')}
    state = dict(base)
    for k, v in (req.get('values') or {}).items():
        if kinds.get(k) == 'date_input' and isinstance(v, list) and len(v) == 2:
            state[k] = tuple(dt.date.fromisoformat(x[:10]) for x in v)
        elif isinstance(v, list):
            m = raw.get(k, {})
            state[k] = [m.get(str(x), x) for x in v]
        else:
            state[k] = v
    blocks, _, status = app.run(state)
    items = report_doc.convert(blocks)
    filters_probe.annotate_totals(items)
    return report_doc.strip_private(items), status


def compute_team(apps, export_kpi, report_doc, filters_probe, req, name, nav=None):
    """Sale Sup 'Cả 2': apps = {'all': app data ghép, 'tan': ..., 'vy': ...} → bảng tách theo team
    + dòng Total chung (team_merge.py). Lọc 1 ĐDKD / thiếu app team → chỉ tính trên data ghép."""
    def one(app):
        export_kpi._app = app
        return compute(app, export_kpi, report_doc, filters_probe, req, name, nav)
    items, status = one(apps['all'])
    if req.get('ddkd') or not apps.get('tan') or not apps.get('vy'):  # 1 NV chỉ thuộc 1 team
        return items, status
    import team_merge
    it_t, _ = one(apps['tan'])
    it_v, _ = one(apps['vy'])
    export_kpi._app = apps['all']
    import os
    labels, cwd = [], os.getcwd()
    for k in ('tan', 'vy'):
        try:  # tên Sup đọc từ Target_KPI của team (đường dẫn data tương đối theo repo)
            os.chdir(apps[k].repo)
            labels.append('SS ' + apps[k].ns['_ss_name_m'](req['month_key']))
        except Exception:  # noqa: BLE001  App.py cũ chưa có _ss_name_m
            labels = None
            break
        finally:
            os.chdir(cwd)
    return team_merge.merge_items(it_t, it_v, items, labels), status
