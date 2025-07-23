import ccxt
import pprint

from freqtrade.configuration import Configuration
from freqtrade.resolvers import ExchangeResolver

#config = Configuration.from_files(["user_data/config_examples/config_exhange.example.json"])

# Test ccxt
exchange = ccxt.indodax()
markets = exchange.load_markets()

# Load the markets to ensure the exchange's metadata is fetched
exchange.load_markets()

# Uncomment fot test freqtrade
# exchange = ExchangeResolver.load_exchange(config)

print("test markets", markets['BTC/IDR'])
print("test fetch_ticker", exchange.fetch_ticker('BTC/IDR'))
print("test fetch_ohlcv", exchange.fetch_ohlcv('BTC/IDR', timeframe='1m', limit=5))
print("available options", exchange.options)
print("supported methods", exchange.has)
print("exchange api", exchange.api)
pprint.pprint(exchange.describe())


#tickers = exchange.fetch_tickers()
#for pair, ticker in tickers.items():
    #print(f"{pair}: {ticker}")
