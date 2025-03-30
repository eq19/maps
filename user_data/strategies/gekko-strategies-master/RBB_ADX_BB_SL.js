/*
	RSI Bull and Bear + ADX modifier
	1. Use different RSI-strategies depending on a longer trend
	2. But modify this slighly if shorter BULL/BEAR is detected
	-
	12 feb 2017
	-
	(CC-BY-SA 4.0) Tommie Hansen
	https://creativecommons.org/licenses/by-sa/4.0/

    Merge of BBRSI, BB - BradT7

    BBRSI - https://github.com/atselevich/gekko/blob/develop/strategies/BBRSI.js

    BB strategy - okibcn 2018-01-03 - https://github.com/askmike/gekko/pull/1623

	-
	17 avr 2018:
	Rewritten by nmikaty to include Long and Short orders + trailing stop loss
	https://github.com/nmikaty/Gekko-Strategies

*/

// req's
var log = require('../core/log.js');
var config = require('../core/util.js').getConfig();

// strategy
var strat = {
	
	/* INIT */
	init: function()
	{
		// core
		this.name = 'RSI Bull and Bear + ADX + BB + SL';
		this.requiredHistory = config.tradingAdvisor.historySize;
		this.resetTrend();

		// debug? set to false to disable all logging/messages/stats (improves performance in backtests)
		this.debug = false;

		// Global commision for a roundtrip - For estimation for Long + Short
		if( this.debug ) this.trxCommission = 0.30;

		// performance
		config.backtest.batchSize = 1000; // increase performance
		config.silent = true; // NOTE: You may want to set this to 'false' @ live
		config.debug = false;

	    // BB
	    this.nsamples = 0;
	    this.BBtrend = {
	      zone: 'none',  // none, top, high, low, bottom
	      duration: 0,
	      persisted: false
	    }

		// Nico - keeps track of open positions
		this.inALong = false;
		this.inAShort = false;

		this.stopLoss = this.settings.stopLoss;

		// Long & Short activation
		if (this.settings.activateLongs == 1) {
			this.activateLongs = true;
		}else{
			this.activateLongs = false;
		}
		if (this.settings.activateShorts == 1) {
			this.activateShorts = true;
		}else{
			this.activateShorts = false;
		}

		
		// SMA
		this.addIndicator('maSlow', 'SMA', this.settings.SMA.long );
		this.addIndicator('maFast', 'SMA', this.settings.SMA.short );
		
		// RSI
		this.addIndicator('BULL_RSI', 'RSI', { interval: this.settings.BULL.rsi });
		this.addIndicator('BEAR_RSI', 'RSI', { interval: this.settings.BEAR.rsi });
		
		// ADX
		this.addIndicator('ADX', 'ADX', this.settings.ADX.adx );
		
  		// BB
  		this.addIndicator('bb', 'BBANDS', this.settings.bbands);

		// MOD (RSI modifiers)
		this.BULL_MOD_high = this.settings.BULL.mod_high;
		this.BULL_MOD_low = this.settings.BULL.mod_low;
		this.BEAR_MOD_high = this.settings.BEAR.mod_high;
		this.BEAR_MOD_low = this.settings.BEAR.mod_low;
		
		// debug stuff
		this.startTime = new Date();
		
		// add min/max if debug
		if( this.debug ){
			this.stat = {
				adx: { min: 1000, max: 0 },
				bear: { min: 1000, max: 0 },
				bull: { min: 1000, max: 0 }
			};
		}
		
		/* MESSAGES */
		
		// message the user about required history
		log.info("====================================");
		log.info('Running', this.name);
		log.info('====================================');
		log.info("Make sure your warmup period matches SMA_long and that Gekko downloads data if needed");
		
		// warn users
		if( this.requiredHistory < this.settings.SMA_long )
		{
			log.warn("*** WARNING *** Your Warmup period is lower then SMA_long. If Gekko does not download data automatically when running LIVE the strategy will default to BEAR-mode until it has enough data.");
		}
		
	}, // init()
	
	
	/* RESET TREND */
	resetTrend: function()
	{
		var trend = {
			duration: 0,
			direction: 'none',
			longPos: false,
		};
	
		this.trend = trend;
	},
	
	
	/* get low/high for backtest-period */
	lowHigh: function( val, type )
	{
		let cur;
		if( type == 'bear' ) {
			cur = this.stat.bear;
			if( val < cur.min ) this.stat.bear.min = val; // set new
			else if( val > cur.max ) this.stat.bear.max = val;
		}
		else if( type == 'bull' ) {
			cur = this.stat.bull;
			if( val < cur.min ) this.stat.bull.min = val; // set new
			else if( val > cur.max ) this.stat.bull.max = val;
		}
		else {
			cur = this.stat.adx;
			if( val < cur.min ) this.stat.adx.min = val; // set new
			else if( val > cur.max ) this.stat.adx.max = val;
		}
	},
	
	
	/* CHECK */
	check: function()
	{
		// Debug profit estimation
		if( this.debug ) {
			if (!this.initialized){
				this.initialPrice = this.candle.close;
				this.profit = 1;
				this.initialized = true;
			}
		}

		// get all indicators
		let ind = this.indicators,
			maSlow = ind.maSlow.result,
			maFast = ind.maFast.result,
			rsi,
			adx = ind.ADX.result;

		// BB variables
		var BB = this.indicators.bb;
  		var price = this.candle.close;
  		this.nsamples++;
			
		// BB price Zone detection
		var zone = 'none';
		var priceTop = BB.lower + (BB.upper - BB.lower) / 100 * this.settings.BBtrend.upperThreshold;
		var priceBottom = BB.lower + (BB.upper - BB.lower) / 100 * this.settings.BBtrend.lowerThreshold;
		if (price >= priceTop) zone = 'top';
		if ((price < priceTop) && (price >= BB.middle)) zone = 'high';
		if ((price > priceBottom) && (price < BB.middle)) zone = 'low';
		if (price <= priceBottom) zone = 'bottom';
		//if(this.debug) log.debug('current zone:  ', zone);
		//if(this.debug) log.debug('current trend duration:  ', this.BBtrend.duration);

		if (this.BBtrend.zone == zone) {
		  this.BBtrend = {
		    zone: zone,  // none, top, high, low, bottom
		    duration: this.BBtrend.duration+1,
		    persisted: true
		  }
		}
		else {
		  this.BBtrend = {
		    zone: zone,  // none, top, high, low, bottom
		    duration: 0,
		    persisted: false
		  }
		}

		// Stop Loss
		if (this.stopLoss != 0){	
			if (this.inALong){
				if (((this.lastHigh - this.candle.close) / this.lastHigh * 100) > this.stopLoss){
					this.advice('short');
					this.inALong = false;
					if( this.debug ) {
						log.info('Closing long (stop loss');
						this.profit = this.profit + this.profit * ((this.candle.close - this.entryPrice) / this.entryPrice - this.trxCommission / 100);
						log.info('Profit: ' + ((this.candle.close - this.entryPrice) / this.entryPrice * 100  - this.trxCommission).toFixed(2) + '%');
					}
				}
			}
			if (this.inAShort && this.activateShorts){
				if (((this.candle.close - this.lastLow) / this.lastLow * 100) > this.stopLoss){
					this.advice('long');
					this.inAShort = false;
					if( this.debug ) {
						log.info('Closing short (stop loss)');
						this.profit = this.profit + this.profit * ((this.entryPrice - this.candle.close) / this.entryPrice - this.trxCommission / 100);
						log.info('Profit: ' + ((this.entryPrice - this.candle.close) / this.entryPrice * 100  - this.trxCommission).toFixed(2) + '%');
					}
				}
			}
		}

		// BEAR TREND
		// NOTE: maFast will always be under maSlow if maSlow can't be calculated
		if( maFast < maSlow)
		{
			rsi = ind.BEAR_RSI.result;
			this.rsi_hi = this.settings.BEAR.high,
			this.rsi_low = this.settings.BEAR.low;
			
			// ADX trend strength?
			if( adx > this.settings.ADX.high ) this.rsi_hi = this.rsi_hi + this.BEAR_MOD_high;
			else if ( adx < this.settings.ADX.low ) this.rsi_low = this.rsi_low + this.BEAR_MOD_low;

			if(this.debug) this.lowHigh( rsi, 'bear' );
		}

		// BULL TREND
		else
		{
			rsi = ind.BULL_RSI.result;
			this.rsi_hi = this.settings.BULL.high,
			this.rsi_low = this.settings.BULL.low;
			
			// ADX trend strength?
			if( adx > this.settings.ADX.high ) this.rsi_hi = this.rsi_hi + this.BULL_MOD_high;		
			else if( adx < this.settings.ADX.low ) this.rsi_low = this.rsi_low + this.BULL_MOD_low;

			if(this.debug) this.lowHigh( rsi, 'bull' );
		}

		// add adx low/high if debug
		if( this.debug ) this.lowHigh( adx, 'adx');

		// We are in a long
		if (this.inALong){ 
			if ( rsi > this.rsi_hi){ // close long ?
				this.advice('short');
				this.inALong = false;
				if( this.debug ) {
					log.info('Closing long at:' + this.candle.close);
					this.profit = this.profit + this.profit * ((this.candle.close - this.entryPrice) / this.entryPrice - this.trxCommission / 100);
					log.info('Profit: ' + ((this.candle.close - this.entryPrice) / this.entryPrice * 100 - this.trxCommission).toFixed(2) + '%');
				}
			}else{
				if ( this.candle.close > this.lastHigh ) this.lastHigh = this.candle.close;
				if( this.debug ){
					this.trend.duration++;
					//if( this.debug ) log.info('Long since', this.trend.duration, 'candle(s)');
				}
			}
		}

		// We are in a short
		else if (this.inAShort && this.activateShorts){	
			if ( rsi < this.rsi_low){	// close short ?
				this.advice('long');
				this.inAShort = false;
				if( this.debug ) {
					log.info('Closing short at:' + this.candle.close);
					this.profit = this.profit + this.profit * ((this.entryPrice - this.candle.close) / this.entryPrice - this.trxCommission / 100);
					log.info('Profit: ' + ((this.entryPrice - this.candle.close) / this.entryPrice * 100 - this.trxCommission).toFixed(2) + '%');
				}
			}else{
				if ( this.candle.close < this.lastlow ) this.lastLow = this.candle.close;
				if( this.debug ){
					this.trend.duration++;
					//if( this.debug ) log.info('Short since', this.trend.duration, 'candle(s)');
				}
			}
		}
		
		// We are not in a position
		else if ( rsi < this.rsi_low && this.BBtrend.zone == 'bottom' && this.BBtrend.duration >= this.settings.BBtrend.lowerPersistence && this.activateLongs ){	// open long
			this.advice('long');
			this.inALong = true;
			this.lastHigh = this.candle.close;
			this.resetTrend();
			this.trend.direction = 'up';
			if( this.debug ) {
				log.info('Opening long at:' + this.candle.close);
				this.entryPrice = this.candle.close;
			}

		}else if ( rsi > this.rsi_hi && this.BBtrend.zone == 'top' && this.BBtrend.duration >= this.settings.BBtrend.upperPersistence && this.activateShorts ){	// open short
			this.advice('short');
			this.inAShort = true;
			this.lastLow = this.candle.close;
			this.resetTrend();
			this.trend.direction = 'down';
			if( this.debug ) {
				log.info('Opening short at:' + this.candle.close);
				this.entryPrice = this.candle.close;
			}
		}

/*		log.info('BB.upper:' + BB.upper);
		log.info('BB.priceTop:' + priceTop);
		log.info('Price:' + price);
		log.info('BB.priceBottom:' + priceBottom);
		log.info('BB.lower:' + BB.lower);
		log.info('BB zone:' + this.BBtrend.zone);
		log.info('BB duration:' + this.BBtrend.duration);*/

	}, // check()

	
	/* END backtest */
	end: function()
	{
		let seconds = ((new Date()- this.startTime)/1000),
			minutes = seconds/60,
			str;
			
		minutes < 1 ? str = seconds.toFixed(2) + ' seconds' : str = minutes.toFixed(2) + ' minutes';
		
		log.info('====================================');
		log.info('Finished in ' + str);
		log.info('====================================');
	
		// print stats and messages if debug
		if(this.debug)
		{
			let stat = this.stat;
			log.info('BEAR RSI low/high: ' + stat.bear.min + ' / ' + stat.bear.max);
			log.info('BULL RSI low/high: ' + stat.bull.min + ' / ' + stat.bull.max);
			log.info('ADX min/max: ' + stat.adx.min + ' / ' + stat.adx.max);

			// profit
			this.marketProfit = (this.candle.close - this.initialPrice) / this.initialPrice * 100;
			this.profit = (this.profit - 1) * 100;
			log.info('Market Profit: ' + this.marketProfit.toFixed());			
			log.info('Strategy Gross Profit: ' + this.profit.toFixed());
			log.info('Strategy - Market Profit: ' + (this.profit - this.marketProfit).toFixed());
		}
		
	}
	
};

module.exports = strat;