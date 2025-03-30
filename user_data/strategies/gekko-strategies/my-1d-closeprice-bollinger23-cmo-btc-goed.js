// Strategy for Bitcoin
// Strategy works best on 1 day candles.
// config.js must be set to 1 day candles under tradingadvisor for backtests: 
// candleSize: 60 * 24, // 60 minutes * 24 hours produce 1 day candles
// Update: This strategy performs with the following figures:
//
// 2020-05-01 13:40:37 (INFO):
// 2020-05-01 13:40:37 (INFO):     (PROFIT REPORT) start time:                      2017-09-11 00:00:00
// 2020-05-01 13:40:37 (INFO):     (PROFIT REPORT) end time:                        2020-04-18 00:01:00
// 2020-05-01 13:40:37 (INFO):     (PROFIT REPORT) timespan:                        3 years
// 2020-05-01 13:40:37 (INFO):     (PROFIT REPORT) exposure:                        0.4642101869808575
// 2020-05-01 13:40:37 (INFO):
// 2020-05-01 13:40:37 (INFO):     (PROFIT REPORT) start price:                     4153.62 USDT
// 2020-05-01 13:40:37 (INFO):     (PROFIT REPORT) end price:                       7044.35 USDT
// 2020-05-01 13:40:37 (INFO):     (PROFIT REPORT) Market:                          69.59543723%
// 2020-05-01 13:40:37 (INFO):
// 2020-05-01 13:40:37 (INFO):     (PROFIT REPORT) amount of trades:                78
// 2020-05-01 13:40:37 (INFO):     (PROFIT REPORT) original balance:                4000.00000000 USDT
// 2020-05-01 13:40:37 (INFO):     (PROFIT REPORT) current balance:                 27481.44379099 USDT
// 2020-05-01 13:40:37 (INFO):     (PROFIT REPORT) profit:                          23481.44379099 USDT (587.03609477%)
// 2020-05-01 13:40:37 (INFO):     (PROFIT REPORT) simulated yearly profit:         9027.805225812277 USDT (225.69513064530696%)
// 2020-05-01 13:40:37 (INFO):     (PROFIT REPORT) sharpe ratio:                    7.3620804095970405
// 2020-05-01 13:40:37 (INFO):     (PROFIT REPORT) expected downside:               -4.946606162398828

// Strategy for Bitcoin
// Strategy works best on 1 day candles.
// config.js must be set to 1 day candles under tradingadvisor for backtests: 
// candleSize: 60 * 24, // 60 minutes * 24 hours produce 1 day candles

// Determine generic variables through the script
// e.g. the limit that has to cross before taking action
var bbandslimit = 0
var cmolimit = 0
var atrlimit = 0
var strat = {};

// Configure the indicators to use in this strategy
strat.init = function() {
  console.log("initialize Tulip indicators")
  this.addTulipIndicator('bbands','bbands', {
    optInTimePeriod: 23,
    optInNbStdDevs: 2
  })
  this.addTulipIndicator('cmo','cmo', {
    optInTimePeriod: 14
  })
  this.addTulipIndicator('atr','atr', {
    optInTimePeriod: 14
  })
}

// Start the actual strategy and check this on each candle.
// See config.js for the timeframe this candle is.
strat.check = function(candle) {
  // Configure the indicators for calculation in the strategy
  var day = candle.start.format()
  var bbandsLower = this.tulipIndicators.bbands.result.bbandsLower
  var bbandsMiddle = this.tulipIndicators.bbands.result.bbandsMiddle
  var bbandsUpper = this.tulipIndicators.bbands.result.bbandsUpper
  var cmo = this.tulipIndicators.cmo.result.result
  var atr = this.tulipIndicators.atr.result.result

  // === CONSOLE OUTPUT CONFIGURATION ===
  // Rounding the numbers for easier checking of the indicators on the console
  // Do not use rounded numbers when backtesting, they give worse results
  var candleclose = candle.close.toFixed(2)
  var bbandsnumLower = Number(bbandsLower); bbandsroundLower = bbandsnumLower.toFixed(2);
  var bbandsnumMiddle = Number(bbandsMiddle); bbandsroundMiddle = bbandsnumMiddle.toFixed(2);
  var bbandsnumUpper = Number(bbandsUpper); bbandsroundUpper = bbandsnumUpper.toFixed(2);
  var cmonum = Number(cmo); cmoround = cmonum.toFixed(2);
  var atrnum = Number(atr); atrround = atrnum.toFixed(2);
  console.log("Date: " + day + "\n \t ClosePrice: " + candleclose + "\n \t bbandsLower: " + bbandsroundLower + "\t bbandsMiddle: " + bbandsroundMiddle + "\t bbandsUpper: " + bbandsroundUpper + "\n \t cmo: " + cmoround + "\t atr: " + atrround)

// Determine here under which circumstanses you want to go long
 if ( candleclose > bbandsMiddle && cmo > cmolimit) {
     this.advice('long')
   }
  // If the circumstanses do not meet, go short (do nothing...) 
  else {
     this.advice('short')
  }
}

module.exports = strat;
