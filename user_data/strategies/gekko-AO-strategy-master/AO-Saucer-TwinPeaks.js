const log = require('../core/log');
const AO = require('../strategies/indicators/AO.js');

// Let's create our own strat
var strat = {};
var aoInd = new AO();
var aoLast30 = [];

// Prepare everything our method needs
strat.init = function() {
  this.input = 'candle';
  this.requiredHistory = 34;
}

// What happens on every new candle?
strat.update = function(candle) {
  aoInd.update(candle);
  if (aoInd.result) {
    console.log('AO: ', aoInd.result.toFixed(2));
    aoLast30.push(aoInd.result);
    if (aoLast30.length > 30){
      aoLast30.shift();
    }
}

// For debugging purposes.
strat.log = function() {

  }
}

// Based on the newly calculated
// information, check if we should
// update or not.
strat.check = function(candle) {

  if (aoLast30.length == 30){

    // Sell if 3 red histograms bars (all above 0)
    if (aoLast30[29] < aoLast30[28] && aoLast30[28] < aoLast30[27] && aoLast30[27] > 0){
      this.advice('short');
    }

    //Buy on zero line upward cross
    if (aoLast30[29] > 0 && aoLast30[28] < 0 && aoLast30[27] < 0){
      this.advice('long');
    }

    // //Sell on zero line downward cross
    // if (aoLast30[29] < 0 && aoLast30[28] > 0 && aoLast30[27] > 0){
    //   this.advice('short');
    // }

    // Buy on bullish saucer
    if (aoLast30[27] > aoLast30[28] && aoLast30[29] > aoLast30[28] && aoLast30[27] > 0 && aoLast30[28] > 0 && aoLast30[29] > 0){
      this.advice('long');
    }

    // Twin peaks: if bullish saucer forms below zero line
    if (aoLast30[27] > aoLast30[28] && aoLast30[29] > aoLast30[28] && aoLast30[27] < 0 && aoLast30[28] < 0 && aoLast30[29] < 0){
      // Check if array is above zero line, break if it is
      for (i in aoLast30){
        //console.log(aoLast30[i]);
        if (aoLast30[i] > 0) {
          //console.log('One bar in aoLast30 > 0')
          return;
        }
        // j = 3rd candle, k = 2nd candle, l = 1st candle of any potential saucer
        //console.log('All 30 candles less than 0')
        var j = i, k = i + 1, l = i + 2;
        if (i + 1 != aoLast30.length) {
              // if l > k && j > k && l has a gap from current saucer, send buy signal (twin peaks)
          if (aoLast30[l] > aoLast30[k] && aoLast30[j] > aoLast30[k] && l < 24){
            this.advice('long');
          }
        }

      }
  
    }
  }







  // Sell on Twin Peaks above zero line


  
}

module.exports = strat;
