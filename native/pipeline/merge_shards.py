"""Ghép kết quả lượt 1 của các máy chạy song song (export_reports.py --shard i/n).

  python merge_shards.py --prev _prev --shards _shards --out _reports

Bản cũ (_prev) làm nền → chép đè phần mới của từng máy → index.json mỗi tháng tính lại
danh sách ngày có file, gộp lỗi + thời gian chạy của các máy.
"""
import argparse
import json
import os
import shutil


def _load(p):
    try:
        return json.load(open(p, encoding='utf-8'))
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--prev')
    ap.add_argument('--shards', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    shards = sorted(os.path.join(a.shards, d) for d in os.listdir(a.shards)
                    if os.path.isfile(os.path.join(a.shards, d, 'manifest.json')))
    if not shards:
        raise SystemExit('Không có kết quả máy nào')
    shutil.rmtree(a.out, ignore_errors=True)
    if a.prev and os.path.isdir(a.prev):
        shutil.copytree(a.prev, a.out, ignore=shutil.ignore_patterns('.git'))
    os.makedirs(a.out, exist_ok=True)

    special = {'index.json', 'timing.json', 'manifest.json'}
    for sd in shards:
        for root, _, files in os.walk(sd):
            rel = os.path.relpath(root, sd)
            for fn in files:
                if fn in special:
                    continue
                dst = os.path.join(a.out, rel, fn)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copyfile(os.path.join(root, fn), dst)

    man = _load(os.path.join(shards[0], 'manifest.json'))
    for m in man.get('kpi_months') or []:
        mk = m['key']
        idxs = [i for i in (_load(os.path.join(sd, 'kpi', mk, 'index.json')) for sd in shards) if i]
        if not idxs:
            continue
        idx = dict(idxs[0])
        out_dir = os.path.join(a.out, 'kpi', mk)
        if idx.get('plan_dates'):
            idx['dates'] = [d for d in idx['plan_dates']
                            if os.path.isfile(os.path.join(out_dir, 'TURNOVER', f'{d}.json'))]
        idx['errors'] = [e for i in idxs for e in (i.get('errors') or [])]
        timing = {}
        for sd in shards:
            timing.update(_load(os.path.join(sd, 'kpi', mk, 'timing.json')) or {})
        if timing:
            with open(os.path.join(out_dir, 'timing.json'), 'w', encoding='utf-8') as fh:
                json.dump(timing, fh, ensure_ascii=False, indent=0)
        with open(os.path.join(out_dir, 'index.json'), 'w', encoding='utf-8') as fh:
            json.dump(idx, fh, ensure_ascii=False, indent=1)
    with open(os.path.join(a.out, 'manifest.json'), 'w', encoding='utf-8') as fh:
        json.dump(man, fh, ensure_ascii=False, indent=1)
    print(f'Đã ghép {len(shards)} máy → {a.out}')


if __name__ == '__main__':
    main()
