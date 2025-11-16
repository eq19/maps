freqtrade convert-data --format-from json --format-to jsongz --datadir user_data/data/binance -t 1m 3m 5m 15m 30m 1h 2h 4h 6h 8h 12h 1d 3d 1w 1M --erase
freqtrade convert-data --format-from json --format-to jsongz -t 1m 3m 5m 15m 30m 1h 2h 4h 6h 8h 12h 1d 3d 1w 1M --erase --candle-types futures -p
