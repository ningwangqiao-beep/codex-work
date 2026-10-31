#!/usr/bin/env python3
"""Read-only USD-M perpetual market snapshots; Python 3.10+, no dependencies."""
import argparse
import json
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from decimal import Decimal
from urllib.parse import urlencode, urlparse


def utc(ms=None):
    return datetime.fromtimestamp(ms / 1000, timezone.utc).isoformat() if ms is not None else datetime.now(timezone.utc).isoformat()


class Client:
    def __init__(self, base, timeout=10):
        self.base, self.timeout = base.rstrip('/'), timeout

    def get(self, path, **params):
        url = self.base + path + ('?' + urlencode(params) if params else '')
        result = {'source': url, 'fetched_at': None, 'data': None, 'errors': []}
        for attempt in range(2):
            try:
                with urllib.request.urlopen(url, timeout=self.timeout) as response:
                    result['http_status'] = response.status
                    data = json.load(response)
                    if isinstance(data, dict) and data.get('code', 0) < 0:
                        raise ValueError('Binance error: ' + json.dumps(data))
                    result['data'] = data
                result['fetched_at'] = utc()
                return result
            except (urllib.error.URLError, ValueError, OSError) as exc:
                error = {'attempt': attempt + 1, 'at': utc(), 'message': str(exc)}
                if isinstance(exc, urllib.error.HTTPError):
                    error.update(http_status=exc.code, body=exc.read().decode('utf-8', 'replace'))
                result['errors'].append(error)
                if attempt == 0:
                    time.sleep(0.5)
        result['fetched_at'] = utc()
        return result


def snapshot(client, symbol):
    s = {'symbol': symbol, 'market': 'USD-M perpetual', 'base_url': client.base,
         'environment': ('mainnet' if urlparse(client.base).hostname == 'fapi.binance.com' else
                         'testnet' if urlparse(client.base).hostname in ('testnet.binancefuture.com', 'demo-fapi.binance.com') else 'custom'),
         'started_at': utc(), 'data': {}, 'alerts': []}
    d = s['data']
    d['server_time'] = client.get('/fapi/v1/time')
    for name, path, params in [
        ('latest_price', '/fapi/v1/ticker/price', {}),
        ('premium', '/fapi/v1/premiumIndex', {}),
        ('klines', '/fapi/v1/klines', {'interval': '15m', 'limit': 5}),
        ('open_interest', '/fapi/v1/openInterest', {}),
        ('ticker_24h', '/fapi/v1/ticker/24hr', {}),
        ('long_short_ratio', '/futures/data/globalLongShortAccountRatio', {'period': '5m', 'limit': 1}),
        ('oi_history', '/futures/data/openInterestHist', {'period': '5m', 'limit': 14})]:
        d[name] = client.get(path, symbol=symbol, **params)
    # Use exchange time sampled BEFORE requesting candles; never call a candle closed early.
    server = d['server_time']['data']
    bars = d['klines']['data']
    d['klines']['raw'] = bars
    d['klines']['data'] = None
    if server and bars is not None:
        now = int(server['serverTime'])
        def candle(b):
            return dict(open_time=utc(b[0]), close_time=utc(b[6]), open=b[1], high=b[2], low=b[3], close=b[4], volume=b[5])
        closed = [b for b in bars if int(b[6]) < now]
        current = [b for b in bars if int(b[0]) <= now <= int(b[6])]
        d['klines']['data'] = {'closed': [candle(b) for b in closed[-3:]], 'current': candle(current[0]) if current else None}
        if closed:
            change = (Decimal(closed[-1][4]) / Decimal(closed[-1][1]) - 1) * 100
            d['klines']['data']['last_closed_change_pct'] = str(change)
            if abs(change) >= 2:
                s['alerts'].append({'type': 'candle_15m', 'change_pct': str(change), 'threshold_pct': 2})
    premium = d['premium']['data']
    if premium and abs(Decimal(premium['lastFundingRate'])) >= Decimal('0.0005'):
        s['alerts'].append({'type': 'funding_rate', 'rate': premium['lastFundingRate'], 'threshold': '0.0005'})
    hist = d['oi_history']['data']
    d['oi_history']['one_hour_change'] = None
    if hist:
        hist = sorted(hist, key=lambda x: int(x['timestamp']))
        last = hist[-1]
        older = [x for x in hist if int(x['timestamp']) == int(last['timestamp']) - 3600000]
        if older and Decimal(older[-1]['sumOpenInterest']) > 0:
            change = (Decimal(last['sumOpenInterest']) / Decimal(older[-1]['sumOpenInterest']) - 1) * 100
            d['oi_history']['one_hour_change'] = {'change_pct': str(change), 'from': utc(older[-1]['timestamp']), 'to': utc(last['timestamp'])}
            if abs(change) >= 3:
                s['alerts'].append({'type': 'oi_1h', 'change_pct': str(change), 'threshold_pct': 3})
    required = ['server_time', 'latest_price', 'premium', 'klines', 'open_interest']
    s['status'] = 'ok' if all(d[k]['data'] is not None for k in required) else 'partial_or_unavailable'
    s['finished_at'] = utc()
    return s


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--base-url', default='https://fapi.binance.com')
    p.add_argument('--symbol', default='ETHUSDT')
    p.add_argument('--loop', action='store_true')
    p.add_argument('--interval', type=float, default=60)
    p.add_argument('--jsonl', default='snapshots.jsonl')
    p.add_argument('--timeout', type=float, default=10)
    args = p.parse_args()
    if args.interval <= 0 or args.timeout <= 0:
        p.error('interval and timeout must be positive')
    if urlparse(args.base_url).scheme not in ('http', 'https'):
        p.error('base-url must use http or https')
    client = Client(args.base_url, args.timeout)
    try:
        while True:
            start = time.monotonic()
            result = snapshot(client, args.symbol.upper())
            line = json.dumps(result, ensure_ascii=False, separators=(',', ':'))
            print(line, flush=True)
            if args.loop:
                with open(args.jsonl, 'a', encoding='utf-8') as f:
                    f.write(line + '\n')
                time.sleep(max(0, args.interval - (time.monotonic() - start)))
            else:
                return 0 if result['status'] == 'ok' else 1
    except KeyboardInterrupt:
        return 0


if __name__ == '__main__':
    raise SystemExit(main())
