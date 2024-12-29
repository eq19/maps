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

telegram_config = config.get("telegram")
if telegram_config:
    telegram_id = telegram_config.get("chat_id")
    print("Notification ID from config is", telegram_id)
else:
    print("Notification ID is not found.")

#exchange = ExchangeResolver.load_exchange(config)
#print(exchange)
ticker = exchange.fetch_ticker('BTC/IDR')
print(ticker)

# Fetch tickers for all pairs
#tickers = exchange.fetch_tickers()
#for pair, ticker in tickers.items():
    #print(f"{pair}: {ticker}")
