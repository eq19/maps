# Mc Duck's Broker
![g12](https://user-images.githubusercontent.com/1235670/122944929-7f49a080-d378-11eb-9af9-a1525bcc6a18.png)

This is a combination of strategies and configurations for the Freqtrade bot.
For more information about Freqtrade, please visit their [documentation](https://www.freqtrade.io/).

Folder | &nbsp; | &nbsp;
---- | ---- | ----
**dev**|Development / testing of new strategies | local install
**test** | Dry run strategies | docker
**live** | Strategies in production | docker

## Notes
* Each strategy should have it's own configuration
* Secrets should go in config.private.json

## Configurations structure
The different parts of the bot's necessary configurations are broken into multiple relevant parts. This way it's easier to test a strategy with multiple stake currencies, exchanges or configurations.

The loading order of configurations should be as follows:
* config.base.json *loads generic options required by freqtrade*
* config.strategy*.json *custom configuration for the strategy*
* config.currency*.json *stake currency and pairs to use*
* config.exchange*.json *special configurations for the exchange*

## Strategies structure
The strategies should be located in /dev/user_data/strategies.

There will be a helper file ```custom_indicators.py``` that will contain the different indicators ported for use with this bot.

If the strategy can be optimized in any way (hyperopting or by manually editing the different values) then there should be at least to different strategy files: the main strategy and original values, a child strategy which inherits the main strategy and where we can modify and optimize the different signal values.


## How to start dev environment:

### Run Freqtrade's installer
* ```cd``` into dev folder.
* ```chmod +x setup.sh``` 
* ```./setup.sh --install```

**Note:** in order to generate plots and do hyperopts, install all the dependencies when asked.

## How to contribute to this repository

Everyone is encouraged to improve this repository, we are all here to learn and improve.

Just create a new branch to develop and test your new strategies.
You should create a new item in our board with your strategy description and if you can, backtesting and different plotting results. 
When you are satisfied with your results, don't hesitate to sent a PR.
