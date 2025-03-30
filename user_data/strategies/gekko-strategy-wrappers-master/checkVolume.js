// Gab0 method of stacking strategies.
// two RSI_BULL_BEAR that are consulted depending on SMA result
// this concept is a sample, this is entirely customizable
// RSI_BULL_BEAR by @TommieHansen, sample concept by @BradT7

var _ = require('lodash');
var log = require('../core/log.js');
var Wrapper = require('strategyWrapperRules');

// strategy first declared as Wrapper object!
var method = Wrapper;
method.init = function() {

    this.age = 0;

    this.currentTrend;
    this.requiredHistory = -1;


    var STRATEGY = "RSI_BULL_BEAR";
    this.STRATEGY = this.createChild(STRATEGY, this.settings);

    this.lastVolumesCount = this.settings.lastVolumes;

    this.lastVolumes = [];
}


method.update = function(candle) {

}


method.log = function() {

}


method.check = function(candle) {

    // childCheck required for each wrapper check;
    this.checkChildren();

    this.lastVolumes.push(candle.volume);

    if (this.lastVolumes.length > this.lastVolumesCount)
        this.lastVolumes.shift();

    // now our strategy logic of selecting the consultant RBB;

    var medianVolumes = this.lastVolumes.reduce(function(a,b){return a+b;},0);
    if (candle.volume > medianVolumes)
        this.listenAdvice(this.STRATEGY);


	// and thats it;
}

module.exports = method;
