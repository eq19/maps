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
print(config)

api_server_config = config.get("api_server")
if api_server_config:
    ip_address = api_server_config.get("listen_ip_address")
    print("IP from config is", ip_address)
else:
    print("API server config not found.")

# Retrieve the value of "chat_id" under the "telegram" section
chat_id = config.get("api_server.listen_ip_address")
print("API Server from config is", chat_id)


# Retrieve the value of "chat_id" under the "telegram" section
ip_address = config.get("api_server.listen_ip_address")
print("API Server from config is", ip_address)

exchange = ExchangeResolver.load_exchange(config)
ticker = exchange.fetch_ticker('BTC/IDR')
print(ticker)

# Fetch tickers for all pairs
#tickers = exchange.fetch_tickers()
#for pair, ticker in tickers.items():
    #print(f"{pair}: {ticker}")
