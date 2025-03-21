

oneYearAgo=$$(date -v -365d '+%Y%m%d')
6monthsAgo=$$(date -v -183d '+%Y%m%d')
twoYearAgo=$$(date -v -730d '+%Y%m%d')
backtestStartDate=$$(date -v -7d '+%Y%m%d')
hyperoptStartDate=$(6monthsAgo)
hyperoptEndDate=$$(date -v -8d '+%Y%m%d')


get-days:
	@echo $(hyperoptStartDate)
	@echo $(hyperoptEndDate)

download-data:
	@echo "Downloading Data..."
	docker compose run --rm freqtrade download-data --config user_data/config.json --timeframes 15m --timerange $(hyperoptStartDate)-

download-data-detail:
	@echo "Downloading Data..."
	docker compose run --rm freqtrade download-data --config user_data/config.json --timeframes 5m 15m --timerange $(hyperoptStartDate)-

optimize-all:
	@echo "Optimizing All Spaces..."
	docker compose run --rm freqtrade hyperopt --hyperopt-loss ComprehensiveTradeOptimizationLoss --strategy AwesomeCombinationStrategy --config user_data/config.json -e 4500 --timerange $(hyperoptStartDate)-$(hyperoptEndDate) --timeframe 15m --spaces all

optimize-default:
	@echo "Optimizing Default Spaces..."
	docker compose run --rm freqtrade hyperopt --hyperopt-loss DefaultSpaceCombinedHyperOptLoss --strategy AwesomeCombinationStrategy --config user_data/config.json -e 4500 --timerange $(hyperoptStartDate)-$(hyperoptEndDate) --timeframe 15m --spaces default
	# docker compose run --rm freqtrade hyperopt --hyperopt-loss ComprehensiveTradeOptimizationLoss --strategy AwesomeCombinationStrategy --config user_data/config.json -e 4500 --timerange $(hyperoptStartDate)-$(hyperoptEndDate) --timeframe 15m --spaces default

optimize-default-detail:
	@echo "Optimizing Default Spaces..."
	docker compose run --rm freqtrade hyperopt --hyperopt-loss DefaultSpaceCombinedHyperOptLoss --strategy AwesomeCombinationStrategy --config user_data/config.json -e 3000 --timerange $(hyperoptStartDate)-$(hyperoptEndDate) --timeframe 15m --timeframe-detail 5m --spaces default

optimize-buy:
	@echo "Optimizing Buy Space..."
	docker compose run --rm freqtrade hyperopt --hyperopt-loss SharpeHyperOptLoss --strategy AwesomeCombinationStrategy --config user_data/config.json -e 500 --timerange $(hyperoptStartDate)-$(hyperoptEndDate) --timeframe 15m --spaces buy --timeframe-detail 5m
	# docker compose run --rm freqtrade hyperopt --hyperopt-loss BuySpaceCombinedHyperOptLoss --strategy AwesomeCombinationStrategy --config user_data/config.json -e 500 --timerange $(hyperoptStartDate)-$(hyperoptEndDate) --timeframe 15m --spaces buy --timeframe-detail 5m

optimize-sell:
	@echo "Optimizing Sell Space..."
	docker compose run --rm freqtrade hyperopt --hyperopt-loss SortinoHyperOptLoss --strategy AwesomeCombinationStrategy --config user_data/config.json -e 500 --timerange $(hyperoptStartDate)-$(hyperoptEndDate) --timeframe 15m --spaces sell --timeframe-detail 5m

optimize-roi:
	@echo "Optimizing ROI Space..."
	docker compose run --rm freqtrade hyperopt --hyperopt-loss ProfitDrawDownHyperOptLoss --strategy AwesomeCombinationStrategy --config user_data/config.json -e 500 --timerange $(hyperoptStartDate)-$(hyperoptEndDate) --timeframe 15m --spaces roi --timeframe-detail 5m

optimize-stoploss:
	@echo "Optimizing Stoploss Space..."
	docker compose run --rm freqtrade hyperopt --hyperopt-loss MaxDrawDownRelativeHyperOptLoss --strategy AwesomeCombinationStrategy --config user_data/config.json -e 300 --timerange $(hyperoptStartDate)-$(hyperoptEndDate) --timeframe 15m --spaces stoploss

optimize-trailing:
	@echo "Optimizing Trailing Space..."
	docker compose run --rm freqtrade hyperopt --hyperopt-loss CalmarHyperOptLoss --strategy AwesomeCombinationStrategy --config user_data/config.json -e 300 --timerange $(hyperoptStartDate)-$(hyperoptEndDate) --timeframe 15m --spaces trailing

optimize-trades:
	@echo "Optimizing Trades Space..."
	docker compose run --rm freqtrade hyperopt --hyperopt-loss ShortTradeDurHyperOptLoss --strategy AwesomeCombinationStrategy --config user_data/config.json -e 100 --timerange $(hyperoptStartDate)-$(hyperoptEndDate) --timeframe 15m --spaces trades

optimize-protection:
	@echo "Optimizing Protection Space..."
	docker compose run --rm freqtrade hyperopt --hyperopt-loss SortinoHyperOptLoss --strategy AwesomeCombinationStrategy --config user_data/config.json -e 300 --timerange $(hyperoptStartDate)-$(hyperoptEndDate) --timeframe 15m --spaces protection

backtest:
	@echo "Conducting Backtest..."
	docker compose run --rm freqtrade backtesting --strategy AwesomeCombinationStrategy --dry-run-wallet 963 --timerange $(backtestStartDate)- --export none

backtest-detail:
	@echo "Conducting Backtest..."
	docker compose run --rm freqtrade backtesting --strategy AwesomeCombinationStrategy --timeframe-detail 15m --dry-run-wallet 963 --timerange $(backtestStartDate)- --export none

show-backtest-results:
	@echo "Show Backtest Results..."
	docker compose run --rm freqtrade backtesting-show --show-pair-list

test-pairlist:
	@echo "Test Pairlist..."
	docker compose run --rm freqtrade test-pairlist --config user_data/config-with-dynamic-pairlist-15m.json --quote USDT

edge-positions:
	@echo "Edge Positions"
	docker compose run --rm freqtrade edge --config user_data/config.json --strategy AwesomeCombinationStrategy --timerange $(hyperoptStartDate)-$(hyperoptEndDate)

optimize-spaces:
	make optimize-buy & make optimize-sell & make optimize-roi & make optimize-stoploss & make optimize-trailing & make optimize-trades & make optimize-protection
