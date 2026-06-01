from copy import deepcopy


class ParamBuilder:

    def __init__(self, param, fibbo, epochs):
        self.param = param
        self.fibbo = fibbo
        self.epochs = int(epochs)
        self.params = {}

    def int_param(self, default, low, high):
        if low > high:
            low, high = high, low

        return {
            "type": "IntParameter",
            "low": int(low),
            "high": int(high),
            "default": int(default),
            "optimize": self.optimize
        }

    def dec_param(self, default, low, high, decimals=3):
        if low > high:
            low, high = high, low

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

            if not isinstance(section_params, dict):
                continue

            self.params[section] = {}

            for key, value in section_params.items():

                self.optimize = (
                    self.param == "nil"
                    or key == self.param
                )

                if isinstance(value, bool):

                    self.params[section][key] = (
                        self.bool_param(value)
                    )

                elif isinstance(value, int):

                    if value == 0:
                        low, high = 0, 100
                    else:
                        low = max(
                            0,
                            value - self.epochs * 0.5
                        )
                        high = min(
                            value * 2,
                            value + self.epochs * 0.5
                        )

                    self.params[section][key] = (
                        self.int_param(
                            value,
                            low,
                            high
                        )
                    )

                elif isinstance(value, float):

                    percent = max(
                        0.02,
                        min(
                            0.1,
                            self.epochs * 0.002
                        )
                    )

                    decimals = (
                        4 if value < 0.05
                        else 3 if value < 1
                        else 2
                    )

                    low = round(
                        value * (1 - percent),
                        decimals
                    )

                    high = round(
                        value * (1 + percent),
                        decimals
                    )

                    self.params[section][key] = (
                        self.dec_param(
                            value,
                            low,
                            high,
                            decimals
                        )
                    )

                elif isinstance(value, str):

                    if key == "buy_fib_level":
                        choices = ["0.618", "0.786"]

                    elif key == "sell_fib_level":
                        choices = ["0.236", "0.382"]

                    elif key in (
                        "buy_fast_dema",
                        "sell_fast_dema"
                    ):
                        choices = ["5", "8", "13", "21"]

                    elif key in (
                        "buy_slow_ema",
                        "sell_slow_ema"
                    ):
                        choices = ["34", "55", "89", "144"]

                    elif "indicator" in key:
                        choices = ["NONE"]

                    else:
                        choices = [value]

                    self.params[section][key] = (
                        self.cat_param(
                            value,
                            choices
                        )
                    )

        # --------------------------------------------------
        # ROI remapping
        # --------------------------------------------------

        if "roi" in self.params:

            roi_dict = fibbo_params.get(
                "roi",
                {}
            )

            new_roi = {}

            sorted_times = sorted(
                [int(k) for k in roi_dict.keys()],
                reverse=True
            )

            roi_t_names = [
                "roi_t1",
                "roi_t2",
                "roi_t3"
            ]

            roi_p_names = [
                "roi_p1",
                "roi_p2",
                "roi_p3"
            ]

            for i in range(
                min(
                    3,
                    len(sorted_times)
                )
            ):

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

                percent = max(
                    0.02,
                    min(
                        0.1,
                        self.epochs * 0.002
                    )
                )

                decimals = (
                    4 if p_val < 0.05
                    else 3 if p_val < 1
                    else 2
                )

                low = round(
                    p_val * (1 - percent),
                    decimals
                )

                high = round(
                    p_val * (1 + percent),
                    decimals
                )

                if p_val >= 1 and round(p_val) == p_val:

                    new_roi[p_key] = {
                        "type": "IntParameter",
                        "low": max(
                            1,
                            int(low)
                        ),
                        "high": max(
                            int(low),
                            int(high)
                        ),
                        "default": int(p_val),
                        "optimize": True
                    }

                else:

                    new_roi[p_key] = (
                        self.dec_param(
                            p_val,
                            low,
                            high,
                            decimals
                        )
                    )

            self.params["roi"] = new_roi

        # --------------------------------------------------
        # ATR Risk Parameter
        # Freqtrade 2025.12 compatible
        # --------------------------------------------------

        stoploss_cfg = fibbo_params.get(
            "stoploss",
            {}
        )

        atr_value = None

        if isinstance(stoploss_cfg, dict):
            atr_value = stoploss_cfg.get(
                "atr_stoploss_multiplier"
            )

        if atr_value is not None:

            if "protection" not in self.params:
                self.params["protection"] = {}

            self.optimize = (
                self.param == "nil"
                or self.param
                == "atr_stoploss_multiplier"
            )

            percent = max(
                0.02,
                min(
                    0.1,
                    self.epochs * 0.002
                )
            )

            decimals = 2

            low = max(
                0.5,
                round(
                    atr_value * (
                        1 - percent
                    ),
                    decimals
                )
            )

            high = round(
                atr_value * (
                    1 + percent
                ),
                decimals
            )

            param = self.dec_param(
                atr_value,
                low,
                high,
                decimals
            )

            param["optimize"] = (
                self.optimize
            )

            self.params[
                "protection"
            ][
                "atr_stoploss_multiplier"
            ] = param

        # remove obsolete stoploss bucket

        if (
            "stoploss" in self.params
            and isinstance(
                self.params["stoploss"],
                dict
            )
        ):
            self.params["stoploss"] = {}

        return self.params
