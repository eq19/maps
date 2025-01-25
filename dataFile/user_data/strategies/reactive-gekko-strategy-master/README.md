# reactive-gekko-strategy
In the coming weeks this plans to become a trading strategy that reacts to market changes, finding and running only the most profitable indicators.

## Ive decided to go down a different route. Instead of a strategy Im building a seperate node layer to manage gekko and its strategies. Visit https://github.com/DustinJSilk/reactive-trader  

## Plugin VS strategy

Probably should have made it a plugin. But we're this far along so we'll steam ahead and make sure it works. Once (if) it works I'll reevaluate the decision.

## Install

Run these 3 commands from your Gekko repository:

- $ git submodule init
- $ git submodule add https://github.com/DustinJSilk/reactive-gekko-strategy.git
- $ ./reactive-gekko-strategy/install-strategy.sh


## Roadmap

The basic future:

- ~~Setup installation~~
- Have strategy extend another strategy
- ~~Add Stochastic strategy~~
- Use all strategies or pick from a list defined in the config
- Setup automatic strategy testing
- Setup automatic strategy switching
- Add Genetic Algorithm
- Figure out how to run backtesting

This will change as we move along.
