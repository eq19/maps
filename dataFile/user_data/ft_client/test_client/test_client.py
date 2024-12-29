import ccxt

from freqtrade.configuration import Configuration
from freqtrade.resolvers import ExchangeResolver

# Test ccxt
exchange = ccxt.indodax()
print(exchange.fetch_ticker('BTC/IDR'))

# Test freqtrade
config = Configuration.from_files(["user_data/config_examples/config_indodax.example.json"])
exchange = ExchangeResolver.load_exchange(config)
tickers = exchange.fetch_tickers()
for pair, ticker in tickers.items():
    print(f"{pair}: {ticker}")
print(exchange.fetch_ohlcv('BTC/IDR', timeframe='1m', limit=5))
