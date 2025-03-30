// Strategy for Bitcoin
// Strategy works best on 1 day candles.
// config.js must be set to 1 day candles under tradingadvisor for backtests: 
// candleSize: 60 * 24, // 60 minutes * 24 hours produce 1 day candles

var strat = {};

strat.init = function() {
  console.log("initialize Tulip indicators")
  this.addTulipIndicator('sma','sma', {
    optInTimePeriod: 23
  })
  this.addTulipIndicator('rsi','rsi', {
    optInTimePeriod: 14
  })
}


strat.check = function(candle) {
  var day = candle.start.format()
  // Determine sma and daily close price
  const sma = this.tulipIndicators.sma.result.result
  const rsi = this.tulipIndicators.rsi.result.result
  const candleclose = candle.close

  // If candleprice is higher than sma, go long
  if (candleclose > sma && rsi > 55) {
    // console.log(day, sma, candleclose, rsi)
    this.advice('long')
  }
  else {
    this.advice('short')
  }
}

module.exports = strat;
