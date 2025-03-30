// Strategy for Bitcoin
// Strategy works best on 3 day candles.
// config.js must be set to 3 day candles under tradingadvisor for backtests: 
// candleSize: 60 * 72, // 60 minutes * 48 hours produce 3 day candles

var strat = {};

strat.init = function() {
  console.log("initialize Tulip indicators")
  this.addTulipIndicator('sma','sma', {
    optInTimePeriod: 24 // 24 seems to give the best results
  })
}


strat.check = function(candle) {
  var day = candle.start.format()
  // Determine ema21 and daily close price
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

