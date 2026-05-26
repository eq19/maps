from tvDatafeed import TvDatafeed,Interval
import multiprocessing as mp
from datetime import date, timedelta
import pandas as pd
import numpy as np
from lib.ma import MovingAveragesCalculate
from lib.mom import MomentumANDVolatilityCalculate
from lib.cycle import CycleCalculate
from lib.trend import TrendCalculate
from lib.oscillators import OscillatorsCalculate
import logging

logger = logging.getLogger(__name__)

username = 'roma@nikitin.me'
password = 'GameOver42!'

stock_info = {
    'SP500':{'symbol':'SPX', 'exchange':'SP', 'lag':'r', 'interval':'1H' },
    'Dow_Jones': {'symbol':'DJI', 'exchange':'DJ', 'lag':'r', 'interval':'1H'},
    'NASDAQ': {'symbol':'IXIC', 'exchange':'NASDAQ', 'lag':'15', 'interval':'1H'},
    'FTSE_100': {'symbol':'E100', 'exchange':'EURONEXT', 'lag':'15', 'interval':'1H'},
    'DAX': {'symbol':'DAX', 'exchange':'XETR', 'lag':'15', 'interval':'1H'},
    'CAC_40': {'symbol':'PX1', 'exchange':'EURONEXT', 'lag':'15', 'interval':'1H'},
    'Nikkei_225': {'symbol':'NI225', 'exchange':'TVC', 'lag':'r', 'interval':'1H'},
    'Hang_Seng': {'symbol':'HSI', 'exchange':'TVC', 'lag':'r', 'interval':'1H'},
    'Shanghai': {'symbol':'950082', 'exchange':'SSE', 'lag':'15', 'interval':'1H'},
    'BSE': {'symbol':'BSE500', 'exchange':'BSE', 'lag':'15', 'interval':'1H'},
    'GOLD': {'symbol':'GOLD', 'exchange':'TVC', 'lag':'r', 'interval':'1H'},
    'Coinbase': {'symbol':'COIN', 'exchange':'NASDAQ', 'lag':'r', 'interval':'1H'},
    'MicroStrategy': {'symbol':'MSTR', 'exchange':'NASDAQ', 'lag':'r', 'interval':'1H'},
    'Galaxy_Digital_Holdings': {'symbol':'GLXY', 'exchange':'TSX', 'lag':'15', 'interval':'1H'},
    'Tesla': {'symbol':'TSLA', 'exchange':'NASDAQ', 'lag':'r', 'interval':'1H'},
    'Inflation': {'symbol':'USIRYY', 'exchange':'ECONOMICS', 'lag':'r', 'interval':'1M'},
    'Interest': {'symbol':'IORB', 'exchange':'BVB', 'lag':'r', 'interval':'1M'},
    'Exchange': {'symbol':'USFER', 'exchange':'ECONOMICS', 'lag':'r', 'interval':'1M'},
    'GDP': {'symbol':'GDP', 'exchange':'FRED', 'lag':'r', 'interval':'1M'},
    'Unemployment': {'symbol':'UNRATE', 'exchange':'FRED', 'lag':'r', 'interval':'1M'}
}


def download_task(train_min_timestamp, max_timestamp, TARGET_VAR, TARGET_TF):
    n_days = (date.today() - pd.to_datetime(train_min_timestamp, unit='s').date()).days

    pool = mp.Pool(mp.cpu_count() - 1)

    #stock_list = []
    #for stock_k in stock_info.keys():
    #    stock_list.append(download_stock_data(stock_k, n_days))

    results=[]
    result_cols = []
    train_min_t = pd.to_datetime(train_min_timestamp, unit='s')
    max_t = pd.to_datetime(max_timestamp, unit='s')
    for stock_k in stock_info.keys():
        result = pool.apply_async(download_stock_data, (stock_k, n_days, max_t, train_min_t))
        results.append(result)

    for result in results:
        result_cols.append(result.get())

    pool.close()

    logger.info('Downloaded all stocks')
    logger.info('Calculating TA')
    result_cols = calculate_stock_index_ta(result_cols, TARGET_VAR, TARGET_TF, train_min_t, max_t)
    logger.info('Calculated TA')

    return result_cols



def download_stock_data(stock_name, n_days, max_t, train_min_t):
    logger.info(f'Downloading: {stock_name}')
    tv = TvDatafeed(username=username, password=password)
    stock_ = stock_info[stock_name]
    symbol = stock_['symbol']
    exchange = stock_['exchange']

    interval = None
    if stock_['lag'] == 'r':
        interval = Interval(stock_['interval'])
    elif stock_['lag'] != 'r':
        interval = Interval(stock_['lag'])

    n_bars = None
    if interval.value == '15':
        n_bars = int(15 * 4 * 6.5 * n_days + 15 * 4 * 200)
    elif interval.value == '1H':
        n_bars = int(6.5 * n_days + 6.5 * 200)
    elif interval.value == '1M':
        n_bars = int(n_days // 12)

    df = None
    try:
        df = tv.get_hist(symbol, exchange, interval, n_bars)
    except Exception as e:
        logger.error(e)

    if df is None:
        try:
            df = tv.get_hist(symbol, exchange, interval, n_bars)
        except Exception as e:
            logger.error(e)
    
    if df is None:
        df = pd.DataFrame(index=pd.DataFrame(index=pd.date_range(start=train_min_t, end=max_t)))
        df['symbol'] = None
        df['open'] = 0
        df['high'] = 0
        df['low'] = 0
        df['close'] = 0
        df['volume'] = 0

    if interval.value == '15':
        df = df.shift()
    
    df = df.asfreq('1h', method='ffill').fillna(0)
    
    if np.all(df.index.minute != 0):
        df.index = df.index + timedelta(minutes=int(60 - df.index.minute[0]))
    
    df = df.sort_index()

    df = df.loc[:max_t]

    return {stock_name:df}
    

def calculate_stock_index_ta(result_cols, TARGET_VAR, TARGET_TF, train_min_t, max_t):

    index_s_list = []
    for i in range(len(result_cols)):
        rc = result_cols[i]
        for name, df_t in rc.items():
            df_t = df_t.drop(columns='symbol')
            df_t.columns = [x.lower() for x in df_t.columns]
            df_t['hlc3'] = (df_t['high'] + df_t['low'] + df_t['close']) / 3
            df_t['hl2'] = (df_t['high'] + df_t['low']) / 2
            df_t['ohlc4'] = (df_t['open'] + df_t['high'] + df_t['low'] + df_t['close']) / 4

            df_t['hlc3_log'] = np.log(df_t['hlc3'])
            df_t['hl2_log'] = np.log(df_t['hl2'])
            df_t['ohlc4_log'] = np.log(df_t['ohlc4'])

            df_t['close_log'] = np.log(df_t['close'])
            df_t['high_log'] = np.log(df_t['high'])
            df_t['low_log'] = np.log(df_t['low'])
            df_t['open_log'] = np.log(df_t['open'])
            df_t = df_t.apply(lambda x: x.replace([np.inf,-np.inf], np.nan))
            df_t = df_t.fillna(0)
            df_t = df_t.reset_index()
            df_t = df_t.rename(columns={'datetime':'date'})
            df_t['date'] = pd.to_datetime(df_t['date'])
            df_t = df_t.dropna().drop_duplicates('date').sort_values('date')
            df_t = df_t.set_index('date')
            # filter out 2021
            df_t = df_t.asfreq(TARGET_TF, method='ffill')

            mac = MovingAveragesCalculate(df_t, periods=[20, 50, 100, 200],
                                      kama_periods=[13, 35, 50], hma_periods=[10, 20, 35],
                                      reg_len=6, enable_linreg=False, calc_col=TARGET_VAR)
            df_t = mac.calculate_all()

            # Momentum Indicators
            mvc = MomentumANDVolatilityCalculate(
                df_t, close_col='ohlc4_log', high_col='high_log', low_col='low_log')
            df_t = mvc.calculate_all()

            # Cycle Indicators
            cc = CycleCalculate(df_t, calc_col=TARGET_VAR)
            df_t = cc.calculate_all()

            # Trend Indicators
            tc = TrendCalculate(df_t, close_col='close_log', high_col='high_log', low_col='low_log',
                                open_col='open_log')
            df_t = tc.calculate_all()

            # Oscillator Indicators
            oc = OscillatorsCalculate(df_t, close_col='close_log')
            df_t = oc.calculate_all()

            df_t.columns = ['%-' + name + '_' + x for x in df_t.columns]

            df_t = df_t.loc[train_min_t:max_t]

            cat_col = [x for x in df_t if x.find('pmX_10_3_12_1') != -1]

            for col in cat_col:
                df_t[col] = df_t[col].map({'down': 0, 'up': 1})

            index_s_list.append(df_t)

    return index_s_list
    