"""Nạp các hàm tính toán từ chính App.py (Streamlit) mà KHÔNG chạy phần giao diện.

Cách làm: parse App.py bằng AST, giữ lại
  - toàn bộ import, def, class (ở top-level, bất kể vị trí)
  - các lệnh gán hằng số/cấu hình nằm TRƯỚC đoạn load data của giao diện
    (MONTH_OPTIONS, KPI_COLOR_MOC, MOQ_RULES, init đường dẫn...)
rồi exec trong 1 namespace có module `streamlit` giả.
→ Code tính toán giữ nguyên 100% từ App.py, sửa App.py là pipeline tự theo.
"""
import ast
import os
import sys
import types


class StreamlitStop(Exception):
    """App.py gọi st.stop() (thiếu file, lỗi data...)."""


class _SessionState(dict):
    def __getattr__(self, k):
        try:
            return self[k]
        except KeyError:
            raise AttributeError(k)

    def __setattr__(self, k, v):
        self[k] = v


def _passthrough_decorator(*args, **kwargs):
    """Thay @st.cache_data / @st.cache_data(ttl=...) / @st.fragment: không cache."""
    def wrap(fn):
        fn.clear = lambda *a, **k: None
        return fn
    if len(args) == 1 and callable(args[0]) and not kwargs:
        return wrap(args[0])
    return wrap


class _Noop:
    """Mọi thứ khác (st.markdown, st.columns, components.html, ...) → không làm gì."""
    def __call__(self, *a, **k):
        return _Noop()

    def __getattr__(self, k):
        return _Noop()

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def __iter__(self):
        return iter([_Noop() for _ in range(8)])

    def __bool__(self):
        return False


def _make_fake_streamlit(log):
    st = types.ModuleType('streamlit')
    st.session_state = _SessionState()
    st.query_params = {}
    st.cache_data = _passthrough_decorator
    st.cache_resource = _passthrough_decorator
    st.fragment = _passthrough_decorator

    def _stop(*a, **k):
        raise StreamlitStop('st.stop()')
    st.stop = _stop
    st.rerun = _stop
    for lvl in ('error', 'warning', 'info', 'exception'):
        setattr(st, lvl, (lambda lvl: lambda msg='', *a, **k: log(f'[st.{lvl}] {msg}'))(lvl))
    st.__getattr__ = lambda k: _Noop()

    comps = types.ModuleType('streamlit.components')
    v1 = types.ModuleType('streamlit.components.v1')
    v1.html = _Noop()
    v1.iframe = _Noop()
    v1.declare_component = _Noop()
    comps.v1 = v1
    st.components = comps
    return {'streamlit': st, 'streamlit.components': comps, 'streamlit.components.v1': v1}


def _data_load_line(tree):
    """Dòng bắt đầu phần giao diện load data: `df, mcp = _ensure_core_data(...)`."""
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            names = []
            for t in node.targets:
                names += [e.id for e in getattr(t, 'elts', [t]) if isinstance(e, ast.Name)]
            if 'df' in names and 'mcp' in names:
                return node.lineno
    return None


def load(app_path, log=lambda m: print(m, file=sys.stderr)):
    """Trả về namespace (dict) chứa toàn bộ hàm + hằng số của App.py.

    Lưu ý: App.py dùng đường dẫn tương đối 'data/...' → chdir về thư mục repo.
    """
    app_path = os.path.abspath(app_path)
    src = open(app_path, encoding='utf-8').read()
    tree = ast.parse(src, filename=app_path)
    stop_line = _data_load_line(tree) or 10 ** 9

    keep = []
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef,
                             ast.AsyncFunctionDef, ast.ClassDef)):
            keep.append(node)
            continue
        if node.lineno >= stop_line:
            continue
        seg = ast.get_source_segment(src, node) or ''
        if 'st.' in seg:  # set_page_config, markdown CSS...
            continue
        keep.append(node)

    module = ast.Module(body=keep, type_ignores=[])
    code = compile(module, app_path, 'exec')

    fake = _make_fake_streamlit(log)
    saved = {k: sys.modules.get(k) for k in fake}
    sys.modules.update(fake)
    os.chdir(os.path.dirname(app_path))
    ns = {'__name__': 'app_logic_ns', '__file__': app_path}
    try:
        exec(code, ns)
    finally:
        for k, v in saved.items():
            if v is None:
                sys.modules.pop(k, None)
            else:
                sys.modules[k] = v
    ns['__st__'] = fake['streamlit']
    return ns


def select_month(ns, month_key):
    """Giống người dùng chọn tháng trên Streamlit."""
    ns['__st__'].session_state['report_month_key'] = month_key
    ns['_refresh_paths']()
