```
freqtrade backtesting --strategy TrixV23Strategy --stake-amount 100 --timeframe 1h --max-open-trades -1 --fee 0.001 --dry-run-wallet 1000 --timerange=20210101-
Creating freqtradelocal_freqtrade_run ... done
2021-12-18 11:10:11,380 - freqtrade.configuration.configuration - INFO - Using config: user_data/config.json ...
2021-12-18 11:10:11,383 - freqtrade.loggers - INFO - Verbosity set to 0
2021-12-18 11:10:11,383 - freqtrade.configuration.configuration - INFO - Parameter -i/--timeframe detected ... Using timeframe: 1h ...
2021-12-18 11:10:11,383 - freqtrade.configuration.configuration - INFO - Parameter --max-open-trades detected, overriding max_open_trades to: -1 ...
2021-12-18 11:10:11,383 - freqtrade.configuration.configuration - INFO - Parameter --stake-amount detected, overriding stake_amount to: 100.0 ...
2021-12-18 11:10:11,383 - freqtrade.configuration.configuration - INFO - Parameter --dry-run-wallet detected, overriding dry_run_wallet to: 1000.0 ...
2021-12-18 11:10:11,383 - freqtrade.configuration.configuration - INFO - Parameter --fee detected, setting fee to: 0.001 ...
2021-12-18 11:10:11,383 - freqtrade.configuration.configuration - INFO - Parameter --timerange detected: 20210101- ...
2021-12-18 11:10:12,482 - freqtrade.configuration.configuration - INFO - Using user-data directory: /freqtrade/user_data ...
2021-12-18 11:10:12,483 - freqtrade.configuration.configuration - INFO - Using data directory: /freqtrade/user_data/data/binance ...
2021-12-18 11:10:12,483 - freqtrade.configuration.configuration - INFO - Overriding timeframe with Command line argument
2021-12-18 11:10:12,484 - freqtrade.configuration.check_exchange - INFO - Checking exchange...
2021-12-18 11:10:12,492 - freqtrade.configuration.check_exchange - INFO - Exchange "binance" is officially supported by the Freqtrade development team.
2021-12-18 11:10:12,492 - freqtrade.configuration.configuration - INFO - Using pairlist from configuration.
2021-12-18 11:10:12,492 - freqtrade.configuration.config_validation - INFO - Validating configuration ...
2021-12-18 11:10:12,497 - freqtrade.commands.optimize_commands - INFO - Starting freqtrade in Backtesting mode
2021-12-18 11:10:12,498 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2021-12-18 11:10:12,498 - freqtrade.exchange.exchange - INFO - Using CCXT 1.61.92
2021-12-18 11:10:12,513 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2021-12-18 11:10:13,931 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2021-12-18 11:10:14,524 - TrixV23Strategy - INFO - pandas_ta successfully imported
2021-12-18 11:10:14,647 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy TrixV23Strategy from '/freqtrade/user_data/strategies/TrixV23Strategy.py'...
2021-12-18 11:10:14,647 - freqtrade.strategy.hyper - INFO - Found no parameter file.
2021-12-18 11:10:14,648 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_btc_ema_enabled = True
2021-12-18 11:10:14,648 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_btc_ema_multiplier = 0.996
2021-12-18 11:10:14,648 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_btc_ema_timeperiod = 184
2021-12-18 11:10:14,648 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_ema_enabled = True
2021-12-18 11:10:14,648 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_ema_multiplier = 0.85
2021-12-18 11:10:14,648 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_ema_src = open
2021-12-18 11:10:14,648 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_ema_timeperiod = 10
2021-12-18 11:10:14,648 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_rsi_timeperiod = 14
2021-12-18 11:10:14,648 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_stoch_rsi = 0.901
2021-12-18 11:10:14,648 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_stoch_rsi_enabled = True
2021-12-18 11:10:14,649 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_stoch_rsi_timeperiod = 14
2021-12-18 11:10:14,649 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_trix_signal_timeperiod = 19
2021-12-18 11:10:14,649 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_trix_signal_type = trigger
2021-12-18 11:10:14,649 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_trix_src = low
2021-12-18 11:10:14,649 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_trix_timeperiod = 8
2021-12-18 11:10:14,650 - freqtrade.strategy.hyper - INFO - Strategy Parameter: sell_atr_enabled = True
2021-12-18 11:10:14,650 - freqtrade.strategy.hyper - INFO - Strategy Parameter: sell_atr_multiplier = 4.99
2021-12-18 11:10:14,650 - freqtrade.strategy.hyper - INFO - Strategy Parameter: sell_atr_timeperiod = 30
2021-12-18 11:10:14,650 - freqtrade.strategy.hyper - INFO - Strategy Parameter: sell_rsi_timeperiod = 14
2021-12-18 11:10:14,650 - freqtrade.strategy.hyper - INFO - Strategy Parameter: sell_stoch_rsi = 0.183
2021-12-18 11:10:14,650 - freqtrade.strategy.hyper - INFO - Strategy Parameter: sell_stoch_rsi_enabled = True
2021-12-18 11:10:14,650 - freqtrade.strategy.hyper - INFO - Strategy Parameter: sell_stoch_rsi_timeperiod = 14
2021-12-18 11:10:14,650 - freqtrade.strategy.hyper - INFO - Strategy Parameter: sell_trix_signal_timeperiod = 19
2021-12-18 11:10:14,650 - freqtrade.strategy.hyper - INFO - Strategy Parameter: sell_trix_signal_type = trailing
2021-12-18 11:10:14,650 - freqtrade.strategy.hyper - INFO - Strategy Parameter: sell_trix_src = high
2021-12-18 11:10:14,650 - freqtrade.strategy.hyper - INFO - Strategy Parameter: sell_trix_timeperiod = 10
2021-12-18 11:10:14,650 - freqtrade.strategy.hyper - INFO - No params for protection found, using default values.
2021-12-18 11:10:14,651 - freqtrade.resolvers.strategy_resolver - INFO - Override strategy 'timeframe' with value in config file: 1h.
2021-12-18 11:10:14,651 - freqtrade.resolvers.strategy_resolver - INFO - Override strategy 'stake_currency' with value in config file: USDT.
2021-12-18 11:10:14,651 - freqtrade.resolvers.strategy_resolver - INFO - Override strategy 'stake_amount' with value in config file: 100.0.
2021-12-18 11:10:14,651 - freqtrade.resolvers.strategy_resolver - INFO - Override strategy 'unfilledtimeout' with value in config file: {'buy': 10, 'sell': 30, 'unit': 'minutes', 'exit_timeout_count': 0}.        
2021-12-18 11:10:14,651 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using minimal_roi: {'0': 0.553, '423': 0.144, '751': 0.059, '1342': 0}
2021-12-18 11:10:14,651 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using timeframe: 1h
2021-12-18 11:10:14,652 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using stoploss: -0.31
2021-12-18 11:10:14,652 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using trailing_stop: False
2021-12-18 11:10:14,652 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using trailing_stop_positive_offset: 0.0
2021-12-18 11:10:14,652 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using trailing_only_offset_is_reached: False
2021-12-18 11:10:14,652 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using use_custom_stoploss: True
2021-12-18 11:10:14,652 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using process_only_new_candles: False
2021-12-18 11:10:14,652 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using order_types: {'buy': 'limit', 'sell': 'limit', 'stoploss': 'market', 'stoploss_on_exchange': False}
2021-12-18 11:10:14,652 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using order_time_in_force: {'buy': 'gtc', 'sell': 'gtc'}
2021-12-18 11:10:14,652 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using stake_currency: USDT
2021-12-18 11:10:14,652 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using stake_amount: 100.0
2021-12-18 11:10:14,653 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using protections: []
2021-12-18 11:10:14,653 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using startup_candle_count: 200
2021-12-18 11:10:14,653 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using unfilledtimeout: {'buy': 10, 'sell': 30, 'unit': 'minutes', 'exit_timeout_count': 0}
2021-12-18 11:10:14,653 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using use_sell_signal: True
2021-12-18 11:10:14,653 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using sell_profit_only: True
2021-12-18 11:10:14,653 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using ignore_roi_if_buy_signal: False
2021-12-18 11:10:14,653 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using sell_profit_offset: 0.0
2021-12-18 11:10:14,653 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using disable_dataframe_checks: False
2021-12-18 11:10:14,653 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using ignore_buying_expired_candle_after: 0
2021-12-18 11:10:14,653 - freqtrade.configuration.config_validation - INFO - Validating configuration ...
2021-12-18 11:10:14,661 - freqtrade.resolvers.iresolver - INFO - Using resolved pairlist StaticPairList from '/freqtrade/freqtrade/plugins/pairlist/StaticPairList.py'...
2021-12-18 11:10:15,202 - freqtrade.plugins.pairlistmanager - WARNING - Pair ACM/USDT in your blacklist. Removing it from whitelist...
2021-12-18 11:10:15,202 - freqtrade.plugins.pairlistmanager - WARNING - Pair ASR/USDT in your blacklist. Removing it from whitelist...
2021-12-18 11:10:15,202 - freqtrade.plugins.pairlistmanager - WARNING - Pair ATM/USDT in your blacklist. Removing it from whitelist...
2021-12-18 11:10:15,202 - freqtrade.plugins.pairlistmanager - WARNING - Pair AUD/USDT in your blacklist. Removing it from whitelist...
2021-12-18 11:10:15,203 - freqtrade.plugins.pairlistmanager - WARNING - Pair BAR/USDT in your blacklist. Removing it from whitelist...
2021-12-18 11:10:15,203 - freqtrade.plugins.pairlistmanager - WARNING - Pair BTC/USDT in your blacklist. Removing it from whitelist...
2021-12-18 11:10:15,203 - freqtrade.plugins.pairlistmanager - WARNING - Pair BUSD/USDT in your blacklist. Removing it from whitelist...
2021-12-18 11:10:15,203 - freqtrade.plugins.pairlistmanager - WARNING - Pair CHZ/USDT in your blacklist. Removing it from whitelist...
2021-12-18 11:10:15,203 - freqtrade.plugins.pairlistmanager - WARNING - Pair CITY/USDT in your blacklist. Removing it from whitelist...
2021-12-18 11:10:15,203 - freqtrade.plugins.pairlistmanager - WARNING - Pair CTXC/USDT in your blacklist. Removing it from whitelist...
2021-12-18 11:10:15,203 - freqtrade.plugins.pairlistmanager - WARNING - Pair EUR/USDT in your blacklist. Removing it from whitelist...
2021-12-18 11:10:15,203 - freqtrade.plugins.pairlistmanager - WARNING - Pair FOR/USDT in your blacklist. Removing it from whitelist...
2021-12-18 11:10:15,204 - freqtrade.plugins.pairlistmanager - WARNING - Pair FTT/USDT in your blacklist. Removing it from whitelist...
2021-12-18 11:10:15,204 - freqtrade.plugins.pairlistmanager - WARNING - Pair GBP/USDT in your blacklist. Removing it from whitelist...
2021-12-18 11:10:15,204 - freqtrade.plugins.pairlistmanager - WARNING - Pair HBAR/USDT in your blacklist. Removing it from whitelist...
2021-12-18 11:10:15,204 - freqtrade.plugins.pairlistmanager - WARNING - Pair JUV/USDT in your blacklist. Removing it from whitelist...
2021-12-18 11:10:15,204 - freqtrade.plugins.pairlistmanager - WARNING - Pair NMR/USDT in your blacklist. Removing it from whitelist...
2021-12-18 11:10:15,204 - freqtrade.plugins.pairlistmanager - WARNING - Pair OG/USDT in your blacklist. Removing it from whitelist...
2021-12-18 11:10:15,205 - freqtrade.plugins.pairlistmanager - WARNING - Pair PSG/USDT in your blacklist. Removing it from whitelist...
2021-12-18 11:10:15,205 - freqtrade.plugins.pairlistmanager - WARNING - Pair SHIB/USDT in your blacklist. Removing it from whitelist...
2021-12-18 11:10:15,205 - freqtrade.plugins.pairlistmanager - WARNING - Pair SLP/USDT in your blacklist. Removing it from whitelist...
2021-12-18 11:10:15,205 - freqtrade.plugins.pairlistmanager - WARNING - Pair TUSD/USDT in your blacklist. Removing it from whitelist...
2021-12-18 11:10:15,205 - freqtrade.plugins.pairlistmanager - WARNING - Pair USDC/USDT in your blacklist. Removing it from whitelist...
2021-12-18 11:10:15,205 - freqtrade.plugins.pairlistmanager - WARNING - Pair XVS/USDT in your blacklist. Removing it from whitelist...
2021-12-18 11:10:15,207 - freqtrade.data.history.history_utils - INFO - Using indicator startup period: 200 ...
2021-12-18 11:10:15,229 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair 1INCH/USDT, data starts at 2020-12-25 05:00:00
2021-12-18 11:10:15,379 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair ADX/USDT, data starts at 2021-10-29 10:00:00
2021-12-18 11:10:15,398 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair AGLD/USDT, data starts at 2021-10-05 07:00:00
2021-12-18 11:10:15,529 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair ALICE/USDT, data starts at 2021-03-15 06:00:00
2021-12-18 11:10:15,551 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair ALPACA/USDT, data starts at 2021-08-11 08:00:00
2021-12-18 11:10:15,602 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair AMP/USDT, data starts at 2021-11-23 06:00:00
2021-12-18 11:10:15,752 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair AR/USDT, data starts at 2021-05-14 12:00:00
2021-12-18 11:10:15,850 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair ATA/USDT, data starts at 2021-06-07 06:00:00
2021-12-18 11:10:15,910 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair AUCTION/USDT, data starts at 2021-10-29 10:00:00
2021-12-18 11:10:15,965 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair AUTO/USDT, data starts at 2021-04-02 09:00:00
2021-12-18 11:10:16,135 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair BADGER/USDT, data starts at 2021-03-02 08:00:00
2021-12-18 11:10:16,160 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair BAKE/USDT, data starts at 2021-04-30 12:00:00
2021-12-18 11:10:16,450 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair BETA/USDT, data starts at 2021-10-08 12:00:00
2021-12-18 11:10:16,574 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair BNX/USDT, data starts at 2021-11-04 11:00:00
2021-12-18 11:10:16,596 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair BOND/USDT, data starts at 2021-07-05 06:00:00
2021-12-18 11:10:16,624 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair BTCST/USDT, data starts at 2021-01-13 06:00:00
2021-12-18 11:10:16,634 - freqtrade.data.converter - INFO - Missing data fillup for BTCST/USDT: before: 7893 - after: 8002 - 1.38%
2021-12-18 11:10:16,707 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair BTG/USDT, data starts at 2021-04-16 07:00:00
2021-12-18 11:10:16,808 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair BURGER/USDT, data starts at 2021-04-30 12:00:00
2021-12-18 11:10:16,862 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair C98/USDT, data starts at 2021-07-23 12:00:00
2021-12-18 11:10:16,888 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair CAKE/USDT, data starts at 2021-02-19 06:00:00
2021-12-18 11:10:16,917 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair CELO/USDT, data starts at 2021-01-05 08:00:00
2021-12-18 11:10:17,040 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair CFX/USDT, data starts at 2021-03-29 11:00:00
2021-12-18 11:10:17,060 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair CHESS/USDT, data starts at 2021-10-22 06:00:00
2021-12-18 11:10:17,122 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair CKB/USDT, data starts at 2021-01-26 12:00:00
2021-12-18 11:10:17,144 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair CLV/USDT, data starts at 2021-07-29 06:00:00
2021-12-18 11:10:17,466 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair CVP/USDT, data starts at 2021-10-04 10:00:00
2021-12-18 11:10:17,485 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair DAR/USDT, data starts at 2021-11-04 08:00:00
2021-12-18 11:10:17,623 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair DEGO/USDT, data starts at 2021-03-10 11:00:00
2021-12-18 11:10:17,749 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair DEXE/USDT, data starts at 2021-07-23 10:00:00
2021-12-18 11:10:17,770 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair DF/USDT, data starts at 2021-09-24 10:00:00
2021-12-18 11:10:17,941 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair DODO/USDT, data starts at 2021-02-19 10:00:00
2021-12-18 11:10:18,129 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair DYDX/USDT, data starts at 2021-09-09 02:00:00
2021-12-18 11:10:18,179 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair ELF/USDT, data starts at 2021-09-08 08:00:00
2021-12-18 11:10:18,235 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair ENS/USDT, data starts at 2021-11-10 07:00:00
2021-12-18 11:10:18,296 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair EPS/USDT, data starts at 2021-04-02 09:00:00
2021-12-18 11:10:18,319 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair ERN/USDT, data starts at 2021-06-22 06:00:00
2021-12-18 11:10:18,475 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair FARM/USDT, data starts at 2021-08-11 08:00:00
2021-12-18 11:10:18,534 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair FIDA/USDT, data starts at 2021-09-30 12:00:00
2021-12-18 11:10:18,624 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair FIRO/USDT, data starts at 2021-01-29 02:00:00
2021-12-18 11:10:18,652 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair FIS/USDT, data starts at 2021-03-03 08:00:00
2021-12-18 11:10:18,710 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair FLOW/USDT, data starts at 2021-07-30 13:00:00
2021-12-18 11:10:18,735 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair FORTH/USDT, data starts at 2021-04-23 09:00:00
2021-12-18 11:10:18,756 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair FRONT/USDT, data starts at 2021-10-04 10:00:00
2021-12-18 11:10:18,911 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair GALA/USDT, data starts at 2021-09-13 06:00:00
2021-12-18 11:10:18,932 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair GHST/USDT, data starts at 2021-08-20 10:00:00
2021-12-18 11:10:18,953 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair GNO/USDT, data starts at 2021-08-30 06:00:00
2021-12-18 11:10:19,007 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair GTC/USDT, data starts at 2021-06-10 10:00:00
2021-12-18 11:10:19,296 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair ICP/USDT, data starts at 2021-05-11 01:00:00
2021-12-18 11:10:19,355 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair IDEX/USDT, data starts at 2021-09-09 08:00:00
2021-12-18 11:10:19,375 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair ILV/USDT, data starts at 2021-09-22 06:00:00
2021-12-18 11:10:19,637 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair JASMY/USDT, data starts at 2021-11-22 12:00:00
2021-12-18 11:10:19,731 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair KEEP/USDT, data starts at 2021-06-17 06:00:00
2021-12-18 11:10:19,795 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair KLAY/USDT, data starts at 2021-06-24 08:00:00
2021-12-18 11:10:19,940 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair KP3R/USDT, data starts at 2021-11-12 10:00:00
2021-12-18 11:10:19,991 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair LAZIO/USDT, data starts at 2021-10-21 12:00:00
2021-12-18 11:10:20,015 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair LINA/USDT, data starts at 2021-03-18 12:00:00
2021-12-18 11:10:20,081 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair LIT/USDT, data starts at 2021-02-04 06:00:00
2021-12-18 11:10:20,104 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair LPT/USDT, data starts at 2021-05-28 05:00:00
2021-12-18 11:10:20,391 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair MASK/USDT, data starts at 2021-05-25 06:00:00
2021-12-18 11:10:20,545 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair MBOX/USDT, data starts at 2021-08-19 08:00:00
2021-12-18 11:10:20,602 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair MDX/USDT, data starts at 2021-05-24 09:00:00
2021-12-18 11:10:20,662 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair MINA/USDT, data starts at 2021-08-10 06:00:00
2021-12-18 11:10:20,686 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair MIR/USDT, data starts at 2021-04-19 11:00:00
2021-12-18 11:10:20,780 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair MLN/USDT, data starts at 2021-07-05 06:00:00
2021-12-18 11:10:20,798 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair MOVR/USDT, data starts at 2021-11-08 06:00:00
2021-12-18 11:10:21,091 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair NU/USDT, data starts at 2021-06-04 05:00:00
2021-12-18 11:10:21,281 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair OM/USDT, data starts at 2021-03-08 09:00:00
2021-12-18 11:10:21,643 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair PERP/USDT, data starts at 2021-03-19 08:00:00
2021-12-18 11:10:21,666 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair PHA/USDT, data starts at 2021-06-25 10:00:00
2021-12-18 11:10:21,685 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair PLA/USDT, data starts at 2021-11-23 06:00:00
2021-12-18 11:10:21,742 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair POLS/USDT, data starts at 2021-05-19 07:00:00
2021-12-18 11:10:21,762 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair POLY/USDT, data starts at 2021-09-09 08:00:00
2021-12-18 11:10:21,844 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair POND/USDT, data starts at 2021-03-09 08:00:00
2021-12-18 11:10:21,863 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair PORTO/USDT, data starts at 2021-11-16 12:00:00
2021-12-18 11:10:21,881 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair POWR/USDT, data starts at 2021-11-17 06:00:00
2021-12-18 11:10:21,905 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair PUNDIX/USDT, data starts at 2021-04-09 04:00:00
2021-12-18 11:10:21,924 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair PYR/USDT, data starts at 2021-11-26 08:00:00
2021-12-18 11:10:21,942 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair QI/USDT, data starts at 2021-11-15 08:00:00
2021-12-18 11:10:21,963 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair QNT/USDT, data starts at 2021-07-29 06:00:00
2021-12-18 11:10:22,022 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair QUICK/USDT, data starts at 2021-08-13 12:00:00
2021-12-18 11:10:22,041 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair RAD/USDT, data starts at 2021-10-07 07:00:00
2021-12-18 11:10:22,066 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair RAMP/USDT, data starts at 2021-03-22 09:00:00
2021-12-18 11:10:22,086 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair RARE/USDT, data starts at 2021-10-11 06:00:00
2021-12-18 11:10:22,107 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair RAY/USDT, data starts at 2021-08-10 06:00:00
2021-12-18 11:10:22,136 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair REEF/USDT, data starts at 2020-12-29 06:00:00
2021-12-18 11:10:22,232 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair REQ/USDT, data starts at 2021-08-20 10:00:00
2021-12-18 11:10:22,251 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair RGT/USDT, data starts at 2021-11-05 06:00:00
2021-12-18 11:10:22,278 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair RIF/USDT, data starts at 2021-01-07 13:00:00
2021-12-18 11:10:22,393 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair RNDR/USDT, data starts at 2021-11-27 10:00:00
2021-12-18 11:10:22,612 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair SFP/USDT, data starts at 2021-02-08 13:00:00
2021-12-18 11:10:23,053 - freqtrade.data.converter - INFO - Missing data fillup for SUN/USDT: before: 8386 - after: 8496 - 1.31%
2021-12-18 11:10:23,069 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair SUPER/USDT, data starts at 2021-03-25 10:00:00
2021-12-18 11:10:23,179 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair SYS/USDT, data starts at 2021-09-24 10:00:00
2021-12-18 11:10:23,371 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair TKO/USDT, data starts at 2021-04-07 13:00:00
2021-12-18 11:10:23,396 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair TLM/USDT, data starts at 2021-04-13 06:00:00
2021-12-18 11:10:23,457 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair TORN/USDT, data starts at 2021-06-11 06:00:00
2021-12-18 11:10:23,508 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair TRIBE/USDT, data starts at 2021-08-24 06:00:00
2021-12-18 11:10:23,572 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair TRU/USDT, data starts at 2021-01-19 07:00:00
2021-12-18 11:10:23,690 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair TVK/USDT, data starts at 2021-08-06 10:00:00
2021-12-18 11:10:23,716 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair TWT/USDT, data starts at 2021-01-27 08:00:00
2021-12-18 11:10:23,824 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair USDP/USDT, data starts at 2021-09-10 04:00:00
2021-12-18 11:10:23,908 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair VGX/USDT, data starts at 2021-11-22 07:00:00
2021-12-18 11:10:23,927 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair VIDT/USDT, data starts at 2021-09-09 08:00:00
2021-12-18 11:10:24,149 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair WAXP/USDT, data starts at 2021-08-23 06:00:00
2021-12-18 11:10:24,392 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair XEC/USDT, data starts at 2021-09-03 10:00:00
2021-12-18 11:10:24,647 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair XVG/USDT, data starts at 2021-06-06 10:00:00
2021-12-18 11:10:24,727 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair YGG/USDT, data starts at 2021-09-24 06:00:00
2021-12-18 11:10:24,930 - freqtrade.optimize.backtesting - INFO - Loading data from 2020-12-23 16:00:00 up to 2021-12-12 15:00:00 (353 days).
2021-12-18 11:10:24,930 - freqtrade.optimize.backtesting - INFO - Dataload complete. Calculating indicators
2021-12-18 11:10:24,930 - freqtrade.optimize.backtesting - INFO - Running backtesting for Strategy TrixV23Strategy
2021-12-18 11:10:28,313 - freqtrade.optimize.backtesting - INFO - Backtesting with data from 2021-01-01 00:00:00 up to 2021-12-12 15:00:00 (345 days).
2021-12-18 11:11:14,153 - freqtrade.misc - INFO - dumping json to "/freqtrade/user_data/backtest_results/backtest-result-2021-12-18_11-11-14.json"
2021-12-18 11:11:14,233 - freqtrade.misc - INFO - dumping json to "/freqtrade/user_data/backtest_results/.last_result.json"
Result for strategy TrixV23Strategy
============================================================= BACKTESTING REPORT ============================================================
|         Pair |   Buys |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |     Avg Duration |   Win  Draw  Loss  Win% |
|--------------+--------+----------------+----------------+-------------------+----------------+------------------+-------------------------|
|     OXT/USDT |     29 |           3.92 |         113.59 |           113.701 |          11.37 |         18:29:00 |    22     5     2  75.9 |
|     SUN/USDT |     28 |           3.89 |         108.92 |           109.033 |          10.90 |         15:28:00 |    24     4     0   100 |
|     DNT/USDT |     31 |           3.46 |         107.28 |           107.388 |          10.74 |         16:46:00 |    21     7     3  67.7 |
|    DEXE/USDT |     19 |           5.06 |          96.16 |            96.253 |           9.63 |         17:54:00 |    12     6     1  63.2 |
|    DOCK/USDT |     31 |           3.02 |          93.58 |            93.670 |           9.37 |         16:04:00 |    25     3     3  80.6 |
|     PNT/USDT |     20 |           4.57 |          91.47 |            91.564 |           9.16 |         23:39:00 |    11     5     4  55.0 |
|     KEY/USDT |     19 |           4.52 |          85.79 |            85.871 |           8.59 |         20:51:00 |    12     6     1  63.2 |
|    VTHO/USDT |     14 |           6.07 |          85.03 |            85.113 |           8.51 |         14:30:00 |    12     1     1  85.7 |
|     ETC/USDT |     23 |           3.60 |          82.77 |            82.854 |           8.29 |         14:26:00 |    18     2     3  78.3 |
|     HNT/USDT |     18 |           4.47 |          80.41 |            80.494 |           8.05 |         17:33:00 |    14     3     1  77.8 |
|     SKL/USDT |     27 |           2.92 |          78.83 |            78.908 |           7.89 |         19:31:00 |    17     7     3  63.0 |
|   THETA/USDT |     19 |           3.99 |          75.78 |            75.861 |           7.59 |         21:00:00 |    15     2     2  78.9 |
|     BTT/USDT |     23 |           3.29 |          75.64 |            75.711 |           7.57 |         19:31:00 |    18     1     4  78.3 |
|     KMD/USDT |     18 |           4.02 |          72.41 |            72.486 |           7.25 |         21:17:00 |    15     2     1  83.3 |
|    CTSI/USDT |     23 |           3.10 |          71.24 |            71.316 |           7.13 |         15:47:00 |    18     3     2  78.3 |
|    MASK/USDT |     20 |           3.55 |          70.94 |            71.010 |           7.10 |   1 day, 0:00:00 |    15     3     2  75.0 |
|    IOTX/USDT |     26 |           2.68 |          69.69 |            69.757 |           6.98 |         23:51:00 |    18     3     5  69.2 |
|     FET/USDT |     23 |           3.00 |          69.11 |            69.177 |           6.92 |         18:23:00 |    16     6     1  69.6 |
|     TLM/USDT |     13 |           5.26 |          68.34 |            68.406 |           6.84 |         22:09:00 |    11     2     0   100 |
|     INJ/USDT |     19 |           3.35 |          63.73 |            63.795 |           6.38 |         19:38:00 |    14     4     1  73.7 |
|    VITE/USDT |     22 |           2.86 |          62.85 |            62.913 |           6.29 |         21:52:00 |    15     7     0   100 |
|     OGN/USDT |     24 |           2.54 |          60.84 |            60.903 |           6.09 |         20:15:00 |    18     4     2  75.0 |
|     WIN/USDT |     17 |           3.53 |          59.98 |            60.037 |           6.00 |         18:49:00 |    13     2     2  76.5 |
|     CHR/USDT |     28 |           2.09 |          58.57 |            58.625 |           5.86 |   1 day, 1:24:00 |    17     4     7  60.7 |
|    MITH/USDT |     18 |           3.18 |          57.18 |            57.241 |           5.72 |   1 day, 1:43:00 |    11     6     1  61.1 |
|     FIO/USDT |     31 |           1.82 |          56.33 |            56.385 |           5.64 |   1 day, 0:27:00 |    19    10     2  61.3 |
|     ONE/USDT |     19 |           2.96 |          56.33 |            56.382 |           5.64 |         22:13:00 |    13     5     1  68.4 |
|    TOMO/USDT |     21 |           2.61 |          54.77 |            54.823 |           5.48 |         16:57:00 |    18     3     0   100 |
|     TWT/USDT |     20 |           2.73 |          54.56 |            54.610 |           5.46 |         20:48:00 |    14     5     1  70.0 |
|     SFP/USDT |     22 |           2.47 |          54.35 |            54.401 |           5.44 |         14:30:00 |    19     2     1  86.4 |
|     NKN/USDT |     19 |           2.77 |          52.56 |            52.610 |           5.26 |   1 day, 8:06:00 |    13     3     3  68.4 |
|     ATA/USDT |     13 |           3.95 |          51.29 |            51.339 |           5.13 |         19:09:00 |    11     1     1  84.6 |
|    NANO/USDT |     17 |           3.00 |          50.94 |            50.987 |           5.10 |   1 day, 3:53:00 |    12     4     1  70.6 |
|    QTUM/USDT |     20 |           2.48 |          49.62 |            49.667 |           4.97 |         19:57:00 |    15     5     0   100 |
|     NBS/USDT |     24 |           2.06 |          49.43 |            49.477 |           4.95 |         21:02:00 |    14     6     4  58.3 |
|     WTC/USDT |     19 |           2.60 |          49.33 |            49.380 |           4.94 |         22:54:00 |    14     3     2  73.7 |
|     JST/USDT |     24 |           2.04 |          48.88 |            48.930 |           4.89 |         16:40:00 |    18     1     5  75.0 |
|     LPT/USDT |     16 |           3.04 |          48.62 |            48.667 |           4.87 |   1 day, 4:19:00 |    11     4     1  68.8 |
|    RUNE/USDT |     12 |           4.02 |          48.24 |            48.290 |           4.83 |         13:20:00 |    10     1     1  83.3 |
|     VET/USDT |     15 |           3.21 |          48.12 |            48.173 |           4.82 |         21:20:00 |    11     3     1  73.3 |
|      SC/USDT |     20 |           2.38 |          47.63 |            47.673 |           4.77 |         12:54:00 |    16     1     3  80.0 |
|     TRB/USDT |     15 |           3.11 |          46.58 |            46.631 |           4.66 |         16:08:00 |    13     2     0   100 |
|    POLS/USDT |     16 |           2.83 |          45.29 |            45.337 |           4.53 |         20:22:00 |    11     4     1  68.8 |
|     REQ/USDT |     12 |           3.74 |          44.89 |            44.932 |           4.49 |   1 day, 1:10:00 |     7     3     2  58.3 |
|    BZRX/USDT |     17 |           2.62 |          44.50 |            44.541 |           4.45 |         19:21:00 |    13     3     1  76.5 |
|    DOGE/USDT |     20 |           2.19 |          43.81 |            43.850 |           4.39 |         19:06:00 |    15     5     0   100 |
|   OCEAN/USDT |     19 |           2.30 |          43.66 |            43.700 |           4.37 |         23:22:00 |    12     6     1  63.2 |
|    HIVE/USDT |     22 |           1.96 |          43.18 |            43.226 |           4.32 |   1 day, 5:46:00 |    10     8     4  45.5 |
|     ZRX/USDT |     21 |           2.05 |          43.15 |            43.196 |           4.32 |   1 day, 0:49:00 |    14     4     3  66.7 |
|      NU/USDT |     17 |           2.52 |          42.87 |            42.909 |           4.29 |   1 day, 1:39:00 |    10     4     3  58.8 |
|   MATIC/USDT |     14 |           2.98 |          41.75 |            41.795 |           4.18 |         14:34:00 |    13     1     0   100 |
|     MTL/USDT |     21 |           1.96 |          41.15 |            41.186 |           4.12 |         19:20:00 |    14     5     2  66.7 |
|     AXS/USDT |     20 |           2.05 |          40.99 |            41.033 |           4.10 |   1 day, 2:03:00 |    12     5     3  60.0 |
|    WING/USDT |     28 |           1.46 |          40.97 |            41.007 |           4.10 |         18:28:00 |    20     4     4  71.4 |
|    ARPA/USDT |     26 |           1.55 |          40.22 |            40.260 |           4.03 |         19:32:00 |    19     2     5  73.1 |
|     TRU/USDT |     31 |           1.29 |          40.01 |            40.050 |           4.01 |         23:45:00 |    20     6     5  64.5 |
|    TROY/USDT |     29 |           1.37 |          39.67 |            39.713 |           3.97 |   1 day, 2:43:00 |    21     5     3  72.4 |
|     ZEC/USDT |     16 |           2.37 |          37.94 |            37.979 |           3.80 |         16:08:00 |    13     2     1  81.2 |
|    ROSE/USDT |     31 |           1.20 |          37.16 |            37.194 |           3.72 |         23:35:00 |    19     6     6  61.3 |
|     STX/USDT |     19 |           1.94 |          36.87 |            36.904 |           3.69 |         20:54:00 |    13     5     1  68.4 |
|     CRV/USDT |     24 |           1.52 |          36.53 |            36.568 |           3.66 |         17:42:00 |    17     4     3  70.8 |
|   SUPER/USDT |     17 |           2.12 |          36.11 |            36.142 |           3.61 |         20:46:00 |    12     3     2  70.6 |
|     EPS/USDT |     13 |           2.77 |          36.07 |            36.105 |           3.61 |         15:46:00 |    11     1     1  84.6 |
|     BTG/USDT |     30 |           1.15 |          34.64 |            34.676 |           3.47 |         19:08:00 |    20     7     3  66.7 |
|    FIRO/USDT |     12 |           2.89 |          34.63 |            34.667 |           3.47 |         23:45:00 |    10     2     0   100 |
|    BOND/USDT |     20 |           1.72 |          34.41 |            34.449 |           3.44 |   1 day, 0:00:00 |     9     6     5  45.0 |
|    POND/USDT |     21 |           1.63 |          34.28 |            34.313 |           3.43 |         17:51:00 |    16     2     3  76.2 |
|     KNC/USDT |     24 |           1.42 |          34.17 |            34.199 |           3.42 |         17:32:00 |    19     2     3  79.2 |
|     DOT/USDT |     16 |           2.12 |          33.89 |            33.919 |           3.39 |         16:30:00 |    11     5     0   100 |
|    CELO/USDT |     21 |           1.59 |          33.46 |            33.498 |           3.35 |   1 day, 0:26:00 |    13     6     2  61.9 |
|    AKRO/USDT |     25 |           1.32 |          32.88 |            32.914 |           3.29 |         19:38:00 |    18     3     4  72.0 |
|     BAL/USDT |     18 |           1.81 |          32.51 |            32.546 |           3.25 |         20:03:00 |    14     4     0   100 |
|     TRX/USDT |     20 |           1.61 |          32.20 |            32.231 |           3.22 |         19:09:00 |    16     2     2  80.0 |
|     FTM/USDT |     17 |           1.87 |          31.75 |            31.785 |           3.18 |         15:04:00 |    12     2     3  70.6 |
|    AION/USDT |     21 |           1.50 |          31.60 |            31.636 |           3.16 |         19:51:00 |    17     3     1  81.0 |
|     BAT/USDT |     14 |           2.22 |          31.10 |            31.134 |           3.11 |         13:34:00 |    10     1     3  71.4 |
|    STMX/USDT |     17 |           1.80 |          30.66 |            30.693 |           3.07 |         23:21:00 |     9     6     2  52.9 |
|  BADGER/USDT |     10 |           3.00 |          30.00 |            30.029 |           3.00 |   1 day, 3:42:00 |     6     3     1  60.0 |
|    LUNA/USDT |     23 |           1.29 |          29.69 |            29.717 |           2.97 |         17:42:00 |    13     6     4  56.5 |
|     LSK/USDT |     22 |           1.34 |          29.39 |            29.424 |           2.94 |         15:00:00 |    18     2     2  81.8 |
|     FLM/USDT |     17 |           1.68 |          28.53 |            28.555 |           2.86 |         18:14:00 |    15     2     0   100 |
|     NEO/USDT |     14 |           1.98 |          27.77 |            27.793 |           2.78 |         16:26:00 |    11     3     0   100 |
|   1INCH/USDT |     18 |           1.53 |          27.46 |            27.488 |           2.75 |         16:27:00 |    13     2     3  72.2 |
|     RSR/USDT |     13 |           2.03 |          26.41 |            26.433 |           2.64 |         18:28:00 |     8     4     1  61.5 |
|    GHST/USDT |     12 |           2.09 |          25.11 |            25.134 |           2.51 |         20:30:00 |     9     3     0   100 |
|    IDEX/USDT |      8 |           3.11 |          24.91 |            24.934 |           2.49 |         16:00:00 |     4     3     1  50.0 |
|     RVN/USDT |     31 |           0.80 |          24.68 |            24.708 |           2.47 |         21:25:00 |    20     7     4  64.5 |
|     BCH/USDT |     21 |           1.16 |          24.27 |            24.299 |           2.43 |   1 day, 1:57:00 |    11     5     5  52.4 |
|    IOTA/USDT |     18 |           1.33 |          24.00 |            24.026 |           2.40 |         18:53:00 |    14     3     1  77.8 |
|     LRC/USDT |     22 |           1.08 |          23.75 |            23.771 |           2.38 |         19:57:00 |    11     7     4  50.0 |
|    FLOW/USDT |     10 |           2.31 |          23.08 |            23.108 |           2.31 |         15:00:00 |     8     0     2  80.0 |
|    AVAX/USDT |     13 |           1.75 |          22.71 |            22.732 |           2.27 |         15:32:00 |     9     3     1  69.2 |
|   AUDIO/USDT |     20 |           1.08 |          21.68 |            21.706 |           2.17 |   1 day, 0:48:00 |    14     2     4  70.0 |
|     DGB/USDT |     16 |           1.35 |          21.68 |            21.698 |           2.17 |         18:08:00 |    12     1     3  75.0 |
|     PHA/USDT |     16 |           1.34 |          21.50 |            21.521 |           2.15 |         23:34:00 |    11     3     2  68.8 |
|    ARDR/USDT |     26 |           0.83 |          21.46 |            21.485 |           2.15 |         16:14:00 |    22     0     4  84.6 |
|   ALPHA/USDT |     15 |           1.40 |          21.07 |            21.087 |           2.11 |         19:16:00 |    12     1     2  80.0 |
|     WRX/USDT |     23 |           0.91 |          21.03 |            21.051 |           2.11 |         21:57:00 |    14     5     4  60.9 |
|     GXS/USDT |     23 |           0.90 |          20.72 |            20.737 |           2.07 |         17:23:00 |    16     4     3  69.6 |
|    NEAR/USDT |      7 |           2.87 |          20.09 |            20.107 |           2.01 |         12:34:00 |     6     0     1  85.7 |
|     EOS/USDT |     19 |           1.03 |          19.59 |            19.614 |           1.96 |         18:19:00 |    14     3     2  73.7 |
|    DATA/USDT |     30 |           0.65 |          19.42 |            19.436 |           1.94 |         23:56:00 |    18     9     3  60.0 |
|    IRIS/USDT |     25 |           0.74 |          18.57 |            18.591 |           1.86 |         21:41:00 |    17     4     4  68.0 |
|    TORN/USDT |      6 |           3.04 |          18.25 |            18.264 |           1.83 |         19:10:00 |     6     0     0   100 |
|     ZIL/USDT |     11 |           1.63 |          17.89 |            17.911 |           1.79 |         15:49:00 |     7     2     2  63.6 |
|     SRM/USDT |     18 |           0.99 |          17.83 |            17.844 |           1.78 |         22:07:00 |    11     5     2  61.1 |
|     RAD/USDT |      3 |           5.89 |          17.68 |            17.700 |           1.77 |         14:40:00 |     3     0     0   100 |
|     XVG/USDT |      7 |           2.52 |          17.65 |            17.671 |           1.77 |         18:09:00 |     5     2     0   100 |
|     XLM/USDT |     18 |           0.94 |          16.93 |            16.942 |           1.69 |         17:40:00 |    14     1     3  77.8 |
|    CELR/USDT |     22 |           0.77 |          16.84 |            16.862 |           1.69 |         20:00:00 |    14     4     4  63.6 |
|     LIT/USDT |     13 |           1.24 |          16.07 |            16.082 |           1.61 |         14:51:00 |    11     1     1  84.6 |
|     TVK/USDT |     11 |           1.46 |          16.02 |            16.033 |           1.60 |         15:44:00 |     9     1     1  81.8 |
|    WAXP/USDT |      5 |           3.10 |          15.48 |            15.500 |           1.55 |         13:00:00 |     5     0     0   100 |
|     MIR/USDT |      7 |           2.18 |          15.27 |            15.287 |           1.53 |         18:43:00 |     6     1     0   100 |
|    BAKE/USDT |     11 |           1.36 |          15.00 |            15.017 |           1.50 |         21:44:00 |     8     2     1  72.7 |
|    RAMP/USDT |     22 |           0.65 |          14.34 |            14.358 |           1.44 |   1 day, 1:03:00 |    11     7     4  50.0 |
|    GALA/USDT |      4 |           3.57 |          14.29 |            14.300 |           1.43 |         21:15:00 |     2     1     1  50.0 |
|     FIS/USDT |     22 |           0.65 |          14.22 |            14.238 |           1.42 |   1 day, 6:46:00 |    13     6     3  59.1 |
|   STRAX/USDT |     13 |           1.08 |          13.98 |            13.997 |           1.40 |         16:32:00 |    10     1     2  76.9 |
|     ICX/USDT |     19 |           0.74 |          13.98 |            13.995 |           1.40 |         23:03:00 |    13     3     3  68.4 |
|     REP/USDT |     23 |           0.60 |          13.85 |            13.863 |           1.39 |         19:23:00 |    16     4     3  69.6 |
|    PERP/USDT |     16 |           0.86 |          13.76 |            13.774 |           1.38 |         21:52:00 |     9     5     2  56.2 |
|    VIDT/USDT |      9 |           1.48 |          13.32 |            13.335 |           1.33 |   1 day, 0:20:00 |     6     2     1  66.7 |
|  PUNDIX/USDT |     18 |           0.70 |          12.66 |            12.673 |           1.27 |         16:50:00 |    13     2     3  72.2 |
|     DCR/USDT |     19 |           0.66 |          12.57 |            12.585 |           1.26 |         20:44:00 |    13     1     5  68.4 |
|   TFUEL/USDT |     28 |           0.45 |          12.57 |            12.580 |           1.26 |         20:32:00 |    16     5     7  57.1 |
|    DEGO/USDT |     17 |           0.74 |          12.57 |            12.579 |           1.26 |   1 day, 3:14:00 |    10     3     4  58.8 |
|     RIF/USDT |     23 |           0.54 |          12.31 |            12.323 |           1.23 |         19:31:00 |    16     4     3  69.6 |
|    STPT/USDT |     33 |           0.37 |          12.18 |            12.192 |           1.22 |         23:45:00 |    17     9     7  51.5 |
|   FRONT/USDT |      3 |           3.93 |          11.79 |            11.800 |           1.18 |   1 day, 0:40:00 |     2     1     0   100 |
|     MDX/USDT |     18 |           0.64 |          11.45 |            11.461 |           1.15 |   1 day, 1:27:00 |    11     4     3  61.1 |
|     LTO/USDT |     23 |           0.47 |          10.72 |            10.726 |           1.07 |   1 day, 3:05:00 |    14     6     3  60.9 |
|     LTC/USDT |     21 |           0.50 |          10.52 |            10.528 |           1.05 |         18:26:00 |    15     2     4  71.4 |
|    DENT/USDT |     14 |           0.72 |          10.07 |            10.080 |           1.01 |   1 day, 2:51:00 |     8     1     5  57.1 |
|     XEM/USDT |     11 |           0.89 |           9.81 |             9.823 |           0.98 |         22:49:00 |     6     3     2  54.5 |
|     COS/USDT |     21 |           0.46 |           9.72 |             9.732 |           0.97 |   1 day, 1:57:00 |    14     5     2  66.7 |
|     ETH/USDT |      5 |           1.81 |           9.06 |             9.065 |           0.91 |         21:48:00 |     4     0     1  80.0 |
|     UNI/USDT |      7 |           1.28 |           8.97 |             8.981 |           0.90 |         23:51:00 |     3     4     0   100 |
|     TCT/USDT |     28 |           0.30 |           8.36 |             8.373 |           0.84 |   1 day, 2:26:00 |    17     5     6  60.7 |
|    WNXM/USDT |     19 |           0.42 |           7.98 |             7.984 |           0.80 |         19:51:00 |    12     4     3  63.2 |
|    REEF/USDT |     26 |           0.30 |           7.91 |             7.914 |           0.79 |         16:53:00 |    17     3     6  65.4 |
|    ANKR/USDT |     22 |           0.33 |           7.33 |             7.333 |           0.73 |   1 day, 0:22:00 |    14     3     5  63.6 |
|      DF/USDT |      7 |           0.96 |           6.72 |             6.722 |           0.67 |   1 day, 1:00:00 |     4     2     1  57.1 |
|     C98/USDT |     12 |           0.55 |           6.61 |             6.612 |           0.66 |         17:45:00 |     9     2     1  75.0 |
|     ADX/USDT |      2 |           3.11 |           6.21 |             6.218 |           0.62 |         15:00:00 |     2     0     0   100 |
|     UMA/USDT |     23 |           0.26 |           6.02 |             6.028 |           0.60 |         18:52:00 |    14     3     6  60.9 |
|     PLA/USDT |      1 |           5.89 |           5.89 |             5.900 |           0.59 |         16:00:00 |     1     0     0   100 |
|     ENJ/USDT |     19 |           0.30 |           5.72 |             5.725 |           0.57 |         19:44:00 |    11     5     3  57.9 |
|     REN/USDT |     17 |           0.33 |           5.60 |             5.607 |           0.56 |   1 day, 1:25:00 |    10     4     3  58.8 |
|     BNB/USDT |      9 |           0.59 |           5.29 |             5.294 |           0.53 |         19:27:00 |     6     1     2  66.7 |
|     ANT/USDT |     24 |           0.21 |           5.01 |             5.015 |           0.50 |   1 day, 0:02:00 |    15     5     4  62.5 |
|    BAND/USDT |     18 |           0.27 |           4.93 |             4.937 |           0.49 |   1 day, 0:30:00 |     8     6     4  44.4 |
|     ONT/USDT |     20 |           0.23 |           4.59 |             4.599 |           0.46 |         17:06:00 |    14     1     5  70.0 |
|    IOST/USDT |     15 |           0.26 |           3.94 |             3.946 |           0.39 |         21:36:00 |    10     3     2  66.7 |
|     ORN/USDT |     11 |           0.34 |           3.76 |             3.762 |           0.38 |         21:55:00 |     5     3     3  45.5 |
|     ELF/USDT |      8 |           0.45 |           3.57 |             3.573 |           0.36 |   1 day, 8:30:00 |     3     3     2  37.5 |
|   SUSHI/USDT |     14 |           0.22 |           3.06 |             3.062 |           0.31 |         16:09:00 |    10     2     2  71.4 |
|     BNT/USDT |     13 |           0.23 |           2.99 |             2.990 |           0.30 |         20:32:00 |     7     5     1  53.8 |
|     CVC/USDT |     21 |           0.13 |           2.80 |             2.801 |           0.28 |         15:26:00 |    16     1     4  76.2 |
|   TRIBE/USDT |     10 |           0.24 |           2.41 |             2.411 |           0.24 |   1 day, 3:06:00 |     5     4     1  50.0 |
|     ICP/USDT |      9 |           0.24 |           2.19 |             2.193 |           0.22 |   1 day, 3:00:00 |     6     2     1  66.7 |
|      OM/USDT |     21 |           0.09 |           1.99 |             1.993 |           0.20 |   1 day, 0:09:00 |    13     5     3  61.9 |
|     ILV/USDT |      4 |           0.45 |           1.81 |             1.809 |           0.18 |         22:45:00 |     3     1     0   100 |
|     XEC/USDT |     15 |           0.12 |           1.73 |             1.728 |           0.17 |   1 day, 1:28:00 |    10     3     2  66.7 |
|    EGLD/USDT |     15 |           0.11 |           1.65 |             1.656 |           0.17 |         21:00:00 |    10     1     4  66.7 |
|    AUTO/USDT |     12 |           0.11 |           1.29 |             1.290 |           0.13 |         21:25:00 |     5     3     4  41.7 |
|    SUSD/USDT |     28 |           0.04 |           1.17 |             1.176 |           0.12 |  1 day, 13:13:00 |     9    13     6  32.1 |
|    KEEP/USDT |     10 |           0.11 |           1.14 |             1.136 |           0.11 |         16:36:00 |     5     3     2  50.0 |
|    PERL/USDT |     35 |           0.03 |           1.06 |             1.056 |           0.11 |   1 day, 1:15:00 |    23     6     6  65.7 |
|     GNO/USDT |      5 |           0.20 |           1.00 |             1.001 |           0.10 |  1 day, 10:12:00 |     3     2     0   100 |
|     HOT/USDT |     21 |           0.05 |           0.98 |             0.983 |           0.10 |   1 day, 0:06:00 |    14     3     4  66.7 |
|     ERN/USDT |     14 |           0.04 |           0.56 |             0.556 |           0.06 |         22:39:00 |     7     4     3  50.0 |
|     GTC/USDT |      8 |           0.06 |           0.47 |             0.470 |           0.05 |   1 day, 4:52:00 |     4     2     2  50.0 |
|     GRT/USDT |     19 |           0.02 |           0.46 |             0.465 |           0.05 |   1 day, 0:13:00 |    10     6     3  52.6 |
|    DYDX/USDT |      3 |           0.11 |           0.34 |             0.342 |           0.03 |         11:00:00 |     2     1     0   100 |
|     BNX/USDT |      1 |           0.13 |           0.13 |             0.133 |           0.01 |         16:00:00 |     1     0     0   100 |
|     AMP/USDT |      0 |           0.00 |           0.00 |             0.000 |           0.00 |             0:00 |     0     0     0     0 |
|     ENS/USDT |      0 |           0.00 |           0.00 |             0.000 |           0.00 |             0:00 |     0     0     0     0 |
|   JASMY/USDT |      0 |           0.00 |           0.00 |             0.000 |           0.00 |             0:00 |     0     0     0     0 |
|    KP3R/USDT |      0 |           0.00 |           0.00 |             0.000 |           0.00 |             0:00 |     0     0     0     0 |
|   PORTO/USDT |      0 |           0.00 |           0.00 |             0.000 |           0.00 |             0:00 |     0     0     0     0 |
|    POWR/USDT |      0 |           0.00 |           0.00 |             0.000 |           0.00 |             0:00 |     0     0     0     0 |
|     PYR/USDT |      0 |           0.00 |           0.00 |             0.000 |           0.00 |             0:00 |     0     0     0     0 |
|      QI/USDT |      0 |           0.00 |           0.00 |             0.000 |           0.00 |             0:00 |     0     0     0     0 |
|    RNDR/USDT |      0 |           0.00 |           0.00 |             0.000 |           0.00 |             0:00 |     0     0     0     0 |
|     VGX/USDT |      0 |           0.00 |           0.00 |             0.000 |           0.00 |             0:00 |     0     0     0     0 |
|    NULS/USDT |     32 |          -0.00 |          -0.06 |            -0.056 |          -0.01 |         21:39:00 |    21     5     6  65.6 |
|     WAN/USDT |     13 |          -0.02 |          -0.27 |            -0.266 |          -0.03 |         21:55:00 |    10     1     2  76.9 |
|    MBOX/USDT |      8 |          -0.08 |          -0.61 |            -0.607 |          -0.06 |  1 day, 12:00:00 |     4     3     1  50.0 |
|    USDP/USDT |      4 |          -0.23 |          -0.92 |            -0.919 |          -0.09 | 7 days, 23:00:00 |     0     1     3     0 |
|     CKB/USDT |     16 |          -0.06 |          -0.96 |            -0.959 |          -0.10 |         20:34:00 |     9     3     4  56.2 |
|    BEAM/USDT |     31 |          -0.03 |          -1.02 |            -1.024 |          -0.10 |   1 day, 1:56:00 |    22     4     5  71.0 |
|    LINK/USDT |     12 |          -0.15 |          -1.74 |            -1.745 |          -0.17 |         23:10:00 |     6     5     1  50.0 |
|     MBL/USDT |     23 |          -0.09 |          -2.04 |            -2.044 |          -0.20 |         19:03:00 |    16     5     2  69.6 |
|     BTS/USDT |     21 |          -0.11 |          -2.24 |            -2.238 |          -0.22 |         15:31:00 |    13     3     5  61.9 |
|  BURGER/USDT |     17 |          -0.15 |          -2.63 |            -2.636 |          -0.26 |         21:11:00 |    13     1     3  76.5 |
|     CFX/USDT |     16 |          -0.17 |          -2.68 |            -2.683 |          -0.27 |   1 day, 5:11:00 |     9     3     4  56.2 |
|     FIL/USDT |     19 |          -0.16 |          -2.96 |            -2.963 |          -0.30 |         21:22:00 |    14     1     4  73.7 |
|   WAVES/USDT |     20 |          -0.15 |          -3.07 |            -3.076 |          -0.31 |         20:57:00 |    12     3     5  60.0 |
|     SOL/USDT |     14 |          -0.26 |          -3.69 |            -3.696 |          -0.37 |         21:04:00 |     9     2     3  64.3 |
|    CAKE/USDT |      7 |          -0.55 |          -3.87 |            -3.874 |          -0.39 |         17:17:00 |     3     2     2  42.9 |
|     XMR/USDT |     14 |          -0.28 |          -3.92 |            -3.928 |          -0.39 |         20:39:00 |     8     2     4  57.1 |
|   ALICE/USDT |     13 |          -0.32 |          -4.16 |            -4.160 |          -0.42 |         21:37:00 |     9     1     3  69.2 |
|    HARD/USDT |     24 |          -0.20 |          -4.84 |            -4.848 |          -0.48 |         23:12:00 |    11     6     7  45.8 |
|     RGT/USDT |      3 |          -1.84 |          -5.51 |            -5.516 |          -0.55 |         14:40:00 |     1     0     2  33.3 |
|    UNFI/USDT |     21 |          -0.28 |          -5.98 |            -5.984 |          -0.60 |         21:46:00 |    12     4     5  57.1 |
|     CTK/USDT |     18 |          -0.36 |          -6.50 |            -6.502 |          -0.65 |   1 day, 2:50:00 |    11     5     2  61.1 |
|     YFI/USDT |     15 |          -0.47 |          -7.04 |            -7.043 |          -0.70 |         21:04:00 |     7     4     4  46.7 |
|     YGG/USDT |      4 |          -1.88 |          -7.50 |            -7.510 |          -0.75 |  1 day, 10:30:00 |     0     3     1     0 |
|     RAY/USDT |      8 |          -0.95 |          -7.61 |            -7.622 |          -0.76 |   1 day, 2:15:00 |     4     0     4  50.0 |
|    AGLD/USDT |      4 |          -1.91 |          -7.65 |            -7.653 |          -0.77 |  1 day, 16:30:00 |     2     1     1  50.0 |
|     QNT/USDT |     10 |          -0.78 |          -7.83 |            -7.840 |          -0.78 |   1 day, 5:00:00 |     4     3     3  40.0 |
|    ATOM/USDT |     19 |          -0.41 |          -7.85 |            -7.857 |          -0.79 |         21:35:00 |    11     4     4  57.9 |
|    FARM/USDT |     10 |          -0.82 |          -8.18 |            -8.187 |          -0.82 |  1 day, 11:06:00 |     3     5     2  30.0 |
|     ADA/USDT |     16 |          -0.51 |          -8.24 |            -8.244 |          -0.82 |   1 day, 2:15:00 |     9     5     2  56.2 |
|     TKO/USDT |     19 |          -0.45 |          -8.47 |            -8.481 |          -0.85 |   1 day, 3:44:00 |    11     5     3  57.9 |
|     MDT/USDT |     24 |          -0.36 |          -8.59 |            -8.601 |          -0.86 |   1 day, 2:35:00 |    13     7     4  54.2 |
|     MKR/USDT |     17 |          -0.53 |          -9.06 |            -9.069 |          -0.91 |   1 day, 5:11:00 |    10     4     3  58.8 |
|    FIDA/USDT |      3 |          -3.60 |         -10.79 |           -10.804 |          -1.08 | 2 days, 19:20:00 |     2     0     1  66.7 |
|     DIA/USDT |     33 |          -0.33 |         -10.82 |           -10.832 |          -1.08 |         20:09:00 |    22     6     5  66.7 |
|     SNX/USDT |     12 |          -0.91 |         -10.87 |           -10.885 |          -1.09 |         13:45:00 |     9     0     3  75.0 |
|     ONG/USDT |     27 |          -0.41 |         -10.97 |           -10.981 |          -1.10 |   1 day, 2:56:00 |    19     5     3  70.4 |
|    MOVR/USDT |      1 |         -11.03 |         -11.03 |           -11.036 |          -1.10 |   1 day, 3:00:00 |     0     0     1     0 |
|     ZEN/USDT |     21 |          -0.53 |         -11.08 |           -11.091 |          -1.11 |         14:49:00 |    15     2     4  71.4 |
|     SXP/USDT |     18 |          -0.62 |         -11.09 |           -11.098 |          -1.11 |         15:43:00 |    13     0     5  72.2 |
| AUCTION/USDT |      1 |         -11.19 |         -11.19 |           -11.199 |          -1.12 |          3:00:00 |     0     0     1     0 |
|     KSM/USDT |     11 |          -1.04 |         -11.39 |           -11.401 |          -1.14 |   1 day, 1:16:00 |     7     1     3  63.6 |
|    YFII/USDT |     15 |          -0.84 |         -12.66 |           -12.670 |          -1.27 |   1 day, 2:52:00 |     9     4     2  60.0 |
|    COTI/USDT |     12 |          -1.15 |         -13.86 |           -13.870 |          -1.39 |         13:40:00 |     9     0     3  75.0 |
|     XTZ/USDT |     15 |          -0.96 |         -14.35 |           -14.363 |          -1.44 |         15:20:00 |     9     3     3  60.0 |
|    DASH/USDT |     19 |          -0.76 |         -14.40 |           -14.411 |          -1.44 |         15:47:00 |    13     1     5  68.4 |
|     BEL/USDT |     19 |          -0.76 |         -14.46 |           -14.479 |          -1.45 |         18:03:00 |    12     2     5  63.2 |
|    KLAY/USDT |      9 |          -1.62 |         -14.56 |           -14.570 |          -1.46 |  2 days, 9:20:00 |     3     2     4  33.3 |
|    PAXG/USDT |     25 |          -0.61 |         -15.13 |           -15.150 |          -1.51 |  1 day, 12:05:00 |     7     8    10  28.0 |
|    BETA/USDT |      3 |          -5.19 |         -15.56 |           -15.573 |          -1.56 |         23:00:00 |     1     0     2  33.3 |
|     GTO/USDT |     22 |          -0.73 |         -16.13 |           -16.151 |          -1.62 |   1 day, 8:14:00 |    14     5     3  63.6 |
|     DAR/USDT |      1 |         -16.18 |         -16.18 |           -16.198 |          -1.62 |         14:00:00 |     0     0     1     0 |
|     BLZ/USDT |     20 |          -0.82 |         -16.49 |           -16.507 |          -1.65 |         21:54:00 |    12     2     6  60.0 |
|      AR/USDT |     11 |          -1.55 |         -17.03 |           -17.051 |          -1.71 |         23:00:00 |     4     5     2  36.4 |
|   LAZIO/USDT |      2 |          -8.82 |         -17.63 |           -17.650 |          -1.77 |   1 day, 3:00:00 |     0     0     2     0 |
|    COMP/USDT |     17 |          -1.04 |         -17.64 |           -17.658 |          -1.77 |         16:46:00 |    10     2     5  58.8 |
|    AAVE/USDT |     15 |          -1.20 |         -17.96 |           -17.974 |          -1.80 |         17:52:00 |     8     2     5  53.3 |
|     MLN/USDT |     13 |          -1.45 |         -18.90 |           -18.919 |          -1.89 |  1 day, 10:42:00 |     9     1     3  69.2 |
|   STORJ/USDT |     21 |          -0.92 |         -19.42 |           -19.443 |          -1.94 |         20:03:00 |    13     3     5  61.9 |
|     SYS/USDT |      7 |          -3.28 |         -22.94 |           -22.959 |          -2.30 |  1 day, 21:00:00 |     3     2     2  42.9 |
|    DUSK/USDT |     22 |          -1.08 |         -23.80 |           -23.822 |          -2.38 |         21:38:00 |    13     4     5  59.1 |
|   CHESS/USDT |      3 |          -8.00 |         -24.00 |           -24.021 |          -2.40 |  1 day, 10:40:00 |     0     1     2     0 |
|    LINA/USDT |     18 |          -1.37 |         -24.72 |           -24.749 |          -2.47 |   1 day, 1:17:00 |    11     3     4  61.1 |
|    RARE/USDT |      4 |          -6.33 |         -25.33 |           -25.355 |          -2.54 |  2 days, 5:30:00 |     1     1     2  25.0 |
|    DODO/USDT |     14 |          -1.82 |         -25.50 |           -25.523 |          -2.55 |         16:34:00 |     9     0     5  64.3 |
|    KAVA/USDT |     20 |          -1.28 |         -25.53 |           -25.559 |          -2.56 |         22:03:00 |    12     2     6  60.0 |
|     AVA/USDT |     21 |          -1.22 |         -25.59 |           -25.618 |          -2.56 |   1 day, 1:20:00 |    12     4     5  57.1 |
|   QUICK/USDT |     12 |          -2.16 |         -25.91 |           -25.939 |          -2.59 |         18:05:00 |     7     1     4  58.3 |
|     XRP/USDT |     14 |          -1.86 |         -26.03 |           -26.059 |          -2.61 |         20:43:00 |     7     3     4  50.0 |
|    MINA/USDT |      7 |          -3.73 |         -26.12 |           -26.150 |          -2.62 |  1 day, 18:09:00 |     2     2     3  28.6 |
|    ALGO/USDT |     15 |          -1.78 |         -26.70 |           -26.727 |          -2.67 |         23:36:00 |     8     1     6  53.3 |
|   BTCST/USDT |     25 |          -1.11 |         -27.64 |           -27.669 |          -2.77 |   1 day, 5:36:00 |    14     8     3  56.0 |
|     OMG/USDT |     22 |          -1.29 |         -28.46 |           -28.487 |          -2.85 |         19:11:00 |    12     3     7  54.5 |
|     CLV/USDT |     11 |          -2.62 |         -28.86 |           -28.893 |          -2.89 |  2 days, 2:44:00 |     6     1     4  54.5 |
|  ALPACA/USDT |      7 |          -4.16 |         -29.12 |           -29.148 |          -2.91 |  2 days, 2:17:00 |     3     0     4  42.9 |
|     CVP/USDT |      3 |          -9.85 |         -29.55 |           -29.584 |          -2.96 | 4 days, 20:20:00 |     0     1     2     0 |
|    POLY/USDT |      7 |          -4.24 |         -29.68 |           -29.706 |          -2.97 |   1 day, 8:51:00 |     3     1     3  42.9 |
|    MANA/USDT |     20 |          -1.65 |         -32.90 |           -32.937 |          -3.29 |   1 day, 1:42:00 |    13     2     5  65.0 |
|     FUN/USDT |     19 |          -1.87 |         -35.47 |           -35.504 |          -3.55 |         22:35:00 |    12     1     6  63.2 |
|    SAND/USDT |     25 |          -1.46 |         -36.56 |           -36.592 |          -3.66 |   1 day, 4:14:00 |    16     4     5  64.0 |
|   FORTH/USDT |     16 |          -2.34 |         -37.43 |           -37.468 |          -3.75 |  1 day, 10:38:00 |     3     8     5  18.8 |
|     UTK/USDT |     25 |          -1.51 |         -37.64 |           -37.675 |          -3.77 |         23:53:00 |    13     5     7  52.0 |
|     MFT/USDT |     28 |          -2.04 |         -57.25 |           -57.305 |          -5.73 |         23:34:00 |    14     6     8  50.0 |
|     RLC/USDT |     21 |          -3.07 |         -64.41 |           -64.479 |          -6.45 |         18:54:00 |    11     2     8  52.4 |
|        TOTAL |   4384 |           0.93 |        4083.07 |          4087.156 |         408.72 |         22:10:00 |  2847   818   719  64.9 |
========================================================== BUY TAG STATS ===========================================================
|   TAG |   Buys |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |
|-------+--------+----------------+----------------+-------------------+----------------+----------------+-------------------------|
| TOTAL |   4384 |           0.93 |        4083.07 |          4087.156 |         408.72 |       22:10:00 |  2847   818   719  64.9 |
======================================================= SELL REASON STATS ========================================================
|        Sell Reason |   Sells |   Win  Draws  Loss  Win% |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |
|--------------------+---------+--------------------------+----------------+----------------+-------------------+----------------|
|                roi |    2080 |   1262   818     0   100 |           4.86 |       10103.1  |         10113.2   |          37.56 |
|        sell_signal |    1584 |   1584     0     0   100 |           1.21 |        1908.92 |          1910.82  |           7.1  |
| trailing_stop_loss |     712 |      0     0   712     0 |         -10.96 |       -7801.61 |         -7809.41  |         -29    |
|          stop_loss |       4 |      0     0     4     0 |         -31.14 |        -124.55 |          -124.676 |          -0.46 |
|         force_sell |       4 |      1     0     3  25.0 |          -0.69 |          -2.74 |            -2.745 |          -0.01 |
======================================================== LEFT OPEN TRADES REPORT ========================================================
|       Pair |   Buys |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |
|------------+--------+----------------+----------------+-------------------+----------------+----------------+-------------------------|
| SUPER/USDT |      1 |           0.15 |           0.15 |             0.149 |           0.01 |        1:00:00 |     1     0     0   100 |
|  PAXG/USDT |      1 |          -0.20 |          -0.20 |            -0.200 |          -0.02 |        1:00:00 |     0     0     1     0 |
| FORTH/USDT |      1 |          -0.85 |          -0.85 |            -0.853 |          -0.09 |        1:00:00 |     0     0     1     0 |
|  IDEX/USDT |      1 |          -1.84 |          -1.84 |            -1.842 |          -0.18 |        1:00:00 |     0     0     1     0 |
|      TOTAL |      4 |          -0.69 |          -2.74 |            -2.745 |          -0.27 |        1:00:00 |     1     0     3  25.0 |
=============== SUMMARY METRICS ================
| Metric                 | Value               |
|------------------------+---------------------|
| Backtesting from       | 2021-01-01 00:00:00 |
| Backtesting to         | 2021-12-12 15:00:00 |
| Max open trades        | 269                 |
|                        |                     |
| Total/Daily Avg Trades | 4384 / 12.71        |
| Starting balance       | 1000.000 USDT       |
| Final balance          | 5087.156 USDT       |
| Absolute profit        | 4087.156 USDT       |
| Total profit %         | 408.72%             |
| Trades per day         | 12.71               |
| Avg. daily profit %    | 1.18%               |
| Avg. stake amount      | 100.000 USDT        |
| Total trade volume     | 438400.000 USDT     |
|                        |                     |
| Best Pair              | OXT/USDT 113.59%    |
| Worst Pair             | RLC/USDT -64.41%    |
| Best trade             | DNT/USDT 55.24%     |
| Worst trade            | MANA/USDT -31.14%   |
| Best day               | 213.146 USDT        |
| Worst day              | -332.471 USDT       |
| Days win/draw/lose     | 171 / 97 / 78       |
| Avg. Duration Winners  | 13:34:00            |
| Avg. Duration Loser    | 1 day, 12:12:00     |
| Rejected Buy signals   | 0                   |
|                        |                     |
| Min balance            | 997.635 USDT        |
| Max balance            | 5450.985 USDT       |
| Drawdown               | 508.82%             |
| Drawdown               | 509.325 USDT        |
| Drawdown high          | 3708.862 USDT       |
| Drawdown low           | 3199.537 USDT       |
| Drawdown Start         | 2021-09-19 10:00:00 |
| Drawdown End           | 2021-09-28 23:00:00 |
| Market change          | 561.59%             |
================================================
```