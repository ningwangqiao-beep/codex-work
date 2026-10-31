import unittest
from unittest.mock import patch
from urllib.error import URLError
from monitor import Client, snapshot

class Tests(unittest.TestCase):
    def test_retry(self):
        with patch('monitor.urllib.request.urlopen', side_effect=URLError('blocked')) as request, patch('monitor.time.sleep'):
            r = Client('https://example.org').get('/x')
        self.assertEqual(request.call_count, 2)
        self.assertIsNone(r['data'])
        self.assertEqual(len(r['errors']), 2)

    def test_boundaries_and_alerts(self):
        class Fake:
            base = 'https://fapi.binance.com'
            def get(self, path, **params):
                now = 4 * 900000
                bars = [[i*900000, '100','103','99','102','5',(i+1)*900000-1] for i in range(5)]
                values = {'/fapi/v1/time': {'serverTime': now}, '/fapi/v1/klines': bars,
                          '/fapi/v1/premiumIndex': {'lastFundingRate': '-0.0005'},
                          '/futures/data/openInterestHist': [{'timestamp': 0, 'sumOpenInterest': '100'}, {'timestamp': 3600000, 'sumOpenInterest': '103'}]}
                return {'source': path, 'fetched_at':'test', 'data':values.get(path, {}), 'errors':[]}
        s = snapshot(Fake(), 'ETHUSDT')
        bars = s['data']['klines']['data']
        self.assertEqual(len(bars['closed']), 3)
        self.assertEqual(bars['current']['open_time'], '1970-01-01T01:00:00+00:00')
        self.assertEqual({a['type'] for a in s['alerts']}, {'candle_15m','funding_rate','oi_1h'})

if __name__ == '__main__': unittest.main()
