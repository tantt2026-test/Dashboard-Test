"""Ghép kết quả các máy dò ô lọc (native/ci/probe.sh) vào bản lượt 1 đã publish.

  python merge_probes.py --probes _probes --out _reports

Mỗi máy dò 1 báo cáo nặng (probe_code.txt): chép đè thư mục báo cáo đó của từng tháng
(bản có cách áp ô lọc + các bản tính sẵn) và gộp thời gian chạy vào timing.json.
"""
import argparse
import json
import os
import shutil


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--probes', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    done = []
    for d in sorted(os.listdir(a.probes)):
        root = os.path.join(a.probes, d)
        try:
            code = open(os.path.join(root, 'probe_code.txt'), encoding='utf-8').read().strip()
        except OSError:
            continue
        kpi = os.path.join(root, 'kpi')
        for mk in os.listdir(kpi) if os.path.isdir(kpi) else []:
            src = os.path.join(kpi, mk, code)
            dst = os.path.join(a.out, 'kpi', mk, code)
            if not os.path.isdir(src) or not os.path.isdir(os.path.dirname(dst)):
                continue
            os.makedirs(dst, exist_ok=True)
            for fn in os.listdir(src):
                shutil.copyfile(os.path.join(src, fn), os.path.join(dst, fn))
            tf = os.path.join(kpi, mk, 'timing.json')
            if os.path.isfile(tf):
                t = json.load(open(tf, encoding='utf-8'))
                of = os.path.join(a.out, 'kpi', mk, 'timing.json')
                cur = json.load(open(of, encoding='utf-8')) if os.path.isfile(of) else {}
                if code in t:
                    cur[code] = t[code]
                with open(of, 'w', encoding='utf-8') as fh:
                    json.dump(cur, fh, ensure_ascii=False, indent=0)
        done.append(code)
    print('Đã ghép dò ô lọc:', ', '.join(done) or '(không có)')


if __name__ == '__main__':
    main()
