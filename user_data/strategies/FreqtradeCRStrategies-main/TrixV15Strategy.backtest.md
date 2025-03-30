```
freqtrade backtesting --strategy TrixV15Strategy --stake-amount 100 --timeframe 1h --max-open-trades -1 --fee 0.001 --dry-run-wallet 1000 --timerange=20210101-
Creating freqtradelocal_freqtrade_run ... done
2021-12-17 18:06:18,580 - freqtrade.configuration.configuration - INFO - Using config: user_data/config.json ...
2021-12-17 18:06:18,582 - freqtrade.loggers - INFO - Verbosity set to 0
2021-12-17 18:06:18,582 - freqtrade.configuration.configuration - INFO - Parameter -i/--timeframe detected ... Using timeframe: 1h ...
2021-12-17 18:06:18,582 - freqtrade.configuration.configuration - INFO - Parameter --max-open-trades detected, overriding max_open_trades to: -1 ...
2021-12-17 18:06:18,583 - freqtrade.configuration.configuration - INFO - Parameter --stake-amount detected, overriding stake_amount to: 100.0 ...
2021-12-17 18:06:18,583 - freqtrade.configuration.configuration - INFO - Parameter --dry-run-wallet detected, overriding dry_run_wallet to: 1000.0 ...
2021-12-17 18:06:18,583 - freqtrade.configuration.configuration - INFO - Parameter --fee detected, setting fee to: 0.001 ...
2021-12-17 18:06:18,583 - freqtrade.configuration.configuration - INFO - Parameter --timerange detected: 20210101- ...
2021-12-17 18:06:19,763 - freqtrade.configuration.configuration - INFO - Using user-data directory: /freqtrade/user_data ...
2021-12-17 18:06:19,764 - freqtrade.configuration.configuration - INFO - Using data directory: /freqtrade/user_data/data/binance ...
2021-12-17 18:06:19,764 - freqtrade.configuration.configuration - INFO - Overriding timeframe with Command line argument
2021-12-17 18:06:19,765 - freqtrade.configuration.check_exchange - INFO - Checking exchange...
2021-12-17 18:06:19,773 - freqtrade.configuration.check_exchange - INFO - Exchange "binance" is officially supported by the Freqtrade development team.
2021-12-17 18:06:19,773 - freqtrade.configuration.configuration - INFO - Using pairlist from configuration.
2021-12-17 18:06:19,774 - freqtrade.configuration.config_validation - INFO - Validating configuration ...
2021-12-17 18:06:19,779 - freqtrade.commands.optimize_commands - INFO - Starting freqtrade in Backtesting mode
2021-12-17 18:06:19,779 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2021-12-17 18:06:19,779 - freqtrade.exchange.exchange - INFO - Using CCXT 1.61.92
2021-12-17 18:06:19,794 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2021-12-17 18:06:22,421 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2021-12-17 18:06:23,019 - TrixV15Strategy - INFO - pandas_ta successfully imported
2021-12-17 18:06:23,098 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy TrixV15Strategy from '/freqtrade/user_data/strategies/TrixV15Strategy.py'...
2021-12-17 18:06:23,099 - freqtrade.strategy.hyper - INFO - Loading parameters from file /freqtrade/user_data/strategies/TrixV15Strategy.json
2021-12-17 18:06:23,117 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_ema_multiplier = 0.85
2021-12-17 18:06:23,117 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_ema_src = open
2021-12-17 18:06:23,117 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_ema_timeperiod = 10
2021-12-17 18:06:23,117 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_ema_timeperiod_enabled = True
2021-12-17 18:06:23,117 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_stoch_rsi = 0.901
2021-12-17 18:06:23,117 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_stoch_rsi_enabled = True
2021-12-17 18:06:23,117 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_trix_signal_timeperiod = 19
2021-12-17 18:06:23,117 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_trix_signal_type = trigger
2021-12-17 18:06:23,117 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_trix_src = low
2021-12-17 18:06:23,118 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_trix_timeperiod = 8
2021-12-17 18:06:23,118 - freqtrade.strategy.hyper - INFO - Strategy Parameter: sell_stoch_rsi = 0.183
2021-12-17 18:06:23,118 - freqtrade.strategy.hyper - INFO - Strategy Parameter: sell_stoch_rsi_enabled = True
2021-12-17 18:06:23,118 - freqtrade.strategy.hyper - INFO - Strategy Parameter: sell_trix_signal_timeperiod = 19
2021-12-17 18:06:23,118 - freqtrade.strategy.hyper - INFO - Strategy Parameter: sell_trix_signal_type = trailing
2021-12-17 18:06:23,118 - freqtrade.strategy.hyper - INFO - Strategy Parameter: sell_trix_src = high
2021-12-17 18:06:23,118 - freqtrade.strategy.hyper - INFO - Strategy Parameter: sell_trix_timeperiod = 10
2021-12-17 18:06:23,119 - freqtrade.strategy.hyper - INFO - No params for protection found, using default values.
2021-12-17 18:06:23,119 - freqtrade.resolvers.strategy_resolver - INFO - Override strategy 'timeframe' with value in config file: 1h.
2021-12-17 18:06:23,119 - freqtrade.resolvers.strategy_resolver - INFO - Override strategy 'stake_currency' with value in config file: USDT.
2021-12-17 18:06:23,119 - freqtrade.resolvers.strategy_resolver - INFO - Override strategy 'stake_amount' with value in config file: 100.0.
2021-12-17 18:06:23,119 - freqtrade.resolvers.strategy_resolver - INFO - Override strategy 'unfilledtimeout' with value in config file: {'buy': 10, 'sell': 30, 'unit': 'minutes', 'exit_timeout_count': 0}.        
2021-12-17 18:06:23,119 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using minimal_roi: {'0': 0.5529999999999999, '423': 0.14400000000000002, '751': 0.059, '1342': 0}
2021-12-17 18:06:23,120 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using timeframe: 1h
2021-12-17 18:06:23,120 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using stoploss: -0.31
2021-12-17 18:06:23,120 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using trailing_stop: False
2021-12-17 18:06:23,120 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using trailing_stop_positive_offset: 0.0
2021-12-17 18:06:23,120 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using trailing_only_offset_is_reached: False
2021-12-17 18:06:23,120 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using use_custom_stoploss: False
2021-12-17 18:06:23,120 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using process_only_new_candles: False
2021-12-17 18:06:23,120 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using order_types: {'buy': 'limit', 'sell': 'limit', 'stoploss': 'market', 'stoploss_on_exchange': False}
2021-12-17 18:06:23,120 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using order_time_in_force: {'buy': 'gtc', 'sell': 'gtc'}
2021-12-17 18:06:23,121 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using stake_currency: USDT
2021-12-17 18:06:23,121 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using stake_amount: 100.0
2021-12-17 18:06:23,121 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using protections: []
2021-12-17 18:06:23,121 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using startup_candle_count: 19
2021-12-17 18:06:23,121 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using unfilledtimeout: {'buy': 10, 'sell': 30, 'unit': 'minutes', 'exit_timeout_count': 0}
2021-12-17 18:06:23,121 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using use_sell_signal: True
2021-12-17 18:06:23,121 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using sell_profit_only: True
2021-12-17 18:06:23,121 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using ignore_roi_if_buy_signal: False
2021-12-17 18:06:23,121 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using sell_profit_offset: 0.0
2021-12-17 18:06:23,121 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using disable_dataframe_checks: False
2021-12-17 18:06:23,121 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using ignore_buying_expired_candle_after: 0
2021-12-17 18:06:23,122 - freqtrade.configuration.config_validation - INFO - Validating configuration ...
2021-12-17 18:06:23,129 - freqtrade.resolvers.iresolver - INFO - Using resolved pairlist StaticPairList from '/freqtrade/freqtrade/plugins/pairlist/StaticPairList.py'...
2021-12-17 18:06:23,659 - freqtrade.plugins.pairlistmanager - WARNING - Pair ACM/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:06:23,659 - freqtrade.plugins.pairlistmanager - WARNING - Pair ASR/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:06:23,659 - freqtrade.plugins.pairlistmanager - WARNING - Pair ATM/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:06:23,660 - freqtrade.plugins.pairlistmanager - WARNING - Pair AUD/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:06:23,660 - freqtrade.plugins.pairlistmanager - WARNING - Pair BAR/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:06:23,660 - freqtrade.plugins.pairlistmanager - WARNING - Pair BTC/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:06:23,660 - freqtrade.plugins.pairlistmanager - WARNING - Pair BUSD/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:06:23,660 - freqtrade.plugins.pairlistmanager - WARNING - Pair CHZ/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:06:23,660 - freqtrade.plugins.pairlistmanager - WARNING - Pair CITY/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:06:23,660 - freqtrade.plugins.pairlistmanager - WARNING - Pair CTXC/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:06:23,660 - freqtrade.plugins.pairlistmanager - WARNING - Pair EUR/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:06:23,661 - freqtrade.plugins.pairlistmanager - WARNING - Pair FOR/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:06:23,661 - freqtrade.plugins.pairlistmanager - WARNING - Pair FTT/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:06:23,661 - freqtrade.plugins.pairlistmanager - WARNING - Pair GBP/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:06:23,661 - freqtrade.plugins.pairlistmanager - WARNING - Pair HBAR/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:06:23,661 - freqtrade.plugins.pairlistmanager - WARNING - Pair JUV/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:06:23,661 - freqtrade.plugins.pairlistmanager - WARNING - Pair NMR/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:06:23,661 - freqtrade.plugins.pairlistmanager - WARNING - Pair OG/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:06:23,662 - freqtrade.plugins.pairlistmanager - WARNING - Pair PSG/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:06:23,662 - freqtrade.plugins.pairlistmanager - WARNING - Pair SHIB/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:06:23,662 - freqtrade.plugins.pairlistmanager - WARNING - Pair SLP/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:06:23,662 - freqtrade.plugins.pairlistmanager - WARNING - Pair TUSD/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:06:23,662 - freqtrade.plugins.pairlistmanager - WARNING - Pair USDC/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:06:23,662 - freqtrade.plugins.pairlistmanager - WARNING - Pair XVS/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:06:23,664 - freqtrade.data.history.history_utils - INFO - Using indicator startup period: 19 ...
2021-12-17 18:06:23,839 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair ADX/USDT, data starts at 2021-10-29 10:00:00
2021-12-17 18:06:23,859 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair AGLD/USDT, data starts at 2021-10-05 07:00:00
2021-12-17 18:06:23,998 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair ALICE/USDT, data starts at 2021-03-15 06:00:00
2021-12-17 18:06:24,020 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair ALPACA/USDT, data starts at 2021-08-11 08:00:00
2021-12-17 18:06:24,073 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair AMP/USDT, data starts at 2021-11-23 06:00:00
2021-12-17 18:06:24,227 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair AR/USDT, data starts at 2021-05-14 12:00:00
2021-12-17 18:06:24,328 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair ATA/USDT, data starts at 2021-06-07 06:00:00
2021-12-17 18:06:24,387 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair AUCTION/USDT, data starts at 2021-10-29 10:00:00
2021-12-17 18:06:24,443 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair AUTO/USDT, data starts at 2021-04-02 09:00:00
2021-12-17 18:06:24,618 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair BADGER/USDT, data starts at 2021-03-02 08:00:00
2021-12-17 18:06:24,644 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair BAKE/USDT, data starts at 2021-04-30 12:00:00
2021-12-17 18:06:24,941 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair BETA/USDT, data starts at 2021-10-08 12:00:00
2021-12-17 18:06:25,068 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair BNX/USDT, data starts at 2021-11-04 11:00:00
2021-12-17 18:06:25,090 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair BOND/USDT, data starts at 2021-07-05 06:00:00
2021-12-17 18:06:25,117 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair BTCST/USDT, data starts at 2021-01-13 06:00:00
2021-12-17 18:06:25,127 - freqtrade.data.converter - INFO - Missing data fillup for BTCST/USDT: before: 7893 - after: 8002 - 1.38%
2021-12-17 18:06:25,200 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair BTG/USDT, data starts at 2021-04-16 07:00:00
2021-12-17 18:06:25,303 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair BURGER/USDT, data starts at 2021-04-30 12:00:00
2021-12-17 18:06:25,357 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair C98/USDT, data starts at 2021-07-23 12:00:00
2021-12-17 18:06:25,383 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair CAKE/USDT, data starts at 2021-02-19 06:00:00
2021-12-17 18:06:25,411 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair CELO/USDT, data starts at 2021-01-05 08:00:00
2021-12-17 18:06:25,534 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair CFX/USDT, data starts at 2021-03-29 11:00:00
2021-12-17 18:06:25,554 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair CHESS/USDT, data starts at 2021-10-22 06:00:00
2021-12-17 18:06:25,617 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair CKB/USDT, data starts at 2021-01-26 12:00:00
2021-12-17 18:06:25,639 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair CLV/USDT, data starts at 2021-07-29 06:00:00
2021-12-17 18:06:25,959 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair CVP/USDT, data starts at 2021-10-04 10:00:00
2021-12-17 18:06:25,978 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair DAR/USDT, data starts at 2021-11-04 08:00:00
2021-12-17 18:06:26,108 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair DEGO/USDT, data starts at 2021-03-10 11:00:00
2021-12-17 18:06:26,229 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair DEXE/USDT, data starts at 2021-07-23 10:00:00
2021-12-17 18:06:26,249 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair DF/USDT, data starts at 2021-09-24 10:00:00
2021-12-17 18:06:26,408 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair DODO/USDT, data starts at 2021-02-19 10:00:00
2021-12-17 18:06:26,598 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair DYDX/USDT, data starts at 2021-09-09 02:00:00
2021-12-17 18:06:26,650 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair ELF/USDT, data starts at 2021-09-08 08:00:00
2021-12-17 18:06:26,707 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair ENS/USDT, data starts at 2021-11-10 07:00:00
2021-12-17 18:06:26,770 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair EPS/USDT, data starts at 2021-04-02 09:00:00
2021-12-17 18:06:26,794 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair ERN/USDT, data starts at 2021-06-22 06:00:00
2021-12-17 18:06:26,948 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair FARM/USDT, data starts at 2021-08-11 08:00:00
2021-12-17 18:06:27,008 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair FIDA/USDT, data starts at 2021-09-30 12:00:00
2021-12-17 18:06:27,095 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair FIRO/USDT, data starts at 2021-01-29 02:00:00
2021-12-17 18:06:27,123 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair FIS/USDT, data starts at 2021-03-03 08:00:00
2021-12-17 18:06:27,176 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair FLOW/USDT, data starts at 2021-07-30 13:00:00
2021-12-17 18:06:27,200 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair FORTH/USDT, data starts at 2021-04-23 09:00:00
2021-12-17 18:06:27,221 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair FRONT/USDT, data starts at 2021-10-04 10:00:00
2021-12-17 18:06:27,377 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair GALA/USDT, data starts at 2021-09-13 06:00:00
2021-12-17 18:06:27,398 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair GHST/USDT, data starts at 2021-08-20 10:00:00
2021-12-17 18:06:27,419 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair GNO/USDT, data starts at 2021-08-30 06:00:00
2021-12-17 18:06:27,471 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair GTC/USDT, data starts at 2021-06-10 10:00:00
2021-12-17 18:06:27,759 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair ICP/USDT, data starts at 2021-05-11 01:00:00
2021-12-17 18:06:27,819 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair IDEX/USDT, data starts at 2021-09-09 08:00:00
2021-12-17 18:06:27,839 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair ILV/USDT, data starts at 2021-09-22 06:00:00
2021-12-17 18:06:28,094 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair JASMY/USDT, data starts at 2021-11-22 12:00:00
2021-12-17 18:06:28,188 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair KEEP/USDT, data starts at 2021-06-17 06:00:00
2021-12-17 18:06:28,250 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair KLAY/USDT, data starts at 2021-06-24 08:00:00
2021-12-17 18:06:28,391 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair KP3R/USDT, data starts at 2021-11-12 10:00:00
2021-12-17 18:06:28,443 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair LAZIO/USDT, data starts at 2021-10-21 12:00:00
2021-12-17 18:06:28,469 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair LINA/USDT, data starts at 2021-03-18 12:00:00
2021-12-17 18:06:28,535 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair LIT/USDT, data starts at 2021-02-04 06:00:00
2021-12-17 18:06:28,560 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair LPT/USDT, data starts at 2021-05-28 05:00:00
2021-12-17 18:06:28,850 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair MASK/USDT, data starts at 2021-05-25 06:00:00
2021-12-17 18:06:29,005 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair MBOX/USDT, data starts at 2021-08-19 08:00:00
2021-12-17 18:06:29,064 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair MDX/USDT, data starts at 2021-05-24 09:00:00
2021-12-17 18:06:29,125 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair MINA/USDT, data starts at 2021-08-10 06:00:00
2021-12-17 18:06:29,150 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair MIR/USDT, data starts at 2021-04-19 11:00:00
2021-12-17 18:06:29,244 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair MLN/USDT, data starts at 2021-07-05 06:00:00
2021-12-17 18:06:29,263 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair MOVR/USDT, data starts at 2021-11-08 06:00:00
2021-12-17 18:06:29,557 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair NU/USDT, data starts at 2021-06-04 05:00:00
2021-12-17 18:06:29,749 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair OM/USDT, data starts at 2021-03-08 09:00:00
2021-12-17 18:06:30,114 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair PERP/USDT, data starts at 2021-03-19 08:00:00
2021-12-17 18:06:30,138 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair PHA/USDT, data starts at 2021-06-25 10:00:00
2021-12-17 18:06:30,157 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair PLA/USDT, data starts at 2021-11-23 06:00:00
2021-12-17 18:06:30,215 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair POLS/USDT, data starts at 2021-05-19 07:00:00
2021-12-17 18:06:30,237 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair POLY/USDT, data starts at 2021-09-09 08:00:00
2021-12-17 18:06:30,323 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair POND/USDT, data starts at 2021-03-09 08:00:00
2021-12-17 18:06:30,343 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair PORTO/USDT, data starts at 2021-11-16 12:00:00
2021-12-17 18:06:30,361 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair POWR/USDT, data starts at 2021-11-17 06:00:00
2021-12-17 18:06:30,386 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair PUNDIX/USDT, data starts at 2021-04-09 04:00:00
2021-12-17 18:06:30,406 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair PYR/USDT, data starts at 2021-11-26 08:00:00
2021-12-17 18:06:30,425 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair QI/USDT, data starts at 2021-11-15 08:00:00
2021-12-17 18:06:30,447 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair QNT/USDT, data starts at 2021-07-29 06:00:00
2021-12-17 18:06:30,507 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair QUICK/USDT, data starts at 2021-08-13 12:00:00
2021-12-17 18:06:30,528 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair RAD/USDT, data starts at 2021-10-07 07:00:00
2021-12-17 18:06:30,554 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair RAMP/USDT, data starts at 2021-03-22 09:00:00
2021-12-17 18:06:30,575 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair RARE/USDT, data starts at 2021-10-11 06:00:00
2021-12-17 18:06:30,597 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair RAY/USDT, data starts at 2021-08-10 06:00:00
2021-12-17 18:06:30,721 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair REQ/USDT, data starts at 2021-08-20 10:00:00
2021-12-17 18:06:30,741 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair RGT/USDT, data starts at 2021-11-05 06:00:00
2021-12-17 18:06:30,769 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair RIF/USDT, data starts at 2021-01-07 13:00:00
2021-12-17 18:06:30,886 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair RNDR/USDT, data starts at 2021-11-27 10:00:00
2021-12-17 18:06:31,109 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair SFP/USDT, data starts at 2021-02-08 13:00:00
2021-12-17 18:06:31,562 - freqtrade.data.converter - INFO - Missing data fillup for SUN/USDT: before: 8206 - after: 8315 - 1.33%
2021-12-17 18:06:31,579 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair SUPER/USDT, data starts at 2021-03-25 10:00:00
2021-12-17 18:06:31,696 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair SYS/USDT, data starts at 2021-09-24 10:00:00
2021-12-17 18:06:31,894 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair TKO/USDT, data starts at 2021-04-07 13:00:00
2021-12-17 18:06:31,920 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair TLM/USDT, data starts at 2021-04-13 06:00:00
2021-12-17 18:06:31,982 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair TORN/USDT, data starts at 2021-06-11 06:00:00
2021-12-17 18:06:32,035 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair TRIBE/USDT, data starts at 2021-08-24 06:00:00
2021-12-17 18:06:32,103 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair TRU/USDT, data starts at 2021-01-19 07:00:00
2021-12-17 18:06:32,226 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair TVK/USDT, data starts at 2021-08-06 10:00:00
2021-12-17 18:06:32,255 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair TWT/USDT, data starts at 2021-01-27 08:00:00
2021-12-17 18:06:32,369 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair USDP/USDT, data starts at 2021-09-10 04:00:00
2021-12-17 18:06:32,458 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair VGX/USDT, data starts at 2021-11-22 07:00:00
2021-12-17 18:06:32,478 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair VIDT/USDT, data starts at 2021-09-09 08:00:00
2021-12-17 18:06:32,708 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair WAXP/USDT, data starts at 2021-08-23 06:00:00
2021-12-17 18:06:32,964 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair XEC/USDT, data starts at 2021-09-03 10:00:00
2021-12-17 18:06:33,231 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair XVG/USDT, data starts at 2021-06-06 10:00:00
2021-12-17 18:06:33,316 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair YGG/USDT, data starts at 2021-09-24 06:00:00
2021-12-17 18:06:33,527 - freqtrade.optimize.backtesting - INFO - Loading data from 2020-12-31 05:00:00 up to 2021-12-12 15:00:00 (346 days).
2021-12-17 18:06:33,528 - freqtrade.optimize.backtesting - INFO - Dataload complete. Calculating indicators
2021-12-17 18:06:33,528 - freqtrade.optimize.backtesting - INFO - Running backtesting for Strategy TrixV15Strategy
2021-12-17 18:06:35,733 - freqtrade.optimize.backtesting - INFO - Backtesting with data from 2021-01-01 00:00:00 up to 2021-12-12 15:00:00 (345 days).
2021-12-17 18:06:58,386 - freqtrade.misc - INFO - dumping json to "/freqtrade/user_data/backtest_results/backtest-result-2021-12-17_18-06-58.json"
2021-12-17 18:06:58,487 - freqtrade.misc - INFO - dumping json to "/freqtrade/user_data/backtest_results/.last_result.json"
Result for strategy TrixV15Strategy
============================================================= BACKTESTING REPORT =============================================================
|         Pair |   Buys |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |      Avg Duration |   Win  Draw  Loss  Win% |
|--------------+--------+----------------+----------------+-------------------+----------------+-------------------+-------------------------|
|     OXT/USDT |     40 |           4.95 |         198.10 |           198.301 |          19.83 |          21:28:00 |    33     7     0   100 |
|     KEY/USDT |     26 |           5.35 |         139.08 |           139.222 |          13.92 |    1 day, 4:05:00 |    16     9     1  61.5 |
|   THETA/USDT |     25 |           5.50 |         137.40 |           137.536 |          13.75 |   1 day, 16:31:00 |    20     5     0   100 |
|     ENJ/USDT |     27 |           5.07 |         136.81 |           136.943 |          13.69 |    1 day, 7:49:00 |    15    12     0   100 |
|     GTO/USDT |     35 |           3.86 |         135.07 |           135.207 |          13.52 |   1 day, 14:51:00 |    24    11     0   100 |
|     FET/USDT |     30 |           4.28 |         128.53 |           128.661 |          12.87 |          22:06:00 |    21     9     0   100 |
|    POND/USDT |     37 |           3.27 |         121.03 |           121.152 |          12.12 |    1 day, 2:18:00 |    28     8     1  75.7 |
|     PNT/USDT |     31 |           3.89 |         120.73 |           120.854 |          12.09 |   1 day, 10:12:00 |    19    10     2  61.3 |
|    BEAM/USDT |     45 |           2.60 |         116.85 |           116.965 |          11.70 |    1 day, 8:13:00 |    30    15     0   100 |
|    VTHO/USDT |     25 |           4.54 |         113.52 |           113.629 |          11.36 |   1 day, 12:53:00 |    20     5     0   100 |
|     CHR/USDT |     34 |           3.29 |         111.77 |           111.886 |          11.19 |   1 day, 15:05:00 |    20    12     2  58.8 |
|     SUN/USDT |     41 |           2.69 |         110.11 |           110.221 |          11.02 |          18:03:00 |    31     9     1  75.6 |
|     MDT/USDT |     42 |           2.55 |         107.20 |           107.309 |          10.73 |   1 day, 11:27:00 |    26    14     2  61.9 |
|    IOTX/USDT |     33 |           3.19 |         105.12 |           105.229 |          10.52 |   1 day, 17:22:00 |    22     8     3  66.7 |
|    NEAR/USDT |     23 |           4.53 |         104.19 |           104.294 |          10.43 |          22:55:00 |    17     6     0   100 |
|    HARD/USDT |     33 |           3.06 |         100.88 |           100.977 |          10.10 |   1 day, 12:27:00 |    20    12     1  60.6 |
|    DOCK/USDT |     40 |           2.48 |          99.32 |            99.420 |           9.94 |    1 day, 4:06:00 |    29    10     1  72.5 |
|     SKL/USDT |     38 |           2.52 |          95.61 |            95.703 |           9.57 |    1 day, 0:27:00 |    25    11     2  65.8 |
|    RAMP/USDT |     27 |           3.50 |          94.49 |            94.581 |           9.46 |   1 day, 16:07:00 |    16    11     0   100 |
|     DNT/USDT |     46 |           2.01 |          92.60 |            92.696 |           9.27 |    1 day, 9:31:00 |    32    11     3  69.6 |
|    DATA/USDT |     38 |           2.42 |          91.86 |            91.955 |           9.20 |   1 day, 22:22:00 |    23    13     2  60.5 |
|     ETC/USDT |     30 |           3.02 |          90.58 |            90.672 |           9.07 |    1 day, 1:16:00 |    20     8     2  66.7 |
|     OGN/USDT |     32 |           2.80 |          89.59 |            89.682 |           8.97 |    1 day, 2:11:00 |    23     8     1  71.9 |
|    QTUM/USDT |     26 |           3.40 |          88.27 |            88.361 |           8.84 |          20:44:00 |    19     7     0   100 |
|     TCT/USDT |     35 |           2.48 |          86.70 |            86.791 |           8.68 |   1 day, 14:10:00 |    23    11     1  65.7 |
|     FIS/USDT |     37 |           2.31 |          85.49 |            85.573 |           8.56 |    1 day, 3:34:00 |    25    11     1  67.6 |
|     REQ/USDT |     12 |           6.91 |          82.87 |            82.955 |           8.30 |  2 days, 11:00:00 |     6     6     0   100 |
|     AXS/USDT |     31 |           2.66 |          82.61 |            82.695 |           8.27 |   1 day, 13:19:00 |    20    10     1  64.5 |
|    CELO/USDT |     32 |           2.58 |          82.44 |            82.524 |           8.25 |    1 day, 5:54:00 |    21    10     1  65.6 |
|     NKN/USDT |     30 |           2.74 |          82.22 |            82.299 |           8.23 |   1 day, 16:52:00 |    19     9     2  63.3 |
|   ALPHA/USDT |     25 |           3.28 |          82.12 |            82.197 |           8.22 |   1 day, 14:38:00 |    17     8     0   100 |
|     KMD/USDT |     25 |           3.25 |          81.25 |            81.327 |           8.13 |    1 day, 8:36:00 |    17     7     1  68.0 |
|     WRX/USDT |     25 |           3.22 |          80.54 |            80.621 |           8.06 |   2 days, 4:38:00 |    14     9     2  56.0 |
|    CELR/USDT |     31 |           2.59 |          80.23 |            80.311 |           8.03 |   1 day, 12:41:00 |    21     9     1  67.7 |
|     COS/USDT |     29 |           2.71 |          78.58 |            78.660 |           7.87 |    1 day, 1:35:00 |    22     7     0   100 |
|     NBS/USDT |     34 |           2.30 |          78.25 |            78.332 |           7.83 |    1 day, 3:55:00 |    20    12     2  58.8 |
|     TRU/USDT |     37 |           2.09 |          77.50 |            77.578 |           7.76 |   2 days, 3:10:00 |    20    14     3  54.1 |
|     LTO/USDT |     26 |           2.96 |          76.93 |            77.010 |           7.70 |   1 day, 21:00:00 |    15    11     0   100 |
|   STRAX/USDT |     27 |           2.83 |          76.46 |            76.532 |           7.65 |    1 day, 9:27:00 |    19     7     1  70.4 |
|    AION/USDT |     27 |           2.76 |          74.42 |            74.491 |           7.45 |    1 day, 0:02:00 |    21     6     0   100 |
|    MITH/USDT |     27 |           2.74 |          73.92 |            73.995 |           7.40 |    1 day, 9:04:00 |    16    10     1  59.3 |
|     WTC/USDT |     31 |           2.37 |          73.34 |            73.410 |           7.34 |    1 day, 0:41:00 |    24     5     2  77.4 |
|   AUDIO/USDT |     28 |           2.60 |          72.81 |            72.879 |           7.29 |    1 day, 2:32:00 |    20     7     1  71.4 |
|    TOMO/USDT |     28 |           2.56 |          71.64 |            71.708 |           7.17 |    1 day, 2:39:00 |    22     6     0   100 |
|     DIA/USDT |     45 |           1.58 |          71.27 |            71.337 |           7.13 |    1 day, 9:40:00 |    31    12     2  68.9 |
|     GXS/USDT |     37 |           1.92 |          71.17 |            71.237 |           7.12 |   1 day, 17:08:00 |    25    10     2  67.6 |
|      OM/USDT |     32 |           2.20 |          70.42 |            70.488 |           7.05 |    1 day, 9:19:00 |    17    15     0   100 |
|   1INCH/USDT |     29 |           2.42 |          70.13 |            70.204 |           7.02 |          23:35:00 |    19     9     1  65.5 |
|      NU/USDT |     20 |           3.41 |          68.19 |            68.260 |           6.83 |    1 day, 8:54:00 |    10    10     0   100 |
|     MTL/USDT |     37 |           1.79 |          66.19 |            66.256 |           6.63 |    1 day, 4:28:00 |    25    11     1  67.6 |
|     FIO/USDT |     40 |           1.65 |          65.98 |            66.045 |           6.60 |    1 day, 8:56:00 |    25    13     2  62.5 |
|    STPT/USDT |     37 |           1.74 |          64.52 |            64.587 |           6.46 |   1 day, 17:54:00 |    19    17     1  51.4 |
|    FIRO/USDT |     21 |           3.07 |          64.45 |            64.513 |           6.45 |    1 day, 3:06:00 |    15     6     0   100 |
|     INJ/USDT |     27 |           2.35 |          63.37 |            63.438 |           6.34 |    1 day, 1:53:00 |    18     8     1  66.7 |
|    NULS/USDT |     39 |           1.57 |          61.22 |            61.280 |           6.13 |    1 day, 5:29:00 |    25    13     1  64.1 |
|   ALICE/USDT |     22 |           2.74 |          60.36 |            60.424 |           6.04 |    1 day, 6:27:00 |    15     6     1  68.2 |
|    WNXM/USDT |     23 |           2.55 |          58.58 |            58.641 |           5.86 |          22:39:00 |    15     8     0   100 |
|    PERP/USDT |     18 |           3.21 |          57.71 |            57.771 |           5.78 |   2 days, 3:50:00 |    10     8     0   100 |
|    COTI/USDT |     21 |           2.68 |          56.38 |            56.441 |           5.64 |          19:49:00 |    15     6     0   100 |
|  BURGER/USDT |     21 |           2.62 |          55.04 |            55.099 |           5.51 |   1 day, 17:57:00 |    16     5     0   100 |
|    CTSI/USDT |     35 |           1.56 |          54.60 |            54.651 |           5.47 |    1 day, 2:48:00 |    24     8     3  68.6 |
|     BAL/USDT |     24 |           2.23 |          53.45 |            53.506 |           5.35 |          20:10:00 |    18     6     0   100 |
|    GALA/USDT |      7 |           7.55 |          52.83 |            52.878 |           5.29 |    1 day, 0:26:00 |     4     3     0   100 |
|     TRB/USDT |     26 |           1.97 |          51.25 |            51.302 |           5.13 |          18:02:00 |    22     3     1  84.6 |
|    KEEP/USDT |     18 |           2.84 |          51.11 |            51.158 |           5.12 |    1 day, 0:20:00 |    10     8     0   100 |
|     BTT/USDT |     32 |           1.57 |          50.09 |            50.135 |           5.01 |   1 day, 16:39:00 |    21     8     3  65.6 |
|     ICX/USDT |     23 |           2.16 |          49.67 |            49.722 |           4.97 |    1 day, 6:16:00 |    17     5     1  73.9 |
|     ONE/USDT |     21 |           2.34 |          49.08 |            49.134 |           4.91 |          22:54:00 |    14     6     1  66.7 |
|    ROSE/USDT |     32 |           1.51 |          48.37 |            48.423 |           4.84 |   1 day, 21:52:00 |    21     8     3  65.6 |
|     WAN/USDT |     18 |           2.68 |          48.27 |            48.320 |           4.83 |    1 day, 3:43:00 |    14     4     0   100 |
|     ZEC/USDT |     20 |           2.40 |          48.09 |            48.135 |           4.81 |    1 day, 7:09:00 |    16     4     0   100 |
|    VITE/USDT |     27 |           1.76 |          47.43 |            47.476 |           4.75 |    1 day, 8:02:00 |    17     8     2  63.0 |
|     BAT/USDT |     20 |           2.37 |          47.42 |            47.466 |           4.75 |    1 day, 2:00:00 |    15     4     1  75.0 |
|    ALGO/USDT |     22 |           2.15 |          47.24 |            47.284 |           4.73 |   1 day, 18:46:00 |    14     7     1  63.6 |
|    DENT/USDT |     16 |           2.94 |          47.01 |            47.057 |           4.71 |   2 days, 2:22:00 |    11     4     1  68.8 |
|     KNC/USDT |     28 |           1.65 |          46.33 |            46.376 |           4.64 |    1 day, 9:15:00 |    19     8     1  67.9 |
|    YFII/USDT |     19 |           2.44 |          46.31 |            46.354 |           4.64 |    1 day, 1:06:00 |    13     6     0   100 |
|   MATIC/USDT |     14 |           3.29 |          45.99 |            46.038 |           4.60 |          14:04:00 |    13     1     0   100 |
|     TRX/USDT |     23 |           1.93 |          44.39 |            44.439 |           4.44 |    1 day, 5:21:00 |    19     3     1  82.6 |
|    MASK/USDT |     21 |           2.11 |          44.21 |            44.252 |           4.43 |  2 days, 13:26:00 |    13     6     2  61.9 |
|    ANKR/USDT |     30 |           1.47 |          44.19 |            44.237 |           4.42 |    1 day, 9:24:00 |    19    10     1  63.3 |
|    NANO/USDT |     29 |           1.49 |          43.33 |            43.377 |           4.34 |    1 day, 5:29:00 |    19     8     2  65.5 |
|     RVN/USDT |     31 |           1.40 |          43.30 |            43.342 |           4.33 |   2 days, 8:33:00 |    20     8     3  64.5 |
|      SC/USDT |     21 |           1.99 |          41.73 |            41.774 |           4.18 |   1 day, 21:54:00 |    17     3     1  81.0 |
|     TKO/USDT |     22 |           1.82 |          40.08 |            40.123 |           4.01 |   1 day, 21:16:00 |    13     9     0   100 |
|     MKR/USDT |     22 |           1.81 |          39.85 |            39.887 |           3.99 |  2 days, 11:19:00 |    12    10     0   100 |
|    IDEX/USDT |     13 |           3.05 |          39.66 |            39.701 |           3.97 |          15:55:00 |     7     5     1  53.8 |
|     ATA/USDT |     17 |           2.31 |          39.29 |            39.330 |           3.93 |    1 day, 6:07:00 |    12     4     1  70.6 |
|     MIR/USDT |     14 |           2.80 |          39.23 |            39.271 |           3.93 |          20:47:00 |    11     3     0   100 |
|     EPS/USDT |     21 |           1.86 |          39.05 |            39.092 |           3.91 |   1 day, 11:03:00 |    16     3     2  76.2 |
|    STMX/USDT |     23 |           1.69 |          38.88 |            38.923 |           3.89 |    1 day, 1:10:00 |    16     5     2  69.6 |
|     STX/USDT |     28 |           1.33 |          37.10 |            37.142 |           3.71 |  2 days, 12:28:00 |    17     8     3  60.7 |
|    UNFI/USDT |     27 |           1.36 |          36.82 |            36.852 |           3.69 |   1 day, 17:29:00 |    17     8     2  63.0 |
|     ORN/USDT |     15 |           2.44 |          36.65 |            36.688 |           3.67 |    1 day, 4:08:00 |    10     5     0   100 |
|    DEXE/USDT |     23 |           1.59 |          36.58 |            36.614 |           3.66 |    1 day, 4:05:00 |    13     9     1  56.5 |
|    DUSK/USDT |     28 |           1.31 |          36.57 |            36.606 |           3.66 |   1 day, 19:58:00 |    18     9     1  64.3 |
|   TFUEL/USDT |     32 |           1.13 |          36.09 |            36.131 |           3.61 |  3 days, 13:04:00 |    22     7     3  68.8 |
|    PERL/USDT |     42 |           0.86 |          36.05 |            36.086 |           3.61 |   1 day, 15:01:00 |    26    14     2  61.9 |
|     RAD/USDT |      8 |           4.21 |          33.72 |            33.750 |           3.38 |          16:22:00 |     8     0     0   100 |
|  BADGER/USDT |     18 |           1.86 |          33.49 |            33.519 |           3.35 |    1 day, 7:10:00 |    10     7     1  55.6 |
|     LPT/USDT |     24 |           1.37 |          32.88 |            32.911 |           3.29 |   2 days, 5:10:00 |    14     9     1  58.3 |
|     LIT/USDT |     19 |           1.68 |          31.91 |            31.944 |           3.19 |   2 days, 2:38:00 |    13     5     1  68.4 |
|     ZRX/USDT |     24 |           1.32 |          31.80 |            31.828 |           3.18 |  2 days, 12:05:00 |    15     8     1  62.5 |
|    TORN/USDT |     14 |           2.26 |          31.64 |            31.669 |           3.17 |    1 day, 9:30:00 |    10     4     0   100 |
|     RAY/USDT |      8 |           3.92 |          31.34 |            31.376 |           3.14 |  4 days, 19:52:00 |     6     1     1  75.0 |
|    AVAX/USDT |     18 |           1.70 |          30.65 |            30.681 |           3.07 |          20:47:00 |    13     4     1  72.2 |
|    BOND/USDT |     22 |           1.32 |          29.09 |            29.115 |           2.91 |  2 days, 20:33:00 |     9    11     2  40.9 |
|    IRIS/USDT |     31 |           0.93 |          28.74 |            28.774 |           2.88 |    1 day, 6:41:00 |    21     8     2  67.7 |
|     BCH/USDT |     21 |           1.36 |          28.61 |            28.639 |           2.86 |   4 days, 9:49:00 |    12     8     1  57.1 |
|     RIF/USDT |     38 |           0.74 |          28.16 |            28.186 |           2.82 |   1 day, 12:43:00 |    22    14     2  57.9 |
|     UMA/USDT |     29 |           0.96 |          27.82 |            27.848 |           2.78 |  2 days, 18:35:00 |    17    11     1  58.6 |
|     CVC/USDT |     27 |           0.99 |          26.80 |            26.831 |           2.68 |   2 days, 2:29:00 |    22     3     2  81.5 |
|     CKB/USDT |     29 |           0.92 |          26.75 |            26.774 |           2.68 |   1 day, 10:02:00 |    22     5     2  75.9 |
|     GTC/USDT |     12 |           2.16 |          25.92 |            25.950 |           2.59 |   1 day, 17:50:00 |     9     1     2  75.0 |
|    POLS/USDT |     24 |           1.07 |          25.66 |            25.682 |           2.57 |    1 day, 7:58:00 |    14     9     1  58.3 |
|     REN/USDT |     23 |           1.10 |          25.20 |            25.226 |           2.52 |    1 day, 6:55:00 |    15     7     1  65.2 |
|     HNT/USDT |     27 |           0.93 |          25.18 |            25.203 |           2.52 |   2 days, 2:38:00 |    18     7     2  66.7 |
|     XVG/USDT |      9 |           2.74 |          24.65 |            24.670 |           2.47 |          17:53:00 |     8     1     0   100 |
|   SUPER/USDT |     23 |           1.04 |          23.99 |            24.015 |           2.40 |    1 day, 5:44:00 |    15     6     2  65.2 |
|     XLM/USDT |     27 |           0.88 |          23.83 |            23.853 |           2.39 |  2 days, 20:58:00 |    19     6     2  70.4 |
|     RSR/USDT |     17 |           1.39 |          23.59 |            23.617 |           2.36 |    1 day, 5:25:00 |    12     4     1  70.6 |
|     CRV/USDT |     37 |           0.64 |          23.51 |            23.535 |           2.35 |    1 day, 6:41:00 |    27     7     3  73.0 |
|   FRONT/USDT |      9 |           2.57 |          23.11 |            23.128 |           2.31 |   1 day, 13:27:00 |     6     3     0   100 |
|   FORTH/USDT |     24 |           0.95 |          22.68 |            22.704 |           2.27 |   2 days, 6:10:00 |    10    12     2  41.7 |
|     DAR/USDT |      5 |           4.45 |          22.23 |            22.253 |           2.23 |          12:36:00 |     4     0     1  80.0 |
|    TROY/USDT |     32 |           0.68 |          21.76 |            21.782 |           2.18 |    1 day, 4:21:00 |    19    11     2  59.4 |
|     PHA/USDT |     19 |           1.13 |          21.40 |            21.426 |           2.14 |    1 day, 9:19:00 |    12     6     1  63.2 |
|    LUNA/USDT |     20 |           1.06 |          21.10 |            21.122 |           2.11 |  2 days, 20:27:00 |    12     7     1  60.0 |
|     MBL/USDT |     34 |           0.61 |          20.77 |            20.792 |           2.08 |          18:32:00 |    25     7     2  73.5 |
|     ANT/USDT |     33 |           0.61 |          20.22 |            20.236 |           2.02 |    1 day, 8:07:00 |    19    11     3  57.6 |
|     NEO/USDT |     17 |           1.17 |          19.85 |            19.874 |           1.99 |   1 day, 13:42:00 |    11     5     1  64.7 |
|    WING/USDT |     37 |           0.53 |          19.69 |            19.708 |           1.97 |   1 day, 11:18:00 |    24    10     3  64.9 |
|     VET/USDT |     14 |           1.40 |          19.62 |            19.639 |           1.96 |   1 day, 15:00:00 |    11     2     1  78.6 |
|    RUNE/USDT |     20 |           0.97 |          19.33 |            19.352 |           1.94 |          20:15:00 |    14     4     2  70.0 |
|     MLN/USDT |     11 |           1.71 |          18.77 |            18.791 |           1.88 |  4 days, 10:33:00 |     7     4     0   100 |
|      DF/USDT |      7 |           2.68 |          18.74 |            18.761 |           1.88 |    1 day, 7:00:00 |     5     2     0   100 |
|  ALPACA/USDT |     12 |           1.50 |          18.04 |            18.062 |           1.81 |   3 days, 2:10:00 |     6     6     0   100 |
|     ELF/USDT |     11 |           1.63 |          17.94 |            17.961 |           1.80 |  2 days, 17:05:00 |     4     7     0   100 |
|     TLM/USDT |     19 |           0.94 |          17.85 |            17.868 |           1.79 |    1 day, 0:47:00 |    13     4     2  68.4 |
|   BTCST/USDT |     30 |           0.57 |          17.24 |            17.261 |           1.73 |   1 day, 11:28:00 |    17    12     1  56.7 |
|    BZRX/USDT |     30 |           0.52 |          15.46 |            15.475 |           1.55 |    1 day, 5:44:00 |    20     6     4  66.7 |
|     WIN/USDT |     22 |           0.70 |          15.29 |            15.310 |           1.53 |   1 day, 15:46:00 |    16     4     2  72.7 |
|     XMR/USDT |     21 |           0.71 |          14.84 |            14.851 |           1.49 |   1 day, 16:31:00 |    14     6     1  66.7 |
|     XTZ/USDT |     25 |           0.57 |          14.36 |            14.372 |           1.44 |    1 day, 0:02:00 |    14    10     1  56.0 |
|     ZEN/USDT |     32 |           0.45 |          14.30 |            14.318 |           1.43 |    1 day, 7:19:00 |    24     6     2  75.0 |
|     BNB/USDT |     14 |           0.98 |          13.68 |            13.690 |           1.37 |   3 days, 0:04:00 |     7     6     1  50.0 |
|    VIDT/USDT |      9 |           1.50 |          13.54 |            13.551 |           1.36 |    1 day, 7:53:00 |     6     3     0   100 |
|    FARM/USDT |     17 |           0.75 |          12.83 |            12.846 |           1.28 |   1 day, 21:14:00 |     6    11     0   100 |
|     JST/USDT |     24 |           0.49 |          11.86 |            11.869 |           1.19 |   2 days, 9:35:00 |    17     4     3  70.8 |
|    DODO/USDT |     23 |           0.51 |          11.82 |            11.832 |           1.18 |   1 day, 12:05:00 |    17     5     1  73.9 |
|    GHST/USDT |     18 |           0.65 |          11.64 |            11.647 |           1.16 |    1 day, 7:37:00 |    14     3     1  77.8 |
|    IOST/USDT |     23 |           0.50 |          11.42 |            11.428 |           1.14 |    1 day, 8:52:00 |    14     8     1  60.9 |
|     BNT/USDT |     17 |           0.65 |          11.10 |            11.113 |           1.11 |   1 day, 15:18:00 |    10     7     0   100 |
|    MBOX/USDT |     15 |           0.73 |          11.00 |            11.012 |           1.10 |    1 day, 3:36:00 |     9     5     1  60.0 |
|    HIVE/USDT |     41 |           0.25 |          10.40 |            10.412 |           1.04 |    1 day, 8:53:00 |    20    16     5  48.8 |
|     SRM/USDT |     26 |           0.37 |           9.53 |             9.537 |           0.95 |   1 day, 20:23:00 |    17     7     2  65.4 |
| AUCTION/USDT |      7 |           1.33 |           9.29 |             9.297 |           0.93 |    1 day, 5:43:00 |     4     3     0   100 |
|    IOTA/USDT |     24 |           0.37 |           8.83 |             8.834 |           0.88 |   1 day, 12:18:00 |    16     7     1  66.7 |
|     CFX/USDT |     23 |           0.37 |           8.47 |             8.476 |           0.85 |   2 days, 8:47:00 |    11    11     1  47.8 |
|     GNO/USDT |      7 |           1.20 |           8.43 |             8.437 |           0.84 |  5 days, 11:00:00 |     4     3     0   100 |
|   TRIBE/USDT |     14 |           0.58 |           8.06 |             8.068 |           0.81 |   3 days, 8:43:00 |     5     9     0   100 |
|   STORJ/USDT |     25 |           0.30 |           7.59 |             7.599 |           0.76 |   1 day, 14:53:00 |    16     7     2  64.0 |
|     ZIL/USDT |     14 |           0.49 |           6.80 |             6.807 |           0.68 |    1 day, 4:34:00 |    10     3     1  71.4 |
|     BNX/USDT |      3 |           2.26 |           6.78 |             6.786 |           0.68 |          14:00:00 |     3     0     0   100 |
|     QNT/USDT |     12 |           0.53 |           6.31 |             6.320 |           0.63 |  2 days, 21:50:00 |     6     5     1  50.0 |
|     AMP/USDT |      2 |           3.10 |           6.21 |             6.214 |           0.62 |           8:00:00 |     2     0     0   100 |
|     XEM/USDT |     18 |           0.34 |           6.18 |             6.188 |           0.62 |   3 days, 3:27:00 |    11     6     1  61.1 |
|     PLA/USDT |      3 |           1.97 |           5.90 |             5.906 |           0.59 |    1 day, 2:00:00 |     2     1     0   100 |
|    ARDR/USDT |     33 |           0.17 |           5.72 |             5.728 |           0.57 |   1 day, 19:07:00 |    28     2     3  84.8 |
|    AGLD/USDT |      8 |           0.60 |           4.82 |             4.821 |           0.48 |   1 day, 11:45:00 |     4     4     0   100 |
|    DOGE/USDT |     29 |           0.15 |           4.42 |             4.427 |           0.44 |   1 day, 12:14:00 |    21     6     2  72.4 |
|     VGX/USDT |      5 |           0.74 |           3.70 |             3.706 |           0.37 |    1 day, 9:24:00 |     4     0     1  80.0 |
|  PUNDIX/USDT |     25 |           0.12 |           3.09 |             3.091 |           0.31 |    1 day, 9:22:00 |    18     5     2  72.0 |
|    MANA/USDT |     28 |           0.10 |           2.88 |             2.887 |           0.29 |   1 day, 19:34:00 |    20     6     2  71.4 |
|     SNX/USDT |     16 |           0.17 |           2.78 |             2.783 |           0.28 |          20:00:00 |    13     2     1  81.2 |
|    SUSD/USDT |     30 |           0.09 |           2.61 |             2.609 |           0.26 |  5 days, 23:20:00 |    13    17     0   100 |
|     ILV/USDT |      5 |           0.47 |           2.37 |             2.376 |           0.24 |          22:00:00 |     4     1     0   100 |
|    PAXG/USDT |     12 |           0.19 |           2.29 |             2.292 |           0.23 | 21 days, 10:10:00 |     4     7     1  33.3 |
|     ENS/USDT |      2 |           1.09 |           2.19 |             2.188 |           0.22 |    1 day, 0:00:00 |     1     1     0   100 |
|    WAXP/USDT |      6 |           0.22 |           1.31 |             1.307 |           0.13 |  2 days, 20:00:00 |     4     1     1  66.7 |
|     ADX/USDT |      6 |           0.13 |           0.79 |             0.786 |           0.08 |    1 day, 4:10:00 |     4     1     1  66.7 |
|     TVK/USDT |     12 |           0.06 |           0.74 |             0.744 |           0.07 |   1 day, 22:15:00 |     9     2     1  75.0 |
|    POWR/USDT |      0 |           0.00 |           0.00 |             0.000 |           0.00 |              0:00 |     0     0     0     0 |
|     PYR/USDT |      0 |           0.00 |           0.00 |             0.000 |           0.00 |              0:00 |     0     0     0     0 |
|    RNDR/USDT |      1 |           0.00 |           0.00 |             0.000 |           0.00 |  3 days, 13:00:00 |     0     1     0     0 |
|    USDP/USDT |      7 |           0.00 |           0.00 |             0.000 |           0.00 | 11 days, 14:00:00 |     0     7     0     0 |
|   WAVES/USDT |     27 |          -0.00 |          -0.13 |            -0.126 |          -0.01 |   1 day, 18:49:00 |    15    10     2  55.6 |
|    POLY/USDT |      9 |          -0.03 |          -0.28 |            -0.283 |          -0.03 |   1 day, 19:40:00 |     5     2     2  55.6 |
|     LRC/USDT |     25 |          -0.02 |          -0.54 |            -0.537 |          -0.05 |  2 days, 13:53:00 |    13     9     3  52.0 |
|     HOT/USDT |     29 |          -0.02 |          -0.61 |            -0.614 |          -0.06 |   1 day, 23:27:00 |    20     6     3  69.0 |
|    REEF/USDT |     29 |          -0.04 |          -1.24 |            -1.244 |          -0.12 |    1 day, 9:54:00 |    18     9     2  62.1 |
|    ARPA/USDT |     34 |          -0.08 |          -2.59 |            -2.590 |          -0.26 |   1 day, 18:25:00 |    20    11     3  58.8 |
|     BTS/USDT |     26 |          -0.14 |          -3.74 |            -3.748 |          -0.37 |   3 days, 2:16:00 |    16     8     2  61.5 |
|     SYS/USDT |     10 |          -0.39 |          -3.89 |            -3.896 |          -0.39 |   2 days, 4:54:00 |     6     3     1  60.0 |
|     SOL/USDT |     21 |          -0.21 |          -4.46 |            -4.463 |          -0.45 |    1 day, 1:06:00 |    15     4     2  71.4 |
|     C98/USDT |     17 |          -0.27 |          -4.51 |            -4.517 |          -0.45 |    1 day, 4:49:00 |    13     3     1  76.5 |
|     ONT/USDT |     25 |          -0.18 |          -4.53 |            -4.532 |          -0.45 |   3 days, 5:36:00 |    16     7     2  64.0 |
|    AAVE/USDT |     16 |          -0.32 |          -5.08 |            -5.090 |          -0.51 |   4 days, 2:19:00 |    10     5     1  62.5 |
|     AVA/USDT |     27 |          -0.20 |          -5.46 |            -5.467 |          -0.55 |  2 days, 17:58:00 |    16     9     2  59.3 |
|    ATOM/USDT |     21 |          -0.27 |          -5.71 |            -5.712 |          -0.57 |   2 days, 4:17:00 |    10    10     1  47.6 |
|     XEC/USDT |     16 |          -0.38 |          -6.06 |            -6.066 |          -0.61 |   1 day, 16:15:00 |    12     3     1  75.0 |
|     LSK/USDT |     30 |          -0.22 |          -6.52 |            -6.528 |          -0.65 |    1 day, 4:10:00 |    22     5     3  73.3 |
|     CLV/USDT |     18 |          -0.38 |          -6.80 |            -6.809 |          -0.68 |  2 days, 20:53:00 |     7    10     1  38.9 |
|    AKRO/USDT |     31 |          -0.22 |          -6.91 |            -6.920 |          -0.69 |   1 day, 10:06:00 |    18    10     3  58.1 |
|     ETH/USDT |      9 |          -0.93 |          -8.38 |            -8.390 |          -0.84 |  2 days, 13:47:00 |     7     1     1  77.8 |
|     ADA/USDT |     17 |          -0.51 |          -8.62 |            -8.633 |          -0.86 |  2 days, 22:21:00 |    10     6     1  58.8 |
|    AUTO/USDT |     20 |          -0.45 |          -8.94 |            -8.945 |          -0.89 |  2 days, 16:48:00 |    12     6     2  60.0 |
|    FLOW/USDT |     16 |          -0.56 |          -9.02 |            -9.027 |          -0.90 |   2 days, 3:00:00 |    11     3     2  68.8 |
|     LTC/USDT |     33 |          -0.28 |          -9.24 |            -9.246 |          -0.92 |   1 day, 12:00:00 |    23     7     3  69.7 |
|    COMP/USDT |     13 |          -0.76 |          -9.84 |            -9.852 |          -0.99 |  5 days, 18:55:00 |     9     3     1  69.2 |
|     RGT/USDT |      6 |          -1.67 |         -10.04 |           -10.045 |          -1.00 |  2 days, 17:20:00 |     3     2     1  50.0 |
|     FTM/USDT |     26 |          -0.39 |         -10.23 |           -10.244 |          -1.02 |    1 day, 1:53:00 |    17     5     4  65.4 |
|     DCR/USDT |     18 |          -0.58 |         -10.38 |           -10.386 |          -1.04 |  4 days, 15:43:00 |    11     5     2  61.1 |
|     ERN/USDT |     15 |          -0.84 |         -12.59 |           -12.603 |          -1.26 |   1 day, 12:28:00 |     7     6     2  46.7 |
|    LINK/USDT |     20 |          -0.63 |         -12.67 |           -12.685 |          -1.27 |   2 days, 4:09:00 |     9    10     1  45.0 |
|     FUN/USDT |     23 |          -0.59 |         -13.65 |           -13.669 |          -1.37 |   3 days, 6:23:00 |    12     9     2  52.2 |
|    DASH/USDT |     24 |          -0.59 |         -14.08 |           -14.096 |          -1.41 |  3 days, 14:42:00 |    15     7     2  62.5 |
|    CAKE/USDT |     12 |          -1.23 |         -14.80 |           -14.815 |          -1.48 |  2 days, 19:35:00 |     7     4     1  58.3 |
|     MDX/USDT |     21 |          -0.74 |         -15.44 |           -15.457 |          -1.55 |   2 days, 3:06:00 |    13     6     2  61.9 |
|    MINA/USDT |     11 |          -1.55 |         -17.04 |           -17.055 |          -1.71 |  2 days, 23:44:00 |     4     5     2  36.4 |
|    KLAY/USDT |     10 |          -1.71 |         -17.14 |           -17.154 |          -1.72 |   6 days, 8:24:00 |     5     4     1  50.0 |
|   JASMY/USDT |      2 |          -9.13 |         -18.25 |           -18.273 |          -1.83 |  3 days, 16:00:00 |     1     0     1  50.0 |
|      QI/USDT |      3 |          -6.45 |         -19.35 |           -19.369 |          -1.94 |          22:20:00 |     2     0     1  66.7 |
|     UNI/USDT |     13 |          -1.54 |         -20.08 |           -20.098 |          -2.01 |    1 day, 3:14:00 |     6     6     1  46.2 |
|     YGG/USDT |      9 |          -2.27 |         -20.39 |           -20.407 |          -2.04 |    1 day, 8:13:00 |     3     4     2  33.3 |
|     TWT/USDT |     22 |          -1.02 |         -22.46 |           -22.481 |          -2.25 |    1 day, 7:44:00 |    15     4     3  68.2 |
|    BETA/USDT |      6 |          -3.83 |         -23.00 |           -23.021 |          -2.30 |   2 days, 3:30:00 |     2     3     1  33.3 |
|     RLC/USDT |     24 |          -0.97 |         -23.21 |           -23.238 |          -2.32 |  2 days, 17:40:00 |    12    10     2  50.0 |
|    BAND/USDT |     27 |          -0.88 |         -23.86 |           -23.881 |          -2.39 |   1 day, 16:36:00 |    17     7     3  63.0 |
|   SUSHI/USDT |     21 |          -1.14 |         -23.95 |           -23.970 |          -2.40 |  2 days, 11:31:00 |    13     6     2  61.9 |
|     YFI/USDT |     16 |          -1.52 |         -24.32 |           -24.346 |          -2.43 |   5 days, 2:49:00 |    10     4     2  62.5 |
|     REP/USDT |     32 |          -0.78 |         -24.94 |           -24.970 |          -2.50 |   1 day, 13:43:00 |    19     9     4  59.4 |
|    RARE/USDT |      4 |          -6.31 |         -25.24 |           -25.269 |          -2.53 |   6 days, 3:15:00 |     1     2     1  25.0 |
|    KP3R/USDT |      2 |         -12.62 |         -25.24 |           -25.269 |          -2.53 |    1 day, 5:00:00 |     1     0     1  50.0 |
|     DOT/USDT |     20 |          -1.30 |         -26.05 |           -26.075 |          -2.61 |          15:57:00 |    13     5     2  65.0 |
|    DEGO/USDT |     27 |          -1.00 |         -26.98 |           -27.012 |          -2.70 |    1 day, 7:20:00 |    17     5     5  63.0 |
|     FLM/USDT |     24 |          -1.17 |         -28.00 |           -28.025 |          -2.80 |   1 day, 11:22:00 |    18     4     2  75.0 |
|   PORTO/USDT |      3 |          -9.51 |         -28.53 |           -28.560 |          -2.86 |    1 day, 2:20:00 |     1     1     1  33.3 |
|     FIL/USDT |     20 |          -1.43 |         -28.54 |           -28.567 |          -2.86 |  2 days, 17:33:00 |    13     5     2  65.0 |
|     CVP/USDT |      8 |          -3.59 |         -28.73 |           -28.762 |          -2.88 |   4 days, 2:22:00 |     4     3     1  50.0 |
|   OCEAN/USDT |     23 |          -1.26 |         -29.06 |           -29.085 |          -2.91 |    1 day, 2:00:00 |    13     7     3  56.5 |
|    SAND/USDT |     28 |          -1.10 |         -30.91 |           -30.944 |          -3.09 |   1 day, 21:49:00 |    17     8     3  60.7 |
|    DYDX/USDT |      4 |          -7.74 |         -30.97 |           -31.003 |          -3.10 |   5 days, 6:45:00 |     1     2     1  25.0 |
|    MOVR/USDT |      2 |         -15.57 |         -31.14 |           -31.169 |          -3.12 |   3 days, 0:00:00 |     0     1     1     0 |
|     CTK/USDT |     26 |          -1.27 |         -33.05 |           -33.078 |          -3.31 |    1 day, 7:32:00 |    14    10     2  53.8 |
|      AR/USDT |     19 |          -1.88 |         -35.67 |           -35.703 |          -3.57 |  2 days, 12:35:00 |     9     7     3  47.4 |
|    FIDA/USDT |      4 |          -9.06 |         -36.23 |           -36.263 |          -3.63 |  5 days, 16:00:00 |     1     1     2  25.0 |
|     KSM/USDT |     17 |          -2.25 |         -38.28 |           -38.319 |          -3.83 |   1 day, 11:25:00 |    10     5     2  58.8 |
|     DGB/USDT |     21 |          -1.94 |         -40.80 |           -40.843 |          -4.08 |    1 day, 6:31:00 |    12     6     3  57.1 |
|     XRP/USDT |     15 |          -2.81 |         -42.09 |           -42.134 |          -4.21 |   2 days, 1:40:00 |     7     5     3  46.7 |
|     OMG/USDT |     22 |          -1.99 |         -43.71 |           -43.752 |          -4.38 |   2 days, 5:05:00 |    12     7     3  54.5 |
|     BTG/USDT |     31 |          -1.51 |         -46.66 |           -46.708 |          -4.67 |   1 day, 22:19:00 |    17    11     3  54.8 |
|    BAKE/USDT |     15 |          -3.21 |         -48.22 |           -48.267 |          -4.83 |   1 day, 23:04:00 |     9     3     3  60.0 |
|   LAZIO/USDT |      6 |          -8.40 |         -50.38 |           -50.425 |          -5.04 |   2 days, 7:20:00 |     3     1     2  50.0 |
|     BEL/USDT |     27 |          -1.89 |         -51.01 |           -51.058 |          -5.11 |   2 days, 0:47:00 |    15     9     3  55.6 |
|     SFP/USDT |     25 |          -2.18 |         -54.53 |           -54.587 |          -5.46 |   2 days, 3:55:00 |    16     5     4  64.0 |
|     EOS/USDT |     26 |          -2.10 |         -54.67 |           -54.727 |          -5.47 |   1 day, 15:05:00 |    18     5     3  69.2 |
|     BLZ/USDT |     24 |          -2.35 |         -56.40 |           -56.460 |          -5.65 |   1 day, 16:55:00 |    14     6     4  58.3 |
|     UTK/USDT |     32 |          -1.76 |         -56.47 |           -56.524 |          -5.65 |    1 day, 7:02:00 |    15    13     4  46.9 |
|     SXP/USDT |     25 |          -2.29 |         -57.23 |           -57.292 |          -5.73 |  2 days, 19:46:00 |    16     4     5  64.0 |
|     ICP/USDT |     15 |          -4.01 |         -60.14 |           -60.201 |          -6.02 |   1 day, 18:32:00 |     6     6     3  40.0 |
|     GRT/USDT |     24 |          -3.05 |         -73.29 |           -73.365 |          -7.34 |   1 day, 11:40:00 |    12     8     4  50.0 |
|   QUICK/USDT |     10 |          -7.76 |         -77.55 |           -77.632 |          -7.76 |   4 days, 0:36:00 |     6     1     3  60.0 |
|    EGLD/USDT |     21 |          -3.81 |         -80.03 |           -80.108 |          -8.01 |  2 days, 15:23:00 |    13     4     4  61.9 |
|    LINA/USDT |     23 |          -3.49 |         -80.34 |           -80.417 |          -8.04 |   1 day, 12:52:00 |    13     6     4  56.5 |
|     MFT/USDT |     34 |          -2.50 |         -85.09 |           -85.174 |          -8.52 |  2 days, 15:32:00 |    19     9     6  55.9 |
|   CHESS/USDT |      7 |         -12.50 |         -87.52 |           -87.607 |          -8.76 |   2 days, 4:43:00 |     1     3     3  14.3 |
|    KAVA/USDT |     30 |          -3.03 |         -91.01 |           -91.098 |          -9.11 |   3 days, 2:46:00 |    19     6     5  63.3 |
|     ONG/USDT |     38 |          -2.95 |        -112.13 |          -112.240 |         -11.22 |   1 day, 18:58:00 |    24     7     7  63.2 |
|        TOTAL |   5933 |           1.02 |        6031.66 |          6037.690 |         603.77 |   1 day, 18:58:00 |  3790  1742   401  63.9 |
=========================================================== BUY TAG STATS ===========================================================
|   TAG |   Buys |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |    Avg Duration |   Win  Draw  Loss  Win% |
|-------+--------+----------------+----------------+-------------------+----------------+-----------------+-------------------------|
| TOTAL |   5933 |           1.02 |        6031.66 |          6037.690 |         603.77 | 1 day, 18:58:00 |  3790  1742   401  63.9 |
===================================================== SELL REASON STATS =====================================================
|   Sell Reason |   Sells |   Win  Draws  Loss  Win% |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |
|---------------+---------+--------------------------+----------------+----------------+-------------------+----------------|
|           roi |    3571 |   1829  1742     0   100 |           4.26 |       15204.3  |         15219.5   |          56.52 |
|   sell_signal |    1957 |   1957     0     0   100 |           1.23 |        2406.09 |          2408.5   |           8.94 |
|     stop_loss |     361 |      0     0   361     0 |         -31.14 |      -11240.8  |        -11252     |         -41.79 |
|    force_sell |      44 |      4     0    40   9.1 |          -7.68 |        -337.93 |          -338.264 |          -1.26 |
========================================================= LEFT OPEN TRADES REPORT ==========================================================
|       Pair |   Buys |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |      Avg Duration |   Win  Draw  Loss  Win% |
|------------+--------+----------------+----------------+-------------------+----------------+-------------------+-------------------------|
|  ROSE/USDT |      1 |           2.33 |           2.33 |             2.328 |           0.23 |           2:00:00 |     1     0     0   100 |
|  EGLD/USDT |      1 |           0.97 |           0.97 |             0.970 |           0.10 |          14:00:00 |     1     0     0   100 |
| SUPER/USDT |      1 |           0.15 |           0.15 |             0.149 |           0.01 |           1:00:00 |     1     0     0   100 |
|   UMA/USDT |      1 |           0.02 |           0.02 |             0.021 |           0.00 |           8:00:00 |     1     0     0   100 |
|   RVN/USDT |      1 |          -0.08 |          -0.08 |            -0.077 |          -0.01 |          11:00:00 |     0     0     1     0 |
|  PAXG/USDT |      1 |          -0.20 |          -0.20 |            -0.200 |          -0.02 |           1:00:00 |     0     0     1     0 |
|  HIVE/USDT |      1 |          -0.38 |          -0.38 |            -0.384 |          -0.04 |          13:00:00 |     0     0     1     0 |
|  BZRX/USDT |      1 |          -0.52 |          -0.52 |            -0.519 |          -0.05 |           6:00:00 |     0     0     1     0 |
|   ANT/USDT |      1 |          -0.56 |          -0.56 |            -0.560 |          -0.06 |           5:00:00 |     0     0     1     0 |
| FORTH/USDT |      1 |          -0.85 |          -0.85 |            -0.853 |          -0.09 |           1:00:00 |     0     0     1     0 |
|   RIF/USDT |      1 |          -1.15 |          -1.15 |            -1.148 |          -0.11 |          14:00:00 |     0     0     1     0 |
|   YGG/USDT |      1 |          -1.33 |          -1.33 |            -1.332 |          -0.13 |          13:00:00 |     0     0     1     0 |
|  IDEX/USDT |      1 |          -1.84 |          -1.84 |            -1.842 |          -0.18 |           1:00:00 |     0     0     1     0 |
|   KEY/USDT |      1 |          -2.28 |          -2.28 |            -2.282 |          -0.23 |           3:00:00 |     0     0     1     0 |
|   LTC/USDT |      1 |          -3.56 |          -3.56 |            -3.565 |          -0.36 |  3 days, 21:00:00 |     0     0     1     0 |
|   WRX/USDT |      1 |          -4.52 |          -4.52 |            -4.529 |          -0.45 |  3 days, 21:00:00 |     0     0     1     0 |
|  VITE/USDT |      1 |          -5.01 |          -5.01 |            -5.012 |          -0.50 |  3 days, 23:00:00 |     0     0     1     0 |
|   GTC/USDT |      1 |          -5.78 |          -5.78 |            -5.789 |          -0.58 |  2 days, 13:00:00 |     0     0     1     0 |
|   ADX/USDT |      1 |          -6.75 |          -6.75 |            -6.754 |          -0.68 |  3 days, 22:00:00 |     0     0     1     0 |
|  POLY/USDT |      1 |          -7.08 |          -7.08 |            -7.084 |          -0.71 |  3 days, 20:00:00 |     0     0     1     0 |
| 1INCH/USDT |      1 |          -7.08 |          -7.08 |            -7.087 |          -0.71 |  3 days, 22:00:00 |     0     0     1     0 |
|   SXP/USDT |      1 |          -7.19 |          -7.19 |            -7.196 |          -0.72 |  3 days, 22:00:00 |     0     0     1     0 |
|  BAKE/USDT |      1 |          -7.48 |          -7.48 |            -7.489 |          -0.75 |  3 days, 23:00:00 |     0     0     1     0 |
| TFUEL/USDT |      1 |          -8.05 |          -8.05 |            -8.058 |          -0.81 |  3 days, 23:00:00 |     0     0     1     0 |
|   BNB/USDT |      1 |          -8.73 |          -8.73 |            -8.741 |          -0.87 |   9 days, 6:00:00 |     0     0     1     0 |
|   XLM/USDT |      1 |          -9.20 |          -9.20 |            -9.210 |          -0.92 |  3 days, 22:00:00 |     0     0     1     0 |
|   ETC/USDT |      1 |          -9.27 |          -9.27 |            -9.284 |          -0.93 |   4 days, 0:00:00 |     0     0     1     0 |
|   RAY/USDT |      1 |          -9.44 |          -9.44 |            -9.449 |          -0.94 |  3 days, 22:00:00 |     0     0     1     0 |
| STRAX/USDT |      1 |          -9.49 |          -9.49 |            -9.500 |          -0.95 |  3 days, 21:00:00 |     0     0     1     0 |
|   XRP/USDT |      1 |          -9.97 |          -9.97 |            -9.983 |          -1.00 |   3 days, 1:00:00 |     0     0     1     0 |
|   LIT/USDT |      1 |         -10.06 |         -10.06 |           -10.072 |          -1.01 |   4 days, 0:00:00 |     0     0     1     0 |
|   REP/USDT |      1 |         -10.14 |         -10.14 |           -10.154 |          -1.02 |  2 days, 17:00:00 |     0     0     1     0 |
|   ONG/USDT |      1 |         -10.27 |         -10.27 |           -10.277 |          -1.03 |  3 days, 23:00:00 |     0     0     1     0 |
|  FIDA/USDT |      1 |         -10.98 |         -10.98 |           -10.994 |          -1.10 |  3 days, 23:00:00 |     0     0     1     0 |
|   ICP/USDT |      1 |         -11.39 |         -11.39 |           -11.398 |          -1.14 |  4 days, 10:00:00 |     0     0     1     0 |
|   VGX/USDT |      1 |         -13.01 |         -13.01 |           -13.021 |          -1.30 |   4 days, 7:00:00 |     0     0     1     0 |
|   EPS/USDT |      1 |         -13.53 |         -13.53 |           -13.541 |          -1.35 |  3 days, 23:00:00 |     0     0     1     0 |
| WAVES/USDT |      1 |         -14.57 |         -14.57 |           -14.585 |          -1.46 |  3 days, 22:00:00 |     0     0     1     0 |
|  GHST/USDT |      1 |         -15.80 |         -15.80 |           -15.819 |          -1.58 |  9 days, 22:00:00 |     0     0     1     0 |
|   PHA/USDT |      1 |         -19.17 |         -19.17 |           -19.193 |          -1.92 |  2 days, 15:00:00 |     0     0     1     0 |
|   JST/USDT |      1 |         -19.60 |         -19.60 |           -19.617 |          -1.96 | 20 days, 20:00:00 |     0     0     1     0 |
|   DCR/USDT |      1 |         -19.66 |         -19.66 |           -19.680 |          -1.97 |  3 days, 20:00:00 |     0     0     1     0 |
|  MINA/USDT |      1 |         -21.26 |         -21.26 |           -21.282 |          -2.13 |  11 days, 9:00:00 |     0     0     1     0 |
| JASMY/USDT |      1 |         -24.15 |         -24.15 |           -24.173 |          -2.42 |  6 days, 10:00:00 |     0     0     1     0 |
|      TOTAL |     44 |          -7.68 |        -337.93 |          -338.264 |         -33.83 |  3 days, 13:00:00 |     4     0    40   9.1 |
=============== SUMMARY METRICS ================
| Metric                 | Value               |
|------------------------+---------------------|
| Backtesting from       | 2021-01-01 00:00:00 |
| Backtesting to         | 2021-12-12 15:00:00 |
| Max open trades        | 269                 |
|                        |                     |
| Total/Daily Avg Trades | 5933 / 17.2         |
| Starting balance       | 1000.000 USDT       |
| Final balance          | 7037.690 USDT       |
| Absolute profit        | 6037.690 USDT       |
| Total profit %         | 603.77%             |
| Trades per day         | 17.2                |
| Avg. daily profit %    | 1.75%               |
| Avg. stake amount      | 100.000 USDT        |
| Total trade volume     | 593300.000 USDT     |
|                        |                     |
| Best Pair              | OXT/USDT 198.10%    |
| Worst Pair             | ONG/USDT -112.13%   |
| Best trade             | DNT/USDT 55.24%     |
| Worst trade            | MDT/USDT -31.14%    |
| Best day               | 297.207 USDT        |
| Worst day              | -1606.388 USDT      |
| Days win/draw/lose     | 285 / 5 / 55        |
| Avg. Duration Winners  | 13:29:00            |
| Avg. Duration Loser    | 5 days, 21:39:00    |
| Rejected Buy signals   | 0                   |
|                        |                     |
| Min balance            | 1014.400 USDT       |
| Max balance            | 8337.489 USDT       |
| Drawdown               | 2419.06%            |
| Drawdown               | 2421.476 USDT       |
| Drawdown high          | 4515.515 USDT       |
| Drawdown low           | 2094.040 USDT       |
| Drawdown Start         | 2021-05-10 16:00:00 |
| Drawdown End           | 2021-06-22 12:00:00 |
| Market change          | 559.54%             |
================================================
```