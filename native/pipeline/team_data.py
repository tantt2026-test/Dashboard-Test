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
    return fn


def _header_row(a, b, max_rows=15):
    n = min(len(a), len(b), max_rows)
    for i in range(n):
        ra = [str(x).strip() for x in a.iloc[i].tolist()]
        rb = [str(x).strip() for x in b.iloc[i].tolist()]
        if ra == rb and sum(1 for x in ra if x and x.lower() != 'nan') >= 3:
            return i
    return None


def combine_xlsx(pa, pb, out):
    a = pd.read_excel(pa, header=None)
    b = pd.read_excel(pb, header=None)
    h = _header_row(a, b) if a.shape[1] == b.shape[1] else None
    if h is None:
        shutil.copyfile(pa, out)  # khác mẫu → không ghép được, giữ bản A
        return False
    body_b = b.iloc[h + 1:]
    body_b = body_b[body_b.notna().any(axis=1)]
    _write_xlsx(pd.concat([a, body_b], ignore_index=True), out)
    return True


def _write_xlsx(df, out):
    """xlsxwriter (nhanh hơn openpyxl) + ngày tạo cố định → cùng data thì file giống hệt từng byte
    (export_kpi so dấu vân tay file để biết tháng nào không đổi)."""
    import datetime as dt
    with pd.ExcelWriter(out, engine='xlsxwriter') as w:
        df.to_excel(w, header=False, index=False)
        w.book.set_properties({'created': dt.datetime(2000, 1, 1)})


def _combine_job(args):
    pa, pb, dst, label = args
    try:
        combine_xlsx(pa, pb, dst)
    except Exception as e:  # noqa: BLE001
        print(f'⚠ ghép {label} lỗi: {e}', file=sys.stderr)
        shutil.copyfile(pa, dst)


def combine_dirs(da, db, out, workers=None):
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
                jobs.append((os.path.join(ma, fa[k]), os.path.join(mb, fb[k]), dst, f'{m}/{name}'))
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
