import numpy
from pandas import DataFrame
from freqtrade.configuration import Configuration
from freqtrade.data.dataprovider import DataProvider
from freqtrade.freqai.data_kitchen import FreqaiDataKitchen
from freqtrade.resolvers import StrategyResolver
import generate_dataset

def column_feature(dataframe: DataFrame) -> list:  # list[str]
    column_names = dataframe.columns
    feature = [c for c in column_names if c[0] == '%']
    return feature

def column_label(dataframe: DataFrame) -> list:  # list[str]
    column_names = dataframe.columns
    label = [c for c in column_names if c[0] == '&']
    return label

def load_data(pair: str = 'ETH/USDT', timerange: str = '20210701-20220701', window: int = 1,
              return_column_feature: bool = False):

    config = Configuration.from_files(['./config.json'])
    config['timerange'] = timerange

    strategy = StrategyResolver.load_strategy(config=config)
    strategy.freqai_info = config['freqai']
    strategy.dp = DataProvider(config=config, exchange=None, pairlists=None, rpc=None)

    timeframe = strategy.timeframe
    dataframe = strategy.dp.get_pair_dataframe(pair, timeframe)

    dk = FreqaiDataKitchen(config=config, live=False, pair=pair)
    dataframe = dk.use_strategy_to_populate_indicators(
        strategy=strategy, prediction_dataframe=dataframe, pair=pair
    )

    feature = dataframe[column_feature(dataframe)].to_numpy(dtype='float32')
    feature_mask = (dataframe['volume'] > 0).to_numpy(dtype='bool')

    label = dataframe[column_label(dataframe)].to_numpy(dtype='float32')
    label_mask = numpy.full(len(label), True, dtype='bool')

    x_train, y_train, x_test, y_test = (
        generate_dataset.generate_dataset(feature, feature_mask, label, label_mask, window=window, batch_size=200,
                                          split_ratio=0.95, train_include_test=False, enable_window_nomalization=True)
    )

    if len(x_train) == 0 or len(x_test) == 0:
        raise Exception

    if not return_column_feature:
        return (x_train, y_train, x_test, y_test)
    else:
        return (x_train, y_train, x_test, y_test, column_feature(dataframe))
