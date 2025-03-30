// Strategy for Bitcoin
// Strategy works best on 4 HOUR candles!!
// config.js must be set to 1 day candles under tradingadvisor for backtests: 
// candleSize: 60 * 24, // 60 minutes * 24 hours produce 1 day candles
// Update: This strategy performs with the following figures:
//
// 2020-05-15 20:02:07 (INFO):
// 2020-05-15 20:02:07 (INFO):     (PROFIT REPORT) start time:                      2017-09-12 15:59:00
// 2020-05-15 20:02:07 (INFO):     (PROFIT REPORT) end time:                        2020-04-18 00:01:00
// 2020-05-15 20:02:07 (INFO):     (PROFIT REPORT) timespan:                        3 years
// 2020-05-15 20:02:07 (INFO):     (PROFIT REPORT) exposure:                        0.519507147763404
// 2020-05-15 20:02:07 (INFO):
// 2020-05-15 20:02:07 (INFO):     (PROFIT REPORT) start price:                     4258.72 USDT
// 2020-05-15 20:02:07 (INFO):     (PROFIT REPORT) end price:                       7044.35 USDT
// 2020-05-15 20:02:07 (INFO):     (PROFIT REPORT) Market:                          65.41002930%
// 2020-05-15 20:02:07 (INFO):
// 2020-05-15 20:02:07 (INFO):     (PROFIT REPORT) amount of trades:                292
// 2020-05-15 20:02:07 (INFO):     (PROFIT REPORT) original balance:                4000.00000000 USDT
// 2020-05-15 20:02:07 (INFO):     (PROFIT REPORT) current balance:                 29608.54360071 USDT
// 2020-05-15 20:02:07 (INFO):     (PROFIT REPORT) profit:                          25608.54360071 USDT (640.21359002%)
// 2020-05-15 20:02:07 (INFO):     (PROFIT REPORT) simulated yearly profit:         9862.897842825185 USDT (246.5724460706296%)
// 2020-05-15 20:02:07 (INFO):     (PROFIT REPORT) sharpe ratio:                    30.02254704722622
// 2020-05-15 20:02:07 (INFO):     (PROFIT REPORT) expected downside:               -3.137037874492998


// Determine generic variables through the script
// e.g. the limit that has to cross before taking action
var cmolimit = 0
var strat = {};

// Configure the indicators to use in this strategy
strat.init = function () {
  this.addTulipIndicator('dema', 'dema', {
    optInTimePeriod: 9
  })
  this.addTulipIndicator('sma', 'sma', {
    optInTimePeriod: 21
  })
  this.addTulipIndicator('cmo', 'cmo', {
    optInTimePeriod: 14
  })
}

// Start the actual strategy and check this on each candle.
// See config.js for the timeframe this candle is.
strat.check = function (candle) {
  // Configure the indicators for calculation in the strategy
  var day = candle.start.format()
  var dema = this.tulipIndicators.dema.result.result
  var sma = this.tulipIndicators.sma.result.result
  var cmo = this.tulipIndicators.cmo.result.result

  // === CONSOLE OUTPUT CONFIGURATION ===
  // Rounding the numbers for easier checking of the indicators on the console
  // Do not use rounded numbers when backtesting, they give worse results
  var candleclose = candle.close.toFixed(2)
  var demanum = Number(dema); demaround = demanum.toFixed(2);
  var smanum = Number(sma); smaround = smanum.toFixed(2);
  var cmonum = Number(cmo); cmoround = cmonum.toFixed(2);

  console.log("Date: " + day + "\n \t ClosePrice: " + candleclose + "\n \t dema: " + demaround + "\t sma: " + smaround + "\n \t cmo: " + cmoround)

  // Determine here under which circumstanses you want to go long
  if (dema > sma) {
    // if ( dema > sma && cmo > cmolimit) {
    this.advice('long')
  }
  // If the circumstanses do not meet, go short (do nothing...) 
  else {
    this.advice('short')
  }
}

module.exports = strat;