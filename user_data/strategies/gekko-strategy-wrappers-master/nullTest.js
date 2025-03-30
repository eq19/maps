// Gab0 method of stacking strategies.
// two RSI_BULL_BEAR that are consulted depending on SMA result
// this concept is a sample, this is entirely customizable
// RSI_BULL_BEAR by @TommieHansen, sample concept by @BradT7

var _ = require('lodash');
var log = require('../core/log.js');
var Wrapper = require('./strategyWrapperRules');

// OUR STRATEGY INITS AS A WRAPPER OBJECT, NOT AS EMPTY {} ;
var method = Wrapper;
method.init = function() {

    this.age = 0;
    this.children = [];
    this.currentTrend;
    this.requiredHistory = -1;

    var STRATEGY = "RSI_BULL_BEAR";


   // here we init child strategies. 
   // take note that each one takes corresponding subdict of this.settings;
   // or just the full settings.. depending on the architecture employed;
   this.RBB = this.createChild(STRATEGY, this.settings);


}


method.update = function(candle) {
}


method.log = function() {
}



method.check = function(candle) {

    // this clear last advice and do a tick for each children strategy!
    this.checkChildren(candle);

    // if children strat sent advice, propogate it;
    // -> this is a dummy Wrapper;
    this.listenAdvice(this.RBB);


	// and thats it;
}


module.exports = method;
