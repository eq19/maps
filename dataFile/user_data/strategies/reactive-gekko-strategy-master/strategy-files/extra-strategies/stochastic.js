const log = require('../core/log.js');
const config = require('../core/util.js').getConfig();
const strat = {};

const talib = require('talib');

const Position = {
  ABOVE: !!1,
  BELOW: !!0
};

strat.init = function() {
  this.requiredHistory = config.tradingAdvisor.historySize;

  this.addTalibIndicator('mystoch', 'stoch', this.settings);

  this.position = null;

  this.last = {
    outSlowK: null,
    outSlowD: null
  }
}

strat.update = function(candle) {

}

strat.log = function() {
  // your code!
}

strat.check = function(candle) {
  const {outSlowK, outSlowD} = this.talibIndicators.mystoch.result;
  // console.log(outSlowK, outSlowD);
  if (this.last.outSlowD && this.last.outSlowK) {
    const lastVergence = this.vergence(this.last.outSlowD, this.last.outSlowK);
    const currVergence = this.vergence(outSlowD, outSlowK);
    const hasFlipped = lastVergence != currVergence;
    const position = this.getPosition(outSlowD, outSlowK);

    if (hasFlipped) {
      if (position == Position.ABOVE) {
        this.advice('short');

      } else if (position == Position.BELOW) {
        this.advice('long');

      }
    }
  }

  this.last = {outSlowK, outSlowD};
}

strat.getPosition = function(d, k) {
  return d > k;
}

strat.vergence = function(d, k) {
  return d > k;
}

module.exports = strat;
