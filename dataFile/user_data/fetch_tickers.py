from freqtrade.exchange import ExchangeManager
from freqtrade.configuration import Configuration

# Load configuration
config = Configuration.from_files(["config.json"])

# Initialize the exchange
exchange = ExchangeManager(exchange_config=config["exchange"], config=config)

# Fetch ticker for a specific pair
ticker = exchange.fetch_ticker('BTC/IDR')
print(ticker)

# Print all ticker data
#tickers = exchange.fetch_tickers()
#for pair, ticker in tickers.items():
#    print(f"{pair}: {ticker}")
