# fibbo_param_builder.py

from copy import deepcopy

class FibboParamBuilder:
    def __init__(self, param, fibbo, epochs):
        self.param = param
        self.fibbo = fibbo
        self.epochs = epochs
        self.params = {}

    def int_param(self, default, low, high):
        return {
            "type": "IntParameter",
            "low": low,
            "high": high,
            "default": default,
            "optimize": self.optimize
        }

    def dec_param(self, default, low, high, decimals=3):
        return {
            "type": "DecimalParameter",
            "low": round(low, decimals),
            "high": round(high, decimals),
            "default": round(default, decimals),
            "decimals": decimals,
            "optimize": self.optimize
        }

    def bool_param(self, default):
        return {
            "type": "BooleanParameter",
            "default": default,
            "optimize": self.optimize
        }

    def cat_param(self, default, choices):
        return {
            "type": "CategoricalParameter",
            "choices": choices,
            "default": default,
            "optimize": self.optimize
        }

    def build(self):
        fibbo_params = self.fibbo.get("params", {})

        for section, section_params in fibbo_params.items():
            self.params[section] = {}

            for key, value in section_params.items():
                self.optimize = True if self.param == "nil" or key == self.param else False

                if isinstance(value, bool):
                    self.params[section][key] = self.bool_param(value)

                elif isinstance(value, int):
                    low, high = 0, value * 2
                    if key == "cooldown_lookback":
                        low, high = 2, min(self.epochs * 2, 48)
                    elif "rsi" in key or "stoch" in key:
                        low, high = 0, 100
                    elif "period" in key:
                        low, high = 5, 50
                    elif "trade_limit" in key:
                        low, high = 2, 10
                    elif "duration" in key:
                        low, high = 12, 200
                    elif "open_trades" in key:
                        low, high = 70, 100

                    self.params[section][key] = self.int_param(value, low, high)

                elif isinstance(value, float):
                    low, high = 0.01, value * 2
                    decimals = 3
                    if "stop" in key or "offset" in key:
                        if "positive_offset" in key:
                            low, high = 0.5, 1.0
                        elif "positive" in key:
                            low, high = 0.01, 0.5
                        else:
                            low, high = 1.0, 3.0
                    elif "roi" in section:
                        if key == "0":
                            low, high = 0.01, 0.20
                        elif key == "2":
                            low, high = 0.01, 0.10
                        else:
                            low, high = 0.01, 0.05

                    self.params[section][key] = self.dec_param(value, low, high, decimals)

                elif isinstance(value, str):
                    if key == "buy_fib_level" or key == "sell_fib_level":
                        choices = ["0.236", "0.382", "0.618", "0.786"]
                    elif key == "buy_fast_dema":
                        choices = ["5", "8", "13", "21"]
                    elif key == "buy_slow_ema":
                        choices = ["34", "55", "89", "144"]
                    elif "indicator" in key:
                        choices = ["NONE"]
                    else:
                        choices = [value]
                    self.params[section][key] = self.cat_param(value, choices)

        # ROI re-mapping
        if "roi" in self.params:
            roi_dict = fibbo_params.get("roi", {})
            new_roi = {}
            sorted_times = sorted([int(k) for k in roi_dict.keys()], reverse=True)
            roi_t_names = ["roi_t1", "roi_t2", "roi_t3"]
            roi_p_names = ["roi_p1", "roi_p2", "roi_p3"]

            for i in range(min(3, len(sorted_times))):
                t_key = roi_t_names[i]
                p_key = roi_p_names[i]
                t_val = sorted_times[i]
                p_val = roi_dict[str(t_val)]

                self.optimize = True if self.param == "nil" or t_key == self.param or p_key == self.param else False
                new_roi[t_key] = self.int_param(t_val, 10, 600)
                new_roi[p_key] = self.dec_param(p_val, 0.01, 0.3)

            self.params["roi"] = new_roi

        # Replace stoploss with atr_stoploss_multiplier
        if "stoploss" in self.params and "stoploss" in fibbo_params["stoploss"]:
            del self.params["stoploss"]["stoploss"]
            self.optimize = True if self.param == "nil" or "atr_stoploss_multiplier" == self.param else False
            self.params["stoploss"]["atr_stoploss_multiplier"] = self.dec_param(1.5, 1, 3)

        return self.params
