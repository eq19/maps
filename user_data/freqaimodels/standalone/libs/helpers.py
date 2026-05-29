
import json
import uuid
import numpy as np
import pandas as pd
import pandas_ta as ta
import talib
import plotly.express as px
import logging
import time
import numba as nb

logger = logging.getLogger(__name__)


nb.jit
def calculate_speed(df: pd.DataFrame, target='close'):
    df[f'{target}_speed'] = df[target].pct_change(1)
    df[f'{target}_acceleration'] = df[f'{target}_speed'].pct_change(1)
    df[f'{target}_rising'] = np.where(df[target] > df[target].shift(1), 1, 0)

    return df

nb.jit
def create_target(df, long, method='polyfit', polyfit_var='close', pct=0.1):
    if method == 'polyfit':

        trend_list = []
        slope_list = []
        start_list = []
        end_list = []

        index_l = np.arange(long)
        rolling_df = df[polyfit_var].rolling(window=long, min_periods=long)
        for roll in rolling_df:
            if len(roll) < long:
                continue
            slope_array = np.round(np.polyfit(index_l, roll.values, deg=1)[-2], decimals=8)
            slope_list.append(slope_array)
            trend_list.append(np.where(slope_array > 0, 1, np.where(slope_array == 0, 0, -1)).tolist())
            start_list.append(roll.index[0])
            end_list.append(roll.index[long-1])

    if method == 'pct':
        df_copy = df.copy()
        trend_list = []
        start_list = []
        end_list = []
        for i in df_copy.close.rolling(window=long):
            start_list.append(i.index[0])
            end_list.append(i.index[long -1])
            if i.shape[0] < long:
                continue
            if (i.iloc[0] / i.iloc[long -1]) > 1 + pct:
                trend_list.append(1)
            elif (i.iloc[0] / i.iloc[long -1]) < 1 - pct:
                trend_list.append(-1)
            else:
                trend_list.append(0)

    y = pd.DataFrame({'trend': trend_list, 'slope': slope_list, 'start_windows': start_list, 'end_windows': end_list})
    return y

nb.jit
def create_lag(data: pd.DataFrame, lag_len: int, ignore_columns = ['trend', 'pmX_10_3_12_1', 'pmX_10_3_12_1_6H', 'pmX_10_3_12_1_1D', 'date', 'open', 'close', 'high', 'low']):
    logger.info(f"ENTER .create_lag() {data.shape} {lag_len}")
    start_time = time.time()

    lags_array = []

    if type(lag_len) is int:
        lag_len = list(range(1, lag_len))

    for col in data.columns:
        # skip ignored columns
        if col in ignore_columns:
            continue

        if hasattr(data[col], 'dtype') and data[col].dtype == object:
            continue

        lag_df = pd.DataFrame()

        # add classic lag
        if (col.find('_std') == -1
            and col.find('_upper_band') == -1
            and col.find('_lower_band') == -1
            and col.find('_upper_envelope') == -1
            and col.find('_lower_envelope') == -1
            and col.find('%-dist_to_') == -1
            and col.find('%-s1') == -1
            and col.find('%-s2') == -1
            and col.find('%-s3') == -1
            and col.find('%-r1') == -1
            and col.find('%-r2') == -1
            and col.find('%-r3') == -1):
            # iterate all lags
            for ind, lag in enumerate(lag_len):
                f = f'{col}_lag_{lag}'
                lag_df[f] = data[col].shift(lag)

        # check if column is not trend or candle pattern or alpha
        if (col.find('_std') == -1
            and col.find('_upper_band') == -1
            and col.find('_lower_band') == -1
            and col.find('_upper_envelope') == -1
            and col.find('_lower_envelope') == -1
            and col.find('%-dist_to_') == -1
            and col.find('%-s1') == -1
            and col.find('%-s2') == -1
            and col.find('%-s3') == -1
            and col.find('%-r1') == -1
            and col.find('%-r2') == -1
            and col.find('%-r3') == -1
            and col.find('date') == -1
            and col.find('_change_') == -1
            and col.find('_diff_') == -1
            and col.find('trend') == -1
            and col.find('%-CDL') == -1
            and col.find('%-alpha') == -1
            and col.find('pmX') == -1
            and col.find('SUPERT') == -1
            and col.find('_diff') == -1
            and col.find('_divergence') == -1
            and col.find('_signal') == -1):
            # calculate diff and div lag stats
            for ind, lag in enumerate(lag_len):
                f = f'{col}_lag_{lag}'
                if ind == 0:
                    lag_df[ f +'_diff_lag_0'] = lag_df[f] - data[col]
                    if (data[col] != 0).all():
                        lag_df[ f +'_div_lag_0'] = lag_df[f] / data[col]
                    else:
                        lag_df[ f +'_div_lag_0'] = 0
                else:
                    lag_df[f'{f}_diff_lag_{lag -1}'] = lag_df[f] - lag_df[f'{col}_lag_{lag -1}']
                    if (lag_df[f'{col}_lag_{lag -1}'] != 0).all():
                        lag_df[f'{f}_div_lag_{lag -1}'] = lag_df[f] / lag_df[f'{col}_lag_{lag -1}']
                    else:
                        lag_df[f'{f}_div_lag_{lag -1}'] = 0

            # lag_df[ f +f'_diff_lag_all'] = lag_df[f'{col}_lag_{lag_len[0]}'] - lag_df[f'{col}_lag_{lag_len[-1]}']
            # if (lag_df[f'{col}_lag_{lag_len[-1]}'] != 0).all():
            #     lag_df[ f +f'_div_lag_all'] = lag_df[f'{col}_lag_{lag_len[0]}'] / lag_df[f'{col}_lag_{lag_len[-1]}']
            # else:
            #     lag_df[ f +f'_div_lag_all'] = 0

        # add lag to array
        lags_array.append(lag_df)

    data = pd.concat([data] + lags_array, axis=1)
    data = data.copy()

    # export columns to csv
    # with (open(f'lag_columns.json', 'w')) as f:
        # json.dump(data.columns.tolist(), f)

    logger.info(f"EXIT .create_lag() {data.shape} {lag_len}, execution time: {time.time() - start_time:.2f} seconds")

    return data


def create_lag_from_trend(data, lag_len):
    data = pd.DataFrame(data).copy()
    col = data.columns

    if type(lag_len) is int:
        lag_len = range(1, lag_len)

    for col in data.columns:
        for lag in lag_len:
            f = f'{col}_lag_{lag}'
            data[f] = data[col].shift(lag *6)
    return data.drop(columns=col).fillna(-2)


def load_resource(path, name, freq='1H', date_key='timestamp', date_unit='s', value_key='value', shift=0):
    # load resource
    rdf = pd.read_csv(path)
    if (date_unit):
        rdf[date_key] = pd.to_datetime(rdf[date_key], unit=date_unit)
    else: rdf[date_key] = pd.to_datetime(rdf[date_key])
    rdf.set_index(date_key, inplace=True)

    if (shift > 0):
        rdf[value_key] = rdf[value_key].shift(shift)

    rdf = rdf.asfreq(freq, method='ffill')

    # remove additional columns
    for col in rdf.columns:
        if col != value_key:
            rdf.drop(columns=col, inplace=True)

    # rename value column
    rdf.rename(columns={value_key: name}, inplace=True)

    # caluclate some metric features
    # bias
    rdf[f'{name}_bias_6'] = ta.bias(rdf[name], length=6)
    rdf[f'{name}_bias_12'] = ta.bias(rdf[name], length=12)
    rdf[f'{name}_bias_24'] = ta.bias(rdf[name], length=24)
    # mom
    rdf[f'{name}_mom_6'] = ta.mom(rdf[name], length=6)
    rdf[f'{name}_mom_12'] = ta.mom(rdf[name], length=12)
    rdf[f'{name}_mom_24'] = ta.mom(rdf[name], length=24)
    # roc
    rdf[f'{name}_roc_6'] = ta.roc(rdf[name], length=6)
    rdf[f'{name}_roc_12'] = ta.roc(rdf[name], length=12)
    rdf[f'{name}_roc_24'] = ta.roc(rdf[name], length=24)
    # rsi
    rdf[f'{name}_rsi_6'] = ta.rsi(rdf[name], length=6)
    rdf[f'{name}_rsi_12'] = ta.rsi(rdf[name], length=12)
    rdf[f'{name}_rsi_24'] = ta.rsi(rdf[name], length=24)
    # slope
    rdf[f'{name}_slope_6'] = ta.slope(rdf[name], length=6)
    rdf[f'{name}_slope_12'] = ta.slope(rdf[name], length=12)
    rdf[f'{name}_slope_24'] = ta.slope(rdf[name], length=24)
    # sma
    rdf[f'{name}_sma_6'] = ta.sma(rdf[name], length=6)
    rdf[f'{name}_sma_12'] = ta.sma(rdf[name], length=12)
    rdf[f'{name}_sma_24'] = ta.sma(rdf[name], length=24)
    # # percent_return
    # rdf[f'{name}_percent_return_6'] = ta.percent_return(rdf[name], length=6)
    # rdf[f'{name}_percent_return_12'] = ta.percent_return(rdf[name], length=12)
    # rdf[f'{name}_percent_return_24'] = ta.percent_return(rdf[name], length=24)
    # # log_return
    # rdf[f'{name}_log_return_6'] = ta.log_return(rdf[name], length=6)
    # rdf[f'{name}_log_return_12'] = ta.log_return(rdf[name], length=12)
    # rdf[f'{name}_log_return_24'] = ta.log_return(rdf[name], length=24)

    return rdf

def load_many_resources(resources, freq='1H', date_key='timestamp', date_unit='s'):
    many_dfs = []
    for [path, name, value_key, shift] in resources:
        many_dfs.append(load_resource(path, name, freq, date_key, date_unit, value_key, shift))
        print(f'Loaded {name} from {path} with shape {many_dfs[-1].shape}')
    return pd.concat(many_dfs, axis=1)

def split_data_oot(data, y, eval_date='2022-12-01', test_date='2022-12-14'):

    train_data = data[:eval_date].copy()
    eval_data = data[eval_date:test_date].copy()
    test_data = data[test_date:].copy()

    train_y = y[:eval_date].copy()
    eval_y = y[eval_date:test_date].copy()
    test_y = y[test_date:].copy()

    return train_data, train_y, eval_data, eval_y, test_data, test_y

def create_col_trend(col, pred_target, df, method='polyfit'):
    #if col == 'trend' or col.find('pmX') != -1 or col.find('date') != -1:
    #    return
    trend_col = create_target(df, pred_target, method=method, polyfit_var=col)
    trend_col = (trend_col[['trend', 'slope', 'end_windows']].set_index('end_windows')
        .rename(columns={
            'trend': col + '_trend',
            'slope': col + '_slope'
            }
        ))
    return trend_col

def create_target_last(df, pred_target, method='polyfit', polyfit_var=None):
    target = create_target(df, pred_target,
                                       method='polyfit', polyfit_var=polyfit_var)

    target = target[['trend', 'slope', 'start_windows']].set_index('start_windows')

    target['&-trend_long'] = np.where(target['trend'] == 1, 'trend_long', 'trend_not_long')
    target['&-trend_short'] = np.where(target['trend'] == -1, 'trend_short', 'trend_not_short')

    return target

def extract_currencies(symbol):
    # from BTC/USDT:USDT extract base and quote currencies
    base = symbol.split('/')[0]
    quote = symbol.split('/')[1].split(':')[0]
    market = base + quote
    return [market, base, quote]


def extract_currencies_simple(symbol):
    # from BTC/USDT extract base and quote currencies
    base = symbol.split('/')[0]
    quote = symbol.split('/')[1]
    market = base + quote
    return [market, base, quote]

def get_uuid_from_key(key: str):
    namespaceUUID = uuid.UUID('296aa47c-9f5c-4995-a2b8-857ab9a372b5')
    return str(uuid.uuid3(namespaceUUID, key))
