# stratscorer
Tool for backtesting and scoring algorithmic strategies based on Freqtrade backtesting output

## Issues and solutions

### ERROR - Directory `/opt/stratscorer/user_data` does not exist.

**Problem**

After installing stratscorer, starting the script shows an error similar like this:

```
$ ./start.py
2023-02-16 20:53:37,448 - freqtrade - INFO - freqtrade 2023.1
2023-02-16 20:53:37,451 - freqtrade.configuration.load_config - INFO - Using config: /opt/freqtrade/user_data/spot_config.json ...
2023-02-16 20:53:37,451 - freqtrade.loggers - INFO - Verbosity set to 0
2023-02-16 20:53:37,452 - freqtrade.configuration.configuration - INFO - Using max_open_trades: 10 ...
2023-02-16 20:53:37,452 - freqtrade - ERROR - Directory `/opt/stratscorer/user_data` does not exist. Please use `freqtrade create-userdir` to create a user directory
```

**Solution**

Freqtrade by default searches in the directory Directory ``./user_data/.`` for user data. Add the following line with the full path to your config.json file (or other freqtrade configuration file you are currently using):

```
 "user_data_dir": "/dir/to/freqtrade/user_data/",
```

For example like this:

```
    "bot_name": "freqtrade",
    "initial_state": "running",
    "user_data_dir": "/dir/to/freqtrade/user_data/",
    "force_entry_enable": false,
    "internals": {
        "process_throttle_secs": 5
    }
```

# Strategy sources

There are many sources where to find strategies. One of the websites that has given me lot's of inspiration is: https://bt.robot.co.network/
On the webpage http://140.238.173.243/strategies.php is a list of github scraped strategies where I can try to download more than enough strategies for my youtube movies.
THe website also has some quantstats for a strategy. See: http://140.238.173.243/quant.php?hash=54ee97a63c383c599a330d8ebe34bb455d9ac5a81502a1f573deb0d5bb21dc53&month=202304&config=kucoin_USDT.html&strategy=EI3v2_tag_cofi_green. Based on: https://github.com/ranaroussi/quantstats


