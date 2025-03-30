var log = require('../core/log.js');

var strat = {
    init: function() {
        this.requiredHistory = this.tradingAdvisor.historySize;

        this.addTulipIndicator('rsi', 'rsi', {
            optInTimePeriod: this.settings.rsiTimePeriod
        });     

        this.data = {
            entryPrice: undefined,
            exitPrice: undefined,
            slExitPrice: undefined 
        }
    },
    
    update: function(candle) {
        const price = candle.close;
    },

    check: function(candle) {
        const price = candle.close;

        // Buy
        if(this.data.entryPrice === undefined) {
            const percentDump = ((candle.close - candle.open) / candle.open) * 100;
            if( (percentDump <= this.settings.percentDump)
                && (this.tulipIndicators.rsi.result.result <= this.settings.lowerLimit)
            ) {
                this.data.entryPrice = price; 
                const tpPercent = (Math.abs(percentDump) * this.settings.tpPercentRatio) / 100; 
                this.data.exitPrice = price * (tpPercent + 1);
                if(this.settings.slRR !== 0) {
                    this.data.slExitPrice = price - (price * (tpPercent / this.settings.slRR));
                }
                this.advice('long');          
            }
        // Sell
        } else {
            if( price >= this.data.exitPrice
                || price <= this.data.slExitPrice
            ) {
                this.data.entryPrice = undefined;
                this.data.exitPrice = undefined;
                this.advice('short');
            }
        }
    },
};

module.exports = strat;