"""Verify every unique production image URL with curl and make inspection sheets."""
import concurrent.futures
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def check(item):
    photo_id, caption = item
    url = f'https://images.unsplash.com/{photo_id}?w=1600&q=80&auto=format&fit=crop'
    result = subprocess.run(['curl', '-L', '--retry', '2', '--max-time', '90', '-s', '-o', str(ROOT/'evidence/photos'/f'{photo_id}.jpg'), '-w', '%{http_code}', url], capture_output=True, text=True)
    return {'id': photo_id, 'caption': caption, 'url': url, 'status': result.stdout, 'exit': result.returncode}


if __name__ == '__main__':
    (ROOT/'evidence/photos').mkdir(exist_ok=True)
    groups = json.loads((ROOT/'content/photos.json').read_text())
    unique = dict(pair for pairs in groups.values() for pair in pairs)
    saved = ROOT/'evidence/image-checks.json'
    previous = {r['id']:r for r in json.loads(saved.read_text())} if saved.exists() else {}
    pending = [(k,v) for k,v in unique.items() if k not in previous or previous[k]['status'] != '200']
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        fresh = {r['id']:r for r in pool.map(check, pending)}
    results = [fresh[k] if k in fresh else previous[k] for k in unique]
    (ROOT/'evidence/image-checks.json').write_text(json.dumps(results, indent=2, ensure_ascii=False))
    for row in results:
        print(row['status'], row['id'])
    print(f"Images checked: {len(results)}; HTTP 200: {sum(r['status']=='200' for r in results)}")
