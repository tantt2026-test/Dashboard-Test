"""Bộ data theo Sale Sup cho app native: 'tan' (data/ của Dashboard-Test), 'vy' (data/ của repo
Tantt2026/Vyntt_Dashboard) và 'all' (ghép 2 bộ — cùng 1 App.py tính trên data gộp, như 1 team lớn).

  python team_data.py combine <data_tan> <data_vy> <out_data>
  python team_data.py prepare <team> <out_root> [--app App.py] [--tan data] [--vy data_vy]
      → out_root/App.py + out_root/data (để HeadlessApp / export_reports chạy như repo thường)

Ghép file: 2 file cùng loại do Onetech xuất cùng mẫu → giữ phần đầu (tiêu đề/bộ lọc + dòng tên cột)
của file A rồi nối các dòng dữ liệu của file B (bỏ phần đầu của B). Dòng tên cột = dòng đầu tiên
giống hệt nhau ở cả 2 file (≥3 ô có chữ). File chỉ 1 bên có → chép nguyên.
"""
import os
import shutil
import sys

import pandas as pd

# File Onetech có ô số ghi 'Infinity' / 'NaN' (vd TARGETACTUAL BY OUTLET T11) → openpyxl lỗi khi đọc
# và bỏ cả file B khi ghép. Đọc thành ô trống (giống App.py).
try:
    from openpyxl.worksheet import _reader as _oxr
    if not getattr(_oxr, '_inf_ok', False):
        _oxr_cast = _oxr._cast_number

        def _cast_number_safe(value):
            try:
                return _oxr_cast(value)
            except ValueError:
                if str(value).strip().lower().lstrip('+-') in ('infinity', 'inf', 'nan'):
                    return None
                raise
        _oxr._cast_number = _cast_number_safe
        _oxr._inf_ok = True
except Exception:  # noqa: BLE001
    pass

COMBINE_VER = '4'
try:
    import python_calamine  # noqa: F401
    _HAS_CALAMINE = True
except Exception:  # noqa: BLE001
    _HAS_CALAMINE = False  # đổi khi đổi cách ghép → bỏ kết quả ghép đã lưu (cache)

TEAMS = {
    'tan': {'name': 'Trương Thanh Tân', 'prefix': ''},
    'vy': {'name': 'Nguyễn Thị Tường Vy', 'prefix': 't/vy/', 'repo': 'Tantt2026/Vyntt_Dashboard'},
    'all': {'name': 'Cả 2 Sup', 'prefix': 't/all/'},
}


def _key(fn):
    """Tên chung để ghép: file Combo mỗi team đặt tên khác (Tân_Combo… / Vy_Combo…)."""
    low = fn.lower()
    if 'combo' in low and low.endswith(('.xlsx', '.xls')):
        return 'combo_off' if 'off' in low else 'combo_on'
    # DS xét duyệt CH (Tạo mới Kênh ON): tên mới DanhSachYeuCauXetDuyetCuaHang / tên cũ DanhSachXetDuyetCuaHang
    if low.replace('_', '').startswith(('danhsachyeucauxetduyetcuahang.', 'danhsachxetduyetcuahang.')):
        return 'xet_duyet_ch'
    return fn


def _header_row(a, b, max_rows=15):
    # so không phân biệt hoa/thường: 2 team xuất file cùng mẫu nhưng có lúc lệch chữ hoa/thường
    # 1 ô tiêu đề (vd 'SaleTeam' / 'Saleteam') → so phân biệt hoa thường sẽ không khớp dòng nào,
    # combine_xlsx tưởng khác mẫu rồi bỏ hẳn file B (im lặng mất hết KPI/Target của team đó).
    n = min(len(a), len(b), max_rows)
    for i in range(n):
        ra = [str(x).strip() for x in a.iloc[i].tolist()]
        rb = [str(x).strip() for x in b.iloc[i].tolist()]
        if [x.lower() for x in ra] == [x.lower() for x in rb] and sum(
            1 for x in ra if x and x.lower() != 'nan'
        ) >= 3:
            return i
    return None


def _read_raw(p):
    """Đọc thô (header=None). App Mac có python-calamine → nhanh gấp nhiều lần openpyxl; không có
    (GitHub / Streamlit) hoặc lỗi → openpyxl như cũ. File ghép ra đọc lại giống hệt (đã so từng file)."""
    if _HAS_CALAMINE:
        try:
            return pd.read_excel(p, header=None, engine='calamine')
        except Exception:  # noqa: BLE001
            pass
    return pd.read_excel(p, header=None)


def combine_xlsx(pa, pb, out):
    a = _read_raw(pa)
    b = _read_raw(pb)
    h = _header_row(a, b) if a.shape[1] == b.shape[1] else None
    if h is None:
        shutil.copyfile(pa, out)  # khác mẫu → không ghép được, giữ bản A
        return False
    body_b = b.iloc[h + 1:]
    body_b = body_b[body_b.notna().any(axis=1)]
    _write_xlsx(pd.concat([a, body_b], ignore_index=True), out)
    return True


def _write_xlsx(df, out):
    """xlsxwriter ghi thẳng từng dòng (nhanh gấp ~2 lần df.to_excel, đọc lại ra y hệt) + ngày tạo cố
    định → cùng data thì file giống hệt từng byte (export_kpi so dấu vân tay file để biết tháng nào
    không đổi)."""
    import datetime as dt
    import xlsxwriter
    wb = xlsxwriter.Workbook(out, {
        'constant_memory': True, 'default_date_format': 'yyyy-mm-dd hh:mm:ss', 'nan_inf_to_errors': True,
        'strings_to_formulas': False, 'strings_to_urls': False, 'strings_to_numbers': False,
    })
    wb.set_properties({'created': dt.datetime(2000, 1, 1)})
    ws = wb.add_worksheet('Sheet1')
    for i, row in enumerate(df.astype(object).where(pd.notna(df), None).values.tolist()):
        ws.write_row(i, 0, row)
    wb.close()


def _combine_job(args):
    pa, pb, dst, label = args[:4]
    cached = args[4] if len(args) > 4 else None
    try:
        combine_xlsx(pa, pb, dst)
        if cached:
            try:
                shutil.copyfile(dst, cached + '.tmp')
                os.replace(cached + '.tmp', cached)
            except OSError:
                pass
    except Exception as e:  # noqa: BLE001
        print(f'⚠ ghép {label} lỗi: {e}', file=sys.stderr)
        shutil.copyfile(pa, dst)


def _file_sha(p):
    import hashlib
    h = hashlib.sha1()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def _cache_prune(cache_dir, days=4):
    import time
    lim = time.time() - days * 86400
    try:
        for f in os.listdir(cache_dir):
            fp = os.path.join(cache_dir, f)
            if os.path.isfile(fp) and os.path.getmtime(fp) < lim:
                os.remove(fp)
    except OSError:
        pass


def combine_dirs(da, db, out, workers=None, cache_dir=None):
    """cache_dir (app Mac): lưu kết quả ghép từng file theo nội dung 2 file nguồn → lần sau
    (data / App.py mới nhưng phần lớn file không đổi) chỉ ghép lại file thật sự đổi."""
    """Ghép data/ThangXX của 2 team → out/ThangXX (nhiều file cùng lúc)."""
    os.makedirs(out, exist_ok=True)
    jobs = []
    months = sorted(set(os.listdir(da) if os.path.isdir(da) else []) | set(os.listdir(db) if os.path.isdir(db) else []))
    for m in months:
        ma, mb, mo = os.path.join(da, m), os.path.join(db, m), os.path.join(out, m)
        if not (os.path.isdir(ma) or os.path.isdir(mb)):
            continue
        os.makedirs(mo, exist_ok=True)
        fa = {_key(f): f for f in (os.listdir(ma) if os.path.isdir(ma) else []) if not f.startswith(('.', '~$'))}
        fb = {_key(f): f for f in (os.listdir(mb) if os.path.isdir(mb) else []) if not f.startswith(('.', '~$'))}
        for k in sorted(set(fa) | set(fb)):
            name = fa.get(k) or fb.get(k)
            dst = os.path.join(mo, name)
            if k in fa and k in fb and name.lower().endswith(('.xlsx', '.xls')):
                pa, pb = os.path.join(ma, fa[k]), os.path.join(mb, fb[k])
                cached = None
                if cache_dir:
                    os.makedirs(cache_dir, exist_ok=True)
                    cached = os.path.join(cache_dir, f'{COMBINE_VER}_{_file_sha(pa)}_{_file_sha(pb)}.xlsx')
                    if os.path.isfile(cached):
                        shutil.copyfile(cached, dst)
                        os.utime(cached)  # còn dùng → không bị dọn
                        continue
                jobs.append((pa, pb, dst, f'{m}/{name}', cached))
            else:
                shutil.copyfile(os.path.join(ma, fa[k]) if k in fa else os.path.join(mb, fb[k]), dst)
    # file lớn trước cho chia đều
    jobs.sort(key=lambda j: -(os.path.getsize(j[0]) + os.path.getsize(j[1])))
    if jobs and workers == 1:
        for j in jobs:
            _combine_job(j)
    elif jobs:
        import multiprocessing as mp
        with mp.get_context('spawn').Pool(workers or min(6, os.cpu_count() or 2)) as pool:
            pool.map(_combine_job, jobs, chunksize=1)
    if cache_dir:
        _cache_prune(cache_dir)


def prepare(team, out_root, app='App.py', tan='data', vy='data_vy'):
    os.makedirs(out_root, exist_ok=True)
    shutil.copyfile(app, os.path.join(out_root, 'App.py'))
    dst = os.path.join(out_root, 'data')
    shutil.rmtree(dst, ignore_errors=True)
    if team == 'tan':
        shutil.copytree(tan, dst)
    elif team == 'vy':
        shutil.copytree(vy, dst)
    else:
        combine_dirs(tan, vy, dst)
    return out_root


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'combine':
        combine_dirs(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd == 'prepare':
        import argparse
        ap = argparse.ArgumentParser()
        ap.add_argument('cmd')
        ap.add_argument('team')
        ap.add_argument('out')
        ap.add_argument('--app', default='App.py')
        ap.add_argument('--tan', default='data')
        ap.add_argument('--vy', default='data_vy')
        a = ap.parse_args()
        prepare(a.team, a.out, a.app, a.tan, a.vy)
    print('ok')
