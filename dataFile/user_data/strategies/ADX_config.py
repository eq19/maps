{
    "dry_run": true,
    "ticker_interval": "15m",
    "max_open_trades": -1,
    "tradable_balance_ratio": 1.00,
    "stake_currency": "USDT",
    "stake_amount": 120,
    "fiat_display_currency": "USD",
    "amend_last_stake_amount": true,
    "dry_run_wallet": 10000,

    "unfilledtimeout": {
        "buy": 10,
        "sell": 30
    },
    "bid_strategy": {
        "ask_last_balance": 0.0,
        "use_order_book": false,
        "order_book_top": 1,
        "check_depth_of_market": {
            "enabled": false,
            "bids_to_ask_delta": 1
        }
    },
    "ask_strategy":{
        "use_order_book": false,
        "order_book_min": 1,
        "order_book_max": 1,
        "use_sell_signal": true,
        "sell_profit_only": false,
        "ignore_roi_if_buy_signal": false
    },
    "exchange": {
        "name": "binance",
        "key": "",
        "secret": "",
        "ccxt_config": {"enableRateLimit": true},
        "ccxt_async_config": {
            "enableRateLimit": true,
            "rateLimit": 200
        },
        "pair_whitelist": [
            "BTC/USDT",
            "ETH/USDT",
            "THETA/USDT",
            "MATIC/USDT",
            "TFUEL/USDT",
            "BCH/USDT",
            "ADA/USDT",
            "EOS/USDT",
            "BAND/USDT",
            "ENJ/USDT",
            "ETC/USDT",
            "VET/USDT",
            "TRX/USDT",
            "HBAR/USDT",
            "ONT/USDT",
            "IOST/USDT",
            "XTZ/USDT",
            "MBL/USDT",
            "ZIL/USDT",
            "OMG/USDT",
            "ZEC/USDT",
            "COS/USDT",
            "XMR/USDT",
            "NEO/USDT",
            "WRX/USDT",
            "ATOM/USDT",
            "DASH/USDT",
            "IOTX/USDT",
            "KAVA/USDT",
            "REN/USDT",
            "ICX/USDT",
            "RVN/USDT",
            "ALGO/USDT",
            "QTUM/USDT",
            "BAT/USDT",
            "DREP/USDT",
            "ONG/USDT",
            "ZRX/USDT",
            "BTT/USDT",
            "BNT/USDT",
            "ANKR/USDT",
            "ONE/USDT",
            "OGN/USDT",
            "IOTA/USDT",
            "TROY/USDT",
            "AION/USDT",
            "FET/USDT",
            "WIN/USDT",
            "NANO/USDT",
            "CHZ/USDT",
            "WAVES/USDT",
            "HIVE/USDT",
            "FTM/USDT",
            "PERL/USDT",
            "CELR/USDT",
            "COTI/USDT",
            "FTT/USDT",
            "TOMO/USDT",
            "DOGE/USDT",
            "CTSI/USDT",
            "NKN/USDT",
            "BEAM/USDT",
            "ARPA/USDT",
            "RLC/USDT",
            "DENT/USDT",
            "WTC/USDT"
        ],
        "pair_blacklist": [

        ]
    },
    "pairlists": [
        {"method": "StaticPairList"}
    ],
    "edge": {
        "enabled": false,
        "process_throttle_secs": 3600,
        "calculate_since_number_of_days": 7,
        "allowed_risk": 0.01,
        "stoploss_range_min": -0.01,
        "stoploss_range_max": -0.1,
        "stoploss_range_step": -0.01,
        "minimum_winrate": 0.60,
        "minimum_expectancy": 0.20,
        "min_trade_number": 10,
        "max_trade_duration_minute": 1440,
        "remove_pumps": false
    },
    "telegram": {
        "enabled": true,
        "token": "",
        "chat_id": ""
    },
    "initial_state": "running",
    "forcebuy_enable": false,
    "internals": {
        "process_throttle_secs": 5
    }
}
