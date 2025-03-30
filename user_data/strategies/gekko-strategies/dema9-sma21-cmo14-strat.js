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

  // Determine here under which circumstanses you want to go long
  // if (dema > sma) {
  if (dema > sma && cmo > cmolimit) {
    this.advice('long')
  }
  // If the circumstanses do not meet, go short (do nothing...) 
  else {
    this.advice('short')
  }
}

module.exports = strat;