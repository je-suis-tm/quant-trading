## Monte Carlo simulation in trading is nothing but house of cards

![alt text](https://raw.githubusercontent.com/tattooday/quant-trading/master/Monte%20Carlo%20project/preview/xkcd_curve_fitting.png)

Why do I put this picture (see <a href=https://www.explainxkcd.com/wiki/index.php/2048:_Curve-Fitting>here</a> for explanation) right in front of everything? Have I caught your attention? Hopefully I have. These days, blogs on data science topic are dime a dozen. Some blogs teach you how to use decision tree/random forrest to predict the stock price movement, others illustrate the possibility of back-propagation neural network to forecast a bond price. The brutal truth is, most of them are nothing but house of cards.

Monte Carlo, my first thought on these two words is the grand casino, where you meet Famke Janssen in tuxedo and introduce yourself, 'Bond, James Bond'. Indeed, the simulation is named after the infamous casino. It actually refers to the computer simulation of massive amount of random events. This unconventional mathematical method is extremely powerful in the study of stochastic process. Here comes the argument on Linkedin that caught my eyes the other day. "Stock price can be seemed as a <a href=https://en.wikipedia.org/wiki/Wiener_process>Wiener Process</a>. Hence, we can use Monte Carlo simulation to predict the stock price." said a data science blog. Well, in order to be a Wiener Process, we have to assume the stock price is continuous in time. In reality, the market closes. The overnight volatility exists. But that is not the biggest issue here. The biggest issue is, can we really use Monte Carlo simulation to predict the stock price, even a range or its direction?

The author offered a quite interesting idea. As he suggested, the first step was to run as many simulations as possible on stochastic differential equations to predict stock price. The goal of simulations was to pick a best fitted curve (in translation, the smallest standard deviation) compared to the historical data. There might exist a hidden pattern in the historical log return. The best fitted curve had the potential to replicate the hidden pattern and reflect it in the future forecast. The idea sounds neat, doesn't it? Inspired by his idea, we can build up the simulation accordingly. To fully unlock the potential of Monte Carlo simulation on fat tail events, the ticker we pick is General Electric, one of the worst performing stock in 2018. The share price of GE plunged 57.9% in 2018 thanks to its long history of M&A failures. The time horizon of the data series is 2016/1/15-2019/1/15. We split the series into halves, the first half as training horizon and the second half as testing horizon. Monte Carlo simulation will only justify its power if it can predict an extreme event like this.

Let's take a look at the figure below. Wow, what a great fit! The best fit is almost like running a cool linear regression with valid input. As you can see, it smoothly fits the curve in training horizon.

![alt text](https://raw.githubusercontent.com/tattooday/quant-trading/master/Monte%20Carlo%20project/preview/ge%20simulation.png)

If we extend it to testing horizon...

![alt text](https://raw.githubusercontent.com/tattooday/quant-trading/master/Monte%20Carlo%20project/preview/ge%20versus.png)

Oops, house of cards collapses.

![alt text](https://raw.githubusercontent.com/tattooday/quant-trading/master/Monte%20Carlo%20project/preview/ge%20accuracy.png)

![alt text](https://raw.githubusercontent.com/tattooday/quant-trading/master/Monte%20Carlo%20project/preview/ge%20simulation2.png)

![alt text](https://raw.githubusercontent.com/tattooday/quant-trading/master/Monte%20Carlo%20project/preview/nvda%20versus.png)

![alt text](https://raw.githubusercontent.com/tattooday/quant-trading/master/Monte%20Carlo%20project/preview/nvda%20simulation.png)


