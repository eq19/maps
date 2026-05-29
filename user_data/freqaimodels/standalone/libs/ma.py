import itertools
import talib
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import pandas_ta as ta
import lib.helpers as h

class MovingAveragesCalculate:

    def __init__(self, data:pd.DataFrame, periods=None, kama_periods=None, hma_periods=None, reg_len=None, enable_linreg=False,
                calc_col='close'):
        self.data = data.copy()
        self.periods = periods
        self.kama_periods = kama_periods
        self.hma_periods = hma_periods
        self.reg_len = reg_len
        self.enable_linreg = enable_linreg
        self.calc_col = calc_col

        self.ti_dict = {
            "SMA": [self.calculate_SMA_period, self.calculate_SMA_features],
            "EMA": [self.calculate_EMA_period, self.calculate_EMA_features],
            "HT_TRENDLINE": [self.calculate_HT_TRENDLINE],
            "KAMA": [self.calculate_KAMA_period, self.calculate_KAMA_features],
            # "VIDYA": [self.calculate_VIDYA_period, self.calculate_VIDYA_features],
            "ZLSMA": [self.calculate_ZLSMA_period, self.calculate_ZLSMA_features],
            "HMA": [self.calculate_HMA_period, self.calculate_HMA_features],
            "JMA": [self.calculate_JMA_period, self.calculate_JMA_features],
            # "TRIMA": [self.calculate_TRIMA_period, self.calculate_TRIMA_features]
            # "LINREG": [self.calculate_LINREG_period]
        }

    def calculate_SMA(self, n_step=14):
        sma = self.data[self.calc_col].rolling(window=n_step, min_periods = 1).mean()
        return sma

    def calculate_SMA_std(self, n_step=14):
        sma = self.data[self.calc_col].rolling(window=n_step, min_periods = 1).std()
        return sma

    def calculate_SMA_custom_data(self, data_w, n_step=14):
        sma = data_w.rolling(window=n_step, min_periods = 1).mean()
        return sma

    def calculate_SMA_period(self):
        for p in self.periods:
            self.data[f'sma_{p}'] = self.calculate_SMA(p).fillna(0)

        return self.data

    def calculate_SMA_features(self):
        # calculate all sma periods
        self.extract_features_ma("sma", self.periods)
        self.extract_features_ma_differences("sma", "sma", self.periods, self.periods)

        return self.data.copy()

    def calculate_EMA(self, n_step=14):
        ema = self.data[self.calc_col].ewm(span=n_step, min_periods=1, adjust=False, ignore_na=False).mean()
        return ema

    def calculate_EMA_custom_data(self, data_w, n_step=14):
        ema = data_w.ewm(span=n_step, min_periods=1, adjust=False, ignore_na=False).mean()
        return ema

    def calculate_EMA_period(self):
        for p in self.periods:
            #self.data['ema_'+str(p)] = self.calculate_EMA(p).fillna(0)
            self.data['ema_'+str(p)] = talib.EMA(self.data[self.calc_col], p).fillna(0)

        return self.data

    def calculate_EMA_features(self):
        self.extract_features_ma("ema", self.periods)
        self.extract_features_ma_differences("ema", "ema", self.periods, self.periods)
        self.extract_features_ma_differences("ema", "sma", self.periods, self.periods)
        return self.data.copy()

    def calculate_HT_TRENDLINE(self):
        self.data['ht_trendline'] = talib.HT_TRENDLINE(self.data[self.calc_col])
        self.data['ht_trendline'] = self.data['ht_trendline'].fillna(self.data['ht_trendline'].mean())

        return self.data.copy()

    def calculate_KAMA(self, n_step=14):
        kama = talib.KAMA(self.data[self.calc_col], n_step)
        kama = kama.fillna(kama.mean())
        return kama

    def calculate_KAMA_period(self):
        for p in self.kama_periods:
            self.data[f'kama_{p}'] = self.calculate_KAMA(p)
        return self.data

    def calculate_KAMA_features(self):
        self.extract_features_ma("kama", self.kama_periods)
        self.extract_features_ma_differences("kama", "kama", self.kama_periods, self.kama_periods)
        self.extract_features_ma_differences("sma", "kama", self.periods, self.kama_periods)
        self.extract_features_ma_differences("ema", "kama", self.periods, self.kama_periods)
        return self.data.copy()

    def calculate_ZLSMA_period(self):
        for p in self.kama_periods:
            data = ta.zlma(self.data[self.calc_col], p).fillna(0)
            self.data[f'zlsma_{p}'] = data

        return self.data

    def calculate_ZLSMA_features(self):
        self.extract_features_ma("zlsma", self.kama_periods)
        self.extract_features_ma_differences("zlsma", "zlsma", self.kama_periods, self.kama_periods)
        self.extract_features_ma_differences("zlsma", "kama", self.kama_periods, self.kama_periods)
        # self.extract_features_ma_differences("zlsma", "vidya", self.kama_periods, self.kama_periods)
        self.extract_features_ma_differences("sma", "zlsma", self.periods, self.kama_periods)
        self.extract_features_ma_differences("ema", "zlsma", self.periods, self.kama_periods)

        return self.data.copy()

    def calculate_VIDYA(self, n_step=14):
        alpha = 2 / (n_step + 1)
        df_temp = self.data[[self.calc_col]].copy()
        df_temp['cmo'] = talib.CMO(df_temp[self.calc_col], n_step).abs()
        df_temp['vidya'] = 0
        df_temp['vidya'] = (df_temp[self.calc_col] * alpha * df_temp.cmo)
        df_temp['vidya'] += (1 - alpha * df_temp.cmo) * df_temp.vidya.shift(1)
        df_temp = df_temp.fillna(df_temp.mean())

        return df_temp['cmo'], df_temp['vidya']

    def calculate_VIDYA_period(self):
        for p in self.kama_periods:
            temp = self.calculate_VIDYA(p)
            self.data[f'vidya_{p}'] = temp[1]
            self.data[f'cmo_{p}'] = temp[0]
            if (self.enable_linreg):
                self.data = pd.concat([self.data, self.calculate_REGR_forecast(f'vidya{p}')], axis=1).fillna(0)

        return self.data

    def calculate_VIDYA_features(self):
        self.extract_features_ma("vidya", self.kama_periods)
        self.extract_features_ma_differences("vidya", "vidya", self.kama_periods, self.kama_periods)
        self.extract_features_ma_differences("sma", "vidya", self.periods, self.kama_periods)
        self.extract_features_ma_differences("ema", "vidya", self.periods, self.kama_periods)
        self.extract_features_ma_differences("kama", "vidya", self.kama_periods, self.kama_periods)

        return self.data.copy()

    def calculate_WMA(self, data, n_step):
        weights = np.arange(1,n_step+1)
        wma = data.rolling(n_step).apply(lambda prices: np.dot(prices, weights)/weights.sum(), raw=True)
        return wma.fillna(wma.mean())

    #- hma = wma(2 * wma(data, period // 2) - wma(data, period), sqrt(period))

    def calculate_HMA(self, n_step=14):
        wma_1 = 2 * self.calculate_WMA(self.data[self.calc_col], n_step // 2)
        wma_2 = self.calculate_WMA(self.data[self.calc_col], n_step)
        hma = self.calculate_WMA(wma_1 - wma_2, int(np.sqrt(n_step)))
        return hma

    def calculate_HMA_period(self):
        for p in self.hma_periods:
            self.data[f'hma_{p}'] = self.calculate_HMA(p)

            if (self.enable_linreg):
                self.data = pd.concat([self.data, self.calculate_REGR_forecast(f'hma_{p}')], axis=1).fillna(0)
        return self.data

    def calculate_HMA_features(self):
        self.extract_features_ma("hma", self.hma_periods)
        self.extract_features_ma_differences("hma", "hma", self.hma_periods, self.hma_periods)
        # self.extract_features_ma_differences("hma", "vidya", self.hma_periods, self.kama_periods)
        self.extract_features_ma_differences("hma", "kama", self.hma_periods, self.kama_periods)
        self.extract_features_ma_differences("hma", "zlsma", self.hma_periods, self.kama_periods)
        self.extract_features_ma_differences("hma", "sma", self.hma_periods, self.periods)
        self.extract_features_ma_differences("hma", "ema", self.hma_periods, self.periods)

        return self.data.copy()

    def calculate_JMA_period(self):
        for p in self.hma_periods:
            self.data[f'jma_{p}'] = ta.jma(self.data[self.calc_col], p).fillna(0)

            if (self.enable_linreg):
                self.data = pd.concat([self.data, self.calculate_REGR_forecast(f'jma_{p}')], axis=1).fillna(0)
        return self.data

    def calculate_JMA_features(self):
        self.extract_features_ma("jma", self.hma_periods)
        self.extract_features_ma_differences("jma", "hma", self.hma_periods, self.hma_periods)
        self.extract_features_ma_differences("jma", "jma", self.hma_periods, self.hma_periods)
        # self.extract_features_ma_differences("jma", "vidya", self.hma_periods, self.kama_periods)
        self.extract_features_ma_differences("jma", "kama", self.hma_periods, self.kama_periods)
        self.extract_features_ma_differences("jma", "zlsma", self.hma_periods, self.kama_periods)
        self.extract_features_ma_differences("jma", "sma", self.hma_periods, self.periods)
        self.extract_features_ma_differences("jma", "ema", self.hma_periods, self.periods)
        return self.data.copy()

    def calculate_TRIMA_period(self):
        for p in self.hma_periods:
            self.data[f'trima_{p}'] = ta.trima(self.data[self.calc_col], p).fillna(0)
        return self.data

    def calculate_TRIMA_features(self):
        self.extract_features_ma("trima", self.hma_periods)
        self.extract_features_ma_differences("trima", "hma", self.hma_periods, self.hma_periods)
        self.extract_features_ma_differences("trima", "jma", self.hma_periods, self.hma_periods)
        # self.extract_features_ma_differences("trima", "vidya", self.hma_periods, self.kama_periods)
        self.extract_features_ma_differences("trima", "kama", self.hma_periods, self.kama_periods)
        self.extract_features_ma_differences("trima", "zlsma", self.hma_periods, self.kama_periods)
        self.extract_features_ma_differences("trima", "sma", self.hma_periods, self.periods)
        self.extract_features_ma_differences("trima", "ema", self.hma_periods, self.periods)

        return self.data.copy()

    def calculate_LINREG(self, n_step=14):
        linreg = talib.LINEARREG(self.data[self.calc_col], n_step)
        return linreg.fillna(linreg.mean())

    def calculate_LINREG_period(self):
        for p in self.hma_periods:
            self.data['linreg_'+str(p)] = self.calculate_LINREG(p)
        return self.data

    def calculate_REGR_forecast(self, col_name):
        temp = pd.DataFrame()
        col = col_name
        for i in self.data[col].rolling(window=self.reg_len):
            if i.shape[0] < self.reg_len:
                continue
            lr = LinearRegression()
            df_for_learn = pd.DataFrame()
            df_for_learn['ind'] = list(range(i.shape[0]))
            df_for_learn['ind_2'] = df_for_learn['ind'] ** 2
            df_for_learn['ind_exp'] = np.exp(df_for_learn['ind'])

            lr.fit(df_for_learn, i)
            df_for_predict = pd.DataFrame()
            df_for_predict.loc[0, 'ind'] = i.shape[0]*2
            df_for_predict['ind_2'] = df_for_predict['ind'] ** 2
            df_for_predict['ind_exp'] = np.exp(df_for_predict['ind'])

            temp_1 = pd.DataFrame()
            temp_1['pred_'+col] = lr.predict(df_for_predict)
            temp_1['date_ind'] = i.index[-1]

            temp = pd.concat([temp, temp_1], axis=0, ignore_index=True)

        return temp.set_index('date_ind')

    def calculate_all(self, ti_list=None):
        """
        TODO add desc
        :param ti_list:
        :return:
        """
        if ti_list:
            for ti in ti_list:
                if ti not in self.ti_dict.keys():
                    raise KeyError(f'Cant calculate indicators {ti}')
                for ti_f in self.ti_dict[ti]:
                    self.data = ti_f()
        else:
            for ti in self.ti_dict.keys():
                for ti_f in self.ti_dict[ti]:
                    self.data = ti_f()

        return self.data

    def extract_features_ma(self, ma: str, periods_ma = [6, 12, 24, 48]):
        # extract ma features
        for p in periods_ma:
            self.data[f'{ma}_{p}_divergence'] = (self.data[self.calc_col] - self.data[f'{ma}_{p}'])/self.data[self.calc_col]
            self.data[f'{ma}_{p}_signal'] = np.where(self.data[f'{ma}_{p}_divergence'] > 0, 1, 0)
            # speed of change
            self.data[f'{ma}_{p}_change_1'] = self.data[f'{ma}_{p}'].pct_change(1)
            self.data[f'{ma}_{p}_change_2'] = self.data[f'{ma}_{p}'].pct_change(2)
            self.data[f'{ma}_{p}_change_3'] = self.data[f'{ma}_{p}'].pct_change(3)
            # acceleration of change
            self.data[f'{ma}_{p}_acceleration'] = self.data[f'{ma}_{p}_change_1'].pct_change(1)
            # std
            self.data[f'{ma}_{p}_std'] = self.data[self.calc_col].rolling(window=p, min_periods = 1).std()
            # bands
            self.data[f'{ma}_{p}_upper_band'] = self.data[f'{ma}_{p}'] + 2 * self.data[f'{ma}_{p}_std']
            self.data[f'{ma}_{p}_lower_band'] = self.data[f'{ma}_{p}'] - 2 * self.data[f'{ma}_{p}_std']
            # position inside the band
            self.data[f'{ma}_{p}_band_value'] = (self.data[self.calc_col] - self.data[f'{ma}_{p}_lower_band']) / (self.data[f'{ma}_{p}_upper_band'] - self.data[f'{ma}_{p}_lower_band'])

            # envelopes
            self.data[f'{ma}_{p}_upper_envelope'] = self.data[f'{ma}_{p}'] + 0.03 * self.data[f'{ma}_{p}']
            self.data[f'{ma}_{p}_lower_envelope'] = self.data[f'{ma}_{p}'] - 0.03 * self.data[f'{ma}_{p}']
            # position inside the envelope
            self.data[f'{ma}_{p}_envelope_value'] = (self.data[self.calc_col] - self.data[f'{ma}_{p}_lower_envelope']) / (self.data[f'{ma}_{p}_upper_envelope'] - self.data[f'{ma}_{p}_lower_envelope'])

            # defragment
            self.data = self.data.copy()
            return self.data

    def extract_features_ma_differences(self, ma1: str, ma2: str, periods_ma1 = [6, 12, 24, 48], periods_ma2 = [6, 12, 24, 48]):
        # extract differences between self and each other

        for p1 in periods_ma1:
            for p2 in periods_ma2:
                # skip the self
                if (p1 == p2) and (ma1 == ma2):
                    continue

                # calculate features
                self.data[f'{ma1}_{p1}_{ma2}_{p2}_divergence'] = (self.data[f'{ma1}_{p1}'] - self.data[f'{ma2}_{p2}'])/self.data[self.calc_col]
                self.data[f'{ma1}_{p1}_{ma2}_{p2}_signal'] = np.where(self.data[f'{ma1}_{p1}_{ma2}_{p2}_divergence'] > 0, 1, 0)

        # defragment
        self.data = self.data.copy()
        return self.data




class MovingAveragesCalculator2:
    def __init__(self, col_prefix="", col_target="close", config=None):
        """
        Initialize the MovingAveragesCalculator with the configuration for
        moving average types and periods.
        """
        self.col_prefix = col_prefix
        self.col_target = col_target
        if config is None:
            config = {
                "SMA": [24, 48, 96, 192],
                "EMA": [12, 24, 48, 96],
                "HMA": [12, 24, 48, 96],
                # "JMA": [6, 12, 24, 48],
                "KAMA": [12, 24, 48, 96],
                "ZLSMA": [12, 24, 48, 96],
            }
        self.config = config

    def calculate_moving_averages(self, df: pd.DataFrame):
        """
        Calculate and return a DataFrame containing multiple moving
        averages, as specified by self.config, for the given input
        DataFrame and target column.
        """
        dfs = []
        ma_dfs = {}
        for ma, periods in self.config.items():
            prefix_ma = f'{self.col_prefix}{ma}'
            ma_df = pd.DataFrame(index=df.index)
            for period in periods:
                ma_value = self._calculate_moving_average(df, ma, period, self.col_target)
                ma_value.fillna(0, inplace=True)
                ma_df[f'{prefix_ma}_{period}'] = ma_value
            ma_dfs[ma] = ma_df
            dfs.append(ma_df)

        dfs = self._calculate_differences_between_mas(dfs, ma_dfs)
        ma_df = self.extract_features_ma(df, ma_dfs, ma, periods)

        return self._join_dataframes(df, dfs)

    def _calculate_moving_average(self, df, ma, period, target_col):
        """
        Calculate the indicated moving average type (ma) with the
        specified period for the data (df) and column (target_col).
        """
        if ma == "SMA":
            return talib.SMA(df[target_col], timeperiod=period)
        elif ma == "EMA":
            return talib.EMA(df[target_col], timeperiod=period)
        elif ma == "HMA":
            return ta.hma(df[target_col], length=period)
        elif ma == "JMA":
            return ta.jma(df[target_col], length=period)
        elif ma == "KAMA":
            return talib.KAMA(df[target_col], timeperiod=period)
        elif ma == "ZLSMA":
            return ta.zlma(df[target_col], length=period)

    def _calculate_differences_between_mas(self, dfs, ma_dfs):
        """
        Calculate the differences between the moving averages in ma_dfs.
        """
        for ma1 in ma_dfs.keys():
            for ma2 in ma_dfs.keys():
                ma1_ma2_diff_df = self._calculate_differences(ma_dfs[ma1], ma_dfs[ma2])
                dfs.append(ma1_ma2_diff_df)
        return dfs

    def _calculate_differences(self, df1, df2):
        """
        Calculate the differences between the columns in df1 and df2.
        """
        df_diff = pd.DataFrame(index=df1.index)
        for col1 in df1.columns:
            for col2 in df2.columns:
                if col1 == col2:
                    continue
                divergence = (df1[col1] - df2[col2])/df1[col1]
                df_diff[f"{col1}_{col2}_divergence"] = divergence
                df_diff[f"{col1}_{col2}_signal"] = np.where(divergence > 0, 1, 0)
        return df_diff


    def extract_features_ma(self, df: pd.DataFrame, madfs:dict, ma: str, periods_ma):
        ma_df = madfs[ma]
        prefix_ma = f'{self.col_prefix}{ma}'
        for p in periods_ma:
            ma_df[f'{prefix_ma}_{p}_divergence'] = (df[self.col_target] - ma_df[f'{prefix_ma}_{p}'])/df[self.col_target]
            ma_df[f'{prefix_ma}_{p}_signal'] = np.where(ma_df[f'{prefix_ma}_{p}_divergence'] > 0, 1, 0)
            ma_df[f'{prefix_ma}_{p}_change_1'] = ma_df[f'{prefix_ma}_{p}'].pct_change(1)
            ma_df[f'{prefix_ma}_{p}_change_2'] = ma_df[f'{prefix_ma}_{p}'].pct_change(2)
            ma_df[f'{prefix_ma}_{p}_change_3'] = ma_df[f'{prefix_ma}_{p}'].pct_change(3)
            ma_df[f'{prefix_ma}_{p}_std'] = df[self.col_target].rolling(window=p, min_periods = 1).std()

            # calculate diffrence between current value and value 2 periods ago
            ma_df[f'{prefix_ma}_{p}_diff_1'] = (ma_df[f'{prefix_ma}_{p}'] - ma_df[f'{prefix_ma}_{p}'].shift(1))/ma_df[f'{prefix_ma}_{p}']
            ma_df[f'{prefix_ma}_{p}_diff_2'] = (ma_df[f'{prefix_ma}_{p}'] - ma_df[f'{prefix_ma}_{p}'].shift(2))/ma_df[f'{prefix_ma}_{p}']
            # bands
            upper_band = ma_df[f'{prefix_ma}_{p}'] + 2 * ma_df[f'{prefix_ma}_{p}_std']
            lower_band = ma_df[f'{prefix_ma}_{p}'] - 2 * ma_df[f'{prefix_ma}_{p}_std']
            # position inside the band
            ma_df[f'{prefix_ma}_{p}_band_value'] = (df[self.col_target] - lower_band) / (upper_band - lower_band)

            # envelopes
            upper_envelope = ma_df[f'{prefix_ma}_{p}'] + 0.03 * ma_df[f'{prefix_ma}_{p}']
            lower_envelope = ma_df[f'{prefix_ma}_{p}'] - 0.03 * ma_df[f'{prefix_ma}_{p}']
            # position inside the envelope
            ma_df[f'{prefix_ma}_{p}_envelope_value'] = (df[self.col_target] - lower_envelope) / (upper_envelope - lower_envelope)

            # TODO: add lagged values

        return ma_df


    def _join_dataframes(self, df: pd.DataFrame, dfs: list):
        # concatenate df with all the other dfs
        return pd.concat([df, *dfs], axis=1, join="inner")
