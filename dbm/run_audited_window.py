#!/usr/bin/env python3
"""Run the authorized 87,425-bar window using hash-pinned baseline sources."""
import concurrent.futures
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import urllib.request
import zipfile

import backtest as bt

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'results' / 'window_87425'
CACHE = ROOT.parent / 'work' / 'audited_archives'
BASELINE = '9efbb0c967c7d2d549cbc7fa979ec194b15509cd'
LAST = 1793466240
COUNT = 87425
WINDOW = dict(window_start_utc=bt.iso(bt.START), window_last_bar_open_utc=bt.iso(LAST),
              window_end_exclusive_utc=bt.iso(LAST + 60), window_bars=COUNT)


def archive(record):
    path = CACHE / record['url'].rsplit('/', 1)[-1]
    if not path.exists():
        with urllib.request.urlopen(record['url'], timeout=60) as response:
            path.write_bytes(response.read())
    data = path.read_bytes()
    assert hashlib.sha256(data).hexdigest() == record['sha256'], path
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        assert z.testzip() is None, path
        return list(csv.reader(io.StringIO(z.read(z.namelist()[0]).decode())))


def load():
    audit = ROOT / 'results' / 'rest_completion'
    records = json.loads((audit / 'archive_validation.json').read_text())['downloads']
    records = [r for r in records if r.get('status') == 200]
    assert len(records) == 31 and all(r['checksum_ok'] for r in records)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        raw = [row for rows in pool.map(archive, records) for row in rows]
    assert len(raw) == 86400
    rest_audit = json.loads((audit / 'validation.json').read_text())
    for request in rest_audit['requests']:
        if not request['rows']:
            continue
        stamp = request['url'].split('startTime=')[1].split('&')[0]
        data = (audit / f'rest-{stamp}.json').read_bytes()
        assert hashlib.sha256(data).hexdigest() == request['sha256']
        rows = json.loads(data)
        assert len(rows) == request['rows']
        raw.extend(rows)
    bars = []
    for r in raw:
        stamp = int(r[0])
        scale = 1000000 if stamp > 10**14 else 1000
        assert stamp % (60 * scale) == 0
        assert int(r[6]) == stamp + 60 * scale - 1
        o, h, l, c = map(float, r[1:5])
        assert all(math.isfinite(x) and x > 0 for x in (o, h, l, c))
        assert l <= min(o, c) <= max(o, c) <= h
        assert float(r[5]) >= 0 and int(r[8]) >= 0
        bars.append((stamp // scale, o, h, l, c))
    bars.sort()
    assert len(bars) == COUNT
    assert [b[0] for b in bars] == list(range(bt.START, LAST + 60, 60))
    assert bars[-1026][4] == bars[-1025][1] == 2245.54
    return bars, records


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)
    bars, sources = load()
    bt.END = LAST + 60
    bt.writecsv(OUT / 'input_bars.csv',
                [dict(open_time_utc=bt.iso(t), open=o, high=h, low=l, close=c, **WINDOW)
                 for t, o, h, l, c in bars],
                ['open_time_utc', 'open', 'high', 'low', 'close', *WINDOW])
    validation = dict(valid=True, baseline=BASELINE, **WINDOW, available_bars=len(bars),
                      archive_bars=86400, rest_bars=1025, duplicate_count=0,
                      missing_count=0, ohlc_valid=True, seam_valid=True,
                      archive_sources=sources,
                      input_sha256=hashlib.sha256((OUT / 'input_bars.csv').read_bytes()).hexdigest(),
                      last_bar_closed='Confirmed by commissioning party',
                      valuation='Open end positions marked to final close; no forced sell or hypothetical exit fee.')
    (OUT / 'validation.json').write_text(json.dumps(validation, indent=2) + '\n')
    results = [dict(**bt.simulate(name, bars, OUT), **WINDOW) for name in bt.PARAMS]
    for name in bt.PARAMS:
        for suffix in ['daily_equity', 'baskets', 'fills']:
            path = OUT / f'{name}_{suffix}.csv'
            with path.open(newline='') as f:
                reader = csv.DictReader(f)
                fields = reader.fieldnames
                rows = [dict(**row, **WINDOW) for row in reader]
            bt.writecsv(path, rows, [*fields, *WINDOW])
    (OUT / 'summary.json').write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
