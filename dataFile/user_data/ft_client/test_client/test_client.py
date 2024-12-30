import ccxt

from freqtrade.configuration import Configuration
from freqtrade.resolvers import ExchangeResolver

config = Configuration.from_files(["user_data/config_examples/config_indodax.example.json"])

# Test ccxt
exchange = ccxt.indodax()

# Uncomment fot test freqtrade
# exchange = ExchangeResolver.load_exchange(config)

print("test timeframes", exchange.timeframes)
print("test fetch_ticker", exchange.fetch_ticker('BTC/IDR'))
print("test fetch_ohlcv", exchange.fetch_ohlcv('BTC/IDR', timeframe='1m', limit=5))

#tickers = exchange.fetch_tickers()
#for pair, ticker in tickers.items():
    #print(f"{pair}: {ticker}")
