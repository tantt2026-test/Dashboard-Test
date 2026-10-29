"""Chạy NGUYÊN App.py (cả phần giao diện) mà không cần Streamlit server.

Một module `streamlit` giả:
  - widget (selectbox, multiselect, date_input, radio...) trả về giá trị đặt sẵn trong
    session_state theo `key` — giống người dùng đã chọn trên web;
  - st.markdown / caption / warning / plotly_chart ... được GHI LẠI thành danh sách block
    (kèm tab/expander đang mở) để chuyển sang JSON cho app native;
  - st.cache_data nhớ kết quả thật giữa các lần chạy (đọc Excel 1 lần / tháng).
Nhờ vậy số liệu, format và màu lấy thẳng từ App.py, không viết lại logic báo cáo.
"""
import datetime as dt
import os
import sys
import types


class StopRun(Exception):
    pass


class RerunRequested(Exception):
    pass


class _SessionState(dict):
    def __getattr__(self, k):
        try:
            return self[k]
        except KeyError:
            raise AttributeError(k)

    def __setattr__(self, k, v):
        self[k] = v

    def __delattr__(self, k):
        self.pop(k, None)


def _cache_key(args, kwargs):
    def norm(v):
        try:
            hash(v)
            return v
        except TypeError:
            if isinstance(v, (list, tuple)):
                return tuple(norm(x) for x in v)
            if isinstance(v, dict):
                return tuple(sorted((k, norm(x)) for k, x in v.items()))
            if isinstance(v, set):
                return tuple(sorted(map(repr, v)))
            return ('id', id(v))
    return (tuple(norm(a) for a in args), tuple(sorted((k, norm(v)) for k, v in kwargs.items())))


class Recorder:
    """Một 'phiên' Streamlit: state + các block được vẽ ra."""

    def __init__(self):
        self.session_state = _SessionState()
        self.query_params = {}
        self.blocks = []
        self.section = []  # tab / expander đang mở
        self.memo = {}     # cache_data: (tên hàm, args) → kết quả

    def reset_run(self):
        self.blocks = []
        self.section = []

    def add(self, kind, **data):
        data['kind'] = kind
        data['section'] = list(self.section)
        self.blocks.append(data)


class _Container:
    """st.columns / tabs / expander / popover / container / sidebar."""

    def __init__(self, st, label=None):
        self._st = st
        self._label = label

    def __enter__(self):
        if self._label:
            self._st._rec.section.append(self._label)
        return self

    def __exit__(self, *a):
        if self._label:
            self._st._rec.section.pop()
        return False

    def __getattr__(self, name):
        fn = getattr(self._st, name)
        if not callable(fn):
            return fn

        def call(*a, **k):
            with self:
                return fn(*a, **k)
        return call


def _opt_list(options):
    if options is None:
        return []
    try:
        import pandas as pd
        if isinstance(options, (pd.Series, pd.Index)):
            return options.tolist()
        if isinstance(options, pd.DataFrame):
            return options.iloc[:, 0].tolist()
    except Exception:
        pass
    return list(options)


def make_streamlit(rec):
    st = types.ModuleType('streamlit')
    st._rec = rec
    st.session_state = rec.session_state
    st.query_params = rec.query_params

    # ---- cache ----
    def cache_data(*dargs, **dkw):
        def wrap(fn):
            name = getattr(fn, '__qualname__', fn.__name__)

            def wrapper(*a, **k):
                key = (name, _cache_key(a, k))
                if key not in rec.memo:
                    rec.memo[key] = fn(*a, **k)
                return rec.memo[key]

            def clear(*a, **k):
                for kk in [kk for kk in rec.memo if kk[0] == name]:
                    rec.memo.pop(kk, None)
            wrapper.clear = clear
            wrapper.__wrapped__ = fn
            wrapper.__name__ = fn.__name__
            return wrapper
        if len(dargs) == 1 and callable(dargs[0]) and not dkw:
            return wrap(dargs[0])
        return wrap
    st.cache_data = cache_data
    st.cache_resource = cache_data
    cache_data.clear = lambda: rec.memo.clear()

    def fragment(*a, **k):
        if len(a) == 1 and callable(a[0]):
            return a[0]
        return lambda f: f
    st.fragment = fragment

    # ---- control flow ----
    def stop():
        raise StopRun()

    def rerun(*a, **k):
        raise RerunRequested()
    st.stop = stop
    st.rerun = rerun
    st.experimental_rerun = rerun

    # ---- output ----
    def markdown(body='', unsafe_allow_html=False, **k):
        rec.add('markdown', body=str(body), html=bool(unsafe_allow_html))
    st.markdown = markdown
    st.write = lambda *a, **k: [rec.add('write', body=x if isinstance(x, str) else repr(x)) for x in a] and None
    st.caption = lambda body='', *a, **k: rec.add('caption', body=str(body))
    st.title = lambda body='', *a, **k: rec.add('heading', level=1, body=str(body))
    st.header = lambda body='', *a, **k: rec.add('heading', level=2, body=str(body))
    st.subheader = lambda body='', *a, **k: rec.add('heading', level=3, body=str(body))
    st.text = lambda body='', *a, **k: rec.add('caption', body=str(body))
    st.code = lambda body='', *a, **k: None
    st.divider = lambda *a, **k: rec.add('divider')
    for lvl in ('info', 'warning', 'error', 'success'):
        setattr(st, lvl, (lambda lvl: lambda body='', *a, **k: rec.add('message', level=lvl, body=str(body)))(lvl))
    st.exception = lambda e=None, *a, **k: rec.add('message', level='error', body=repr(e))
    st.toast = lambda *a, **k: None
    st.balloons = st.snow = lambda *a, **k: None

    def plotly_chart(fig, *a, **k):
        try:
            rec.add('plotly', figure=fig.to_plotly_json())
        except Exception as e:
            rec.add('message', level='warning', body=f'plotly: {e}')
    st.plotly_chart = plotly_chart

    def dataframe(data=None, *a, **k):
        rec.add('dataframe', data=data)
    st.dataframe = dataframe
    st.table = dataframe
    st.metric = lambda label, value, delta=None, *a, **k: rec.add('metric', label=str(label), value=str(value),
                                                                 delta=None if delta is None else str(delta))
    st.image = lambda *a, **k: None
    st.set_page_config = lambda *a, **k: None
    st.progress = lambda *a, **k: _Container(st)

    # ---- layout ----
    def columns(spec, *a, **k):
        n = spec if isinstance(spec, int) else len(spec)
        return [_Container(st) for _ in range(n)]
    st.columns = columns
    st.tabs = lambda labels, *a, **k: [_Container(st, str(l)) for l in labels]
    st.expander = lambda label='', *a, **k: _Container(st, str(label))
    st.popover = lambda label='', *a, **k: _Container(st, '__popover__')
    st.container = lambda *a, **k: _Container(st)
    st.empty = lambda *a, **k: _Container(st)
    st.form = lambda *a, **k: _Container(st)
    st.spinner = lambda *a, **k: _Container(st)
    st.status = lambda *a, **k: _Container(st)
    st.sidebar = _Container(st, '__sidebar__')

    # ---- widgets: lấy giá trị từ session_state theo key ----
    ss = rec.session_state

    def _remember(key, val):
        if key is not None:
            ss[key] = val
        return val

    def _widget(fn):
        def wrapped(*a, **k):
            rec.add('widget', key=k.get('key'))
            return fn(*a, **k)
        return wrapped

    def selectbox(label='', options=(), index=0, *a, key=None, **k):
        opts = _opt_list(options)
        if key is not None and key in ss and ss[key] in opts:
            return ss[key]
        if key is not None and ss.get(key) is not None:
            # giá trị đặt sẵn không có trong danh sách → App.py sẽ hiện mục mặc định
            rec.add('widget_miss', key=key, want=str(ss[key]))
        val = opts[index] if (index is not None and opts) else None
        return _remember(key, val)
    st.selectbox = selectbox

    def radio(label='', options=(), index=0, *a, key=None, **k):
        val = selectbox(label, options, index, key=key)
        # Mốc: nội dung báo cáo bắt đầu sau thanh chọn tab chính (key của App.py)
        rec.add('nav' if key == 'main_nav_section' else 'widget', key=key, value=val)
        return val
    st.radio = radio

    def multiselect(label='', options=(), default=None, *a, key=None, **k):
        if key is not None and key in ss:
            opts = set(map(str, _opt_list(options)))
            return [v for v in ss[key] if str(v) in opts]
        val = list(default) if default else []
        return _remember(key, val)
    st.multiselect = multiselect

    def _valued(default):
        def widget(label='', *a, value=default, key=None, **k):
            if key is not None and key in ss:
                return ss[key]
            return _remember(key, value)
        return widget
    st.text_input = _valued('')
    st.text_area = _valued('')
    st.checkbox = _valued(False)
    st.toggle = _valued(False)

    def number_input(label='', min_value=None, max_value=None, value=None, *a, key=None, **k):
        if key is not None and key in ss:
            return ss[key]
        return _remember(key, value if value is not None else (min_value or 0))
    st.number_input = number_input

    def slider(label='', min_value=None, max_value=None, value=None, *a, key=None, **k):
        if key is not None and key in ss:
            return ss[key]
        return _remember(key, value if value is not None else min_value)
    st.slider = slider
    st.select_slider = lambda label='', options=(), value=None, *a, key=None, **k: (
        ss[key] if key in ss else _remember(key, value if value is not None else _opt_list(options)[0]))

    def date_input(label='', value='today', *a, key=None, **k):
        if key is not None and key in ss:
            return ss[key]
        if value in (None, 'today'):
            value = dt.date.today()
        return _remember(key, value)
    st.date_input = date_input

    for _w in ('selectbox', 'multiselect', 'text_input', 'text_area', 'checkbox', 'toggle',
               'number_input', 'slider', 'select_slider', 'date_input'):
        setattr(st, _w, _widget(getattr(st, _w)))

    st.button = lambda *a, **k: False
    st.form_submit_button = lambda *a, **k: False
    st.download_button = lambda *a, **k: False
    st.link_button = lambda *a, **k: False
    st.file_uploader = lambda *a, **k: None
    st.data_editor = lambda data=None, *a, **k: data

    st.__getattr__ = lambda name: (lambda *a, **k: _Container(st))

    # streamlit.components.v1
    comps = types.ModuleType('streamlit.components')
    v1 = types.ModuleType('streamlit.components.v1')
    v1.html = lambda html='', *a, **k: rec.add('component_html', body=str(html))
    v1.iframe = lambda *a, **k: None
    v1.declare_component = lambda *a, **k: (lambda *aa, **kk: None)
    comps.v1 = v1
    st.components = comps
    return {'streamlit': st, 'streamlit.components': comps, 'streamlit.components.v1': v1}


class HeadlessApp:
    """Chạy App.py nhiều lần với các lựa chọn khác nhau, giữ cache data giữa các lần."""

    def __init__(self, app_path):
        self.app_path = os.path.abspath(app_path)
        self.repo = os.path.dirname(self.app_path)
        src = open(self.app_path, encoding='utf-8').read()
        self.code = compile(src, self.app_path, 'exec')
        self.rec = Recorder()
        self.modules = make_streamlit(self.rec)
        self.ns = None

    def run(self, state, _retries=2):
        """state: dict đặt vào session_state trước khi chạy (giống người dùng chọn).
        Trả về (blocks, namespace, trạng thái: 'ok' | 'stop' | 'error: ...').
        App.py gọi st.rerun() (vd. đổi tháng) → chạy lại như Streamlit."""
        for k, v in state.items():
            self.rec.session_state[k] = v
        blocks, ns, status = self._run_once()
        while status == 'rerun' and _retries > 0:
            _retries -= 1
            blocks, ns, status = self._run_once()
        return blocks, ns, status

    def _run_once(self):
        self.rec.reset_run()
        saved = {k: sys.modules.get(k) for k in self.modules}
        sys.modules.update(self.modules)
        cwd = os.getcwd()
        os.chdir(self.repo)
        ns = {'__name__': '__main__', '__file__': self.app_path}
        status = 'ok'
        try:
            exec(self.code, ns)
        except StopRun:
            status = 'stop'
        except RerunRequested:
            status = 'rerun'
        except Exception as e:  # báo cáo lỗi → ghi lại, không làm hỏng cả lần xuất
            status = f'error: {type(e).__name__}: {e}'
        finally:
            os.chdir(cwd)
            for k, v in saved.items():
                if v is None:
                    sys.modules.pop(k, None)
                else:
                    sys.modules[k] = v
        self.ns = ns
        return list(self.rec.blocks), ns, status
