"""Xuất JSON báo cáo cho app native từ chính logic App.py.

  python export_reports.py --app ../Dashboard-Test/App.py --out out/

Kết quả:
  out/manifest.json              danh sách tháng + thời điểm cập nhật
  out/turnover/<Thang10>.json    số liệu Turnover từng NV × từng ngày trong tháng

App tự cộng/tính % khi lọc NV (lib/logic/turnover_logic.dart);
parity_check.py đối chiếu phần đó với build_turnover_report của Python.
"""
import argparse
import calendar
import datetime as dt
import json
import os
import subprocess
import sys

import app_logic

SCHEMA = 1


def _f(x):
    return float(x) if x is not None else 0.0


def month_days(year, month):
    n = calendar.monthrange(year, month)[1]
    return [dt.date(year, month, d) for d in range(1, n + 1)]


def export_turnover(ns, month_key):
    cfg = ns['MONTH_OPTIONS'][month_key]
    app_logic.select_month(ns, month_key)
    df, _mcp = ns['load_main_data'](month_key)
    targets = ns['get_turnover_targets']()

    days = {}
    total_label = ''
    nv = {}
    for d in month_days(cfg['year'], cfg['month']):
        rep, _team_tgt, title = ns['build_turnover_report'](df, d, targets, [])
        tg = ns['get_timegone_stats'](d)
        body = rep.iloc[:-1]
        total_label = str(rep.iloc[-1]['Tên NVBH'])
        rows = []
        for _, r in body.iterrows():
            code, name = str(r['Mã NVBH']), str(r['Tên NVBH'])
            nv[name] = code
            rows.append({
                'code': code,
                'name': name,
                'target': _f(r['Chỉ Tiêu Doanh Số']),
                'today': _f(r['Thực Hiện Ngày']),
                'mtd': _f(r['Doanh Số MTD']),
            })
        days[d.isoformat()] = {
            'timegone': {'total': int(tg[0]), 'elapsed': int(tg[1]),
                         'remain': int(tg[2]), 'pct': float(tg[3])},
            'rows': rows,
        }

    dates = df['date'].dropna() if 'date' in df.columns else []
    return {
        'schema': SCHEMA,
        'report': 'turnover',
        'title': title,
        'month_key': month_key,
        'month_label': cfg['label'],
        'year': cfg['year'],
        'month': cfg['month'],
        'salary_label': ns['MONTH_OPTIONS'][month_key].get('salary', {}).get('TURNOVER', ''),
        'total_label': total_label,
        'data_max_date': max(dates).isoformat() if len(dates) else None,
        'nv': sorted(nv.keys()),
        'days': days,
    }


def git_commit(repo_dir):
    sha = os.environ.get('GITHUB_SHA')
    if sha:
        return sha
    try:
        return subprocess.check_output(['git', '-C', repo_dir, 'rev-parse', 'HEAD'], text=True).strip()
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--app', required=True, help='đường dẫn App.py')
    ap.add_argument('--out', required=True)
    ap.add_argument('--months', nargs='*', help='mặc định: tất cả tháng trong MONTH_OPTIONS có thư mục data')
    a = ap.parse_args()

    out = os.path.abspath(a.out)
    app = os.path.abspath(a.app)
    repo = os.path.dirname(app)
    ns = app_logic.load(app)

    months = a.months or [k for k, v in ns['MONTH_OPTIONS'].items()
                          if os.path.isdir(os.path.join(repo, 'data', v.get('folder', k)))]
    os.makedirs(os.path.join(out, 'turnover'), exist_ok=True)

    now_vn = dt.datetime.utcnow() + dt.timedelta(hours=7)
    manifest = {
        'schema': SCHEMA,
        'generated_at': now_vn.strftime('%Y-%m-%dT%H:%M:%S+07:00'),
        'source_commit': git_commit(repo),
        'months': [],
        'reports': ['turnover'],
    }
    failed = []
    for mk in months:
        try:
            data = export_turnover(ns, mk)
        except Exception as e:  # 1 tháng lỗi không chặn tháng khác
            print(f'✗ {mk}: {e!r}', file=sys.stderr)
            failed.append(mk)
            continue
        with open(os.path.join(out, 'turnover', f'{mk}.json'), 'w', encoding='utf-8') as fh:
            json.dump(data, fh, ensure_ascii=False, separators=(',', ':'))
        manifest['months'].append({'key': mk, 'label': data['month_label'],
                                   'year': data['year'], 'month': data['month']})
        print(f'✓ {mk}: {len(data["nv"])} NV × {len(data["days"])} ngày', file=sys.stderr)

    with open(os.path.join(out, 'manifest.json'), 'w', encoding='utf-8') as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=1)
    if failed and not manifest['months']:
        sys.exit(1)


if __name__ == '__main__':
    main()
