// Strategy for Bitcoin
// Strategy works best on 1 day candles.
// config.js must be set to 1 day candles under tradingadvisor for backtests: 
// candleSize: 60 * 24, // 60 minutes * 24 hours produce 1 day candles

var strat = {};

strat.init = function () {
  console.log("initialize Tulip indicators")
  this.addTulipIndicator('sma', 'sma', {
    optInTimePeriod: 23
  })
  this.addTulipIndicator('rsi', 'rsi', {
    optInTimePeriod: 14
  })
  this.addTulipIndicator('kvo', 'kvo', {
    optInFastPeriod: 36,
    optInSlowPeriod: 55
  })
}

// Values for daytrading are rsi:55, kvo:5000
var rsilimit = 68
var kvolimit = -50000

strat.check = function (candle) {

  // Configure indicators for calculation
  var day = candle.start.format()
  var candleclose = candle.close.toFixed(2)
  var sma = this.tulipIndicators.sma.result.result
  var rsi = this.tulipIndicators.rsi.result.result
  var kvo = this.tulipIndicators.kvo.result.result

  // Rounding the numbers for easier checking of the indicators on the console
  // Do not use rounded numbers when backtesting, they give worse results
  var smanum = Number(sma); smaround = smanum.toFixed(2);
  var rsinum = Number(rsi); rsiround = rsinum.toFixed(2);
  var kvonum = Number(kvo); kvoround = kvonum.toFixed(2);
  console.log("Date: " + day + "\t ClosePrice: " + candleclose + "\t SMA: " + smaround + "\t RSI: " + rsiround + "\t KVO: " + kvoround)

  // If candleprice is higher than sma and rsi os over 55, go long
  if (candleclose > sma && rsi > rsilimit && kvo > kvolimit) {
    // if (candleclose > sma) {
    this.advice('long')
  }
  else {
    this.advice('short')
  }
}

module.exports = strat;
