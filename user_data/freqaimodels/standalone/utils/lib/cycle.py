import talib
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import pandas_ta as ta

class CycleCalculate:

    def __init__(self, data:pd.DataFrame, calc_col='close'):
        self.data = data.copy()
        self.calc_col = calc_col
        self.ti_dict = {
            "HT_DCPERIOD": [self.calculate_HT_DCPERIOD],
            "HT_DCPHASE": [self.calculate_HT_DCPHASE],
            "HT_PHASOR": [self.calculate_HT_PHASOR],
            "HT_SINE": [self.calculate_HT_SINE],
            "HT_TRENDMODE": [self.calculate_HT_TRENDMODE],
            "EBSW": [self.calculate_EBSW],
        }


    def calculate_HT_DCPERIOD(self):
        self.data['ht_dcperdiod'] = talib.HT_DCPERIOD(self.data[self.calc_col]).fillna(method='ffill')
        return self.data

    def calculate_HT_DCPHASE(self):
        self.data['ht_dcphase'] = talib.HT_DCPHASE(self.data[self.calc_col]).fillna(method='ffill')
        return self.data

    def calculate_HT_PHASOR(self):
        ht_phasor_inphase, ht_phasor_quadrature = talib.HT_PHASOR(self.data[self.calc_col])
        self.data['ht_phasor_inphase'] = ht_phasor_inphase.fillna(method='ffill')
        self.data['ht_phasor_quadrature'] = ht_phasor_quadrature.fillna(method='ffill')
        return self.data

    def calculate_HT_SINE(self):
        ht_phasor_sine, ht_phasor_leadsine = talib.HT_SINE(self.data[self.calc_col])
        self.data['ht_sine_sine'] = ht_phasor_sine.fillna(method='ffill')
        self.data['ht_sine_leadsine'] = ht_phasor_leadsine.fillna(method='ffill')
        return self.data

    def calculate_HT_TRENDMODE(self):
        self.data['ht_trendmode'] = talib.HT_TRENDMODE(self.data[self.calc_col]).fillna(method='ffill')
        return self.data

    def calculate_EBSW(self):
        self.data['ebsw'] = ta.ebsw(self.data[self.calc_col]).fillna(method='ffill')
        return self.data

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