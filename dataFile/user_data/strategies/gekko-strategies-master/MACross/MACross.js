var log = require('../core/log.js');

class IndicatorTrend {
    constructor(){
        this.trend = undefined;
        this.persistUp = 0;
        this.persistDown = 0;
        this.prevVal = undefined;
        this.diff = 0;
    }

    update(indicatorValue) {
        if(this.prevVal !== undefined) {
            this.diff = indicatorValue - this.prevVal;
            this.trend = this.diff > 0 ? 'up' : 'down';
            this.persistUp = this.trend === 'up' ? this.persistUp + 1 : 0;
            this.persistDown = this.trend === 'down' ? this.persistDown + 1 : 0;
            this.prevVal = indicatorValue;
        } else if(indicatorValue !== undefined){
            this.prevVal = indicatorValue;
        }
    }
}

var strat = {
    init: function() {
        this.requiredHistory = this.tradingAdvisor.historySize;

        this.addTulipIndicator('shortma', 'sma', {
            optInTimePeriod: this.settings.shortMATimePeriod
        });

        this.addTulipIndicator('longma', 'sma', {
            optInTimePeriod: this.settings.longMATimePeriod
        });   
        
        this.addTulipIndicator('ao', 'ao');

        this.data = {
            trend: {
                bull: false,
                persist: 0,
                diff: 0
            },        
            ao: new IndicatorTrend(),
            shortMA: new IndicatorTrend(),
            longMA: new IndicatorTrend(),
            entryPrice: undefined 
        }
    },

    update: function(candle) {
        const price = candle.close;

        this.data.ao.update(this.tulipIndicators.ao.result.result);
        this.data.shortMA.update(this.tulipIndicators.shortma.result.result);
        this.data.longMA.update(this.tulipIndicators.longma.result.result);

        if((this.tulipIndicators.shortma.result.result !== undefined) && (this.tulipIndicators.longma.result.result !== undefined)) {
            this.data.trend.diff = this.tulipIndicators.shortma.result.result - this.tulipIndicators.longma.result.result;
            this.data.trend.bull = this.data.trend.diff > 0 ? true : false;
            this.data.trend.persist = this.data.trend.bull ? this.data.trend.persist + 1 : 0;
        }
    },

    check: function(candle) {
        const price = candle.close;

        // Buy
        if(this.data.entryPrice === undefined) {
            if(this.data.trend.bull) {
                if( (this.data.trend.persist >= this.settings.trendPersist)
                    && (this.data.ao.trend === 'up')
                    && (this.data.longMA.persistUp >= this.settings.lmaTrendPersist)
                ) {
                    this.data.entryPrice = price;                
                    this.advice('long');
                }
            } 
        // Sell            
        } else {
            if( !this.data.trend.bull 
                || (this.data.longMA.trend === 'down')
            ) {
                    this.data.entryPrice = undefined;
                    this.advice('short');                
            }
        }
    },
};

module.exports = strat;