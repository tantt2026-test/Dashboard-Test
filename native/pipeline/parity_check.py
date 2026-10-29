"""Đối chiếu số trên app (logic Dart) với Streamlit (build_turnover_report của App.py).

  python parity_check.py --app ../Dashboard-Test/App.py --json out/ --dart-app ../app

Mỗi ngày trong tháng × (Tất cả ĐDKD + từng NV + nhiều tổ hợp NV ngẫu nhiên):
so từng ô hiển thị (chuỗi đã format) của bảng, dòng tổng, nhận xét Top/Bottom.
Thoát mã 1 nếu có bất kỳ ô nào lệch → GitHub Action không publish.
"""
import argparse
import json
import os
import random
import subprocess
import sys

import app_logic

COLS = ['STT', 'Tên NVBH', 'Chỉ Tiêu Doanh Số', 'Thực Hiện Ngày', 'Doanh Số MTD',
        '% MTD', 'GAP', 'Bình quân ngày']


def py_display(rep):
    """Format y như nhánh TURNOVER trong App.py (df_display)."""
    d = rep.copy()
    for col in ['Chỉ Tiêu Doanh Số', 'Thực Hiện Ngày', 'Doanh Số MTD', 'GAP']:
        d[col] = d[col].apply(lambda x: f'{x:,.0f}'.replace(',', '.') if isinstance(x, (int, float)) else x)
    d['Bình quân ngày'] = d['Bình quân ngày'].apply(
        lambda x: f'{x:,.1f}'.replace(',', '.') if isinstance(x, (int, float)) else x)
    rows = []
    for _, r in d.iterrows():
        row = {c: str(r[c]) for c in COLS}
        row['code'] = str(r['Mã NVBH'])
        rows.append(row)
    return rows


def py_notes(rep):
    """Nhận xét Top/Bottom 3 — copy logic nhánh TURNOVER của App.py."""
    total_row = rep.iloc[-1]
    df_eval = rep.iloc[:-1].copy()
    df_eval['_pct_val'] = df_eval['% MTD'].str.replace('%', '').astype(float)
    s = df_eval.sort_values(by='_pct_val', ascending=False)
    top3 = ', '.join(f"{r['Tên NVBH']} ({r['% MTD']})" for _, r in s.head(3).iterrows())
    bottom3 = ', '.join(f"{r['Tên NVBH']} ({r['% MTD']})" for _, r in s.tail(3).iloc[::-1].iterrows())
    return top3, bottom3, float(total_row['Doanh Số MTD']), float(total_row['Thực Hiện Ngày']), total_row['% MTD']


FMT_CASES = [[0.25, 1], [0.35, 1], [2.5, 0], [3.5, 0], [-2.5, 0], [0.125, 2], [-0.4, 0],
             [12.25, 1], [99.95, 1], [1234567.5, 0], [-1609125.65, 1], [64.55, 1],
             [0.05, 1], [0.15, 1], [1e9 + 0.5, 0], [37.349999999999994, 1]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--app', required=True)
    ap.add_argument('--json', required=True, help='thư mục output của export_reports.py')
    ap.add_argument('--dart-app', required=True, help='thư mục project Flutter')
    ap.add_argument('--combos', type=int, default=25, help='số tổ hợp NV ngẫu nhiên mỗi ngày')
    a = ap.parse_args()

    json_dir = os.path.abspath(a.json)
    dart_app = os.path.abspath(a.dart_app)
    ns = app_logic.load(os.path.abspath(a.app))
    manifest = json.load(open(os.path.join(json_dir, 'manifest.json'), encoding='utf-8'))
    rnd = random.Random(42)
    total_cells = 0
    mismatches = []

    for m in manifest['months']:
        mk = m['key']
        path = os.path.join(json_dir, 'turnover', f'{mk}.json')
        data = json.load(open(path, encoding='utf-8'))
        app_logic.select_month(ns, mk)
        df, _ = ns['load_main_data'](mk)
        targets = ns['get_turnover_targets']()
        import datetime as dt

        cases = []
        for iso in data['days']:
            filters = [[]] + [[n] for n in data['nv']]
            for _ in range(a.combos):
                k = rnd.randint(2, max(2, len(data['nv'])))
                filters.append(rnd.sample(data['nv'], min(k, len(data['nv']))))
            cases += [{'date': iso, 'filter': f} for f in filters]

        proc = subprocess.run(['dart', 'run', 'tool/parity_cli.dart', path], cwd=dart_app,
                              input=json.dumps({'cases': cases, 'fmt': FMT_CASES}, ensure_ascii=False) + '\n',
                              capture_output=True, text=True)
        if proc.returncode != 0:
            print(proc.stderr, file=sys.stderr)
            sys.exit(2)
        dart = json.loads(proc.stdout)

        for case, got in zip(cases, dart['cases']):
            d = dt.date.fromisoformat(case['date'])
            rep, team_tgt, _ = ns['build_turnover_report'](df, d, targets, case['filter'])
            exp_rows = py_display(rep)
            exp_body, exp_total = exp_rows[:-1], exp_rows[-1]
            top3, bottom3, t_mtd, t_today, t_pct = py_notes(rep)
            exp_result = (f'Đạt {t_mtd:,.0f} / {team_tgt:,.0f} VNĐ ({t_pct} MTD). '
                          f'Thực hiện ngày: {t_today:,.0f} VNĐ.')
            tag = f"{mk} {case['date']} lọc={case['filter'] or 'Tất cả'}"

            if len(exp_body) != len(got['rows']):
                mismatches.append(f'{tag}: số dòng Python={len(exp_body)} App={len(got["rows"])}')
                continue
            for i, (e, g) in enumerate(zip(exp_body, got['rows'])):
                for c in COLS + ['code']:
                    total_cells += 1
                    if e[c] != g[c]:
                        mismatches.append(f'{tag} dòng {i + 1} [{c}]: Python={e[c]!r} App={g[c]!r}')
            for c in COLS:
                total_cells += 1
                if exp_total[c] != got['total'][c]:
                    mismatches.append(f'{tag} TỔNG [{c}]: Python={exp_total[c]!r} App={got["total"][c]!r}')
            for name, e, g in (('Top3', top3, got['top3']), ('Bottom3', bottom3, got['bottom3']),
                               ('Kết quả', exp_result, got['result_text'])):
                total_cells += 1
                if e != g:
                    mismatches.append(f'{tag} {name}: Python={e!r} App={g!r}')

        for (x, nd), g in zip(FMT_CASES, dart['fmt']):
            exp = {'fixed': f'{x:.{nd}f}', 'thousands': f'{x:,.{nd}f}', 'round_str': str(round(x, nd))}
            for k in exp:
                total_cells += 1
                if exp[k] != g[k]:
                    mismatches.append(f'format {x}/{nd} {k}: Python={exp[k]!r} App={g[k]!r}')
        print(f'✓ {mk}: {len(cases)} ca kiểm tra', file=sys.stderr)

    print(f'\nĐã so {total_cells:,} ô. Lệch: {len(mismatches)}')
    for line in mismatches[:50]:
        print('  ✗', line)
    sys.exit(1 if mismatches else 0)


if __name__ == '__main__':
    main()
