import talib
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import pandas_ta as ta
import lib.helpers as h

class MomentumANDVolatilityCalculate:

    def __init__(self, data:pd.DataFrame, open_col='open', close_col='close', high_col='high', low_col='low'):
        self.data = data.copy()
        self.close_col = close_col
        self.high_col = high_col
        self.low_col = low_col
        self.open_col = open_col

        self.ti_dict = {
            "ADX": [self.calculate_ADX],
            "AROON": [self.calculate_AROON],
            "MACD": [self.calculate_MACD],
            "TTM_Squeeze": [self.calculate_TTM_Squeeze],
            "PSY": [self.calculate_PSY],
            "ATR": [self.calculate_ATR],
        }


    def calculate_ADX(self, n_step=14):
        features = pd.DataFrame(index=self.data.index)
        # calculate the indicator
        features['adx_value'] = talib.ADX(self.data[self.high_col], self.data[self.low_col], self.data[self.close_col], n_step).fillna(method='ffill')
        features['adx_plus_di'] = talib.MINUS_DI(self.data[self.high_col], self.data[self.low_col], self.data[self.close_col], timeperiod=n_step)
        features['adx_minus_di'] = talib.PLUS_DI(self.data[self.high_col], self.data[self.low_col], self.data[self.close_col], timeperiod=n_step)

        # extract signals
        features['adx_long_signal'] = np.where((features['adx_value'] > 20) & (features['adx_plus_di'] > features['adx_minus_di']), 1, 0)
        features['adx_short_signal'] = np.where((features['adx_value'] > 20) & (features['adx_plus_di'] < features['adx_minus_di']), 1, 0)
        features['adx_weak_signal'] = np.where((features['adx_value'] < 20), 1, 0)

        features = h.calculate_speed(features, target='adx_value')

        return pd.concat([features, self.data], axis=1)


    def calculate_AROON(self, n_step=14):
        # a_up, a_down = talib.AROON(self.data[self.high_col], self.data[self.low_col], n_step)
        a_osc = talib.AROONOSC(self.data[self.high_col], self.data[self.low_col], timeperiod=n_step)

        # values
        features = pd.DataFrame(index=self.data.index)
        features['aroon_osc'] = a_osc.fillna(method='ffill')

        # extract features
        features['aroon_signal'] = np.where(a_osc > 0, 1, 0)

        features = h.calculate_speed(features, target='aroon_osc')

        return pd.concat([features, self.data], axis=1)


    def calculate_MACD(self, fastperiod=12, slowperiod=26, signalperiod=9):
        # calculate the indicator
        macd, macdsignal, macdhist = talib.MACD(self.data[self.close_col], fastperiod=12, slowperiod=26, signalperiod=9)
        features = pd.DataFrame(index=self.data.index)

        features['macd_value'] = macd
        features['macd_sig'] = macdsignal
        features['macd_hist'] = macdhist

        # extract features
        features['macd_signal'] = np.where(macdhist > 0, 1, 0)

        features = h.calculate_speed(features, 'macd_value')
        features = h.calculate_speed(features, 'macd_sig')
        features = h.calculate_speed(features, 'macd_hist')

        return pd.concat([features, self.data], axis=1)


    def calculate_TTM_Squeeze(self, n_step=14):
        self.data = pd.concat([self.data, ta.squeeze_pro(self.data[self.high_col], self.data[self.low_col], self.data[self.close_col], detailed = True)], axis=1)
        return self.data


    def calculate_PSY(self):
        psy = ta.psl(self.data[self.close_col], self.data[self.open_col], length = 20).fillna(method='ffill')
        features = pd.DataFrame(index=self.data.index)
        features['psy_value'] = psy.fillna(method='ffill')

        # features
        features['psy_signal'] = np.where(psy > 50, 1, 0)

        features = h.calculate_speed(features, 'psy_value')

        return pd.concat([features, self.data], axis=1)

    def calculate_ATR(self):
        features = pd.DataFrame(index=self.data.index)
        features['atr14_value'] = talib.ATR(self.data[self.high_col], self.data[self.low_col], self.data[self.close_col]).fillna(method='ffill')

        features = h.calculate_speed(features, 'atr14_value')

        return pd.concat([features, self.data], axis=1)

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