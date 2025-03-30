// Gab0 method of stacking strategies.
// two RSI_BULL_BEAR that are consulted depending on SMA result
// this concept is a sample, this is entirely customizable
// RSI_BULL_BEAR by @TommieHansen, sample concept by @BradT7

var _ = require('lodash');
var log = require('../core/log.js');
var Wrapper = require('./strategyWrapperRules');

// strategy first declared as Wrapper object!
var method = Wrapper;
method.init = function() {

    var STRATEGY = "RSI_BULL_BEAR";
    this.STRATEGY = this.createChild(STRATEGY, this.settings);

    // SCALPER SETTINGS;
    this.delay = this.settings.scalperDelay; // IN CANDLES;
    this.thresholdPercent = this.settings.scalperThresholdPercent;

	  this.initOnHold();
}


method.update = function(candle) {

}


method.log = function() {

}

method.initOnHold = function () {
    this.adviceOnHold = false;
    this.holdAge = 0;
    this.originalPrice = 0;
}

method.check = function(candle) {

    // childCheck required for each wrapper check;
    this.checkChildren(candle);

	  if (this.adviceOnHold)
	  {
	      if (this.holdAge > this.delay)
        {
	          this.initOnHold();
        } else {
	          var modPercentile = this.originalPrice * (this.thresholdPercent / 100);
	          if (this.adviceOnHold == 'long')
            {
		            var proceedAdvice = candle.close <= this.originalPrice - modPercentile;
                
            }	
            if (this.adviceOnHold == 'short')
            {
	              var proceedAdvice = candle.close >= this.originalPrice + modPercentile;
            }

        if (proceedAdvice)
            {
	              this.advice(this.adviceOnHold);
	              this.initOnHold();
            } else
            {
                this.holdAge++;
            }

        }
    }



    if (this.STRATEGY.lastAdvice)
    {
	      this.adviceOnHold = this.STRATEGY.lastAdvice.recommendation;
	      this.originalPrice = candle.close;
    }

	// and thats it;
}

module.exports = method;
