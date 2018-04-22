# Quant-trading

This folder contains some quantitative trading strategies I found interesting. Note that I only do historical data backtesting. I do have some real time trading strategy I am using. So far it is profitable so I would not share unless you require.

# Strategies:

1. MACD oscillator

This is the easiest trading strategy. It is a momentum trading strategy which holds the belief that upward momentum has more impact on short term moving average than long term moving average. I basically take long moving average and short moving average on the close price of stock. To generate the trading signal, I implement a comparison between two moving averages. When short moving average is larger than long moving average, I set the signal at 1 which implies LONG, vice versa.

![alt text](https://github.com/tattooday/quant-trading/blob/master/preview/momentum%20trading.png)

![alt text](https://github.com/tattooday/quant-trading/blob/master/preview/macd%20oscillator.png)

2. Pair trading

This is so-called statistics arbitrage. It is based on the assumption that two cointegrated stocks would not drift away too far from each other. First of all, I choose two stocks and run Engle-Granger two step analysis (1, run regression. 2, run unit root test on residuals) on both. Next, I standardize the residual and set one sigma away (both sides) as the threshold. After that, I take the standardized residual list and compare with the threshold. When the residual exceeds threshold, it generates the signals. I always long the cheap stock and short the expensive stock. 

![alt text](https://github.com/tattooday/quant-trading/blob/master/preview/ols%20and%20adf.PNG)

![alt text](https://github.com/tattooday/quant-trading/blob/master/preview/residual.png)

![alt text](https://github.com/tattooday/quant-trading/blob/master/preview/pair%20trading.png)

3. Heikin-Ashi candlestick

The rules of Heikin-Ashi is quite tricky. It is a Japanese way to filter out the noise for momentum trading. Basically I do a few transformations on four key benchmarks - Open, Close, High, Low. The next step is to apply unique Heikin-Ashi rules on Heikin-Ashi Open, Close, High, Low. After that, a few signals are generated. I set up the stop loss position so that we don't get screwed up during any market collapse.

Transformations and trading rules can be found here: 

https://quantiacs.com/Blog/Intro-to-Algorithmic-Trading-with-Heikin-Ashi.aspx

![alt text](https://github.com/tattooday/quant-trading/blob/master/preview/heikin%20ashi.png)

![alt text](https://github.com/tattooday/quant-trading/blob/master/preview/backtest.png)

4. London Breakout

To one of my favourite cities in the world! Proud to be a Londoner!

London Breakout is a very simple strategy. Basically, it is to take advantage of Japan market momentum and bring it to London market. Tokyo FX trading hour is GMT 0 - GMT 8:59am. London FX trading hour starts from GMT 8am. There is an hour which Tokyo trading hour overlaps London.The crucial time frame is GMT 7am to GMT 8 am. We look at the performance of Tokyo market. We set upper and lower threshold based on that hour's high and low. Once London market begins, we spend the first couple of minutes to see if the price would breach the boundaries. If it is above threshold, we long the currency pair, vice versa. Nevertheless, we should also set a limit to prevent us from trading in case abnormal open volatility occurs. Normally, we clear our positions based on our target stop loss or stop profit. By the end of the day, if there is still open positions, we clear them out. So London Breakout is a day trading strategy.

![alt text](https://github.com/tattooday/quant-trading/blob/master/preview/LondonBreakOut.png)

![alt text](https://github.com/tattooday/quant-trading/blob/master/preview/London%20Threshold.png)

5.Awesome oscillator

Awesome oscillator is similar to MACD oscillator. Both of em are considered momentum strategies which holds the belief that upward momentum has more impact on short term moving average than long term moving average. Instead of taking moving average on close price, awesome moving average is based on the mean of high and low price. Other than the difference between short term moving average and long term moving average, which called oscillator, there is another way to generate signals ahead of moving average divergence. It is called saucer which is slightly more difficult than MACD. Generally speaking, beating the delay doesnt guarantee a more profitable outcome. From my experience, awesome oscillator delivers a lower Sharpe ratio with a lower maximum drawdown. More details about how saucer generates signals could be found here:

https://www.tradingview.com/wiki/Awesome_Oscillator_(AO)

![alt text](https://github.com/tattooday/quant-trading/blob/master/preview/awesome%20positions.png)

![alt text](https://github.com/tattooday/quant-trading/blob/master/preview/Awesome%20oscillator.png)

![alt text](https://github.com/tattooday/quant-trading/blob/master/preview/awesome%20ma.png)

![alt text](https://github.com/tattooday/quant-trading/blob/master/preview/awesome%20asset.png)

