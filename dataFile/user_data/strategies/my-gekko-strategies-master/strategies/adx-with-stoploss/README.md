# adp-with-stoploss

Estratégia baseada no indicador `ADX: The Trend Strength Indicator` com Stoploss Parámetrizavel.

O índice direcional médio, ou ADX, foi concebido para ajudar os traders a identificarem os mercados tendência e determinar a força da tendência, para permanecerem no lado ótimo de uma operação.

## Parameters

```toml
historySize = 80
optInTimePeriod = 15
candleSize = 10

[general]
stopLoss = 0.10

[thresholds]
up = 30
down = 20
```

## References

https://www.valutrades.com/pt/blog/usando-o-indicador-adx-para-trading-com-forex