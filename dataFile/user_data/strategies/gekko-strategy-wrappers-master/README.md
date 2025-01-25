To facilitate the composition of strategies that are based on strats glued together.
Or to add a simple conditional to existing strat that is reusable to any other (i.e only buys when volume is above threshold);

Examples added, and community examples are welcome;

### Setup

Move `strategyWrapperRules.js` to gekko strategy folder.

### Usage

Check the examples.

### Examples

WRSI_BULL_BEAR: a remake of RSI_BULL_BEAR, now using the wrapper. 
Unintededly it behaved different of the original, trading less with sometimes higher profit.
Found out thats because it tracks the trend separated for each RSI instance.

WRSI_BULL_BEAR depends on `RSI_COMPONENT.js`, so this file should follow `WRSI_BULL_BEAR.js` to `/strategies` folder.


