import talib
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import pandas_ta as ta
import lib.helpers as h

class OscillatorsCalculate:

    def __init__(self, data:pd.DataFrame, close_col='close', high_col='high', low_col='low'):
        self.data = data.copy()
        self.close_col = close_col
        self.high_col = high_col
        self.low_col = low_col

        self.ti_dict = {
            "RSI": [self.calculate_RSI],
            "Fisher": [self.calculate_Fisher_Transform],
            "RVI": [self.calculate_RVI],
            "MFI": [self.calculate_MFI]

        }


    def calculate_RSI(self):
        # calculate the indicator
        rsi = talib.RSI(self.data[self.close_col], timeperiod=14)

        features = pd.DataFrame(index=self.data.index)
        features['rsi_value'] = rsi
        # extract signal
        features['rsi_long_signal'] = np.where(rsi < 30, 1, 0)
        # features['rsi_strong_long'] = np.where(rsi < 20, 1, 0)
        features['rsi_short_signal'] = np.where(rsi > 70, 1, 0)
        # features['rsi_strong_short'] = np.where(rsi > 80, 1, 0)

        features = h.calculate_speed(features, target='rsi_value')

        return pd.concat([features, self.data], axis=1)


    def calculate_Fisher_Transform(self, length=9, signal=1):
        _props = f"_{length}_{signal}"
        fishrt = ta.fisher(self.data[self.high_col], self.data[self.low_col], length=length, signal=signal).fillna(method='ffill')

        # features
        fishrt[f"FISHERT{_props}_signal"] = np.where(fishrt[f"FISHERT{_props}"] > fishrt[f"FISHERTs{_props}"], 1, 0)
        fishrt[f"FISHERT{_props}_rising"] = np.where(abs(fishrt[f"FISHERT{_props}"]) > abs(fishrt[f"FISHERT{_props}"].shift(1)), 1, 0)

        return pd.concat([fishrt, self.data], axis=1)

    def calculate_RVI(self, length=14):
        features = pd.DataFrame(index=self.data.index)

        _props = f"RVI_{length}"
        features['rvi_value'] = ta.rvi(self.data[self.close_col], self.data[self.high_col], self.data[self.low_col], length=length).fillna(method='ffill').values

        # features
        features[f"{_props}_long_signal"] = np.where(features['rvi_value'] < 20, 1, 0)
        features[f"{_props}_short_signal"] = np.where(features['rvi_value'] > 80, 1, 0)

        features = h.calculate_speed(features, target='rvi_value')

        return self.data.copy()

    def calculate_MFI(self, length = 14):
        # calculate the indicator
        mfi = talib.MFI(self.data[self.high_col], self.data[self.low_col], self.data[self.close_col], self.data['volume'], timeperiod=length)

        features = pd.DataFrame(index=self.data.index)
        # extract signal
        features['mfi_long_signal'] = np.where(mfi < 20, 1, 0)
        # features['mfi_strong_long'] = np.where(mfi < 10, 1, 0)
        features['mfi_short_signal'] = np.where(mfi > 80, 1, 0)
        # features['mfi_strong_short'] = np.where(mfi > 90, 1, 0)

        features['mfi_value'] = mfi

        features = h.calculate_speed(features, target='mfi_value')

        return pd.concat([features, self.data], axis=1)

    def calculate_VolumeOscillator(self):
        features = pd.DataFrame(index=self.data.index)
        # Calculate EMAs
        short = self.data['volume'].ewm(span=5, adjust=False).mean()
        long = self.data['volume'].ewm(span=20, adjust=False).mean()

        # Calculate oscillator
        features['volume_osc'] = 100 * (short - long) / long
        features['volume_osc_signal'] = np.where(features['volume_osc'] > 0, 1, 0)

        features = h.calculate_speed(features, target='volume_osc')

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