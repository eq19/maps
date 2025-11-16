import pandas as pd
import requests_cache
import talib.abstract as ta
import yfinance

import plot

requests_cache.install_cache(cache_name='/tmp/requests_cache.sqlite')

stock = 'BTC-USD'
# 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
dataframe = yfinance.download(tickers=stock, interval='15m', start='2022-12-01', end='2023-01-01', progress=False)  # group_by='ticker'
dataframe.reset_index(inplace=True)

if 'Date' in dataframe:
    dataframe = dataframe.rename(columns={'Date': 'date'})
elif 'Datetime' in dataframe:
    dataframe = dataframe.rename(columns={'Datetime': 'date'})

dataframe = dataframe.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'})
print(list(dataframe))

dataframe['EMA9'] = ta.EMA(dataframe['close'], timeperiod=9)
dataframe['EMA12'] = ta.EMA(dataframe['close'], timeperiod=12)
dataframe['RSI9'] = ta.RSI(dataframe['close'], timeperiod=9)
dataframe['RSI14'] = ta.RSI(dataframe['close'], timeperiod=14)

# import generate_answer
# data['signal_answer'] = generate_answer.generate_answer(data['Close'].to_numpy(), window_backward=1, window_forward=200)
dataframe['signal_answer'] = 0

addplot = [
    {
        'column': 'EMA9',
        'kind': 'line',
        'color': 'red',
    },
    {
        'column': 'EMA12',
        'kind': 'scatter',
        'color': 'white',
    },
]

subplot = [
    [
        {
            'column': 'RSI9',
            'kind': 'line',
            'color': 'white',
        },
        {
            'column': 'RSI14',
            'kind': 'line',
        },
    ],
    [
        {
            'column': 'signal_answer',
            'kind': 'line',
        },
    ],
]

plot.plot(stock, dataframe, addplot=addplot, subplot=subplot, filename='tmp_test_plot/a.html')
plot.plot(stock, dataframe, addplot=addplot, subplot=subplot, filename='tmp_test_plot.html')
