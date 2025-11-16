from freqtrade.configuration import Configuration
from freqtrade.data.dataprovider import DataProvider
from freqtrade.freqai.data_kitchen import FreqaiDataKitchen
from freqtrade.resolvers import StrategyResolver

config = Configuration.from_files(['./config.json'])
config['timerange'] = '20210801-20220101'
pair = 'ETH/USDT'

# from FreqaiExampleStrategy import FreqaiExampleStrategy
# strategy = FreqaiExampleStrategy(config=config)
strategy = StrategyResolver.load_strategy(config=config)
strategy.freqai_info = config['freqai']
strategy.dp = DataProvider(config=config, exchange=None, pairlists=None, rpc=None)

# timeframe = strategy.timeframe
timeframe = '5m'
dataframe = strategy.dp.get_pair_dataframe(pair, timeframe)

dk = FreqaiDataKitchen(config=config, live=False, pair=pair)
dataframe = dk.use_strategy_to_populate_indicators(
    strategy=strategy, prediction_dataframe=dataframe, pair=pair
)

print(dataframe)
print(list(dataframe))
