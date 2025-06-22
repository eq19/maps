# fibbo_param_builder.py

from copy import deepcopy

class ParamBuilder:
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
                    low, high = max(0, value - self.epochs * 0.5), min(value * 2, value + self.epochs * 0.5)
                    self.params[section][key] = self.int_param(value, int(low), int(high))

                elif isinstance(value, float):
                    percent = self.epochs * 0.01  # 1% × epochs
                    decimals = 4 if value < 0.05 else 3 if value < 1 else 2
                    low, high = max(0.001, value - value * percent), value + value * percent
                    self.params[section][key] = self.dec_param(value, round(low, decimals), round(high, decimals), decimals)

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
