// Gab0 method of stacking strategies.
// two RSI_BULL_BEAR that are consulted depending on SMA result
// this concept is a sample, this is entirely customizable
// RSI_BULL_BEAR by @TommieHansen, sample concept by @BradT7

var _ = require('lodash');
var log = require('../core/log.js');
var Wrapper = require('./strategyWrapperRules');


var method = Wrapper;
method.init = function() {

    this.age = 0;

    this.currentTrend;
    this.requiredHistory = -1;

  // this SMA will choose wich RSI_BULL_BEAR will be asked for advice;
  // this is a part of this sample concept and is changeable;
  this.selector = this.addIndicator('selector', 'SMA', this.settings.selectorWeight);

   // here we init child strategies. 
   // take note that each one takes corresponding subdict of this.settings;
   this.RBB1 = this.createChild("RSI_BULL_BEAR", this.settings.RBB1);
   this.RBB2 = this.createChild("RSI_BULL_BEAR", this.settings.RBB2);

}


// what happens on every new candle?
method.update = function(candle) {
/*
    this.rsi = this.indicators.rsi.result;
    this.RSIhistory.push(this.rsi);

    if(_.size(this.RSIhistory) > this.interval)
		    // remove oldest RSI value
		    this.RSIhistory.shift();*/

}


method.log = function() {
    // for debugging purposes;;;

}

method.cloneCandle = function(candle) {
//well, some strategies take candle as argument of method.check, some get externally
//as method.candle SOMEHOW; this may be not necessary at all just a reminder - Gab0
return JSON.parse(JSON.stringify(candle));

}


method.check = function(candle) {

    var Selector = this.indicators.selector.result;
    //strategies have to tick on each main strat tick, else they lag behind
    //btw would be genius stuff to be able to skip this, to just "update". only ticking when necessary
    // (guess its impossible)

    // so all child strats should tick here; 
    this.checkChildren(candle);

    // now our strategy logic of selecting the consultant RBB;
    if (Selector > this.settings.selectorThreshold)
    {
       this.listenAdvice(this.RBB1);
    }
    else
    {
       this.listenAdvice(this.RBB2);
    }


}


module.exports = method;
