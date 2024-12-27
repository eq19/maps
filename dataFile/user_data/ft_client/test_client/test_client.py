import ccxt

from freqtrade.resolvers import ExchangeResolver
from freqtrade.configuration import Configuration

# Test ccxt
exchange = ccxt.indodax()
try:
    print(exchange.fetch_ohlcv('BTC/IDR', timeframe='1m', limit=5))
except Exception as e:
    print(f"Error: {e}")

# Test freqtrade
config = Configuration.from_files(["user_data/config_examples/config_indodax.example.json"])
print("timeframe from config is ", config.get("timeframe"))
exchange = ExchangeResolver.load_exchange(config)
ticker = exchange.fetch_ticker('BTC/IDR')
print(ticker)

# Fetch tickers for all pairs
#tickers = exchange.fetch_tickers()
#for pair, ticker in tickers.items():
    #print(f"{pair}: {ticker}")
