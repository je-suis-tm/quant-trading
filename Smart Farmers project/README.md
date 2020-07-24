# Smart Farmers

&nbsp;
-----------------------------------------
### Table of Contents

* <a href=https://github.com/je-suis-tm/quant-trading/tree/master/Smart%20Farmers%20project#intro>Intro</a>

* <a href=https://github.com/je-suis-tm/quant-trading/tree/master/Smart%20Farmers%20project#assumption>Assumption</a>

* <a href=https://github.com/je-suis-tm/quant-trading/tree/master/Smart%20Farmers%20project#theoretical-framework>Theoretical Framework</a>

* <a href=https://github.com/je-suis-tm/quant-trading/tree/master/Smart%20Farmers%20project#empirical-result>Empirical Result</a>

* <a href=https://github.com/je-suis-tm/quant-trading/tree/master/Smart%20Farmers%20project#discussion>Discussion</a>

* <a href=https://github.com/je-suis-tm/quant-trading/tree/master/Smart%20Farmers%20project#further-reading>Further Reading</a>
------------------------------------------------
&nbsp;

### Intro

### Assumption

The key assumption of this project is efficient market hypothesis. As faulty as it sounds, it is the easiest way to model. There is one and only way to be rational but one million different ways to be irrational. We assume farmers are Homo Economicus. Contradicting the behavioral science, they are smart and rational. Their objective is bona fide straight forward, to maximize their margin. Let's aggregate all farmers into one farmer union to eliminate the individual heterogeneity. Here are the detailed assumptions.

* No extreme weather prior to planning, no El Niño, La Niña, if future climate condition impacts crop choice, crop list and cost per crop will be modified accordingly

* No liquidity issue, all crops will be absorbed by the market, those who cannot be consumed in the domestic market will be exported

* No arbitrage between domestic and international agriculture market, no logistic bottleneck, freight cost is low to be ignored

* No sudden demand surge, demand is determined by population, beyond meat and impossible whopper are overhyped, all crops are mainly for culinary use

* No agricultural technology upgrade, expected yield stays the same over the years, vertical farm is not taken into consideration

* Homogenous crop quality, no Michelin-restaurant grade Basmati rice, all crops are sold at market price

### Theoretical Framework

Farmers want to increase as much output as possible, but too much supply can damage the crop price, so they have to find a sweet spot to maximize their margin. Additionally, there is limited plantation area. Each crop requires different amount of plantation area. Crop rotation is a unique constraint for annual crops. Hence, farmers must carefully allocate the land area to different crops.

![alt text](https://github.com/je-suis-tm/quant-trading/blob/master/Smart%20Farmers%20project/preview/naive%20model.PNG) 

![alt text](https://github.com/je-suis-tm/quant-trading/blob/master/Smart%20Farmers%20project/preview/pricing%20mechanism.PNG) 

![alt text](https://github.com/je-suis-tm/quant-trading/blob/master/Smart%20Farmers%20project/preview/price%20change%20derivation.PNG) 

![alt text](https://github.com/je-suis-tm/quant-trading/blob/master/Smart%20Farmers%20project/preview/demand%20model.PNG) 

![alt text](https://github.com/je-suis-tm/quant-trading/blob/master/Smart%20Farmers%20project/preview/naive%20model%20matrix.PNG) 

### Empirical Result

![alt text](https://github.com/je-suis-tm/quant-trading/blob/master/Smart%20Farmers%20project/preview/cabbage%20price.png) 

![alt text](https://github.com/je-suis-tm/quant-trading/blob/master/Smart%20Farmers%20project/preview/cabbage%20production.png) 

![alt text](https://github.com/je-suis-tm/quant-trading/blob/master/Smart%20Farmers%20project/preview/cabbage%20regression.png) 

![alt text](https://github.com/je-suis-tm/quant-trading/blob/master/Smart%20Farmers%20project/preview/cocoa%20price.png) 

![alt text](https://github.com/je-suis-tm/quant-trading/blob/master/Smart%20Farmers%20project/preview/cocoa%20production.png) 

![alt text](https://github.com/je-suis-tm/quant-trading/blob/master/Smart%20Farmers%20project/preview/cocoa%20regression.png) 

![alt text](https://github.com/je-suis-tm/quant-trading/blob/master/Smart%20Farmers%20project/preview/coconut%20price.png) 

![alt text](https://github.com/je-suis-tm/quant-trading/blob/master/Smart%20Farmers%20project/preview/coconut%20production.png) 

![alt text](https://github.com/je-suis-tm/quant-trading/blob/master/Smart%20Farmers%20project/preview/coconut%20regression.png) 

![alt text](https://github.com/je-suis-tm/quant-trading/blob/master/Smart%20Farmers%20project/preview/mango%20price.png) 

![alt text](https://github.com/je-suis-tm/quant-trading/blob/master/Smart%20Farmers%20project/preview/mango%20production.png) 

![alt text](https://github.com/je-suis-tm/quant-trading/blob/master/Smart%20Farmers%20project/preview/mango%20regression.png) 

![alt text](https://github.com/je-suis-tm/quant-trading/blob/master/Smart%20Farmers%20project/preview/rubber%20price.png) 

![alt text](https://github.com/je-suis-tm/quant-trading/blob/master/Smart%20Farmers%20project/preview/rubber%20production.png) 

![alt text](https://github.com/je-suis-tm/quant-trading/blob/master/Smart%20Farmers%20project/preview/rubber%20regression.png) 

![alt text](https://github.com/je-suis-tm/quant-trading/blob/master/Smart%20Farmers%20project/preview/overall%20production.png) 

![alt text](https://github.com/je-suis-tm/quant-trading/blob/master/Smart%20Farmers%20project/preview/oil%20palm%20price.png) 

![alt text](https://github.com/je-suis-tm/quant-trading/blob/master/Smart%20Farmers%20project/preview/oil%20palm%20production.png) 

![alt text](https://github.com/je-suis-tm/quant-trading/blob/master/Smart%20Farmers%20project/preview/oil%20palm%20regression.png) 

### Discussion

![alt text](https://github.com/je-suis-tm/quant-trading/blob/master/Smart%20Farmers%20project/preview/oil%20palm%20vs%20palm%20oil.png) 

The naïve model may work in a closed system that craves for self-sufficiency, e.g. EU, it may not work on powerful agricultural exporters such as US or Canada. To picture crop planning of US farmers, the international market demand should be taken into consideration. This will create a Ricardian international trading system where different countries produce each crop proportionally to its cost and plantation area (comparative advantage).

To preserve the robustness of the model, the original assumptions stay the same, some extra assumptions are needed.

* No trade barrier, no tariff or quota

* All crops trade at Chicago price

* No competition and collusion among farmers

![alt text](https://github.com/je-suis-tm/quant-trading/blob/master/Smart%20Farmers%20project/preview/ricardian%20model.PNG) 

### Further Reading

