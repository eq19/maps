const log = require('../core/log.js');
const fs = require('fs');
const toml = require('toml');

console.log(__dirname);
const InfoMessage = {
  START: 'Running Reactive Strategy',
};

const ErrorMessage = {
  NO_STRATEGIES_FOUND: 'Noe strategies found',
};

class ReativeStrategy {
  constructor() {
    log.info(InfoMessage.START);

    this.runningStrategy = null;

    this.getAvailableStrategies()
        .then(data => this.availableStrategies = data)
        .then(() => this.findMostProfitableStrategy());
  }

  static getInstance() {
    if (!this.instance_) {
      this.instance_ = new ReativeStrategy();
    }

    return this.instance_;
  }

  init() {
    if (!this.runningStrategy) return;

    this.runningStrategy.init.call();
  }

  update() {
    if (!this.runningStrategy) return;

    this.runningStrategy.update.call();
  }

  log() {
    if (!this.runningStrategy) return;

    this.runningStrategy.log.call();
  }

  check() {
    if (!this.runningStrategy) return;

    this.runningStrategy.check.call();
  }

  findMostProfitableStrategy() {
    const strategyName = 'stochastic';
    const strategyFile = './' + strategyName;

    this.setNewStrategy(require(strategyFile));
  }

  setNewStrategy(strategy) {
    // fs.readfile(__dirname + )
    console.log(__dirname);
    // strategy.settings
  }

  getAvailableStrategies() {
    return new Promise((resolve, reject) => {
      fs.readdir(__dirname, (err, files) => {
        if (err) reject(err);
        if (!files || !files.length) reject(ErrorMessage.NO_STRATEGIES_FOUND);

        // Only allow files with at least one character before the '.js'
        resolve(files.filter(file => file.indexOf('.js') >= 1));
      })
    });
  }
}

module.exports = ReativeStrategy.getInstance();
