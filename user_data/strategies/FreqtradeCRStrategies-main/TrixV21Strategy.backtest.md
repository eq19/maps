```
freqtrade backtesting --strategy TrixV21Strategy --stake-amount 100 --timeframe 1h --max-open-trades -1 --fee 0.001 --dry-run-wallet 1000 --timerange=20210101- 
Creating freqtradelocal_freqtrade_run ... done
2021-12-17 18:12:36,436 - freqtrade.configuration.configuration - INFO - Using config: user_data/config.json ...
2021-12-17 18:12:36,438 - freqtrade.loggers - INFO - Verbosity set to 0
2021-12-17 18:12:36,438 - freqtrade.configuration.configuration - INFO - Parameter -i/--timeframe detected ... Using timeframe: 1h ...
2021-12-17 18:12:36,439 - freqtrade.configuration.configuration - INFO - Parameter --max-open-trades detected, overriding max_open_trades to: -1 ...
2021-12-17 18:12:36,439 - freqtrade.configuration.configuration - INFO - Parameter --stake-amount detected, overriding stake_amount to: 100.0 ...
2021-12-17 18:12:36,439 - freqtrade.configuration.configuration - INFO - Parameter --dry-run-wallet detected, overriding dry_run_wallet to: 1000.0 ...
2021-12-17 18:12:36,439 - freqtrade.configuration.configuration - INFO - Parameter --fee detected, setting fee to: 0.001 ...
2021-12-17 18:12:36,439 - freqtrade.configuration.configuration - INFO - Parameter --timerange detected: 20210101- ...
2021-12-17 18:12:37,716 - freqtrade.configuration.configuration - INFO - Using user-data directory: /freqtrade/user_data ...
2021-12-17 18:12:37,717 - freqtrade.configuration.configuration - INFO - Using data directory: /freqtrade/user_data/data/binance ...
2021-12-17 18:12:37,718 - freqtrade.configuration.configuration - INFO - Overriding timeframe with Command line argument
2021-12-17 18:12:37,718 - freqtrade.configuration.check_exchange - INFO - Checking exchange...
2021-12-17 18:12:37,727 - freqtrade.configuration.check_exchange - INFO - Exchange "binance" is officially supported by the Freqtrade development team.
2021-12-17 18:12:37,727 - freqtrade.configuration.configuration - INFO - Using pairlist from configuration.
2021-12-17 18:12:37,727 - freqtrade.configuration.config_validation - INFO - Validating configuration ...
2021-12-17 18:12:37,732 - freqtrade.commands.optimize_commands - INFO - Starting freqtrade in Backtesting mode
2021-12-17 18:12:37,732 - freqtrade.exchange.exchange - INFO - Instance is running with dry_run enabled
2021-12-17 18:12:37,733 - freqtrade.exchange.exchange - INFO - Using CCXT 1.61.92
2021-12-17 18:12:37,749 - freqtrade.exchange.exchange - INFO - Using Exchange "Binance"
2021-12-17 18:12:39,350 - freqtrade.resolvers.exchange_resolver - INFO - Using resolved exchange 'Binance'...
2021-12-17 18:12:39,928 - TrixV21Strategy - INFO - pandas_ta successfully imported
2021-12-17 18:12:40,071 - freqtrade.resolvers.iresolver - INFO - Using resolved strategy TrixV21Strategy from '/freqtrade/user_data/strategies/TrixV21Strategy.py'...
2021-12-17 18:12:40,072 - freqtrade.strategy.hyper - INFO - Loading parameters from file /freqtrade/user_data/strategies/TrixV21Strategy.json
2021-12-17 18:12:40,083 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_ema_guard_multiplier = 0.994
2021-12-17 18:12:40,083 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_ema_guard_timeperiod = 238
2021-12-17 18:12:40,083 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_ema_multiplier = 0.85
2021-12-17 18:12:40,083 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_ema_src = open
2021-12-17 18:12:40,083 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_ema_timeperiod = 10
2021-12-17 18:12:40,083 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_ema_timeperiod_enabled = True
2021-12-17 18:12:40,083 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_stoch_rsi = 0.901
2021-12-17 18:12:40,084 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_stoch_rsi_enabled = True
2021-12-17 18:12:40,084 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_trix_signal_timeperiod = 19
2021-12-17 18:12:40,084 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_trix_signal_type = trigger
2021-12-17 18:12:40,084 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_trix_src = low
2021-12-17 18:12:40,084 - freqtrade.strategy.hyper - INFO - Strategy Parameter: buy_trix_timeperiod = 8
2021-12-17 18:12:40,084 - freqtrade.strategy.hyper - INFO - Strategy Parameter: sell_atr_enabled = True
2021-12-17 18:12:40,084 - freqtrade.strategy.hyper - INFO - Strategy Parameter: sell_atr_multiplier = 4.99
2021-12-17 18:12:40,084 - freqtrade.strategy.hyper - INFO - Strategy Parameter: sell_atr_timeperiod = 30
2021-12-17 18:12:40,084 - freqtrade.strategy.hyper - INFO - Strategy Parameter: sell_stoch_rsi = 0.183
2021-12-17 18:12:40,084 - freqtrade.strategy.hyper - INFO - Strategy Parameter: sell_stoch_rsi_enabled = True
2021-12-17 18:12:40,085 - freqtrade.strategy.hyper - INFO - Strategy Parameter: sell_trix_signal_timeperiod = 19
2021-12-17 18:12:40,085 - freqtrade.strategy.hyper - INFO - Strategy Parameter: sell_trix_signal_type = trailing
2021-12-17 18:12:40,085 - freqtrade.strategy.hyper - INFO - Strategy Parameter: sell_trix_src = high
2021-12-17 18:12:40,085 - freqtrade.strategy.hyper - INFO - Strategy Parameter: sell_trix_timeperiod = 10
2021-12-17 18:12:40,085 - freqtrade.strategy.hyper - INFO - No params for protection found, using default values.
2021-12-17 18:12:40,085 - freqtrade.resolvers.strategy_resolver - INFO - Override strategy 'timeframe' with value in config file: 1h.
2021-12-17 18:12:40,086 - freqtrade.resolvers.strategy_resolver - INFO - Override strategy 'stake_currency' with value in config file: USDT.
2021-12-17 18:12:40,086 - freqtrade.resolvers.strategy_resolver - INFO - Override strategy 'stake_amount' with value in config file: 100.0.
2021-12-17 18:12:40,086 - freqtrade.resolvers.strategy_resolver - INFO - Override strategy 'unfilledtimeout' with value in config file: {'buy': 10, 'sell': 30, 'unit': 'minutes', 'exit_timeout_count': 0}.        
2021-12-17 18:12:40,086 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using minimal_roi: {'0': 0.553, '423': 0.144, '751': 0.059, '1342': 0}
2021-12-17 18:12:40,086 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using timeframe: 1h
2021-12-17 18:12:40,086 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using stoploss: -0.31
2021-12-17 18:12:40,086 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using trailing_stop: False
2021-12-17 18:12:40,086 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using trailing_stop_positive_offset: 0.0
2021-12-17 18:12:40,086 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using trailing_only_offset_is_reached: False
2021-12-17 18:12:40,086 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using use_custom_stoploss: True
2021-12-17 18:12:40,086 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using process_only_new_candles: False
2021-12-17 18:12:40,087 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using order_types: {'buy': 'limit', 'sell': 'limit', 'stoploss': 'market', 'stoploss_on_exchange': False}
2021-12-17 18:12:40,087 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using order_time_in_force: {'buy': 'gtc', 'sell': 'gtc'}
2021-12-17 18:12:40,087 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using stake_currency: USDT
2021-12-17 18:12:40,087 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using stake_amount: 100.0
2021-12-17 18:12:40,087 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using protections: []
2021-12-17 18:12:40,087 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using startup_candle_count: 238
2021-12-17 18:12:40,087 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using unfilledtimeout: {'buy': 10, 'sell': 30, 'unit': 'minutes', 'exit_timeout_count': 0}
2021-12-17 18:12:40,087 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using use_sell_signal: True
2021-12-17 18:12:40,087 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using sell_profit_only: True
2021-12-17 18:12:40,087 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using ignore_roi_if_buy_signal: False
2021-12-17 18:12:40,088 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using sell_profit_offset: 0.0
2021-12-17 18:12:40,088 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using disable_dataframe_checks: False
2021-12-17 18:12:40,088 - freqtrade.resolvers.strategy_resolver - INFO - Strategy using ignore_buying_expired_candle_after: 0
2021-12-17 18:12:40,088 - freqtrade.configuration.config_validation - INFO - Validating configuration ...
2021-12-17 18:12:40,095 - freqtrade.resolvers.iresolver - INFO - Using resolved pairlist StaticPairList from '/freqtrade/freqtrade/plugins/pairlist/StaticPairList.py'...
2021-12-17 18:12:40,635 - freqtrade.plugins.pairlistmanager - WARNING - Pair ACM/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:12:40,635 - freqtrade.plugins.pairlistmanager - WARNING - Pair ASR/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:12:40,635 - freqtrade.plugins.pairlistmanager - WARNING - Pair ATM/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:12:40,635 - freqtrade.plugins.pairlistmanager - WARNING - Pair AUD/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:12:40,635 - freqtrade.plugins.pairlistmanager - WARNING - Pair BAR/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:12:40,635 - freqtrade.plugins.pairlistmanager - WARNING - Pair BTC/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:12:40,636 - freqtrade.plugins.pairlistmanager - WARNING - Pair BUSD/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:12:40,636 - freqtrade.plugins.pairlistmanager - WARNING - Pair CHZ/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:12:40,636 - freqtrade.plugins.pairlistmanager - WARNING - Pair CITY/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:12:40,636 - freqtrade.plugins.pairlistmanager - WARNING - Pair CTXC/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:12:40,636 - freqtrade.plugins.pairlistmanager - WARNING - Pair EUR/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:12:40,636 - freqtrade.plugins.pairlistmanager - WARNING - Pair FOR/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:12:40,636 - freqtrade.plugins.pairlistmanager - WARNING - Pair FTT/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:12:40,637 - freqtrade.plugins.pairlistmanager - WARNING - Pair GBP/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:12:40,637 - freqtrade.plugins.pairlistmanager - WARNING - Pair HBAR/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:12:40,637 - freqtrade.plugins.pairlistmanager - WARNING - Pair JUV/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:12:40,637 - freqtrade.plugins.pairlistmanager - WARNING - Pair NMR/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:12:40,637 - freqtrade.plugins.pairlistmanager - WARNING - Pair OG/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:12:40,637 - freqtrade.plugins.pairlistmanager - WARNING - Pair PSG/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:12:40,637 - freqtrade.plugins.pairlistmanager - WARNING - Pair SHIB/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:12:40,638 - freqtrade.plugins.pairlistmanager - WARNING - Pair SLP/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:12:40,638 - freqtrade.plugins.pairlistmanager - WARNING - Pair TUSD/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:12:40,638 - freqtrade.plugins.pairlistmanager - WARNING - Pair USDC/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:12:40,638 - freqtrade.plugins.pairlistmanager - WARNING - Pair XVS/USDT in your blacklist. Removing it from whitelist...
2021-12-17 18:12:40,640 - freqtrade.data.history.history_utils - INFO - Using indicator startup period: 238 ...
2021-12-17 18:12:40,663 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair 1INCH/USDT, data starts at 2020-12-25 05:00:00
2021-12-17 18:12:40,814 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair ADX/USDT, data starts at 2021-10-29 10:00:00
2021-12-17 18:12:40,834 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair AGLD/USDT, data starts at 2021-10-05 07:00:00
2021-12-17 18:12:40,967 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair ALICE/USDT, data starts at 2021-03-15 06:00:00
2021-12-17 18:12:40,990 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair ALPACA/USDT, data starts at 2021-08-11 08:00:00
2021-12-17 18:12:41,041 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair AMP/USDT, data starts at 2021-11-23 06:00:00
2021-12-17 18:12:41,193 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair AR/USDT, data starts at 2021-05-14 12:00:00
2021-12-17 18:12:41,294 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair ATA/USDT, data starts at 2021-06-07 06:00:00
2021-12-17 18:12:41,353 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair AUCTION/USDT, data starts at 2021-10-29 10:00:00
2021-12-17 18:12:41,410 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair AUTO/USDT, data starts at 2021-04-02 09:00:00
2021-12-17 18:12:41,582 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair BADGER/USDT, data starts at 2021-03-02 08:00:00
2021-12-17 18:12:41,607 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair BAKE/USDT, data starts at 2021-04-30 12:00:00
2021-12-17 18:12:41,904 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair BETA/USDT, data starts at 2021-10-08 12:00:00
2021-12-17 18:12:42,032 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair BNX/USDT, data starts at 2021-11-04 11:00:00
2021-12-17 18:12:42,054 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair BOND/USDT, data starts at 2021-07-05 06:00:00
2021-12-17 18:12:42,081 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair BTCST/USDT, data starts at 2021-01-13 06:00:00
2021-12-17 18:12:42,091 - freqtrade.data.converter - INFO - Missing data fillup for BTCST/USDT: before: 7893 - after: 8002 - 1.38%
2021-12-17 18:12:42,165 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair BTG/USDT, data starts at 2021-04-16 07:00:00
2021-12-17 18:12:42,268 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair BURGER/USDT, data starts at 2021-04-30 12:00:00
2021-12-17 18:12:42,324 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair C98/USDT, data starts at 2021-07-23 12:00:00
2021-12-17 18:12:42,350 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair CAKE/USDT, data starts at 2021-02-19 06:00:00
2021-12-17 18:12:42,378 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair CELO/USDT, data starts at 2021-01-05 08:00:00
2021-12-17 18:12:42,501 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair CFX/USDT, data starts at 2021-03-29 11:00:00
2021-12-17 18:12:42,520 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair CHESS/USDT, data starts at 2021-10-22 06:00:00
2021-12-17 18:12:42,583 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair CKB/USDT, data starts at 2021-01-26 12:00:00
2021-12-17 18:12:42,606 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair CLV/USDT, data starts at 2021-07-29 06:00:00
2021-12-17 18:12:42,927 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair CVP/USDT, data starts at 2021-10-04 10:00:00
2021-12-17 18:12:42,946 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair DAR/USDT, data starts at 2021-11-04 08:00:00
2021-12-17 18:12:43,078 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair DEGO/USDT, data starts at 2021-03-10 11:00:00
2021-12-17 18:12:43,199 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair DEXE/USDT, data starts at 2021-07-23 10:00:00
2021-12-17 18:12:43,219 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair DF/USDT, data starts at 2021-09-24 10:00:00
2021-12-17 18:12:43,379 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair DODO/USDT, data starts at 2021-02-19 10:00:00
2021-12-17 18:12:43,566 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair DYDX/USDT, data starts at 2021-09-09 02:00:00
2021-12-17 18:12:43,618 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair ELF/USDT, data starts at 2021-09-08 08:00:00
2021-12-17 18:12:43,676 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair ENS/USDT, data starts at 2021-11-10 07:00:00
2021-12-17 18:12:43,739 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair EPS/USDT, data starts at 2021-04-02 09:00:00
2021-12-17 18:12:43,763 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair ERN/USDT, data starts at 2021-06-22 06:00:00
2021-12-17 18:12:43,918 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair FARM/USDT, data starts at 2021-08-11 08:00:00
2021-12-17 18:12:43,977 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair FIDA/USDT, data starts at 2021-09-30 12:00:00
2021-12-17 18:12:44,065 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair FIRO/USDT, data starts at 2021-01-29 02:00:00
2021-12-17 18:12:44,093 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair FIS/USDT, data starts at 2021-03-03 08:00:00
2021-12-17 18:12:44,146 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair FLOW/USDT, data starts at 2021-07-30 13:00:00
2021-12-17 18:12:44,171 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair FORTH/USDT, data starts at 2021-04-23 09:00:00
2021-12-17 18:12:44,192 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair FRONT/USDT, data starts at 2021-10-04 10:00:00
2021-12-17 18:12:44,347 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair GALA/USDT, data starts at 2021-09-13 06:00:00
2021-12-17 18:12:44,368 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair GHST/USDT, data starts at 2021-08-20 10:00:00
2021-12-17 18:12:44,389 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair GNO/USDT, data starts at 2021-08-30 06:00:00
2021-12-17 18:12:44,441 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair GTC/USDT, data starts at 2021-06-10 10:00:00
2021-12-17 18:12:44,729 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair ICP/USDT, data starts at 2021-05-11 01:00:00
2021-12-17 18:12:44,789 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair IDEX/USDT, data starts at 2021-09-09 08:00:00
2021-12-17 18:12:44,809 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair ILV/USDT, data starts at 2021-09-22 06:00:00
2021-12-17 18:12:45,063 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair JASMY/USDT, data starts at 2021-11-22 12:00:00
2021-12-17 18:12:45,156 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair KEEP/USDT, data starts at 2021-06-17 06:00:00
2021-12-17 18:12:45,218 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair KLAY/USDT, data starts at 2021-06-24 08:00:00
2021-12-17 18:12:45,359 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair KP3R/USDT, data starts at 2021-11-12 10:00:00
2021-12-17 18:12:45,410 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair LAZIO/USDT, data starts at 2021-10-21 12:00:00
2021-12-17 18:12:45,436 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair LINA/USDT, data starts at 2021-03-18 12:00:00
2021-12-17 18:12:45,503 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair LIT/USDT, data starts at 2021-02-04 06:00:00
2021-12-17 18:12:45,527 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair LPT/USDT, data starts at 2021-05-28 05:00:00
2021-12-17 18:12:45,819 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair MASK/USDT, data starts at 2021-05-25 06:00:00
2021-12-17 18:12:45,975 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair MBOX/USDT, data starts at 2021-08-19 08:00:00
2021-12-17 18:12:46,032 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair MDX/USDT, data starts at 2021-05-24 09:00:00
2021-12-17 18:12:46,094 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair MINA/USDT, data starts at 2021-08-10 06:00:00
2021-12-17 18:12:46,118 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair MIR/USDT, data starts at 2021-04-19 11:00:00
2021-12-17 18:12:46,213 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair MLN/USDT, data starts at 2021-07-05 06:00:00
2021-12-17 18:12:46,232 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair MOVR/USDT, data starts at 2021-11-08 06:00:00
2021-12-17 18:12:46,527 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair NU/USDT, data starts at 2021-06-04 05:00:00
2021-12-17 18:12:46,720 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair OM/USDT, data starts at 2021-03-08 09:00:00
2021-12-17 18:12:47,090 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair PERP/USDT, data starts at 2021-03-19 08:00:00
2021-12-17 18:12:47,115 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair PHA/USDT, data starts at 2021-06-25 10:00:00
2021-12-17 18:12:47,134 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair PLA/USDT, data starts at 2021-11-23 06:00:00
2021-12-17 18:12:47,197 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair POLS/USDT, data starts at 2021-05-19 07:00:00
2021-12-17 18:12:47,218 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair POLY/USDT, data starts at 2021-09-09 08:00:00
2021-12-17 18:12:47,304 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair POND/USDT, data starts at 2021-03-09 08:00:00
2021-12-17 18:12:47,323 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair PORTO/USDT, data starts at 2021-11-16 12:00:00
2021-12-17 18:12:47,342 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair POWR/USDT, data starts at 2021-11-17 06:00:00
2021-12-17 18:12:47,366 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair PUNDIX/USDT, data starts at 2021-04-09 04:00:00
2021-12-17 18:12:47,385 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair PYR/USDT, data starts at 2021-11-26 08:00:00
2021-12-17 18:12:47,404 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair QI/USDT, data starts at 2021-11-15 08:00:00
2021-12-17 18:12:47,426 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair QNT/USDT, data starts at 2021-07-29 06:00:00
2021-12-17 18:12:47,486 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair QUICK/USDT, data starts at 2021-08-13 12:00:00
2021-12-17 18:12:47,505 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair RAD/USDT, data starts at 2021-10-07 07:00:00
2021-12-17 18:12:47,531 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair RAMP/USDT, data starts at 2021-03-22 09:00:00
2021-12-17 18:12:47,552 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair RARE/USDT, data starts at 2021-10-11 06:00:00
2021-12-17 18:12:47,573 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair RAY/USDT, data starts at 2021-08-10 06:00:00
2021-12-17 18:12:47,602 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair REEF/USDT, data starts at 2020-12-29 06:00:00
2021-12-17 18:12:47,697 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair REQ/USDT, data starts at 2021-08-20 10:00:00
2021-12-17 18:12:47,716 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair RGT/USDT, data starts at 2021-11-05 06:00:00
2021-12-17 18:12:47,744 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair RIF/USDT, data starts at 2021-01-07 13:00:00
2021-12-17 18:12:47,860 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair RNDR/USDT, data starts at 2021-11-27 10:00:00
2021-12-17 18:12:48,082 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair SFP/USDT, data starts at 2021-02-08 13:00:00
2021-12-17 18:12:48,551 - freqtrade.data.converter - INFO - Missing data fillup for SUN/USDT: before: 8424 - after: 8534 - 1.31%
2021-12-17 18:12:48,571 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair SUPER/USDT, data starts at 2021-03-25 10:00:00
2021-12-17 18:12:48,713 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair SYS/USDT, data starts at 2021-09-24 10:00:00
2021-12-17 18:12:48,915 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair TKO/USDT, data starts at 2021-04-07 13:00:00
2021-12-17 18:12:48,941 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair TLM/USDT, data starts at 2021-04-13 06:00:00
2021-12-17 18:12:49,004 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair TORN/USDT, data starts at 2021-06-11 06:00:00
2021-12-17 18:12:49,058 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair TRIBE/USDT, data starts at 2021-08-24 06:00:00
2021-12-17 18:12:49,125 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair TRU/USDT, data starts at 2021-01-19 07:00:00
2021-12-17 18:12:49,245 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair TVK/USDT, data starts at 2021-08-06 10:00:00
2021-12-17 18:12:49,272 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair TWT/USDT, data starts at 2021-01-27 08:00:00
2021-12-17 18:12:49,387 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair USDP/USDT, data starts at 2021-09-10 04:00:00
2021-12-17 18:12:49,476 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair VGX/USDT, data starts at 2021-11-22 07:00:00
2021-12-17 18:12:49,496 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair VIDT/USDT, data starts at 2021-09-09 08:00:00
2021-12-17 18:12:49,726 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair WAXP/USDT, data starts at 2021-08-23 06:00:00
2021-12-17 18:12:49,980 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair XEC/USDT, data starts at 2021-09-03 10:00:00
2021-12-17 18:12:50,244 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair XVG/USDT, data starts at 2021-06-06 10:00:00
2021-12-17 18:12:50,329 - freqtrade.data.history.idatahandler - WARNING - Missing data at start for pair YGG/USDT, data starts at 2021-09-24 06:00:00
2021-12-17 18:12:50,538 - freqtrade.optimize.backtesting - INFO - Loading data from 2020-12-22 02:00:00 up to 2021-12-12 15:00:00 (355 days).
2021-12-17 18:12:50,539 - freqtrade.optimize.backtesting - INFO - Dataload complete. Calculating indicators
2021-12-17 18:12:50,539 - freqtrade.optimize.backtesting - INFO - Running backtesting for Strategy TrixV21Strategy
2021-12-17 18:12:52,361 - freqtrade.optimize.backtesting - INFO - Backtesting with data from 2021-01-01 00:00:00 up to 2021-12-12 15:00:00 (345 days).
2021-12-17 18:13:37,751 - freqtrade.misc - INFO - dumping json to "/freqtrade/user_data/backtest_results/backtest-result-2021-12-17_18-13-37.json"
2021-12-17 18:13:37,855 - freqtrade.misc - INFO - dumping json to "/freqtrade/user_data/backtest_results/.last_result.json"
Result for strategy TrixV21Strategy
============================================================= BACKTESTING REPORT ============================================================
|         Pair |   Buys |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |     Avg Duration |   Win  Draw  Loss  Win% |
|--------------+--------+----------------+----------------+-------------------+----------------+------------------+-------------------------|
|     OXT/USDT |     32 |           4.86 |         155.60 |           155.757 |          15.58 |         17:56:00 |    26     4     2  81.2 |
|    IOTX/USDT |     30 |           4.44 |         133.07 |           133.201 |          13.32 |         22:38:00 |    20     5     5  66.7 |
|     SUN/USDT |     32 |           4.01 |         128.17 |           128.298 |          12.83 |         16:19:00 |    26     6     0   100 |
|     PNT/USDT |     22 |           5.65 |         124.29 |           124.411 |          12.44 |   1 day, 0:11:00 |    13     6     3  59.1 |
|     KEY/USDT |     20 |           5.68 |         113.56 |           113.672 |          11.37 |         18:48:00 |    15     4     1  75.0 |
|    DOCK/USDT |     36 |           3.09 |         111.12 |           111.235 |          11.12 |         17:08:00 |    29     4     3  80.6 |
|     ETC/USDT |     21 |           5.19 |         108.97 |           109.084 |          10.91 |         14:49:00 |    17     2     2  81.0 |
|    HIVE/USDT |     34 |           3.07 |         104.48 |           104.586 |          10.46 |   1 day, 1:49:00 |    20    10     4  58.8 |
|     FET/USDT |     23 |           4.46 |         102.60 |           102.706 |          10.27 |         17:42:00 |    18     5     0   100 |
|     CHR/USDT |     34 |           2.99 |         101.70 |           101.805 |          10.18 |   1 day, 1:25:00 |    21     7     6  61.8 |
|    VTHO/USDT |     16 |           6.11 |          97.69 |            97.791 |           9.78 |         14:04:00 |    14     1     1  87.5 |
|     DNT/USDT |     34 |           2.75 |          93.44 |            93.537 |           9.35 |         19:41:00 |    24     5     5  70.6 |
|   THETA/USDT |     23 |           4.00 |          92.07 |            92.165 |           9.22 |         18:16:00 |    19     1     3  82.6 |
|     SKL/USDT |     30 |           2.84 |          85.35 |            85.435 |           8.54 |         19:48:00 |    20     7     3  66.7 |
|     KMD/USDT |     25 |           3.38 |          84.49 |            84.576 |           8.46 |   1 day, 0:48:00 |    18     4     3  72.0 |
|     ENJ/USDT |     21 |           3.85 |          80.90 |            80.982 |           8.10 |         21:34:00 |    11     7     3  52.4 |
|    CELR/USDT |     27 |           2.82 |          76.01 |            76.086 |           7.61 |         18:44:00 |    19     5     3  70.4 |
|     ONE/USDT |     16 |           4.68 |          74.84 |            74.910 |           7.49 |         23:04:00 |    11     5     0   100 |
|     OGN/USDT |     27 |           2.76 |          74.53 |            74.609 |           7.46 |         19:16:00 |    19     5     3  70.4 |
|     TLM/USDT |     13 |           5.71 |          74.23 |            74.306 |           7.43 |         21:09:00 |    12     1     0   100 |
|     DIA/USDT |     36 |           2.00 |          71.98 |            72.050 |           7.20 |         20:50:00 |    26     7     3  72.2 |
|     HNT/USDT |     25 |           2.86 |          71.46 |            71.536 |           7.15 |         20:55:00 |    18     5     2  72.0 |
|    VITE/USDT |     26 |           2.74 |          71.22 |            71.288 |           7.13 |         22:25:00 |    19     6     1  73.1 |
|     WTC/USDT |     24 |           2.84 |          68.07 |            68.134 |           6.81 |         22:08:00 |    18     3     3  75.0 |
|    CELO/USDT |     20 |           3.35 |          67.00 |            67.070 |           6.71 |   1 day, 5:48:00 |    13     6     1  65.0 |
|     REQ/USDT |      8 |           8.26 |          66.09 |            66.156 |           6.62 |  1 day, 16:15:00 |     4     2     2  50.0 |
|     FIO/USDT |     35 |           1.79 |          62.59 |            62.653 |           6.27 |   1 day, 3:02:00 |    22     9     4  62.9 |
|    RUNE/USDT |     17 |           3.58 |          60.93 |            60.995 |           6.10 |         16:07:00 |    14     2     1  82.4 |
|    QTUM/USDT |     22 |           2.76 |          60.82 |            60.879 |           6.09 |         19:49:00 |    16     5     1  72.7 |
|     AXS/USDT |     29 |           2.08 |          60.22 |            60.282 |           6.03 |         22:39:00 |    18     6     5  62.1 |
|     VET/USDT |     14 |           4.15 |          58.14 |            58.196 |           5.82 |         22:43:00 |    11     3     0   100 |
|    DEGO/USDT |     18 |           3.15 |          56.74 |            56.794 |           5.68 |         21:57:00 |    13     3     2  72.2 |
|    NEAR/USDT |     17 |           3.31 |          56.23 |            56.285 |           5.63 |         18:46:00 |    13     2     2  76.5 |
|     BAT/USDT |     15 |           3.71 |          55.70 |            55.759 |           5.58 |         16:04:00 |    10     3     2  66.7 |
|   ALPHA/USDT |     20 |           2.74 |          54.86 |            54.919 |           5.49 |         21:51:00 |    14     4     2  70.0 |
|   MATIC/USDT |     17 |           3.21 |          54.60 |            54.655 |           5.47 |         13:42:00 |    16     1     0   100 |
|     DAR/USDT |      4 |          13.34 |          53.37 |            53.422 |           5.34 |         11:00:00 |     4     0     0   100 |
|     MTL/USDT |     24 |           2.20 |          52.90 |            52.956 |           5.30 |         20:50:00 |    17     6     1  70.8 |
|     INJ/USDT |     22 |           2.40 |          52.87 |            52.920 |           5.29 |         19:44:00 |    16     4     2  72.7 |
|    CTSI/USDT |     29 |           1.80 |          52.33 |            52.387 |           5.24 |         18:12:00 |    20     6     3  69.0 |
|     TRB/USDT |     21 |           2.48 |          52.12 |            52.168 |           5.22 |         19:00:00 |    16     4     1  76.2 |
|    DOGE/USDT |     23 |           2.26 |          52.01 |            52.064 |           5.21 |         22:00:00 |    17     5     1  73.9 |
|     NEO/USDT |     15 |           3.41 |          51.17 |            51.225 |           5.12 |         15:08:00 |    12     3     0   100 |
|    BZRX/USDT |     25 |           2.04 |          51.03 |            51.085 |           5.11 |         18:46:00 |    16     5     4  64.0 |
|    STMX/USDT |     18 |           2.83 |          50.98 |            51.033 |           5.10 |         20:03:00 |    11     5     2  61.1 |
|    POLS/USDT |     16 |           3.08 |          49.30 |            49.345 |           4.93 |         19:41:00 |    11     5     0   100 |
|    WING/USDT |     31 |           1.59 |          49.18 |            49.233 |           4.92 |         23:08:00 |    20     6     5  64.5 |
|    ROSE/USDT |     32 |           1.53 |          49.05 |            49.101 |           4.91 |         23:02:00 |    19     7     6  59.4 |
|      NU/USDT |     12 |           4.02 |          48.24 |            48.288 |           4.83 |         21:45:00 |     7     3     2  58.3 |
|     NBS/USDT |     29 |           1.60 |          46.47 |            46.521 |           4.65 |         21:50:00 |    18     6     5  62.1 |
|    BOND/USDT |     10 |           4.62 |          46.19 |            46.238 |           4.62 |  1 day, 16:48:00 |     4     4     2  40.0 |
|     ATA/USDT |     13 |           3.55 |          46.18 |            46.228 |           4.62 |   1 day, 7:46:00 |    11     1     1  84.6 |
|     BTT/USDT |     26 |           1.74 |          45.31 |            45.359 |           4.54 |         22:55:00 |    18     2     6  69.2 |
|     TRX/USDT |     23 |           1.79 |          41.07 |            41.113 |           4.11 |         19:39:00 |    16     4     3  69.6 |
|   OCEAN/USDT |     17 |           2.40 |          40.72 |            40.758 |           4.08 |   1 day, 0:56:00 |    10     6     1  58.8 |
|    IDEX/USDT |      6 |           6.77 |          40.63 |            40.674 |           4.07 |         15:00:00 |     5     1     0   100 |
|     ZRX/USDT |     22 |           1.83 |          40.30 |            40.341 |           4.03 |   1 day, 1:11:00 |    13     5     4  59.1 |
|    GALA/USDT |      6 |           6.71 |          40.25 |            40.291 |           4.03 |         19:10:00 |     3     2     1  50.0 |
|     SRM/USDT |     23 |           1.72 |          39.50 |            39.535 |           3.95 |         21:52:00 |    16     4     3  69.6 |
|    DATA/USDT |     33 |           1.19 |          39.11 |            39.144 |           3.91 |   1 day, 3:11:00 |    21    10     2  63.6 |
|     ICX/USDT |     21 |           1.85 |          38.89 |            38.924 |           3.89 |         21:26:00 |    16     3     2  76.2 |
|    POND/USDT |     32 |           1.21 |          38.80 |            38.843 |           3.88 |   1 day, 0:17:00 |    22     5     5  68.8 |
|     LRC/USDT |     21 |           1.84 |          38.69 |            38.729 |           3.87 |         20:09:00 |    12     5     4  57.1 |
|    TROY/USDT |     29 |           1.31 |          37.96 |            38.000 |           3.80 |   1 day, 6:39:00 |    17     9     3  58.6 |
|    AION/USDT |     21 |           1.78 |          37.41 |            37.451 |           3.75 |         22:00:00 |    16     4     1  76.2 |
|     FIS/USDT |     21 |           1.75 |          36.75 |            36.786 |           3.68 |   1 day, 5:57:00 |    14     5     2  66.7 |
|    NANO/USDT |     18 |           2.04 |          36.65 |            36.688 |           3.67 |   1 day, 4:03:00 |    11     5     2  61.1 |
|     JST/USDT |     27 |           1.35 |          36.32 |            36.355 |           3.64 |         16:24:00 |    19     1     7  70.4 |
|     EPS/USDT |     11 |           3.28 |          36.10 |            36.133 |           3.61 |   1 day, 4:49:00 |     9     2     0   100 |
|     BCH/USDT |     19 |           1.88 |          35.78 |            35.815 |           3.58 |         19:41:00 |    12     3     4  63.2 |
|      SC/USDT |     20 |           1.76 |          35.13 |            35.161 |           3.52 |         14:51:00 |    15     1     4  75.0 |
|   SUPER/USDT |     16 |           2.19 |          35.07 |            35.110 |           3.51 |         17:34:00 |    10     3     3  62.5 |
|    TOMO/USDT |     25 |           1.40 |          35.01 |            35.041 |           3.50 |         17:48:00 |    19     4     2  76.0 |
|     WIN/USDT |     19 |           1.84 |          34.95 |            34.989 |           3.50 |         21:06:00 |    13     3     3  68.4 |
|     KNC/USDT |     30 |           1.16 |          34.68 |            34.718 |           3.47 |         17:48:00 |    21     5     4  70.0 |
|    WNXM/USDT |     19 |           1.78 |          33.82 |            33.857 |           3.39 |         15:51:00 |    13     3     3  68.4 |
|     FLM/USDT |     21 |           1.59 |          33.46 |            33.491 |           3.35 |         20:40:00 |    18     2     1  85.7 |
|     ZEC/USDT |     16 |           2.07 |          33.13 |            33.165 |           3.32 |         16:34:00 |    12     3     1  75.0 |
|    MBOX/USDT |      7 |           4.58 |          32.07 |            32.100 |           3.21 |         23:17:00 |     4     3     0   100 |
|     STX/USDT |     25 |           1.25 |          31.35 |            31.377 |           3.14 |         20:29:00 |    15     5     5  60.0 |
|    MITH/USDT |     22 |           1.40 |          30.75 |            30.777 |           3.08 |   1 day, 0:19:00 |    13     6     3  59.1 |
|    LUNA/USDT |     25 |           1.22 |          30.56 |            30.588 |           3.06 |         17:48:00 |    15     5     5  60.0 |
|    HARD/USDT |     33 |           0.87 |          28.76 |            28.793 |           2.88 |         20:36:00 |    20     5     8  60.6 |
|     BTG/USDT |     28 |           0.98 |          27.52 |            27.549 |           2.75 |         19:09:00 |    18     7     3  64.3 |
|    FIRO/USDT |     17 |           1.62 |          27.51 |            27.540 |           2.75 |         23:18:00 |    14     2     1  82.4 |
|     PHA/USDT |     11 |           2.40 |          26.44 |            26.462 |           2.65 |   1 day, 5:33:00 |     8     3     0   100 |
|     BAL/USDT |     17 |           1.52 |          25.81 |            25.834 |           2.58 |         17:39:00 |    13     4     0   100 |
|     RVN/USDT |     27 |           0.94 |          25.39 |            25.414 |           2.54 |   1 day, 0:31:00 |    17     6     4  63.0 |
|     LTC/USDT |     28 |           0.90 |          25.18 |            25.201 |           2.52 |         18:26:00 |    21     3     4  75.0 |
|     ZIL/USDT |     11 |           2.27 |          25.02 |            25.045 |           2.50 |         16:49:00 |     8     2     1  72.7 |
|    MASK/USDT |     13 |           1.92 |          24.93 |            24.957 |           2.50 |   1 day, 3:37:00 |     9     2     2  69.2 |
|    DEXE/USDT |     15 |           1.66 |          24.86 |            24.890 |           2.49 |         17:44:00 |     9     5     1  60.0 |
|    WAXP/USDT |      5 |           4.80 |          23.98 |            24.000 |           2.40 |         12:36:00 |     5     0     0   100 |
|    NULS/USDT |     30 |           0.79 |          23.85 |            23.873 |           2.39 |   1 day, 0:10:00 |    18     7     5  60.0 |
|     XLM/USDT |     18 |           1.29 |          23.25 |            23.277 |           2.33 |         18:17:00 |    13     1     4  72.2 |
|     WRX/USDT |     28 |           0.83 |          23.11 |            23.136 |           2.31 |         23:47:00 |    17     7     4  60.7 |
|     LPT/USDT |     15 |           1.54 |          23.05 |            23.074 |           2.31 |   1 day, 7:44:00 |     9     4     2  60.0 |
|    ANKR/USDT |     25 |           0.89 |          22.19 |            22.208 |           2.22 |         23:50:00 |    15     6     4  60.0 |
|    RAMP/USDT |     20 |           1.09 |          21.88 |            21.900 |           2.19 |         23:27:00 |    10     6     4  50.0 |
|     RSR/USDT |     13 |           1.66 |          21.63 |            21.655 |           2.17 |         19:18:00 |     8     4     1  61.5 |
|   1INCH/USDT |     15 |           1.43 |          21.49 |            21.510 |           2.15 |         16:36:00 |    11     2     2  73.3 |
|     ANT/USDT |     30 |           0.72 |          21.46 |            21.481 |           2.15 |         20:04:00 |    18     8     4  60.0 |
|     GXS/USDT |     31 |           0.67 |          20.91 |            20.935 |           2.09 |         21:29:00 |    20     4     7  64.5 |
|    COMP/USDT |     11 |           1.86 |          20.45 |            20.470 |           2.05 |         13:11:00 |     9     0     2  81.8 |
|    FLOW/USDT |     10 |           1.87 |          18.73 |            18.749 |           1.87 |         15:00:00 |     8     0     2  80.0 |
|     NKN/USDT |     24 |           0.78 |          18.61 |            18.629 |           1.86 |   1 day, 7:18:00 |    14     5     5  58.3 |
|     DCR/USDT |     21 |           0.88 |          18.45 |            18.473 |           1.85 |         21:03:00 |    13     3     5  61.9 |
|    GHST/USDT |     11 |           1.67 |          18.32 |            18.340 |           1.83 |         18:11:00 |     9     1     1  81.8 |
|     TWT/USDT |     18 |           1.01 |          18.17 |            18.190 |           1.82 |         23:30:00 |    12     3     3  66.7 |
|   AUDIO/USDT |     22 |           0.80 |          17.55 |            17.566 |           1.76 |         23:16:00 |    15     3     4  68.2 |
|   TFUEL/USDT |     29 |           0.59 |          17.21 |            17.225 |           1.72 |         19:21:00 |    17     5     7  58.6 |
|    IRIS/USDT |     26 |           0.66 |          17.20 |            17.214 |           1.72 |         19:02:00 |    19     3     4  73.1 |
|     XVG/USDT |      5 |           3.30 |          16.50 |            16.520 |           1.65 |         16:48:00 |     5     0     0   100 |
|    AKRO/USDT |     29 |           0.56 |          16.35 |            16.369 |           1.64 |         21:02:00 |    18     6     5  62.1 |
|     MIR/USDT |      8 |           1.93 |          15.40 |            15.420 |           1.54 |         19:45:00 |     6     2     0   100 |
|  BURGER/USDT |     16 |           0.92 |          14.78 |            14.796 |           1.48 |         22:52:00 |    12     2     2  75.0 |
|     CRV/USDT |     31 |           0.45 |          13.84 |            13.849 |           1.38 |         19:56:00 |    22     4     5  71.0 |
|     LTO/USDT |     26 |           0.53 |          13.77 |            13.784 |           1.38 |   1 day, 7:55:00 |    17     4     5  65.4 |
|    IOST/USDT |     14 |           0.95 |          13.26 |            13.271 |           1.33 |         22:56:00 |     9     4     1  64.3 |
|     RIF/USDT |     24 |           0.51 |          12.31 |            12.323 |           1.23 |         19:48:00 |    16     5     3  66.7 |
|     TVK/USDT |     11 |           1.09 |          11.98 |            11.993 |           1.20 |         16:33:00 |     9     1     1  81.8 |
|     DGB/USDT |     18 |           0.66 |          11.93 |            11.940 |           1.19 |         20:37:00 |    10     4     4  55.6 |
|   STRAX/USDT |     18 |           0.66 |          11.89 |            11.900 |           1.19 |         23:37:00 |    11     3     4  61.1 |
|     RAD/USDT |      3 |           3.95 |          11.84 |            11.850 |           1.19 |         13:20:00 |     3     0     0   100 |
|     GTO/USDT |     36 |           0.32 |          11.57 |            11.585 |           1.16 |   1 day, 6:20:00 |    24     6     6  66.7 |
|   STORJ/USDT |     19 |           0.61 |          11.53 |            11.543 |           1.15 |   1 day, 0:32:00 |    11     3     5  57.9 |
|    STPT/USDT |     28 |           0.41 |          11.36 |            11.370 |           1.14 |         22:39:00 |    16     7     5  57.1 |
|    IOTA/USDT |     20 |           0.56 |          11.28 |            11.293 |           1.13 |         17:54:00 |    15     3     2  75.0 |
|     FTM/USDT |     20 |           0.54 |          10.89 |            10.905 |           1.09 |         14:36:00 |    13     4     3  65.0 |
|    PERP/USDT |     19 |           0.57 |          10.77 |            10.776 |           1.08 |         21:28:00 |    11     4     4  57.9 |
|     WAN/USDT |     15 |           0.69 |          10.42 |            10.435 |           1.04 |         20:08:00 |    12     1     2  80.0 |
|     XEM/USDT |     12 |           0.85 |          10.19 |            10.201 |           1.02 |         22:20:00 |     7     3     2  58.3 |
|     EOS/USDT |     18 |           0.55 |           9.96 |             9.971 |           1.00 |         19:07:00 |    13     3     2  72.2 |
|     TCT/USDT |     30 |           0.31 |           9.39 |             9.402 |           0.94 |   1 day, 5:42:00 |    18     7     5  60.0 |
|     SOL/USDT |     20 |           0.46 |           9.16 |             9.167 |           0.92 |         19:09:00 |    14     2     4  70.0 |
|     MDX/USDT |     13 |           0.70 |           9.06 |             9.070 |           0.91 |   1 day, 2:23:00 |     8     3     2  61.5 |
|    ARPA/USDT |     28 |           0.28 |           7.76 |             7.768 |           0.78 |         18:04:00 |    18     2     8  64.3 |
|    PERL/USDT |     43 |           0.18 |           7.67 |             7.673 |           0.77 |   1 day, 0:15:00 |    28     8     7  65.1 |
|     LIT/USDT |     14 |           0.53 |           7.45 |             7.458 |           0.75 |         15:13:00 |    10     2     2  71.4 |
|    UNFI/USDT |     20 |           0.34 |           6.75 |             6.762 |           0.68 |         18:00:00 |    14     2     4  70.0 |
|    TORN/USDT |      9 |           0.73 |           6.53 |             6.538 |           0.65 |   1 day, 4:13:00 |     7     1     1  77.8 |
|  PUNDIX/USDT |     17 |           0.38 |           6.49 |             6.496 |           0.65 |         19:11:00 |    11     2     4  64.7 |
|    DENT/USDT |     10 |           0.63 |           6.29 |             6.296 |           0.63 |   1 day, 2:42:00 |     5     0     5  50.0 |
|     DOT/USDT |     16 |           0.39 |           6.28 |             6.282 |           0.63 |         15:45:00 |    10     5     1  62.5 |
|     TKO/USDT |     20 |           0.30 |           6.01 |             6.017 |           0.60 |   1 day, 0:57:00 |    12     5     3  60.0 |
|    BETA/USDT |      2 |           2.95 |           5.89 |             5.900 |           0.59 |         18:00:00 |     1     1     0   100 |
|   LAZIO/USDT |      1 |           5.89 |           5.89 |             5.900 |           0.59 |         13:00:00 |     1     0     0   100 |
|     RAY/USDT |      8 |           0.70 |           5.56 |             5.570 |           0.56 |   1 day, 1:08:00 |     4     0     4  50.0 |
|   QUICK/USDT |      6 |           0.92 |           5.53 |             5.538 |           0.55 |         17:00:00 |     5     1     0   100 |
|  BADGER/USDT |      7 |           0.74 |           5.18 |             5.184 |           0.52 |   1 day, 2:00:00 |     4     2     1  57.1 |
|     GRT/USDT |     20 |           0.22 |           4.36 |             4.368 |           0.44 |         22:42:00 |    12     5     3  60.0 |
|     UNI/USDT |     12 |           0.36 |           4.34 |             4.346 |           0.43 |         21:55:00 |     6     5     1  50.0 |
|     UTK/USDT |     25 |           0.17 |           4.33 |             4.331 |           0.43 |   1 day, 1:53:00 |    13     8     4  52.0 |
|    AGLD/USDT |      2 |           2.14 |           4.29 |             4.294 |           0.43 |         20:00:00 |     2     0     0   100 |
|    VIDT/USDT |      8 |           0.54 |           4.29 |             4.293 |           0.43 |   1 day, 1:45:00 |     6     1     1  75.0 |
|   SUSHI/USDT |     18 |           0.23 |           4.08 |             4.082 |           0.41 |         16:30:00 |    13     2     3  72.2 |
|     ERN/USDT |     11 |           0.37 |           4.07 |             4.072 |           0.41 |         19:49:00 |     6     3     2  54.5 |
|     CVC/USDT |     26 |           0.15 |           3.97 |             3.978 |           0.40 |         15:21:00 |    20     1     5  76.9 |
|   WAVES/USDT |     22 |           0.16 |           3.60 |             3.608 |           0.36 |         20:22:00 |    13     5     4  59.1 |
|     HOT/USDT |     23 |           0.14 |           3.28 |             3.282 |           0.33 |         20:03:00 |    17     2     4  73.9 |
|    CAKE/USDT |      9 |           0.34 |           3.04 |             3.046 |           0.30 |         16:47:00 |     5     2     2  55.6 |
|    EGLD/USDT |     17 |           0.18 |           3.00 |             3.004 |           0.30 |         20:18:00 |    12     1     4  70.6 |
|     XMR/USDT |     17 |           0.17 |           2.96 |             2.966 |           0.30 |         16:53:00 |    11     2     4  64.7 |
|     ZEN/USDT |     25 |           0.11 |           2.87 |             2.874 |           0.29 |         16:22:00 |    18     3     4  72.0 |
|    DASH/USDT |     20 |           0.13 |           2.66 |             2.665 |           0.27 |         16:48:00 |    13     2     5  65.0 |
|     COS/USDT |     24 |           0.11 |           2.63 |             2.633 |           0.26 |         23:48:00 |    16     5     3  66.7 |
|     ILV/USDT |      5 |           0.47 |           2.37 |             2.376 |           0.24 |         22:00:00 |     4     1     0   100 |
|     ENS/USDT |      1 |           2.19 |           2.19 |             2.188 |           0.22 |         19:00:00 |     1     0     0   100 |
|     ORN/USDT |     11 |           0.18 |           1.98 |             1.986 |           0.20 |         16:44:00 |     7     1     3  63.6 |
|    AVAX/USDT |     16 |           0.12 |           1.87 |             1.875 |           0.19 |         18:38:00 |    10     3     3  62.5 |
|    MANA/USDT |     28 |           0.06 |           1.81 |             1.813 |           0.18 |         22:45:00 |    20     3     5  71.4 |
|    BAKE/USDT |     12 |           0.13 |           1.56 |             1.565 |           0.16 |         21:05:00 |     8     2     2  66.7 |
|    LINK/USDT |     14 |           0.08 |           1.16 |             1.161 |           0.12 |         21:09:00 |     8     5     1  57.1 |
|     GNO/USDT |      3 |           0.32 |           0.95 |             0.950 |           0.10 |         14:00:00 |     2     1     0   100 |
|     BNX/USDT |      2 |           0.44 |           0.89 |             0.886 |           0.09 |         11:30:00 |     2     0     0   100 |
|     RGT/USDT |      1 |           0.82 |           0.82 |             0.824 |           0.08 |         17:00:00 |     1     0     0   100 |
|    COTI/USDT |     15 |           0.04 |           0.62 |             0.619 |           0.06 |         17:08:00 |     9     3     3  60.0 |
|     ADX/USDT |      1 |           0.32 |           0.32 |             0.318 |           0.03 |         11:00:00 |     1     0     0   100 |
|     UMA/USDT |     27 |           0.01 |           0.30 |             0.302 |           0.03 |         18:04:00 |    17     3     7  63.0 |
|    DYDX/USDT |      2 |           0.09 |           0.18 |             0.176 |           0.02 |         15:00:00 |     1     1     0   100 |
|    SUSD/USDT |     52 |           0.00 |           0.10 |             0.102 |           0.01 |  1 day, 12:58:00 |    21    22     9  40.4 |
|    YFII/USDT |     17 |           0.00 |           0.07 |             0.073 |           0.01 |   1 day, 1:35:00 |    10     5     2  58.8 |
|     AMP/USDT |      0 |           0.00 |           0.00 |             0.000 |           0.00 |             0:00 |     0     0     0     0 |
| AUCTION/USDT |      0 |           0.00 |           0.00 |             0.000 |           0.00 |             0:00 |     0     0     0     0 |
|   JASMY/USDT |      0 |           0.00 |           0.00 |             0.000 |           0.00 |             0:00 |     0     0     0     0 |
|    KP3R/USDT |      0 |           0.00 |           0.00 |             0.000 |           0.00 |             0:00 |     0     0     0     0 |
|    MOVR/USDT |      0 |           0.00 |           0.00 |             0.000 |           0.00 |             0:00 |     0     0     0     0 |
|     PLA/USDT |      0 |           0.00 |           0.00 |             0.000 |           0.00 |             0:00 |     0     0     0     0 |
|   PORTO/USDT |      0 |           0.00 |           0.00 |             0.000 |           0.00 |             0:00 |     0     0     0     0 |
|    POWR/USDT |      0 |           0.00 |           0.00 |             0.000 |           0.00 |             0:00 |     0     0     0     0 |
|     PYR/USDT |      0 |           0.00 |           0.00 |             0.000 |           0.00 |             0:00 |     0     0     0     0 |
|    RNDR/USDT |      0 |           0.00 |           0.00 |             0.000 |           0.00 |             0:00 |     0     0     0     0 |
|     XTZ/USDT |     18 |          -0.00 |          -0.07 |            -0.066 |          -0.01 |         14:17:00 |    12     2     4  66.7 |
|     SFP/USDT |     22 |          -0.02 |          -0.33 |            -0.334 |          -0.03 |         19:30:00 |    15     3     4  68.2 |
|    ARDR/USDT |     32 |          -0.02 |          -0.65 |            -0.649 |          -0.06 |         16:21:00 |    24     2     6  75.0 |
|    USDP/USDT |      8 |          -0.15 |          -1.20 |            -1.196 |          -0.12 |  7 days, 9:45:00 |     0     4     4     0 |
|     KSM/USDT |     15 |          -0.08 |          -1.25 |            -1.249 |          -0.12 |   1 day, 5:28:00 |     9     4     2  60.0 |
|     YFI/USDT |     15 |          -0.09 |          -1.38 |            -1.377 |          -0.14 |         18:56:00 |     8     2     5  53.3 |
|     BNT/USDT |     15 |          -0.10 |          -1.53 |            -1.527 |          -0.15 |         18:24:00 |     8     5     2  53.3 |
|     BEL/USDT |     21 |          -0.14 |          -2.94 |            -2.940 |          -0.29 |         16:23:00 |    15     2     4  71.4 |
|     XEC/USDT |      4 |          -0.77 |          -3.08 |            -3.087 |          -0.31 |         19:15:00 |     2     1     1  50.0 |
|     ICP/USDT |      7 |          -0.45 |          -3.17 |            -3.176 |          -0.32 |   1 day, 3:51:00 |     3     3     1  42.9 |
|     BNB/USDT |     12 |          -0.31 |          -3.77 |            -3.772 |          -0.38 |         20:25:00 |     6     2     4  50.0 |
|   TRIBE/USDT |     13 |          -0.29 |          -3.77 |            -3.774 |          -0.38 |   1 day, 7:51:00 |     6     6     1  46.2 |
|    FARM/USDT |      7 |          -0.62 |          -4.37 |            -4.372 |          -0.44 |  1 day, 17:43:00 |     3     3     1  42.9 |
|     ETH/USDT |      9 |          -0.51 |          -4.55 |            -4.550 |          -0.45 |         20:20:00 |     6     0     3  66.7 |
|      DF/USDT |      4 |          -1.27 |          -5.07 |            -5.078 |          -0.51 |         17:15:00 |     2     1     1  50.0 |
|     MBL/USDT |     25 |          -0.21 |          -5.24 |            -5.241 |          -0.52 |         18:41:00 |    17     5     3  68.0 |
|    BAND/USDT |     23 |          -0.24 |          -5.49 |            -5.491 |          -0.55 |         22:26:00 |    12     6     5  52.2 |
|     ONT/USDT |     19 |          -0.29 |          -5.49 |            -5.498 |          -0.55 |         20:54:00 |    13     2     4  68.4 |
|    KEEP/USDT |     16 |          -0.36 |          -5.82 |            -5.829 |          -0.58 |   1 day, 1:22:00 |     6     8     2  37.5 |
|    KLAY/USDT |      6 |          -1.03 |          -6.18 |            -6.189 |          -0.62 | 2 days, 23:50:00 |     2     2     2  33.3 |
|    ALGO/USDT |     17 |          -0.37 |          -6.21 |            -6.220 |          -0.62 |         21:32:00 |    11     1     5  64.7 |
|     SXP/USDT |     19 |          -0.33 |          -6.34 |            -6.344 |          -0.63 |         15:28:00 |    14     0     5  73.7 |
|    REEF/USDT |     22 |          -0.30 |          -6.63 |            -6.638 |          -0.66 |         18:11:00 |    15     1     6  68.2 |
|     CKB/USDT |     18 |          -0.37 |          -6.68 |            -6.691 |          -0.67 |         19:30:00 |    12     2     4  66.7 |
|    AAVE/USDT |     12 |          -0.58 |          -6.90 |            -6.911 |          -0.69 |         18:10:00 |     8     1     3  66.7 |
|    MINA/USDT |      5 |          -1.48 |          -7.41 |            -7.414 |          -0.74 |  1 day, 17:36:00 |     2     1     2  40.0 |
|     SYS/USDT |      8 |          -1.06 |          -8.52 |            -8.526 |          -0.85 |   1 day, 3:38:00 |     5     1     2  62.5 |
|     REN/USDT |     16 |          -0.57 |          -9.15 |            -9.159 |          -0.92 |   1 day, 2:56:00 |     9     3     4  56.2 |
|     QNT/USDT |      4 |          -2.38 |          -9.50 |            -9.512 |          -0.95 |   1 day, 2:15:00 |     2     0     2  50.0 |
|      OM/USDT |     22 |          -0.43 |          -9.51 |            -9.523 |          -0.95 |         23:44:00 |    13     5     4  59.1 |
|    FIDA/USDT |      3 |          -3.60 |         -10.79 |           -10.804 |          -1.08 | 2 days, 19:20:00 |     2     0     1  66.7 |
|     CTK/USDT |     21 |          -0.51 |         -10.80 |           -10.809 |          -1.08 |   1 day, 7:31:00 |    11     7     3  52.4 |
|     REP/USDT |     26 |          -0.42 |         -10.89 |           -10.902 |          -1.09 |   1 day, 0:32:00 |    16     4     6  61.5 |
|    AUTO/USDT |     11 |          -0.99 |         -10.92 |           -10.926 |          -1.09 |   1 day, 6:49:00 |     5     3     3  45.5 |
|    RARE/USDT |      2 |          -5.51 |         -11.01 |           -11.023 |          -1.10 |  1 day, 19:00:00 |     0     1     1     0 |
|     MDT/USDT |     28 |          -0.40 |         -11.29 |           -11.303 |          -1.13 |   1 day, 4:56:00 |    16     7     5  57.1 |
|    PAXG/USDT |     30 |          -0.41 |         -12.20 |           -12.214 |          -1.22 |  1 day, 10:52:00 |    11     9    10  36.7 |
|     ADA/USDT |     17 |          -0.72 |         -12.23 |           -12.247 |          -1.22 |   1 day, 1:56:00 |     9     6     2  52.9 |
|    POLY/USDT |      5 |          -2.62 |         -13.12 |           -13.135 |          -1.31 |   1 day, 6:24:00 |     2     0     3  40.0 |
|     AVA/USDT |     21 |          -0.64 |         -13.45 |           -13.460 |          -1.35 |   1 day, 5:31:00 |    12     5     4  57.1 |
|     GTC/USDT |      7 |          -2.08 |         -14.56 |           -14.571 |          -1.46 |   1 day, 7:00:00 |     3     2     2  42.9 |
|     VGX/USDT |      1 |         -14.70 |         -14.70 |           -14.719 |          -1.47 |  2 days, 0:00:00 |     0     0     1     0 |
|     OMG/USDT |     19 |          -0.78 |         -14.77 |           -14.784 |          -1.48 |         18:51:00 |    10     3     6  52.6 |
|     MKR/USDT |     15 |          -1.00 |         -14.95 |           -14.962 |          -1.50 |   1 day, 7:20:00 |     9     3     3  60.0 |
|    DUSK/USDT |     24 |          -0.63 |         -15.12 |           -15.136 |          -1.51 |         21:18:00 |    14     5     5  58.3 |
|     YGG/USDT |      2 |          -7.84 |         -15.68 |           -15.693 |          -1.57 |   1 day, 8:30:00 |     1     0     1  50.0 |
|     CVP/USDT |      4 |          -4.03 |         -16.12 |           -16.133 |          -1.61 |  3 days, 6:00:00 |     1     1     2  25.0 |
|     BTS/USDT |     26 |          -0.64 |         -16.55 |           -16.569 |          -1.66 |         15:21:00 |    16     3     7  61.5 |
|     TRU/USDT |     28 |          -0.64 |         -17.83 |           -17.851 |          -1.79 |   1 day, 4:32:00 |    17     5     6  60.7 |
|     CFX/USDT |     15 |          -1.19 |         -17.90 |           -17.921 |          -1.79 |  1 day, 12:20:00 |     7     4     4  46.7 |
|     LSK/USDT |     29 |          -0.62 |         -18.11 |           -18.127 |          -1.81 |         18:46:00 |    21     2     6  72.4 |
|   FRONT/USDT |      3 |          -6.05 |         -18.14 |           -18.160 |          -1.82 |  2 days, 2:40:00 |     1     1     1  33.3 |
|     ELF/USDT |      9 |          -2.36 |         -21.25 |           -21.268 |          -2.13 |  1 day, 13:40:00 |     3     3     3  33.3 |
|     C98/USDT |      9 |          -2.44 |         -21.95 |           -21.972 |          -2.20 |   1 day, 1:20:00 |     6     1     2  66.7 |
|     BLZ/USDT |     19 |          -1.18 |         -22.41 |           -22.434 |          -2.24 |         23:00:00 |    11     3     5  57.9 |
|     FIL/USDT |     14 |          -1.62 |         -22.65 |           -22.673 |          -2.27 |         23:00:00 |     9     2     3  64.3 |
|   ALICE/USDT |     13 |          -1.94 |         -25.17 |           -25.195 |          -2.52 |   1 day, 3:00:00 |     6     3     4  46.2 |
|      QI/USDT |      1 |         -25.88 |         -25.88 |           -25.906 |          -2.59 |  1 day, 15:00:00 |     0     0     1     0 |
|     XRP/USDT |     15 |          -1.84 |         -27.62 |           -27.648 |          -2.76 |         19:24:00 |     8     2     5  53.3 |
|     FUN/USDT |     21 |          -1.36 |         -28.63 |           -28.657 |          -2.87 |   1 day, 0:03:00 |    14     1     6  66.7 |
|  ALPACA/USDT |      6 |          -4.80 |         -28.77 |           -28.800 |          -2.88 | 2 days, 15:30:00 |     2     1     3  33.3 |
|   BTCST/USDT |     15 |          -2.07 |         -31.09 |           -31.119 |          -3.11 |   1 day, 2:48:00 |    10     2     3  66.7 |
|   CHESS/USDT |      2 |         -15.57 |         -31.14 |           -31.169 |          -3.12 |  2 days, 1:30:00 |     0     1     1     0 |
|    DODO/USDT |     17 |          -1.91 |         -32.39 |           -32.419 |          -3.24 |         16:11:00 |    11     0     6  64.7 |
|     ONG/USDT |     32 |          -1.01 |         -32.39 |           -32.423 |          -3.24 |         22:38:00 |    21     6     5  65.6 |
|    LINA/USDT |     15 |          -2.52 |         -37.78 |           -37.819 |          -3.78 |   1 day, 3:36:00 |     8     3     4  53.3 |
|      AR/USDT |     14 |          -2.72 |         -38.02 |           -38.062 |          -3.81 |   1 day, 1:13:00 |     5     5     4  35.7 |
|    BEAM/USDT |     38 |          -1.05 |         -39.94 |           -39.979 |          -4.00 |   1 day, 3:58:00 |    24     6     8  63.2 |
|     MFT/USDT |     30 |          -1.34 |         -40.09 |           -40.129 |          -4.01 |         23:12:00 |    15     7     8  50.0 |
|    KAVA/USDT |     21 |          -1.95 |         -40.96 |           -40.999 |          -4.10 |   1 day, 5:43:00 |    12     2     7  57.1 |
|    ATOM/USDT |     18 |          -2.28 |         -41.00 |           -41.036 |          -4.10 |   1 day, 2:17:00 |     7     6     5  38.9 |
|     CLV/USDT |     10 |          -4.17 |         -41.67 |           -41.715 |          -4.17 |  2 days, 5:54:00 |     4     2     4  40.0 |
|   FORTH/USDT |     15 |          -2.90 |         -43.51 |           -43.558 |          -4.36 |  1 day, 13:48:00 |     4     7     4  26.7 |
|     SNX/USDT |     11 |          -4.19 |         -46.07 |           -46.119 |          -4.61 |         12:27:00 |     6     1     4  54.5 |
|     MLN/USDT |      8 |          -7.10 |         -56.84 |           -56.896 |          -5.69 | 2 days, 11:30:00 |     3     1     4  37.5 |
|     RLC/USDT |     19 |          -3.06 |         -58.16 |           -58.216 |          -5.82 |         19:38:00 |    10     3     6  52.6 |
|    SAND/USDT |     30 |          -2.12 |         -63.48 |           -63.544 |          -6.35 |   1 day, 8:42:00 |    18     5     7  60.0 |
|        TOTAL |   4719 |           0.99 |        4691.86 |          4696.551 |         469.66 |         22:51:00 |  3047   892   780  64.6 |
========================================================== BUY TAG STATS ===========================================================
|   TAG |   Buys |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |   Avg Duration |   Win  Draw  Loss  Win% |
|-------+--------+----------------+----------------+-------------------+----------------+----------------+-------------------------|
| TOTAL |   4719 |           0.99 |        4691.86 |          4696.551 |         469.66 |       22:51:00 |  3047   892   780  64.6 |
======================================================= SELL REASON STATS ========================================================
|        Sell Reason |   Sells |   Win  Draws  Loss  Win% |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |
|--------------------+---------+--------------------------+----------------+----------------+-------------------+----------------|
|                roi |    2269 |   1377   892     0   100 |           5.25 |       11915.1  |         11927     |          44.29 |
|        sell_signal |    1669 |   1669     0     0   100 |           1.26 |        2096.77 |          2098.87  |           7.79 |
| trailing_stop_loss |     767 |      0     0   767     0 |         -11.73 |       -9000.1  |         -9009.1   |         -33.46 |
|          stop_loss |      10 |      0     0    10     0 |         -31.14 |        -311.38 |          -311.69  |          -1.16 |
|         force_sell |       4 |      1     0     3  25.0 |          -2.13 |          -8.54 |            -8.545 |          -0.03 |
======================================================== LEFT OPEN TRADES REPORT =========================================================
|      Pair |   Buys |   Avg Profit % |   Cum Profit % |   Tot Profit USDT |   Tot Profit % |     Avg Duration |   Win  Draw  Loss  Win% |
|-----------+--------+----------------+----------------+-------------------+----------------+------------------+-------------------------|
| ROSE/USDT |      1 |           2.33 |           2.33 |             2.328 |           0.23 |          2:00:00 |     1     0     0   100 |
| PAXG/USDT |      1 |          -0.20 |          -0.20 |            -0.200 |          -0.02 |          1:00:00 |     0     0     1     0 |
| BZRX/USDT |      1 |          -0.52 |          -0.52 |            -0.519 |          -0.05 |          6:00:00 |     0     0     1     0 |
|  REP/USDT |      1 |         -10.14 |         -10.14 |           -10.154 |          -1.02 | 2 days, 17:00:00 |     0     0     1     0 |
|     TOTAL |      4 |          -2.13 |          -8.54 |            -8.545 |          -0.85 |         18:30:00 |     1     0     3  25.0 |
=============== SUMMARY METRICS ================
| Metric                 | Value               |
|------------------------+---------------------|
| Backtesting from       | 2021-01-01 00:00:00 |
| Backtesting to         | 2021-12-12 15:00:00 |
| Max open trades        | 269                 |
|                        |                     |
| Total/Daily Avg Trades | 4719 / 13.68        |
| Starting balance       | 1000.000 USDT       |
| Final balance          | 5696.551 USDT       |
| Absolute profit        | 4696.551 USDT       |
| Total profit %         | 469.66%             |
| Trades per day         | 13.68               |
| Avg. daily profit %    | 1.36%               |
| Avg. stake amount      | 100.000 USDT        |
| Total trade volume     | 471900.000 USDT     |
|                        |                     |
| Best Pair              | OXT/USDT 155.60%    |
| Worst Pair             | SAND/USDT -63.48%   |
| Best trade             | DNT/USDT 55.24%     |
| Worst trade            | MANA/USDT -31.14%   |
| Best day               | 184.460 USDT        |
| Worst day              | -274.863 USDT       |
| Days win/draw/lose     | 235 / 17 / 94       |
| Avg. Duration Winners  | 13:18:00            |
| Avg. Duration Loser    | 1 day, 14:54:00     |
| Rejected Buy signals   | 0                   |
|                        |                     |
| Min balance            | 988.138 USDT        |
| Max balance            | 5870.146 USDT       |
| Drawdown               | 731.08%             |
| Drawdown               | 731.814 USDT        |
| Drawdown high          | 3340.155 USDT       |
| Drawdown low           | 2608.341 USDT       |
| Drawdown Start         | 2021-05-08 17:00:00 |
| Drawdown End           | 2021-07-20 19:00:00 |
| Market change          | 512.58%             |
================================================
```