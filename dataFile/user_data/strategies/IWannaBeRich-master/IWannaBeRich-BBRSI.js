/*
  IWannaBeRich strategy - 2018-05-03
 */
// helpers
var _ = require('lodash');
var log = require('../core/log.js');

var bb = require('./indicators/BB.js');
var rsi = require('./indicators/RSI.js');

// let's create our own strat
var strat = {};


// prepare everything our strat needs
strat.init = function () {
  this.name = 'IWannaBeRich-BBRSI';
  this.nsamples = 0;
  this.trend = {
    //zone: 'none',  // none, top, high, low, bottom
    duration: 0,
    persisted: false,
    direction: '', //up, down
    adviced: false 
  //  max: 0,
  //  min: 0
  };

  this.requiredHistory = this.tradingAdvisor.historySize;

  // define the indicators we need
  this.addIndicator('bb', 'BB', this.settings.bbands);
  this.addIndicator('rsi', 'RSI', this.settings.rsi);
}


// what happens on every new candle?
strat.update = function(candle) {
  // 
  /*this.trend = {
    //zone: this.trend.zone, 
    duration: this.trend.duration,
    persisted: this.trend.persisted,
    direction: 
    adviced: this.trend.adviced
    //max: Math.max(this.trend.max, candle.close),
    //min: Math.min(this.trend.min, candle.close)
  }*/
}

// for debugging purposes log the last
// calculated parameters.
strat.log = function (candle) {
   var digits = 8;
   
   var bb = this.indicators.bb;
   var rsi = this.indicators.rsi;

   //BB logging
   //BB.lower; BB.upper; BB.middle are your line values
   log.debug('______________________________________');
   log.debug('calculated BB properties for candle ', this.nsamples);

   if (bb.upper > candle.close) log.debug('\t', 'Upper BB:', bb.upper.toFixed(digits));
   if (bb.middle > candle.close) log.debug('\t', 'Mid   BB:', bb.middle.toFixed(digits));
   if (bb.lower >= candle.close) log.debug('\t', 'Lower BB:', bb.lower.toFixed(digits));
   log.debug('\t', 'price:', candle.close.toFixed(digits));
   if (bb.upper <= candle.close) log.debug('\t', 'Upper BB:', bb.upper.toFixed(digits));
   if (bb.middle <= candle.close) log.debug('\t', 'Mid   BB:', bb.middle.toFixed(digits));
   if (bb.lower < candle.close) log.debug('\t', 'Lower BB:', bb.lower.toFixed(digits));
   log.debug('\t', 'Band gap: ', bb.upper.toFixed(digits) - bb.lower.toFixed(digits));

   //RSI logging
   log.debug('calculated RSI properties for candle:');
   log.debug('\t', 'rsi:', rsi.result.toFixed(digits));
   log.debug('\t', 'price:', candle.close.toFixed(digits)); 
}

// Based on the newly calculated
// information, check if we should
// update or not.
strat.check = function (candle) {
  var bb = this.indicators.bb;
  var price = candle.close;
  this.nsamples++;

  var rsi = this.indicators.rsi;
  var rsiVal = rsi.result;

  //uptrend
  if (price <= bb.lower && rsiVal <= this.settings.rsi.low) {
      // new trend detected
      if(this.trend.direction !== 'up'){
         // reset the state for the new trend
        this.trend = {
          duration: 0,
          persisted: false,
          direction: 'up',
          adviced: false
        };
      }
      this.trend.duration++;
      log.debug('In uptrend since', this.trend.duration, 'candle(s)');

      if(this.trend.duration >= this.settings.rsi.persistence){
          this.trend.persisted = true;
      }

      if(this.trend.persisted && !this.trend.adviced) {
        this.trend.adviced = true;
        this.advice('long');
      } else
        this.advice();
      
      return;
  }
  
  //downtrend
  if (price > bb.middle && rsiVal >= this.settings.rsi.high) {
    // new trend detected
    if(this.trend.direction !== 'down'){
      // reset the state for the new trend
      this.trend = {
      duration: 0,
      persisted: false,
      direction: 'down',
      adviced: false
      };
    }

    this.trend.duration++;

    log.debug('In downtrend since', this.trend.duration, 'candle(s)');

    if(this.trend.duration >= this.settings.rsi.persistence){
      this.trend.persisted = true;
    }

    if(this.trend.persisted && !this.trend.adviced) {
      this.trend.adviced = true;
      this.advice('short');
    } else
      this.advice();

    return;
  }

  //no trend
  this.trend.advice = '';
  this.advice();

}


// Optional for executing code
// after completion of a backtest.
// This block will not execute in
// live use as a live gekko is
// never ending.
strat.end = function() {
  // your code!
}

module.exports = strat;
