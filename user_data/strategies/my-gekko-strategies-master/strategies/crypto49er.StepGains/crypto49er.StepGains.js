/*

  StepGains - Crypto49er 2018-04-21

 */
// helpers
var _ = require('lodash');
var watchPrice = 0.0;
var lowestPrice = 0.0;
var sellPrice = 0.0;
var advised = false;

// Let's create our own buy and sell strategy 
var strat = {};

// Prepare everything our strat needs
strat.init = function() {
    // how many candles do we need as a base
  // before we can start giving advice?
  this.requiredHistory = this.tradingAdvisor.historySize;
  this.watchPriceBuy = this.settings.watchPriceBuy;
  this.watchPriceSell = this.settings.watchPriceSell;
}

// What happens on every new candle?
strat.update = function(candle) {
}

// For debugging purposes.
strat.log = function() {
}

// Based on the newly calculated
// information, check if we should
// update or not.
strat.check = function(candle) {

    if(watchPrice == 0){
        watchPrice = candle.close * this.watchPriceBuy;
    }
    if(candle.close <= watchPrice){
        lowestPrice = candle.close;
    }
    if(candle.close > lowestPrice && !advised){
        this.advice("long");
        sellPrice = candle.close * this.watchPriceSell;
        advised = true;
    }
    if(candle.close > sellPrice && watchPrice != 0 && lowestPrice != 0){
        this.advice("short");
        watchPrice = 0;
        lowestPrice = 0;
        buyPrice = 0;
        sellPrice = 0;
        advised = false;
    }

}

module.exports = strat;