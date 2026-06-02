from copy import deepcopy


class ParamBuilder:

    def __init__(self, param, fibbo, epochs):
        self.param = param
        self.fibbo = fibbo
        self.epochs = int(epochs)
        self.params = {}
        self.optimize = False

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

        # Handle Freqtrade 2025.12 scalar parameters
        if "stoploss" in fibbo_params:
            self.params["stoploss"] = fibbo_params["stoploss"]

        if "max_open_trades" in fibbo_params:
            self.params["max_open_trades"] = fibbo_params["max_open_trades"]

        for section, section_params in fibbo_params.items():

            if section in (
                "stoploss",
                "max_open_trades"
            ):
                continue

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
                        4 if abs(value) < 0.05
                        else 3 if abs(value) < 1
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
                        choices = [
                            "0.618",
                            "0.786"
                        ]

                    elif key == "sell_fib_level":
                        choices = [
                            "0.236",
                            "0.382"
                        ]

                    elif key in (
                        "buy_fast_dema",
                        "sell_fast_dema"
                    ):
                        choices = [
                            "5",
                            "8",
                            "13",
                            "21"
                        ]

                    elif key in (
                        "buy_slow_ema",
                        "sell_slow_ema"
                    ):
                        choices = [
                            "34",
                            "55",
                            "89",
                            "144"
                        ]

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
        # ROI
        # Keep Freqtrade format:
        # {
        #   "0": 0.362,
        #   "38": 0.065,
        #   "200": 0.019,
        #   "542": 0
        # }
        # --------------------------------------------------

        if "roi" in fibbo_params:
            self.params["roi"] = deepcopy(
                fibbo_params["roi"]
            )

        # --------------------------------------------------
        # ATR stoploss multiplier
        # --------------------------------------------------

        protection = fibbo_params.get(
            "protection",
            {}
        )

        atr_value = protection.get(
            "atr_stoploss_multiplier"
        )

        if (
            atr_value is not None
            and atr_value > 0
        ):

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

            low = max(
                0.5,
                round(
                    atr_value * (1 - percent),
                    2
                )
            )

            high = round(
                atr_value * (1 + percent),
                2
            )

            self.params["protection"][
                "atr_stoploss_multiplier"
            ] = self.dec_param(
                atr_value,
                low,
                high,
                2
            )

        return self.params
