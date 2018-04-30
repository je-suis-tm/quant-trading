# oil money project

As I mentioned before, this is a project inspired by an article that i read. During low volatility period, the article recommended to trade Norwegian Krone as the oil price was bouncing back. To my curiosity, I intended to find out if this idea is plausible. First thing came to my mind was whether the correlation between Norwegian Krone and Brent Crude was substantial. Norway is one my fav places in Europe. Unlike Qatar or Saudi or any other gulf countries, it doesnt heavily rely on oil for its gross income. I doubted oil would be the only factor that affects the exchange rate of NOK. I looked into trading statistics of Norway. Basically, most trading partners are in European Union. Prior to stats, I included UK sterling and Euro in my linear regression model. To my surprise, Norway is actually doing a lot of business with US. Thus, the model consisted of EUR, GBP, USD and Brent Crude.

The regression result came out as below.We had a pretty high R square. All T stats and F stats were significant. As the summary suggested, there could be multicollinearity. I wouldnt doubt it as Brent Crude and USD should be negatively correlated.

![alt text](https://github.com/tattooday/quant-trading/blob/master/oil%20money%20project/preview/model%20summary.PNG)
