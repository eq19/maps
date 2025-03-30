# RSI_Bull_Bear_Adx_M1

From: https://forum.gekko.wizb.it/thread-57778.html

This is more a share of the method I'm using for candle batching than of the strategy, but as Tommies RSI strat is rather excellent and so widely known it seemed a good demonstrator.

This strategy runs on 1 minute candles and batches them in the update function. 
The less obvious bit is that instead of keeping one copy of each indicator, it keeps an array of each indicator as long as the candle size for that indicator. Each new minute candle, the next indicator in the array is updated and read. 
The upshot of this is that each minute there is an up to date result of the longer term indicator, allowing far more accurate entry and exit points checked every minute, instead of every 5, 10, 30, 60 etc minutes. This also makes a strategy less sensitive to start time - although it still makes more of a difference than I'd expect!

The timeframe for each indicator is also independent so different candle sizes can be used for bear and bull market indicators - however the indicator candle size and indicator period do become a little interchangeable as they're both changing the amount of time that the indicator is watching the market over.

Other benefits of running at 1 minute is that any stop losses or take profits that you might add can be checked that much more frequently, so are that much more useful at catching quick market movements.

Downsides:

* As with any strategy running on very short timeframes trying to tune it with GA style optimisers can results in huge profits with hundreds of trades per day that will perform absolutely miserably if ran live as the orders simply can't be filled. Tuning requires a little more understanding of what the strategy is doing and inputting sensible parameters.
* Gekko currently has a limitation on the number of candles it can pre-seed a strategy with of around 4000. When running at 1 minute, this is 2.7 days of history so you need to shrink those long SMAs

