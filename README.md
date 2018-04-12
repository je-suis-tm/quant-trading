# quant-trading

This folder contains some quantitative trading strategies I found interesting.

Note that I only do historical data backtesting.

Strategies:

1.MACD oscillator

This is the easiest trading strategy. It is a momentum trading strategy which holds the belief that upward momentum has more impact on short term moving average than long term moving average. I basically take long moving average and short moving average on the close price of stock. To generate the trading signal, I implement a comparison between two moving averages. When short moving average is larger than long moving average, I set the signal at 1 which implies LONG, vice versa.

2. Pair trading

This is so-called statistics arbitrage. It is based on the assumption that two cointegrated stocks would not drift away too far from each other. First of all, I choose two stocks and run Engle-Granger two step analysis (1, run regression. 2, run unit root test on residuals) on both. Next, I standardize the residual and set one sigma away (both sides) as the threshold. After that, I take the standardized residual list and compare with the threshold. When the residual exceeds threshold, it generates the signals. I always long the cheap stock and short the expensive stock. 

3. Heikin-Ashi candlestick

The rules of Heikin-Ashi is quite tricky. It is a Japanese way to filter out the noise for momentum trading. Basically I do a few transformations on four key benchmarks - Open, Close, High, Low. The next step is to apply unique Heikin-Ashi rules on Heikin-Ashi Open, Close, High, Low. After that, a few signals are generated. I set up the stop loss position so that we don't get screwed up during any market collapse.

Heikin-Ashi Candle Calculations

HA_Close = (Open + High + Low + Close) / 4

HA_Open = (previous HA_Open + previous HA_Close) / 2

HA_Low = minimum of Low, HA_Open, and HA_Close

HA_High = maximum of High, HA_Open, and HA_Close


Heikin-Ashi Calculations on First Run

HA_Close = (Open + High + Low + Close) / 4

HA_Open = (Open + Close) / 2

HA_Low = Low

HA_High = High


Go LONG if all of these are met:

Latest Heikin-Ashi candle is bearish

Previous Heikin-Ashi candle was also bearish

Latest Heikin-Ashi candle body is longer than the previous candle

Latest Heikin-Ashi candle has no upper wick


Go SHORT if all of these are met:

Latest Heikin-Ashi candle is bullish

Previous Heikin-Ashi candle was also bullish

Latest Heikin-Ashi candle body is longer than the previous candle

Latest Heikin-Ashi candle has no lower wick


Exit Conditions:

Same as an opposing entry signal except no latest Heikin-Ashi candle body can be smaller



