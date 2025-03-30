// helpers
var _ = require('lodash');
var log = require('../core/log.js');
var PSAR = require('./indicators/PSAR.js');

// let's create our own method
var method = {};

// prepare everything our method needs
method.init = function() {
  this.name = 'PSAR';
  this.requiredHistory = this.tradingAdvisor.historySize;

  // define the indicators we need
  this.addIndicator('psar', 'PSAR', this.settings);
}

// what happens on every new candle?
method.update = function(candle) {
  // nothing!
}

// for debugging purposes: log the last calculated
 //method.log = function(candle) {
    //var digits = 8;
    //var psar = this.indicators.psar;
      
    //log.debug('calculated PSAR properties for candle:');
    //log.debug('\t', 'psar:', psar.result.toFixed(digits));
    //log.debug('\t', 'price:', candle.close.toFixed(digits));
    //}


method.check = function(candle) {
  var psar = this.indicators.psar;
  var psarVal = psar.result;
  var price = candle.close;
  var diff = price - psarVal;

  
  if(diff > 0) {
    log.debug('we are currently in uptrend', message);

    this.advice('long');
    
    
  } else if(diff < 0) {
    log.debug('we are currently in a downtrend', message);

    this.advice('short');
    }
    
    else {
    log.debug('we are currently not in an up or down trend', message);
    this.advice();
  }
}

module.exports = method;
