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
                        self.params[section][key] = self.int_param(value, 0, 100)
                    else:
                        # 1. Define absolute logical boundaries based on the indicator name
                        if "rsi" in key and "period" not in key:
                            abs_low, abs_high = 1, 99
                        elif "stoch_osc" in key:
                            abs_low, abs_high = 1, 99
                        elif "smooth" in key:  # For smoothD and smoothK
                            abs_low, abs_high = 1, 15
                        elif "swing" in key:
                            abs_low, abs_high = 2, 20
                        elif "period" in key or "window" in key:
                            abs_low, abs_high = 2, 300
                        elif "candles" in key or "lookback" in key or "limit" in key:
                            abs_low, abs_high = 1, 500
                        else:
                            abs_low, abs_high = 0, 1000  # Fallback

                        # 2. Calculate your dynamic range
                        dyn_low = value - (self.epochs * 0.5)
                        dyn_high = value + (self.epochs * 0.5)

                        # 3. Clamp the dynamic range within the absolute boundaries
                        low = max(abs_low, dyn_low)
                        high = min(abs_high, dyn_high)
                        
                        # 4. Ensure high is always strictly greater than low
                        if high <= low:
                            high = low + 1

                        self.params[section][key] = self.int_param(value, int(low), int(high))

                elif isinstance(value, float):
                    percent = max(0.02, min(0.1, self.epochs * 0.002))  # 2%–10%
                    decimals = 3 if value < 0.05 else 2 if value < 1 else 1
                    low = max(0.001, round(value * (1 - percent), decimals))
                    high = round(value * (1 + percent), decimals)
                    self.params[section][key] = self.dec_param(value, low, high, decimals)

                elif isinstance(value, str):
                    if "indicator" in key:
                        choices = ["NONE"]
                    elif key == "buy_fib_level":
                        choices = ["0.618", "0.786"]
                    elif key == "sell_fib_level":
                        choices = ["0.236", "0.382"]
                    elif key == "buy_fast_dema" or key == "sell_fast_dema":
                        choices = ["5", "8", "13", "21"]
                    elif key == "buy_slow_ema" or key == "sell_slow_ema":
                        choices = ["34", "55", "89", "144"]
                    elif key == "enter_trade_mode" or key == "exit_trade_mode":
                        choices = ["any", "half", "majority", "all"]
                    else:
                        choices = [value]
                    self.params[section][key] = self.cat_param(value, choices)

        # ROI re-mapping (unchanged)
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

                new_roi[t_key] = {
                    "type": "IntParameter",
                    "low": 0,
                    "high": 600,
                    "default": t_val,
                    "optimize": False
                }

                percent = max(0.02, min(0.1, self.epochs * 0.002))
                decimals = 4 if p_val < 0.05 else 3 if p_val < 1 else 2
                low = max(0.001, round(p_val * (1 - percent), decimals))
                high = round(p_val * (1 + percent), decimals)

                if p_val >= 1 and round(p_val) == p_val:
                    new_roi[p_key] = {
                        "type": "IntParameter",
                        "low": max(1, int(low)),
                        "high": int(high),
                        "default": int(p_val),
                        "optimize": True
                    }
                else:
                    new_roi[p_key] = self.dec_param(p_val, low, high, decimals)

            self.params["roi"] = new_roi

        return self.params
