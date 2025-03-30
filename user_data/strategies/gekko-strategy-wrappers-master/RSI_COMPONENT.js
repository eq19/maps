
var strategy = {};

strategy.init = function(){
    this.addIndicator('RSI', 'RSI', { interval: this.settings.RSI});

    this.resetTrend();
};

strategy.check = function() {

    var ind = this.indicators;
    var rsi = ind.RSI.result;
    if ( rsi > this.settings.RSI_high ) this.short();
    else if( rsi < this.settings.RSI_low ) this.long();

};

strategy.long = function()
{
    if( this.trend.direction !== 'up' ) // new trend? (only act on new trends)
    {
        this.resetTrend();
        this.trend.direction = 'up';
        this.advice('long');
        //log.debug('go long');
    }
    
    if(this.debug)
    {
        this.trend.duration++;
        log.debug ('Long since', this.trend.duration, 'candle(s)');
    }
};


/* SHORT */
strategy.short = function()
{
    // new trend? (else do things)
    if( this.trend.direction !== 'down' )
    {
        this.resetTrend();
        this.trend.direction = 'down';
        this.advice('short');
    }
    
 };

strategy.resetTrend = function()
{
    var trend = {
        duration: 0,
        direction: 'none',
        longPos: false,
    };
    
    this.trend = trend;
};

module.exports = strategy;
