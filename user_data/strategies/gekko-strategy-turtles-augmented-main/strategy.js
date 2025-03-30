/*



enterFast = 27
exitFast = 3
enterSlow = 50
exitSlow = 27

useAtrStop = true
useTrailingAtrStop = true
atrPeriod = 27
renkoPeriod = 9
atrStop = 2

adx = 31
rsiLevel = 69

*/


var _ = require('lodash');
var log = require('../core/log');

var renko = require('technicalindicators').renko;
var bullish = require('technicalindicators').bullish;
var bearish = require('technicalindicators').bearish;
let TRIX = require('technicalindicators').TRIX;
let RSI = require('technicalindicators').RSI;
let PSAR = require('technicalindicators').PSAR;

let ADX = require('technicalindicators').ADX;

var assert = require('assert');

var strat = {};

// from https://github.com/timchepeleff/turtles
// and https://www.npmjs.com/package/technicalindicators
// specifically https://github.com/anandanand84/technicalindicators/blob/066f35bcffbf9f923f45ec28525d1f2a5d063a76/src/chart_types/Renko.ts


strat.init = function() {
  this.input = 'candle';
  this.currentTrend = 'short';
  this.requiredHistory = this.settings.atrPeriod;

  this.renkoCandles
  this.candles = [];
  this.candlesNormal = [];
  this.enterFast = this.settings.enterFast;
  this.exitFast = this.settings.exitFast;
  this.enterSlow = this.settings.enterSlow;
  this.exitSlow = this.settings.exitSlow;
  this.hiekenAshi = this.settings.hiekenAshi;
  this.useAtrStop = this.settings.useAtrStop;
  this.useTrailingAtrStop = this.settings.useTrailingAtrStop;
  this.atrPeriod = this.settings.atrPeriod;
  this.atrStop = this.settings.atrStop;
  this.maxCandlesLength = this.settings.atrPeriod;
  this.adxMin = this.settings.adx;
  this.rsiLevel = this.settings.rsi;
  this.stop = 0

  this.addTalibIndicator('atr', 'atr', { optInTimePeriod: this.atrPeriod });
}

// What happens on every new candle?
strat.update = function(candle) {

  this.candlesNormal.push(candle);

    var renkoCandles = {
      close: [],
      high: [],
      low: [],
      open: [],
      timestamp: [],
      hl2: [],
      hlc3: [],
      volume: [],
      ticker: '.......' // Whatever ticker you'd like
    };

    for(var i = 0; i < this.candlesNormal.length; i++) {

      var candle = this.candlesNormal[i];

      renkoCandles.open.push(candle.open);
      renkoCandles.high.push(candle.high);
      renkoCandles.low.push(candle.low);
      renkoCandles.close.push(candle.close);
      renkoCandles.volume.push(candle.volume);
      renkoCandles.timestamp.push(candle.start);
      renkoCandles.hl2.push((candle.high + candle.low)/2);
      renkoCandles.hlc3.push((candle.high + candle.low + candle.close)/3);
    }

    var result = renko(Object.assign({}, renkoCandles, {period: parseInt(this.settings.atrPeriod/3), brickSize: 0.001, useATR: true}));

    for(var j = 0; j < result.open.length; j++) {

      this.candles.push({
        open: result.open[j],
        high: result.high[j],
        low: result.low[j],
        close: result.close[j],
        hl2: (result.high[j] + result.low[j])/2,
        volume: result.volume[j],
        timestamp: result.timestamp[j]

      })
    }

    //console.log(bullish(this.candlesNormal))

  this.renkoCandles = renkoCandles;

  let inputTRIX = {
    values: renkoCandles.hl2,
    period: this.atrPeriod/2
  }

  // not using, but a reference...
  this.TRIX = TRIX.calculate(inputTRIX).pop()

  // candle-pattern
  this.bullish = bullish(renkoCandles)
  this.bearish = bearish(renkoCandles)

  let inputPSAR = {
    high: renkoCandles.high,
    low: renkoCandles.low,
    step: 0.02,
    max: 0.02
  }

  // not using
  this.PSAR = new PSAR(inputPSAR).result;

  let inputRSI = {
    values: this.renkoCandles.hl2,
    period: this.atrPeriod
  }

  var outputRSI = RSI.calculate(inputRSI).pop();
  this.RSI = 0;

  if(outputRSI >= this.rsiLevel) {
    this.RSI = 1;
  } else if (outputRSI < this.rsiLevel-20) {
    this.RSI = -1;
  } else {
    this.RSI = 0;
  }

  let inputADX = {
    close: this.renkoCandles.close,
    high: this.renkoCandles.high,
    low: this.renkoCandles.low,
    period: this.settings.atrPeriod
  }

  var adx = new ADX(inputADX).result.pop();
  this.indicatorADX = 0;

  if(adx !== undefined) {
    this.indicatorADX = adx.adx > this.adxMin
  }

  this.indicatorPSAR = (this.PSAR.pop()) < renkoCandles.hl2[renkoCandles.hl2.length - 1] ? false : true;
  let start = (this.candles.length < this.maxCandlesLength) ? 0 : (this.candles.length - this.maxCandlesLength)
  this.candles =  this.candles.slice(start)
  this.latestCandle = this.candles[this.candles.length-1]
  this.latestCandle2 = this.candles[this.candles.length-2]

  this.indicatorTRIX = false;
  if(this.latestCandle2 !== undefined) {
    this.indicatorTRIX = this.TRIX < (this.latestCandle.hl2/this.latestCandle2.hl2 - 1)
  }

}
// For debugging purposes.
strat.log = function() {
}

shouldEnterL = function(candle, currentFrame) {
  return checkEnterFastL(candle, currentFrame) ? checkEnterFastL(candle, currentFrame) : checkEnterSlowL(candle, currentFrame)
}

checkEnterFastL = function(candle, currentFrame) {
  if (candle.high > highest(currentFrame.enterFast, currentFrame)) {
    currentFrame.currentTrend = 'fastL'
    return true
  }
}

checkEnterSlowL = function(candle, currentFrame) {
  if (candle.high > highest(currentFrame.enterSlow, currentFrame)) {
    currentFrame.currentTrend = 'slowL'
    return true
  }
}

shouldExitL = function(candle, currentFrame) {
  if (currentFrame.currentTrend === "fastL") {
    return checkExitFastL(candle, currentFrame)
  } else if(currentFrame.currentTrend === "slowL") {
    return checkExitSlowL(candle, currentFrame)
  }
}

checkExitSlowL = function(candle, currentFrame) {
  if (candle.low <= lowest(currentFrame.exitSlow, currentFrame) || (currentFrame.stop !== 0 && candle.close <= currentFrame.stop) ) {
    currentFrame.currentTrend = 'short'
    return true
  }
}

checkExitFastL = function(candle, currentFrame) {
  if (candle.low <= lowest(currentFrame.exitFast, currentFrame) || (currentFrame.stop !== 0 && candle.close <= currentFrame.stop)) {
    currentFrame.currentTrend = 'short'
    return true
  }
}

lowest = function(numberOfCandlesBack, currentFrame) {
  let relaventCandles = currentFrame.candles.slice((currentFrame.maxCandlesLength-numberOfCandlesBack), -1)
  return Math.min.apply(Math, relaventCandles.map(function(c) { return c.low; }))
}

highest = function(numberOfCandlesBack, currentFrame) {
  let relaventCandles = currentFrame.candles.slice((currentFrame.maxCandlesLength-numberOfCandlesBack), -1)
  return Math.max.apply(Math, relaventCandles.map(function(c) { return c.high; }))
}

manageStopLoss = function(candle, currentFrame) {
  if (currentFrame.useAtrStop) {
    let atr = currentFrame.talibIndicators.atr.result.outReal;
    currentFrame.stop = (candle.close - (atr * currentFrame.atrStop))
  }
}

manageTrailingStopLoss = function(candle, currentFrame) {
  if (currentFrame.useTrailingAtrStop) {
    let atr = currentFrame.talibIndicators.atr.result.outReal;

    // Update the stop loss if the newly suggest stop loss is higher than previous value
    if (currentFrame.stop < (candle.close - (atr * currentFrame.atrStop))) {
      currentFrame.stop = candle.close - (atr * currentFrame.atrStop)
    }
  }
}



computeExitSignal = function(candle, currentFrame) {
  if(currentFrame.currentTrend === 'fastL' || currentFrame.currentTrend === 'slowL' || (!currentFrame.RSI && currentFrame.bearish) ) {
    if (shouldExitL(candle, currentFrame) || (!currentFrame.RSI && currentFrame.bearish)  ) {
      currentFrame.currentTrend = 'short';
      currentFrame.stop = 0;
      currentFrame.advice('short');
    }
  }
}

computeEntrySignal = function(candle, currentFrame) {
  if(currentFrame.currentTrend === 'short' ) {
    if (shouldEnterL(candle, currentFrame) || (currentFrame.RSI && currentFrame.bullish && currentFrame.indicatorADX) ) {
      manageStopLoss(candle, currentFrame)

      currentFrame.advice('long');
    }
  }
}


strat.check = function(candle) {

  console.log(candle.start.format('YYYY-MM-DD'))
  // won't do anything until we have slowEntry+1 number of candles
  if (this.candles.length === this.maxCandlesLength) {
    computeExitSignal(candle, this)
    computeEntrySignal(candle, this)
  }
}

module.exports = strat;
