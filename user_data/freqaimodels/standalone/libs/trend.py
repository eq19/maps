import talib
import pandas as pd
import numpy as np
import pandas_ta as ta
from technical.indicators import PMAX

from lib.ma import MovingAveragesCalculate
import lib.helpers as h

def wavetrend(df: pd.DataFrame, close_col = 'close', n1=9, n2=12, n3=3):
    # wavetrend calculation
    esa = ta.ema(df[close_col], n1)
    d = ta.ema(abs(df[close_col] - esa), n1)
    ci = (df[close_col] - esa) / (0.015 * d)
    tci = ta.ema(ci, n2)

    wt1 = tci
    wt2 = ta.sma(wt1, n3)

    df['wavetrend_1'] = wt1.fillna(method='ffill')
    df['wavetrend_2'] = wt2.fillna(method='ffill')
    df['wavetrend_vwap'] = (wt1 - wt2).fillna(method='ffill')

    # extract features for wavetrend
    df['wavetrend_signal'] = np.where(df['wavetrend_1'] > df['wavetrend_2'], 1, 0)

    df['wavetrend_1_diff'] = df['wavetrend_1'].diff()
    df['wavetrend_1_diff_signal'] = np.where(df['wavetrend_1_diff'] > 0, 1, 0)

    df['wavetrend_vwap_diff'] = df['wavetrend_vwap'].diff()
    df['wavetrend_vwap_diff_signal'] = np.where(df['wavetrend_vwap_diff'] > 0, 1, 0)

class TrendCalculate:

    def __init__(self, data: pd.DataFrame, close_col='close', high_col='high', low_col='low', open_col='open'):
        self.data = data.copy()
        self.close_col = close_col
        self.high_col = high_col
        self.low_col = low_col
        self.open_col = open_col

        self.mac = MovingAveragesCalculate(self.data.copy())
        self.ti_dict = {
            "WAVETREND": [self.calculate_WAVETREND],
            "SUPERTREND": [self.calculate_SUPERTREND],
            "HAC": [self.calculate_Heikin_Ashi_Candles],
            "PMAX": [self.calculate_PMAX],
            "CTI": [self.calculate_CTI],
            "INERTIA": [self.calculate_INERTIA],
            "STC": [self.calculate_STC],
            "CHOP": [self.calculate_CHOP],
            "CCI": [self.calculate_CCI],
            "DPO": [self.calculate_DPO]
        }

    def calculate_WAVETREND(self, n1=9, n2=12, n3=3):
        features = pd.DataFrame(index=self.data.index)
        # wavetrend calculation
        esa = self.mac.calculate_EMA_custom_data(self.data[self.close_col], n1)
        d = self.mac.calculate_EMA_custom_data(abs(self.data[self.close_col] - esa), n1)
        ci = (self.data[self.close_col] - esa) / (0.015 * d)
        tci = self.mac.calculate_EMA_custom_data(ci, n2)

        wt1 = tci
        wt2 = self.mac.calculate_SMA_custom_data(wt1, n3)

        features['WT_1'] = wt1.fillna(method='ffill')
        features['WT_2'] = wt2.fillna(method='ffill')
        features['WT_vwap'] = (wt1 - wt2).fillna(method='ffill')

        # extract features for wavetrend
        features['WT_signal'] = np.where(features['WT_1'] > features['WT_2'], 1, 0)

        features = h.calculate_speed(features, target='WT_vwap')
        features = h.calculate_speed(features, target='WT_1')

        return pd.concat([self.data, features], axis=1)

    def calculate_SUPERTREND(self):
        _props1 = "_12_3.0"
        _props2 = "_11_2.0"
        _props3 = "_10_1.0"

        supertrend1 = ta.supertrend(self.data[self.high_col], self.data[self.low_col], self.data[self.close_col], length=12, multiplier=3).fillna(0)
        supertrend1 = supertrend1[[f'SUPERT{_props1}', f'SUPERTd{_props1}']].copy()

        supertrend2 = ta.supertrend(self.data[self.high_col], self.data[self.low_col], self.data[self.close_col], length=11, multiplier=2).fillna(0)
        supertrend2 = supertrend2[[f'SUPERT{_props2}', f'SUPERTd{_props2}']].copy()

        supertrend3 = ta.supertrend(self.data[self.high_col], self.data[self.low_col], self.data[self.close_col], length=10, multiplier=1).fillna(0)
        supertrend3 = supertrend3[[f'SUPERT{_props3}', f'SUPERTd{_props3}']].copy()

        supertrend1['SUPERT_12_diff'] = supertrend1['SUPERT' + _props1] - supertrend2['SUPERT' + _props2]
        supertrend1['SUPERT_12_signal'] = np.where(supertrend1['SUPERT_12_diff'] > 0, 1, 0)

        supertrend1['SUPERT_13_diff'] = supertrend1['SUPERT' + _props1] - supertrend3['SUPERT' + _props3]
        supertrend1['SUPERT_13_signal'] = np.where(supertrend1['SUPERT_13_diff'] > 0, 1, 0)

        supertrend2['SUPERT_23_diff'] = supertrend2['SUPERT' + _props2] - supertrend3['SUPERT' + _props3]
        supertrend2['SUPERT_23_signal'] = np.where(supertrend2['SUPERT_23_diff'] > 0, 1, 0)

        return pd.concat([self.data, supertrend1, supertrend2, supertrend3], axis=1)

    def calculate_Heikin_Ashi_Candles(self):
        ha = pd.DataFrame(index=self.data.index)

        ha['ha_open'] = (self.data[self.open_col].shift() +
                                self.data[self.close_col].shift()) / 2
        ha['ha_close'] = (self.data[self.open_col] + self.data[self.high_col] +
                                 self.data[self.low_col] + self.data[self.close_col]) / 4
        ha['ha_high'] = self.data[[self.open_col, self.close_col, self.high_col]].max(axis=1)
        ha['ha_low'] = self.data[[self.open_col, self.close_col, self.low_col]].min(axis=1)

        ha['ha_trend'] = np.where(ha['ha_close'] > ha['ha_open'], 1, 0)

        return pd.concat([self.data, ha['ha_trend']], axis=1)

    def calculate_PMAX(self):
        df_temp = self.data[[self.open_col, self.high_col, self.low_col, self.close_col, 'volume']].copy()
        df_temp = df_temp.rename(columns={self.open_col: 'open', self.high_col: 'high',
                                          self.low_col: 'low', self.close_col: 'close'})
        f_temp = PMAX(df_temp)
        del df_temp
        f_temp = f_temp[['pm_10_3_12_1', 'pmX_10_3_12_1']]
        # replace signals
        f_temp['pmX_10_3_12_1'] = f_temp['pmX_10_3_12_1'].replace({'down': 0, 'up': 1})

        self.data = pd.concat([self.data, f_temp], axis=1)
        return self.data.copy()

    def calculate_CTI(self):
        self.data['cti'] = ta.cti(self.data[self.close_col]).fillna(method='ffill')
        return self.data.copy()

    def calculate_INERTIA(self):
        self.data['inertia'] = ta.inertia(
            self.data[self.close_col], self.data[self.high_col], self.data[self.low_col]).fillna(method='ffill')
        return self.data.copy()

    def calculate_STC(self):
        self.data = pd.concat(
            [self.data, ta.stc(self.data[self.close_col]).fillna(method='ffill')], axis=1)
        return self.data.copy()

    def calculate_CHOP(self):
        self.data['chop'] = ta.chop(self.data[self.high_col], self.data[self.low_col],
                                    self.data[self.close_col]).fillna(method='ffill')
        return self.data.copy()

    def calculate_CCI(self):
        features = pd.DataFrame(index=self.data.index)
        features['cci'] = ta.cci(self.data[self.high_col], self.data[self.low_col],
                                  self.data[self.close_col]).values

        # extract features
        features['cci_long_signal'] = np.where(features['cci'] > 100, 1, 0)
        features['cci_short_signal'] = np.where(features['cci'] < -100, 1, 0)

        features = h.calculate_speed(features, target='cci')

        return pd.concat([features, self.data], axis=1)

    def calculate_DPO(self, n_step=20):
        features = pd.DataFrame(index=self.data.index)

        features['dpo'] = ta.dpo(self.data[self.close_col], n_step, centered=False).values

        features = h.calculate_speed(features, target='dpo')

        return pd.concat([features, self.data], axis=1)

    def calculate_DPO_on_pred(self, n_step=20):
        t = int(0.5 * n_step) + 1
        ma = self.data.pred_sma_20.shift(t)
        dpo = (self.data[self.close_col].shift(t) - ma).shift(-t)
        self.data['dpo_pred'] = dpo.fillna(dpo.mean())
        return self.data.copy()


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
