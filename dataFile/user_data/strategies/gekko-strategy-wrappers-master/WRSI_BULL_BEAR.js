

var Wrapper = require('./strategyWrapperRules.js');
var strategy = Wrapper;
var config = require ('../core/util.js').getConfig();

strategy.init = function() {


    this.requiredHistory = config.tradingAdvisor.historySize;
    this.addIndicator('maSlow', 'SMA',  this.settings.SMA_long);
    this.addIndicator('maFast', 'SMA',  this.settings.SMA_short);

    var BULL_SETTINGS = {
        'RSI': this.settings.BULL_RSI,
        'RSI_high': this.settings.BULL_RSI_high,
        'RSI_low': this.settings.BULL_RSI_low
    };

    var BEAR_SETTINGS = {
        'RSI': this.settings.BEAR_RSI,
        'RSI_high': this.settings.BEAR_RSI_high,
        'RSI_low': this.settings.BEAR_RSI_low
    };

    this.RSI_BULL = this.createChild("RSI_COMPONENT", BULL_SETTINGS);
    this.RSI_BEAR = this.createChild("RSI_COMPONENT", BEAR_SETTINGS);

};




strategy.check = function(candle) {

    this.checkChildren(candle);

    let ind = this.indicators,
        maSlow = ind.maSlow.result,
        maFast = ind.maFast.result;

    if (maFast < maSlow)
    {
        this.listenAdvice(this.RSI_BEAR);
    }
    else
    {
        this.listenAdvice(this.RSI_BULL);
    }
}

module.exports = strategy;
