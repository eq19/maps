// Strategy for Ethereum
// Strategy works best on 1 day candles.
// config.js must be set to 1 day candles under tradingadvisor for backtests: 
// candleSize: 60 * 24, // 60 minutes * 24 hours produce 1 day candles

var strat = {};

strat.init = function() {
  console.log("initialize Tulip indicators")
  this.addTulipIndicator('sma','sma', {
    optInTimePeriod: 21
  })
}


strat.check = function(candle) {
  var day = candle.start.format()
  // Determine sma and daily close price
  const sma = this.tulipIndicators.sma.result.result
  const candleclose = candle.close

  // Compare closeprice and ema, then take appropriate action
  if (candleclose > sma) {
    this.advice('long')
  }
  else {
    this.advice('short')
  }
}

module.exports = strat;