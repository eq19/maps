var _ = require('lodash');

var Wrapper = {};
// SETUP BASE ATTRIBUTES OF THE STRATEGY (requiredHistory best at NULL which is -1);
Wrapper.children = [];
Wrapper.requiredHistory = -1;
Wrapper.age = 0;

// METHOD TO CREATE CHILDREN STRATEGY WITH GEKKO STRAT BASE CLASS INCORPORATED;
Wrapper.createChild = function(stratname, settings) {
    //  REPRODUCE STEPS ON gekko/plugins/tradingAdvisor.js

    var Consultant = require('../plugins/tradingAdvisor/baseTradingMethod');

    var stratMethod = require('./'+stratname+'.js');

    _.each(stratMethod, function(fn, name) {
        Consultant.prototype[name] = fn;
    });

    Consultant.prototype.collectAdvice = function(advice)
    {
        this.lastAdvice = advice;

    }
    var Strategy = new Consultant(settings);

    Strategy.on('advice', Strategy.collectAdvice );
    this.children.push(Strategy);
    return Strategy;

}

Wrapper.checkChildren = function(candle) {
_.each(this.children, function(child) {
    child.lastAdvice = false;
    child.tick(candle);
})
}

Wrapper.listenAdvice = function(child) {
if (child.lastAdvice) {
this.advice(child.lastAdvice.recommendation)
}
else {
this.advice()
}
}

module.exports = Wrapper;
