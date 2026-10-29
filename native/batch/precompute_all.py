"""Chạy trên Mac (để máy mở): tính sẵn MỌI tổ hợp bộ lọc (pipeline/plan_all.py) bằng GitHub Actions.

  python3 native/batch/precompute_all.py            (token ở ~/.kpi_gh_token: Actions R/W + Contents R)

Lặp: chờ build-reports chạy xong → đếm tổ hợp chưa có ở branch `filters` → mở 1 đợt WAVE máy
(workflow filter-run, mỗi máy 1 phần, ~22 phút) → chờ đợt xong → lặp. Dữ liệu sync mới (commit
khác) thì các máy tự bỏ, đợt sau tính cho commit mới. Hết tổ hợp → chờ dữ liệu mới.
"""
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.request

REPO = 'tantt2026-test/Dashboard-Test'
API = f'https://api.github.com/repos/{REPO}'
WAVE = 18          # GitHub miễn phí cho 20 máy cùng lúc → chừa 2 cho app nhờ tính
BUDGET = 1320      # giây mỗi máy (workflow filter-run giới hạn 30 phút)
HERE = os.path.dirname(os.path.abspath(__file__))
PIPE = os.path.join(HERE, '..', 'pipeline')
PY = sys.argv[1] if len(sys.argv) > 1 else sys.executable
TOKEN = open(os.path.expanduser('~/.kpi_gh_token')).read().strip()
WORK = tempfile.mkdtemp(prefix='kpi_all_')


def log(*a):
    print(time.strftime('%H:%M'), *a, flush=True)


def gh(path, data=None):
    req = urllib.request.Request(API + path, data=json.dumps(data).encode() if data is not None else None,
                                 headers={'Authorization': f'Bearer {TOKEN}', 'Accept': 'application/vnd.github+json'},
                                 method='POST' if data is not None else 'GET')
    with urllib.request.urlopen(req, timeout=60) as r:
        body = r.read()
        return json.loads(body) if body else None


def git(*a):
    return subprocess.run(['git', *a], capture_output=True, text=True)


def runs(wf, status):
    return gh(f'/actions/workflows/{wf}/runs?status={status}&per_page=100')['workflow_runs']


def remaining():
    """(sc, số tổ hợp chưa có, tổng)."""
    rep, fil = os.path.join(WORK, 'rep'), os.path.join(WORK, 'fil')
    for d, br in ((rep, 'reports'), (fil, 'filters')):
        subprocess.run(['rm', '-rf', d])
        git('clone', '-q', '--depth', '1', '--no-checkout' if br == 'filters' else '-q', '-b', br,
            f'https://github.com/{REPO}.git', d)
    out = subprocess.run([PY, '-c', f'''
import json,sys,os
sys.path.insert(0,{PIPE!r})
import plan_all,run_request
sc,p=plan_all.plan({rep!r})
ls=os.popen("git -C {fil} ls-tree -r --name-only HEAD "+sc[:12]+"/ 2>/dev/null").read().split()
have={{os.path.basename(x)[:-5] for x in ls}}
print(json.dumps([sc,sum(run_request.key_of(q) not in have for q in p),len(p)]))
'''], capture_output=True, text=True, cwd=PIPE)
    return json.loads(out.stdout.strip().splitlines()[-1])


def main():
    log('Bắt đầu. Thư mục tạm', WORK)
    wave = 0
    while True:
        busy = runs('build-reports.yml', 'in_progress') + runs('build-reports.yml', 'queued')
        if busy:
            log(f'build-reports đang chạy ({busy[0]["head_sha"][:7]}) → chờ 5 phút')
            time.sleep(300)
            continue
        sc, left, total = remaining()
        log(f'Dữ liệu {sc[:7]}: đã có {total - left}/{total}, còn {left}')
        if left == 0:
            time.sleep(900)
            continue
        wave += 1
        k = min(WAVE, max(1, -(-left // 150)))
        t_start = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        for i in range(k):
            gh('/actions/workflows/filter-run.yml/dispatches',
               {'ref': 'main', 'inputs': {'req': json.dumps({'sc': sc, 'shard': [i, k], 'budget': BUDGET})}})
        log(f'Đợt {wave}: mở {k} máy')
        time.sleep(120)
        while runs('filter-run.yml', 'in_progress') + runs('filter-run.yml', 'queued'):
            time.sleep(60)
        failed = [r for r in gh('/actions/workflows/filter-run.yml/runs?per_page=30')['workflow_runs']
                  if r['conclusion'] == 'failure' and r['created_at'] >= t_start]
        log(f'Đợt {wave} xong' + (f', {len(failed)} máy lỗi gần đây' if failed else ''))


if __name__ == '__main__':
    main()
