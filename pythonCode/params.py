# fibbo_param_builder.py

from copy import deepcopy

class ParamBuilder:
    def __init__(self, param, fibbo, epochs):
        self.param = param
        self.fibbo = fibbo
        self.epochs = int(epochs)
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
                    if value == 0:
                        low, high = 0, 100
                    else:
                        low, high = max(0, value - self.epochs * 0.5), min(value * 2, value + self.epochs * 0.5)
                    self.params[section][key] = self.int_param(value, int(low), int(high))

                elif isinstance(value, float):
                    percent = max(0.02, min(0.1, self.epochs * 0.002))  # 2%–10%
                    decimals = 4 if value < 0.05 else 3 if value < 1 else 2
                    low = max(0.001, round(value * (1 - percent), decimals))
                    high = round(value * (1 + percent), decimals)
                    self.params[section][key] = self.dec_param(value, low, high, decimals)

                elif isinstance(value, str):
                    if key == "buy_fib_level":
                        choices = ["0.618", "0.786"]
                    elif key == "sell_fib_level":
                        choices = ["0.236", "0.382"]
                    elif key == "buy_fast_dema" or key == "sell_fast_dema":
                        choices = ["5", "8", "13", "21"]
                    elif key == "buy_slow_ema" or key == "sell_slow_ema":
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

                # Use fixed time values (non-optimized)
                new_roi[t_key] = {
                    "type": "IntParameter",
                    "low": 0,
                    "high": 600,
                    "default": t_val,
                    "optimize": False
                }

                # Calculate % range for decimal precision tuning
                percent = max(0.02, min(0.1, self.epochs * 0.002))  # 2–10% window
                decimals = 4 if p_val < 0.05 else 3 if p_val < 1 else 2
                low = max(0.001, round(p_val * (1 - percent), decimals))
                high = round(p_val * (1 + percent), decimals)

                # Adjust param type if value behaves like integer
                if p_val >= 1 and round(p_val) == p_val:
                    new_roi[p_key] = {
                        "type": "IntParameter",
                        "low": max(1, int(low)),
                        "high": int(high),
                        "default": int(p_val),
                        "optimize": True
                    }
                else:
                    new_roi[p_key] = self.dec_param(
                        p_val,
                        low,
                        high,
                        decimals
                    )

            self.params["roi"] = new_roi

        # Stoploss Optimization
        if "stoploss" in self.params and "stoploss" in fibbo_params["stoploss"]:
            del self.params["stoploss"]["stoploss"]

            base_val = fibbo_params["stoploss"].get("atr_stoploss_multiplier", 1.5)
            self.optimize = True if self.param == "nil" or self.param == "atr_stoploss_multiplier" else False

            percent = max(0.02, min(0.1, self.epochs * 0.002))  # 2–10%
            decimals = 3 if base_val < 1 else 2
            low = round(max(0.5, base_val * (1 - percent)), decimals)
            high = round(base_val * (1 + percent), decimals)

            if base_val >= 1 and round(base_val) == base_val:
                self.params["stoploss"]["atr_stoploss_multiplier"] = {
                    "type": "IntParameter",
                    "low": max(1, int(low)),
                    "high": int(high),
                    "default": int(base_val),
                    "optimize": self.optimize
                }
            else:
                param = self.dec_param(base_val, low, high, decimals)
                param["optimize"] = self.optimize
                self.params["stoploss"]["atr_stoploss_multiplier"] = param

        return self.params
