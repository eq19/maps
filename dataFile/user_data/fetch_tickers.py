from freqtrade.resolvers import ExchangeResolver

# Initialize exchange
exchange = ExchangeResolver.load_exchange_from_config("user_data/config.json")

# Fetch ticker for a specific pair
ticker = exchange.fetch_ticker('BTC/IDR')
print(ticker)

# Print all ticker data
#tickers = exchange.fetch_tickers()
#for pair, ticker in tickers.items():
#    print(f"{pair}: {ticker}")
