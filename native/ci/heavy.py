"""3 báo cáo dò ô lọc lâu nhất (theo timing.json của lần xuất trước) → chạy dò trên máy riêng.
  python heavy.py _prev        → "TAB_MCP,WEEKLY_PREVIEW,PERFORMANCE"
  python heavy.py _prev 1      → báo cáo nặng thứ 2 (máy dò số 1)
"""
import glob
import json
import sys

N = 3
DEFAULT = ['TAB_MCP', 'WEEKLY_PREVIEW', 'PERFORMANCE']
t = {}
for f in sorted(glob.glob(f'{sys.argv[1]}/kpi/*/timing.json'))[-1:]:
    try:
        t = json.load(open(f, encoding='utf-8'))
    except Exception:
        pass
codes = [c for c, _ in sorted(((c, s) for c, s in t.items() if not c.startswith('nv:')), key=lambda x: -x[1])][:N]
codes = codes if len(codes) == N else DEFAULT
print(codes[int(sys.argv[2])] if len(sys.argv) > 2 else ','.join(codes))
