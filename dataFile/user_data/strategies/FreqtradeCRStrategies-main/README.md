# FreqtradeCRStrategies
[Freqtrade](https://www.freqtrade.io/en/stable/ "Freqtrade documentation") strategies inspired by the [Crypto Robot Youtube channel](https://www.youtube.com/channel/UCGjfXO9kR34es5IsHLyP5eA "Crypto Robot Youtube channel").

- AlligatorStrategy: https://www.youtube.com/watch?v=tHYs5135jUA
- CrossEMAStrategy: https://www.youtube.com/watch?v=z9dbgvAYDuA
- SupertrendStrategy: https://www.youtube.com/watch?v=rl00g3-Iv5A
- TrixStrategy: https://www.youtube.com/watch?v=uE04UROWkjs

**This repository is not affiliated with the channel, it is a personal programming exercise.
Do not use these strategies without (back)testing them.**

## Installation

1. Install Freqtrade (see [documentation](https://www.freqtrade.io/en/stable/docker_quickstart/ "official documentation").)
2. Add strategies to your [user_data/strategies/](user_data/strategies/) folder
3. Set up your [/user_data/config.json](/user_data/config.json) file. You'll find some examples in this repo.
4. Add the dockerfile [/docker/Dockerfile.custom](/docker/Dockerfile.custom)
5. Add the dockerfile and the strategy name in the [docker-compose.yml](/docker-compose.yml)

```
---
version: '3'
services:
  freqtrade:
    build:
      context: .
      dockerfile: "./docker/Dockerfile.custom"
    restart: unless-stopped
    container_name: freqtrade
    volumes:
      - "./user_data:/freqtrade/user_data"
    ports:
      - "127.0.0.1:8080:8080"
    command: >
      trade
      --logfile /freqtrade/user_data/logs/freqtrade.log
      --db-url sqlite:////freqtrade/user_data/tradesv3.sqlite
      --config /freqtrade/user_data/config.json
      --strategy AlligatorStrategy
```
6. In your Freqtrade folder: `sudo docker-compose up -d`

## Backtests

### TrixV15Strategy

```
=============== SUMMARY METRICS ================
| Metric                 | Value               |
|------------------------+---------------------|
| Backtesting from       | 2021-01-01 00:00:00 |
| Backtesting to         | 2021-12-12 15:00:00 |
| Max open trades        | 269                 |
|                        |                     |
| Total/Daily Avg Trades | 5933 / 17.2         |
| Starting balance       | 1000.000 USDT       |
| Final balance          | 7037.690 USDT       |
| Absolute profit        | 6037.690 USDT       |
| Total profit %         | 603.77%             |
| Trades per day         | 17.2                |
| Avg. daily profit %    | 1.75%               |
| Avg. stake amount      | 100.000 USDT        |
| Total trade volume     | 593300.000 USDT     |
|                        |                     |
| Best Pair              | OXT/USDT 198.10%    |
| Worst Pair             | ONG/USDT -112.13%   |
| Best trade             | DNT/USDT 55.24%     |
| Worst trade            | MDT/USDT -31.14%    |
| Best day               | 297.207 USDT        |
| Worst day              | -1606.388 USDT      |
| Days win/draw/lose     | 285 / 5 / 55        |
| Avg. Duration Winners  | 13:29:00            |
| Avg. Duration Loser    | 5 days, 21:39:00    |
| Rejected Buy signals   | 0                   |
|                        |                     |
| Min balance            | 1014.400 USDT       |
| Max balance            | 8337.489 USDT       |
| Drawdown               | 2419.06%            |
| Drawdown               | 2421.476 USDT       |
| Drawdown high          | 4515.515 USDT       |
| Drawdown low           | 2094.040 USDT       |
| Drawdown Start         | 2021-05-10 16:00:00 |
| Drawdown End           | 2021-06-22 12:00:00 |
| Market change          | 559.54%             |
================================================
```

![TrixV15Strategy](https://raw.githubusercontent.com/DarkTipiak/FreqtradeCRStrategies/main/TrixV15Strategy.freqtrade-profit-plot.png)

### TrixV21Strategy

```
=============== SUMMARY METRICS ================
| Metric                 | Value               |
|------------------------+---------------------|
| Backtesting from       | 2021-01-01 00:00:00 |
| Backtesting to         | 2021-12-12 15:00:00 |
| Max open trades        | 269                 |
|                        |                     |
| Total/Daily Avg Trades | 4719 / 13.68        |
| Starting balance       | 1000.000 USDT       |
| Final balance          | 5696.551 USDT       |
| Absolute profit        | 4696.551 USDT       |
| Total profit %         | 469.66%             |
| Trades per day         | 13.68               |
| Avg. daily profit %    | 1.36%               |
| Avg. stake amount      | 100.000 USDT        |
| Total trade volume     | 471900.000 USDT     |
|                        |                     |
| Best Pair              | OXT/USDT 155.60%    |
| Worst Pair             | SAND/USDT -63.48%   |
| Best trade             | DNT/USDT 55.24%     |
| Worst trade            | MANA/USDT -31.14%   |
| Best day               | 184.460 USDT        |
| Worst day              | -274.863 USDT       |
| Days win/draw/lose     | 235 / 17 / 94       |
| Avg. Duration Winners  | 13:18:00            |
| Avg. Duration Loser    | 1 day, 14:54:00     |
| Rejected Buy signals   | 0                   |
|                        |                     |
| Min balance            | 988.138 USDT        |
| Max balance            | 5870.146 USDT       |
| Drawdown               | 731.08%             |
| Drawdown               | 731.814 USDT        |
| Drawdown high          | 3340.155 USDT       |
| Drawdown low           | 2608.341 USDT       |
| Drawdown Start         | 2021-05-08 17:00:00 |
| Drawdown End           | 2021-07-20 19:00:00 |
| Market change          | 512.58%             |
================================================
```

![TrixV21Strategy](https://raw.githubusercontent.com/DarkTipiak/FreqtradeCRStrategies/main/TrixV21Strategy.freqtrade-profit-plot.png)

### TrixV23Strategy

```
=============== SUMMARY METRICS ================
| Metric                 | Value               |
|------------------------+---------------------|
| Backtesting from       | 2021-01-01 00:00:00 |
| Backtesting to         | 2021-12-12 15:00:00 |
| Max open trades        | 269                 |
|                        |                     |
| Total/Daily Avg Trades | 4384 / 12.71        |
| Starting balance       | 1000.000 USDT       |
| Final balance          | 5087.156 USDT       |
| Absolute profit        | 4087.156 USDT       |
| Total profit %         | 408.72%             |
| Trades per day         | 12.71               |
| Avg. daily profit %    | 1.18%               |
| Avg. stake amount      | 100.000 USDT        |
| Total trade volume     | 438400.000 USDT     |
|                        |                     |
| Best Pair              | OXT/USDT 113.59%    |
| Worst Pair             | RLC/USDT -64.41%    |
| Best trade             | DNT/USDT 55.24%     |
| Worst trade            | MANA/USDT -31.14%   |
| Best day               | 213.146 USDT        |
| Worst day              | -332.471 USDT       |
| Days win/draw/lose     | 171 / 97 / 78       |
| Avg. Duration Winners  | 13:34:00            |
| Avg. Duration Loser    | 1 day, 12:12:00     |
| Rejected Buy signals   | 0                   |
|                        |                     |
| Min balance            | 997.635 USDT        |
| Max balance            | 5450.985 USDT       |
| Drawdown               | 508.82%             |
| Drawdown               | 509.325 USDT        |
| Drawdown high          | 3708.862 USDT       |
| Drawdown low           | 3199.537 USDT       |
| Drawdown Start         | 2021-09-19 10:00:00 |
| Drawdown End           | 2021-09-28 23:00:00 |
| Market change          | 561.59%             |
================================================
```

![TrixV23Strategy](https://raw.githubusercontent.com/DarkTipiak/FreqtradeCRStrategies/main/TrixV23Strategy.freqtrade-profit-plot.png)

---

Thanks to Crypto Robot, and to all those who share their knowledge