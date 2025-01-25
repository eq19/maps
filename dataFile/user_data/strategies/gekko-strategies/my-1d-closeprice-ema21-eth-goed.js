// Strategy for Ethereum
// Strategy works best on 1 day candles.
// config.js must be set to 1 day candles under tradingadvisor for backtests: 
// candleSize: 60 * 24, // 60 minutes * 24 hours produce 1 day candles

var strat = {};

strat.init = function() {
  console.log("initialize Tulip indicators")
  this.addTulipIndicator('ema21','ema', {
    optInTimePeriod: 21
  })
}


strat.check = function(candle) {
  var day = candle.start.format()
  // Determine ema21 and daily close price
  const ema21 = this.tulipIndicators.ema21.result.result
  const candleclose = candle.close
  
  // Compare closeprice and ema21, then take appropriate action
  if (candleclose > ema21) {
    this.advice('long')
  }
  else {
    this.advice('short')
  }
}

module.exports = strat;