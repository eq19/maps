// Strategy for Bitcoin
// Strategy works best on 1 day candles.
// config.js must be set to 1 day candles under tradingadvisor for backtests: 
// candleSize: 60 * 24, // 60 minutes * 24 hours produce 1 day candles

// Determine generic variables through the script
// e.g. the limit that has to cross before taking action
var bbandslimit = 0
var rsilimit = 50
var atrlimit = 0
var strat = {};

// Configure the indicators to use in this strategy
strat.init = function () {
  console.log("initialize Tulip indicators")
  this.addTulipIndicator('bbands', 'bbands', {
    optInTimePeriod: 23,
    optInNbStdDevs: 2
  })
  this.addTulipIndicator('rsi', 'rsi', {
    optInTimePeriod: 14
  })
  this.addTulipIndicator('atr', 'atr', {
    optInTimePeriod: 14
  })
}

// Start the actual strategy and check this on each candle.
// See config.js for the timeframe this candle is.
strat.check = function (candle) {
  // Configure the indicators for calculation in the strategy
  var day = candle.start.format()
  var bbandsLower = this.tulipIndicators.bbands.result.bbandsLower
  var bbandsMiddle = this.tulipIndicators.bbands.result.bbandsMiddle
  var bbandsUpper = this.tulipIndicators.bbands.result.bbandsUpper
  var rsi = this.tulipIndicators.rsi.result.result
  var atr = this.tulipIndicators.atr.result.result

  // === CONSOLE OUTPUT CONFIGURATION ===
  // Rounding the numbers for easier checking of the indicators on the console
  // Do not use rounded numbers when backtesting, they give worse results
  var candleclose = candle.close.toFixed(2)
  var bbandsnumLower = Number(bbandsLower); bbandsroundLower = bbandsnumLower.toFixed(2);
  var bbandsnumMiddle = Number(bbandsMiddle); bbandsroundMiddle = bbandsnumMiddle.toFixed(2);
  var bbandsnumUpper = Number(bbandsUpper); bbandsroundUpper = bbandsnumUpper.toFixed(2);
  var rsinum = Number(rsi); rsiround = rsinum.toFixed(2);
  var atrnum = Number(atr); atrround = atrnum.toFixed(2);
  // console.log("Date: " + day + "\n \t ClosePrice: " + candleclose + "\n \t bbandsLower: " + bbandsroundLower + "\t bbandsMiddle: " + bbandsroundMiddle + "\t bbandsUpper: " + bbandsroundUpper + "\n \t rsi: " + rsiround + "\t atr: " + atrround)

  // Determine here under which circumstanses you want to go long
  if (candleclose > bbandsMiddle && rsi > rsilimit) {
    // if (candleclose > bbandsMiddle) {
    this.advice('long')
  }
  // If the circumstanses do not meet, go short (do nothing...) 
  else {
    this.advice('short')
  }
}

module.exports = strat;
