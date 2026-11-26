"""Đọc Excel nhanh cho máy tự tính (Windows/Mac) — không sửa App.py.

1) pd.read_excel / pd.ExcelFile không ghi engine → dùng python-calamine (Rust, nhanh ~4x openpyxl).
   Lỗi → quay về openpyxl như cũ. Ô số ghi chữ 'Infinity'/'NaN' (file Onetech): openpyxl (đã vá ở
   team_data) đọc thành ô trống, calamine đọc thành inf → đổi inf về ô trống cho giống hệt.
   Đã so 85 file data thật T09–T11 (Tân + Vy): giống từng ô.
2) Cache trên đĩa theo NỘI DUNG file (sha1) + tham số đọc: file không đổi giữa 2 lần sync
   (phần lớn file) → không đọc lại Excel. Mỗi lần đọc trả bản mới (unpickle) nên App.py sửa bảng
   tại chỗ cũng không ảnh hưởng cache.
Tắt: đặt biến môi trường KPI_FAST_EXCEL=0.
"""
import hashlib
import math
import os
import pickle
import sys
import time

import numpy as np
import pandas as pd

VERSION = '1'
# GitHub Actions (build-reports) không có python-calamine → tắt hẳn cho CI tính y như cũ
_ENABLED = os.environ.get('KPI_FAST_EXCEL', '1') != '0' and os.environ.get('GITHUB_ACTIONS') != 'true'


def _cache_root():
    if os.environ.get('LOCALAPPDATA'):  # Windows
        return os.environ['LOCALAPPDATA']
    if sys.platform == 'darwin':
        return os.path.expanduser('~/Library/Application Support')
    return os.path.expanduser('~/.cache')


_CACHE_DIR = os.path.join(_cache_root(), 'KPI Dashboard', 'engine', 'xlcache')
_KEEP_DAYS = 10
_XL_EXT = ('.xlsx', '.xlsm')

try:
    import python_calamine  # noqa: F401
    _HAS_CALAMINE = True
except Exception:  # noqa: BLE001
    _HAS_CALAMINE = False

_orig_read_excel = pd.read_excel
_orig_xf_init = pd.ExcelFile.__init__
_sha_memo = {}  # (path, size, mtime) -> sha1


def _is_xlsx_path(io):
    return isinstance(io, (str, os.PathLike)) and str(io).lower().endswith(_XL_EXT) and os.path.isfile(io)


def _file_sha(path):
    st = os.stat(path)
    k = (os.path.abspath(path), st.st_size, st.st_mtime_ns)
    h = _sha_memo.get(k)
    if h is None:
        d = hashlib.sha1()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(1 << 20), b''):
                d.update(chunk)
        h = _sha_memo[k] = d.hexdigest()
    return h


def _fix_inf(obj):
    """inf/-inf (ô chữ 'Infinity') → ô trống, như openpyxl đã vá."""
    if isinstance(obj, dict):
        return {k: _fix_inf(v) for k, v in obj.items()}
    if not isinstance(obj, pd.DataFrame):
        return obj
    for c in obj.columns:
        s = obj[c]
        if s.dtype == object:
            m = s.map(lambda v: isinstance(v, float) and math.isinf(v))
            if m.any():
                obj[c] = s.where(~m, None)
        elif np.issubdtype(s.dtype, np.floating):
            m = np.isinf(s.to_numpy())
            if m.any():
                obj[c] = s.mask(m)
    return obj


def _cacheable(args, kwargs):
    for v in list(args) + list(kwargs.values()):
        if callable(v) or hasattr(v, 'read'):
            return False
    return True


def _cache_path(path, args, kwargs):
    key = repr((VERSION, pd.__version__, _file_sha(path), args, sorted(kwargs.items())))
    return os.path.join(_CACHE_DIR, hashlib.sha1(key.encode('utf-8')).hexdigest() + '.pkl')


def _read(io, args, kwargs):
    if _HAS_CALAMINE:
        try:
            return _fix_inf(_orig_read_excel(io, *args, engine='calamine', **kwargs))
        except Exception:  # noqa: BLE001
            pass
    return _orig_read_excel(io, *args, **kwargs)


def read_excel(io, *args, **kwargs):
    if not _ENABLED or kwargs.get('engine') is not None or not _is_xlsx_path(io):
        return _orig_read_excel(io, *args, **kwargs)
    cp = None
    if _cacheable(args, kwargs):
        try:
            cp = _cache_path(io, args, kwargs)
            if os.path.exists(cp):
                with open(cp, 'rb') as f:
                    out = pickle.load(f)
                try:
                    os.utime(cp, None)  # còn dùng → không bị dọn
                except OSError:
                    pass
                return out
        except Exception:  # noqa: BLE001  cache hỏng → đọc lại
            cp = cp if cp else None
    out = _read(io, args, kwargs)
    if cp:
        try:
            os.makedirs(_CACHE_DIR, exist_ok=True)
            tmp = cp + '.%d.tmp' % os.getpid()
            with open(tmp, 'wb') as f:
                pickle.dump(out, f, protocol=pickle.HIGHEST_PROTOCOL)
            os.replace(tmp, cp)
        except Exception:  # noqa: BLE001
            pass
    return out


def _xf_init(self, path_or_buffer, engine=None, *args, **kwargs):
    if _ENABLED and engine is None and _HAS_CALAMINE and _is_xlsx_path(path_or_buffer):
        try:
            return _orig_xf_init(self, path_or_buffer, 'calamine', *args, **kwargs)
        except Exception:  # noqa: BLE001
            pass
    return _orig_xf_init(self, path_or_buffer, engine, *args, **kwargs)


def _prune():
    try:
        cut = time.time() - _KEEP_DAYS * 86400
        for fn in os.listdir(_CACHE_DIR):
            p = os.path.join(_CACHE_DIR, fn)
            if os.path.getmtime(p) < cut:
                os.remove(p)
    except Exception:  # noqa: BLE001
        pass


def compile_cached(src, path):
    """compile() App.py (~1,2 MB) mất ~20 s trên máy yếu → lưu bản dịch (marshal) theo nội dung + đường dẫn."""
    import marshal
    import sys
    key = hashlib.sha1(repr((VERSION, sys.version, os.path.abspath(path))).encode('utf-8') + src.encode('utf-8')).hexdigest()
    cp = os.path.join(_CACHE_DIR, 'code_' + key + '.bin')
    try:
        if os.path.exists(cp):
            with open(cp, 'rb') as f:
                code = marshal.load(f)
            try:
                os.utime(cp, None)
            except OSError:
                pass
            return code
    except Exception:  # noqa: BLE001
        pass
    code = compile(src, path, 'exec')
    try:
        os.makedirs(_CACHE_DIR, exist_ok=True)
        tmp = cp + '.%d.tmp' % os.getpid()
        with open(tmp, 'wb') as f:
            marshal.dump(code, f)
        os.replace(tmp, cp)
    except Exception:  # noqa: BLE001
        pass
    return code


def install():
    if getattr(pd, '_kpi_fast_excel', False) or not _ENABLED:
        return
    pd.read_excel = read_excel
    pd.ExcelFile.__init__ = _xf_init
    pd._kpi_fast_excel = True
    _prune()
