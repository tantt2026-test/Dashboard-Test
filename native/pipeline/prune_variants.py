"""Dọn file biến thể ô lọc (<ngày>[__nv]__wN.json) của các ngày cũ để branch `reports` không phình.

  python prune_variants.py <thư mục reports> [--keep 2]

Mỗi thư mục kpi/<Tháng>/<CODE>/ (cả t/vy, t/all) chỉ giữ biến thể của `keep` ngày mới nhất.
Ngày cũ hơn: xoá file __wN và đổi ô lọc "tính lại" trong file ngày từ {'mode':'calc','variants':…}
thành {'mode':'unsupported'} → app không chờ file đã xoá mà tính lại bằng App.py
(Mac/Win: máy tính tại chỗ; APK: GitHub filter-run) như mọi ô lọc chưa có bản tính sẵn.
Chạy lại nhiều lần không sao (file đã dọn thì bỏ qua, không đọc JSON).
"""
import json
import os
import re
import sys

_VAR = re.compile(r'^(\d{4}-\d{2}-\d{2})(?:__.+?)?__w\d+\.json$')
_DOC = re.compile(r'^(\d{4}-\d{2}-\d{2})(?:__.+)?\.json$')


def _strip(o):
    n = 0
    if isinstance(o, dict):
        f = o.get('f')
        if isinstance(f, dict) and f.get('mode') == 'calc' and 'variants' in f:
            o['f'] = {'mode': 'unsupported', 'ondemand': True}
            n += 1
        for v in o.values():
            n += _strip(v)
    elif isinstance(o, list):
        for v in o:
            n += _strip(v)
    return n


def prune_dir(d, keep):
    names = os.listdir(d)
    vdays = sorted({m.group(1) for fn in names if (m := _VAR.match(fn))})
    if len(vdays) <= keep:
        return 0, 0, 0
    old = set(vdays[:-keep])
    nfile = nbytes = ndoc = 0
    for fn in names:
        p = os.path.join(d, fn)
        m = _VAR.match(fn)
        if m and m.group(1) in old:
            nbytes += os.path.getsize(p)
            os.remove(p)
            nfile += 1
            continue
        m = _DOC.match(fn)
        if m and m.group(1) in old and not _VAR.match(fn):
            with open(p, 'rb') as fh:
                raw = fh.read()
            if b'"variants"' not in raw:
                continue
            doc = json.loads(raw)
            if _strip(doc):
                with open(p, 'w', encoding='utf-8') as fh:
                    json.dump(doc, fh, ensure_ascii=False, separators=(',', ':'))
                ndoc += 1
    return nfile, nbytes, ndoc


def main():
    root = sys.argv[1]
    keep = int(sys.argv[sys.argv.index('--keep') + 1]) if '--keep' in sys.argv else 2
    tf = tb = td = 0
    for dirpath, _dirs, files in os.walk(root):
        if '.git' in dirpath.split(os.sep):
            continue
        if any(_VAR.match(f) for f in files):
            f, b, d = prune_dir(dirpath, keep)
            tf, tb, td = tf + f, tb + b, td + d
    print(f'Dọn biến thể ô lọc ngày cũ (giữ {keep} ngày mới nhất): xoá {tf} file '
          f'({tb / 1e9:.2f} GB), sửa {td} file ngày')


if __name__ == '__main__':
    main()
