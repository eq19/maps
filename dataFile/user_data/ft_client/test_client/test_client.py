import ccxt

from freqtrade.configuration import Configuration
from freqtrade.resolvers import ExchangeResolver

#config = Configuration.from_files(["user_data/config_examples/config_exhange.example.json"])

# Test ccxt
exchange = ccxt.indodax()

# Load the markets to ensure the exchange's metadata is fetched
exchange.load_markets()

# Uncomment fot test freqtrade
# exchange = ExchangeResolver.load_exchange(config)

print("test timeframes", exchange.options['timeframes'])
print("test fetch_ticker", exchange.fetch_ticker('BTC/IDR'))
print("test fetch_ohlcv", exchange.fetch_ohlcv('BTC/IDR', timeframe='1m', limit=5))

#tickers = exchange.fetch_tickers()
#for pair, ticker in tickers.items():
    #print(f"{pair}: {ticker}")
