# ETHUSDT U 本位永续只读盯盘

Python 3.10+，纯标准库，无 API key、签名、账户访问或下单操作。所有请求均 GET。

## 运行

```sh
python monitor.py
python monitor.py --loop --interval 60 --jsonl snapshots.jsonl
python monitor.py --base-url https://testnet.binancefuture.com
python -m unittest -v
```

单次成功退出 0；必要行情不可用退出 1，同时 stdout 仍输出完整 JSON。循环逐份打印并追加 JSONL；Ctrl-C 停止。默认每 60 秒开始一轮，若一轮超过间隔则完成后立即下一轮。每个请求失败后等待 0.5 秒重试一次；保留每次错误。默认超时每次 10 秒，可用 `--timeout` 修改。不自动切换数据源。自定义 base URL 标记 custom；已知测试网标记 testnet，绝不可当作主网。

## 公开端点与字段字典

所有 data 子项都有 source（完整 URL）、fetched_at（请求结束 UTC）、data（原始数据或标准化 K 线）、errors（每次失败的时间、原文；收到 HTTP 响应时还含状态及正文）。成功含 http_status。隧道失败不代表源站返回状态。

|data 子项|GET 端点|主要字段/单位|
|---|---|---|
|server_time|/fapi/v1/time|serverTime 毫秒，用于 K 线收盘判断|
|latest_price|/fapi/v1/ticker/price|price 最新成交价，USDT|
|premium|/fapi/v1/premiumIndex|markPrice 标记价、indexPrice 指数价（USDT）；lastFundingRate 当前资金费率，小数比率；nextFundingTime 下次结算 UTC epoch 毫秒|
|klines|/fapi/v1/klines?interval=15m&limit=5|data.closed 最近三根已收盘，data.current 当前线；open/high/low/close 为 USDT，volume 为 ETH；open_time/close_time 为 UTC ISO；raw 保留交易所数组|
|open_interest|/fapi/v1/openInterest|openInterest 当前 OI，ETH；time 交易所时间|
|ticker_24h|/fapi/v1/ticker/24hr|priceChangePercent 近 24h 涨跌百分数|
|long_short_ratio|/futures/data/globalLongShortAccountRatio?period=5m&limit=1|longShortRatio 账户多空比、longAccount/shortAccount 比例、timestamp|
|oi_history|/futures/data/openInterestHist?period=5m&limit=14|sumOpenInterest 为 ETH；one_hour_change 包含变化百分数和起止 UTC|

symbol 默认 ETHUSDT，可通过 --symbol 指定。顶层 started_at/finished_at 是本轮 UTC 时间，status 表示必要字段可用性；可选端点失败仍保留 errors。各端点顺序采样，并非原子时点快照。

K 线以最先拉取的交易所时间判断 close_time < serverTime；拿不到交易所时间则不猜测收盘状态。价格保留字符串；计算使用 Decimal。alerts：最近已收盘 K 线 (close/open-1) 绝对值 >=2%；资金费率绝对值 >=0.0005（0.05%）；历史 OI 最近样本与恰好一小时前样本比较，变化绝对值 >=3%。没有精确历史样本时 one_hour_change=null，不用零或估值代替。OI 历史统计可能比当前 OI 延迟，起止时间明确给出。空 alerts 也可能是数据不可用，应同时检查 status/errors。

## 本环境实测：2026-10-31 UTC

按要求依次请求 ping、ETHUSDT 15m limit=3 K 线、premiumIndex、openInterest，均失败：

```
<urlopen error Tunnel connection failed: 403 Forbidden>
```

这是环境出站代理的 CONNECT 403，未建立到币安的 TLS 隧道，**未取得币安 HTTP 状态或响应正文，不是已观测的币安 451**。运行环境 restricted 策略未允许 fapi.binance.com、testnet.binancefuture.com；唯一额外允许的行情域名为 data-api.binance.vision（未拿现货替代合约）。未绕过策略。测试网 ping 与完整快照同样被代理拒绝，故没有可展示的真实测试网行情，evidence/testnet.json 仅为明确标记 testnet 的失败输出。

原始 CONNECT 响应头见 evidence/ping-verbose.txt；逐项探测见 evidence/connectivity.json；完整实跑输出见 evidence/mainnet.json 和 evidence/testnet.json。stdout 里的错误保留每次尝试。单元测试使用明确的合成 fixture，只验证边界与告警，不当成行情演示。
