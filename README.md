# Quant-trading

This folder contains some quantitative trading strategies I found interesting. There are momentum trading, opening range breakout and statistical arbitrage strategies. Note that I only do historical data backtesting (basically via Python not C++). My assumption is that all trades are frictionless. I also might include some weird ideas I came up with. 

1.MACD oscillator

2.Pair trading

3.Heikin-Ashi candlestick

4.London Breakout

5.Awesome oscillator

6.Oil money project

7.Dual Thrust

8.Parabolic SAR

9.Bollinger Bands Pattern Recognition

10. Relative Strength Index

# Strategies:

1. MACD oscillator

This is the easiest trading strategy. It is a momentum trading strategy which holds the belief that upward momentum has more impact on short term moving average than long term moving average. We basically take long moving average and short moving average on the close price of stock. To generate the trading signal, we implement a comparison between two moving averages. When short moving average is larger than long moving average, we set the signal at 1 which implies LONG, vice versa.

![alt text](https://github.com/tattooday/quant-trading/blob/master/preview/macd%20positions.png)

![alt text](https://github.com/tattooday/quant-trading/blob/master/preview/macd%20oscillator.png)

2. Pair trading

This is so-called statistics arbitrage. It is based on the assumption that two cointegrated stocks would not drift away too far from each other. First of all, we choose two stocks and run Engle-Granger two step analysis (1, run regression. 2, run unit root test on residuals) on both. Next, we standardize the residual and set one sigma away (both sides) as the threshold. After that, we take the standardized residual list and compare with the threshold. When the residual exceeds threshold, it generates the signals. We always long the cheap stock and short the expensive stock. 

![alt text](https://github.com/tattooday/quant-trading/blob/master/preview/pair%20trading%20eg%20two%20step.PNG)

![alt text](https://github.com/tattooday/quant-trading/blob/master/preview/pair%20trading%20z%20stats.png)

![alt text](https://github.com/tattooday/quant-trading/blob/master/preview/pair%20trading%20positions.png)

3. Heikin-Ashi candlestick

The rules of Heikin-Ashi are quite tricky. It is a Japanese way to filter out the noise for momentum trading. Basically we do a few transformations on four key benchmarks - Open, Close, High, Low. The next step is to apply unique Heikin-Ashi rules on Heikin-Ashi Open, Close, High, Low. After that, a few signals are generated. We set up the stop loss position so that we don't get screwed up during any market collapse.

Transformations and trading rules can be found here: 


https://quantiacs.com/Blog/Intro-to-Algorithmic-Trading-with-Heikin-Ashi.aspx

![alt text](https://github.com/tattooday/quant-trading/blob/master/preview/heikin-ashi%20positions.png)

![alt text](https://github.com/tattooday/quant-trading/blob/master/preview/heikin-ashi%20asset%20value.png)

4. London Breakout

To one of my favourite cities in the world! Proud to be a Londoner!

London Breakout is a very simple opening range breakout strategy. Basically, it is to take advantage of Japan market momentum and bring it to London market. Tokyo FX trading hour is GMT 0 - GMT 8:59am. London FX trading hour starts from GMT 8am. There is an hour which Tokyo trading hour overlaps London.The crucial time frame is GMT 7am to GMT 8 am. We look at the performance of Tokyo market. We set upper and lower threshold based on that hour's high and low. Once London market begins, we spend the first couple of minutes to see if the price would breach the boundaries. If it is above threshold, we long the currency pair, vice versa. Nevertheless, we should also set a limit to prevent us from trading in case abnormal open volatility occurs. Normally, we clear our positions based on our target stop loss or stop profit. By the end of the day, if there are open positions, we clear them out. So London Breakout is a day trading strategy.

![alt text](https://github.com/tattooday/quant-trading/blob/master/preview/london%20breakout%20positions.png)

![alt text](https://github.com/tattooday/quant-trading/blob/master/preview/london%20breakout%20thresholds.png)

5.Awesome oscillator

Awesome oscillator is similar to MACD oscillator. Both of them are considered as momentum strategies which hold the belief that upward momentum has more impact on short term moving average than long term moving average. Instead of taking moving average on close price, awesome moving average is based on the mean of high and low price. Besides the difference between short term moving average and long term moving average, which is called oscillator, there is another way to generate signals ahead of moving average divergence. It is called saucer which is slightly more complex than MACD. Generally speaking, beating the delay doesnt guarantee a more profitable outcome. From my experience, awesome oscillator delivers a lower Sharpe ratio with a lower maximum drawdown. More details about how saucer generates signals could be found here:

https://www.tradingview.com/wiki/Awesome_Oscillator_(AO)

![alt text](https://github.com/tattooday/quant-trading/blob/master/preview/awesome%20positions.png)

![alt text](https://github.com/tattooday/quant-trading/blob/master/preview/awesome%20oscillator.png)

![alt text](https://github.com/tattooday/quant-trading/blob/master/preview/awesome%20ma.png)

![alt text](https://github.com/tattooday/quant-trading/blob/master/preview/awesome%20asset.png)

6.Oil money project

I came up with this idea after reading an article about how to trade petrocurrency when the volatility of forex is low and oil price is steadily increasing. As it's not a recognized trading strategy like others in this repo (although quite a lot of research on this topic), I store all files inside a separate folder called oil money project. I highly recommend you guys to take a look and give me some feedback. For enquiry on details of this strategy, please refer to readme in the following link.

https://github.com/tattooday/quant-trading/blob/master/Oil%20Money%20project/README.md

7.Dual Thrust

Dual thrust is a very popular opening range breakout strategy, especially in CTA. It is similar to London Breakout strategy. Initially we set up upper and lower thresholds based on previous days open, close, high and low. When the market opens and the price exceeds thresholds, we would take long/short positions prior to upper/lower thresholds. The strategy is quite useful in intra daily trading. However, there is no stop long/short position in this strategy. We reverse our positions when the price goes from one threshold to the other. We need to clear all positions at the end of the day.

Rules of dual thrust can be found in the following link:

https://www.quantconnect.com/tutorials/dual-thrust-trading-algorithm/

![alt text](https://github.com/tattooday/quant-trading/blob/master/preview/dual%20thrust%20positions.png)

8.Parabolic SAR

Parabolic SAR is an indicator to identify stop and reverse of a trend. When it is an uptrend, SAR curve would be below the price. When it is downtrend, SAR curve would be above the price. It is always considered as the resistance to the price momentum. When SAR curve and the price curve crosses over, it is when trades should be executed. The strategy itself is very similar to MACD oscillator (as most momentum trading strategies are). 

However, the calculation of SAR is extremely painful. Info on Parabolic SAR can be found in wikipedia but not very well explained. The most straight forward way is to look at the spreadsheet made of joeu2004. These websites can be found in the following links:

https://en.wikipedia.org/wiki/Parabolic_SAR

https://www.box.com/s/gbtrjuoktgyag56j6lv0

![alt text](https://github.com/tattooday/quant-trading/blob/master/preview/parabolic%20sar%20positions.png)

9.Bollinger Bands Pattern Recognition

Bollinger Bands is a very simple indicator. There are three bands. The mid band is the moving average on the price series. The upper and lower bands are two moving standard deviations away from the moving average. The indicators can be used to test for many different strategies. For volatility trading, contraction and expansion of the band width is a crucial element. For momentum trading, 'walking the band' indicates resistance and support level. For pattern recognition, Bollinger Bands has the capability of testing bottom W, top M, head-shoulder patterns and etc.

For the rules of Bollinger Bands, please refer to the following website:

https://www.tradingview.com/wiki/Bollinger_Bands_(BB)

![alt text](https://github.com/tattooday/quant-trading/blob/master/preview/bollinger%20bands%20positions.png)

10. Relative Strength Index

RSI (Relative Strength Index) is also a popular indicator. It reflects the current strength or weakness of the stock price momentum. The calculation is pretty straight forward. We use 14 days of smoothed moving average (or other moving average methods) to separately calculate the intra daily uptrend and downtrend. We denote uptrend moving average divided by downtrend moving average as the relative strength. We normalize the relative strength by 100 which is called RSI. It is commonly believed that RSI above 70 is overbought and RSI below 30 is oversold. Nevertheless, there could be divergence between RSI momentum and price momentum which this script would not cover that part. The effectiveness of divergence strategy is debatable. We can also apply double bottom pattern recognition technique to RSI to anticipate the trend. Please refer to strategy No.9 Bollinger Bands for details of pattern recognition.

STAY TUNED
