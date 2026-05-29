from datetime import timedelta, datetime
import io
import time
import pandas as pd
import pandas_ta as ta
import talib




# gn_apikey = "2IdssT12vWQHtIZ5NAeYXojHhG5"
# gn_url_base = "https://api.glassnode.com"
# MONGODB_CONNSTRING =  "mongodb://admin:AykM]0t>P2pJj@a6552e1778445424599e1de4b365b486-add215195500a0f5.elb.eu-central-1.amazonaws.com/trendmaster"



# # backend = requests_cache.SQLiteCache('user_data/db/glassnode.cache.sqlite', timeout=30)
# ttl = timedelta(days=1)
# backend = MongoCache(db_name = "trendmaster", connection=pymongo.MongoClient(MONGODB_CONNSTRING))
# # backend.set_ttl(ttl, overwrite=False)
# session = CachedSession('trendmaster', backend=backend, use_cache_dir=True, expire_after=ttl)

# def download_task(t, gn_timestamp_since, gn_timestamp_until):
#     response = session.get(url=gn_url_base + t['path'],
#                 params={
#                     "a": t['symbol'],
#                     "s": gn_timestamp_since,
#                     "u": gn_timestamp_until,
#                     "i": t['resolution'],
#                     "f": "CSV",
#                     "timestamp_format": "humanized",
#                     "api_key": gn_apikey
#     })

#     # print (f"{t['i']} {t['path']} -> {response.status_code}")
#     print(".", end='', flush=True)

#     # if rate limit hit, sleep 10 seconds and retry
#     if response.status_code == 429:
#         print("!", end='', flush=True)
#         time.sleep(10)
#         return download_task(t, gn_timestamp_since, gn_timestamp_until)

#     # if unknown error, return empty list
#     if response.status_code in [500, 403]:
#         print("x", end='', flush=True)
#         print(t['path'], response.text)
#         return []

#     # if success, return json
#     if response.status_code == 200:
#         return response.text




# def process_task(t, gn_timestamp_since, gn_timestamp_until):
#     r = download_task(t, gn_timestamp_since, gn_timestamp_until)
#     if r != None and len(r) > 0:
#         rdf = pd.read_csv(io.StringIO(r))
#         if t['resolution'] == '24h':
#             rdf['timestamp'] = pd.to_datetime(rdf['timestamp'], utc=True) + pd.DateOffset(1)
#         elif t['resolution'] == '1h':
#             rdf['timestamp'] = pd.to_datetime(rdf['timestamp'], utc=True) + pd.offsets.Hour(1)

#         rdf = rdf.set_index('timestamp')
#         # print(t['path'], t['resolution'])
#         # print(rdf)

#         # rename columns
#         for c in rdf.columns:
#             metric_name = f"%-{t['symbol']}_t{t['tier']}_{t['path'].replace('/v1/metrics/', '').replace('/', '_')}_{t['resolution']}_{c}"
#             rdf = rdf.rename(columns={c: metric_name})

#         # caluclate some metric features
#         for name in rdf.columns:
#             # defragment df
#             rdf = rdf.copy()
#             rdf = extract_feature_metrics(rdf, name)

#         rdf = rdf.asfreq('1h', method='ffill')

#         return rdf
#     else:
#         return pd.DataFrame([])

def bias(values, length):
    bma = talib.SMA(values, length)
    return (values / bma) - 1

def extract_feature_metrics(df, name):
    # bias
    df[f'{name}_bias_6'] = bias(df[name], length=6)
    # df[f'{name}_bias_12'] = bias(df[name], length=12)
    df[f'{name}_bias_24'] = bias(df[name], length=24)
    # mom
    df[f'{name}_mom_6'] = talib.MOM(df[name], timeperiod=6)
    # df[f'{name}_mom_12'] = talib.MOM(df[name], timeperiod=12)
    df[f'{name}_mom_24'] = talib.MOM(df[name], timeperiod=24)
    # roc
    df[f'{name}_roc_6'] = talib.ROC(df[name], timeperiod=6)
    # df[f'{name}_roc_12'] = talib.ROC(df[name], timeperiod=12)
    df[f'{name}_roc_24'] = talib.ROC(df[name], timeperiod=24)
    # rsi
    df[f'{name}_rsi_6'] = talib.RSI(df[name], timeperiod=6)
    # df[f'{name}_rsi_12'] = talib.RSI(df[name], timeperiod=12)
    df[f'{name}_rsi_24'] = talib.RSI(df[name], timeperiod=24)
    # # slope
    df[f'{name}_slope_6'] = ta.slope(df[name], length=6)
    # df[f'{name}_slope_12'] = ta.slope(df[name], length=12)
    df[f'{name}_slope_24'] = ta.slope(df[name], length=24)
    # # sma
    df[f'{name}_sma_6'] = talib.SMA(df[name], timeperiod=6)
    # df[f'{name}_sma_12'] = talib.SMA(df[name], timeperiod=12)
    df[f'{name}_sma_24'] = talib.SMA(df[name], timeperiod=24)
    # wma
    df[f'{name}_wma_6'] = talib.WMA(df[name], timeperiod=6)
    # df[f'{name}_wma_12'] = talib.WMA(df[name], timeperiod=12)
    df[f'{name}_wma_24'] = talib.WMA(df[name], timeperiod=24)
    # var
    df[f'{name}_var_6'] = talib.VAR(df[name], timeperiod=6)
    # df[f'{name}_var_12'] = talib.VAR(df[name], timeperiod=12)
    df[f'{name}_var_24'] = talib.VAR(df[name], timeperiod=24)
    # stddev
    df[f'{name}_stddev_6'] = talib.STDDEV(df[name], timeperiod=6, nbdev=1)
    # df[f'{name}_stddev_12'] = talib.STDDEV(df[name], timeperiod=12, nbdev=1)
    df[f'{name}_stddev_24'] = talib.STDDEV(df[name], timeperiod=24, nbdev=1)
    # zscore
    df[f'{name}_zscore_6'] = (df[name] - df[f'{name}_sma_6']) / df[f'{name}_stddev_6']
    # df[f'{name}_zscore_12'] = (df[name] - df[f'{name}_sma_12']) / df[f'{name}_stddev_12']
    df[f'{name}_zscore_24'] = (df[name] - df[f'{name}_sma_24']) / df[f'{name}_stddev_24']

    return df