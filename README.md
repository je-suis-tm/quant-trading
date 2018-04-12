# Quant-trading

This folder contains some quantitative trading strategies I found interesting. Note that I only do historical data backtesting. I do have some real time trading strategy I am using. So far it is profitable so I would not share unless you require.

# Strategies:

1. MACD oscillator

This is the easiest trading strategy. It is a momentum trading strategy which holds the belief that upward momentum has more impact on short term moving average than long term moving average. I basically take long moving average and short moving average on the close price of stock. To generate the trading signal, I implement a comparison between two moving averages. When short moving average is larger than long moving average, I set the signal at 1 which implies LONG, vice versa.

![alt text](https://github.com/tattooday/quant-trading/blob/master/preview/momentum%20trading.png)

![alt text](https://github.com/tattooday/quant-trading/blob/master/preview/macd%20oscillator.png)

2. Pair trading

This is so-called statistics arbitrage. It is based on the assumption that two cointegrated stocks would not drift away too far from each other. First of all, I choose two stocks and run Engle-Granger two step analysis (1, run regression. 2, run unit root test on residuals) on both. Next, I standardize the residual and set one sigma away (both sides) as the threshold. After that, I take the standardized residual list and compare with the threshold. When the residual exceeds threshold, it generates the signals. I always long the cheap stock and short the expensive stock. 

3. Heikin-Ashi candlestick

The rules of Heikin-Ashi is quite tricky. It is a Japanese way to filter out the noise for momentum trading. Basically I do a few transformations on four key benchmarks - Open, Close, High, Low. The next step is to apply unique Heikin-Ashi rules on Heikin-Ashi Open, Close, High, Low. After that, a few signals are generated. I set up the stop loss position so that we don't get screwed up during any market collapse.

Transformations and trading rules can be found here: 

https://quantiacs.com/Blog/Intro-to-Algorithmic-Trading-with-Heikin-Ashi.aspx



