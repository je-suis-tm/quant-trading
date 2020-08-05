# Smart Farmers

&nbsp;
-----------------------------------------
### Table of Contents

* <a href=https://github.com/je-suis-tm/quant-trading/tree/master/Smart%20Farmers%20project#intro>Intro</a>

* <a href=https://github.com/je-suis-tm/quant-trading/tree/master/Smart%20Farmers%20project#assumption>Assumption</a>

* <a href=https://github.com/je-suis-tm/quant-trading/tree/master/Smart%20Farmers%20project#theoretical-framework>Theoretical Framework</a>

* <a href=https://github.com/je-suis-tm/quant-trading/tree/master/Smart%20Farmers%20project#data-specification>Data Specification</a>

* <a href=https://github.com/je-suis-tm/quant-trading/tree/master/Smart%20Farmers%20project#empirical-result>Empirical Result</a>

* <a href=https://github.com/je-suis-tm/quant-trading/tree/master/Smart%20Farmers%20project#discussion>Discussion</a>

* <a href=https://github.com/je-suis-tm/quant-trading/tree/master/Smart%20Farmers%20project#further-reading>Further Reading</a>
------------------------------------------------
&nbsp;

### Intro

:tangerine: :pineapple: :melon: :corn: and :sweet_potato: are something we have been taking for granted. Up until COVID-19, we finally come to senses that farmers are one of our low-paid essential workers. This project is dedicated to the optimal allocation of agricultural resources. By trading agricultural market, we are able to eliminate the inefficiency in the crop market. Ideally no food will be wasted and farmers will be fairly compensated. 

The project per se intends to leverage convex optimization to approximate farmers’ plantation planning for different crops. Assuming farmers are Homo Economicus, their end game is to maximize the profit regarding the price impact from supply and demand. Their decision is constrained by arable land area and biological features of crops. We develop this smart model accordingly to acquire a head start in trading :rice: :coffee: and :chocolate_bar:

### Assumption

The core of this project is Efficient Market Hypothesis. As faulty as it sounds, there is only one way to be rational (call it Pareto Optimal as you may) but one thousand ways to be irrational. Efficient Market Hypothesis allows us to convert head-scratching individual decisions into the simplest form of supply and demand. We aggregate all farmers inside one country into a big farmer union to study their collective behavior. The farmers in the union are presumed to be Homo Economicus. They have one simple but elegant objective, to maximize their margin.

To make the ultimate result more robust, we slightly expand the assumptions.

* No extreme weather prior to farm planning. No flood/drought, volcano eruption, locust invasion, El Niño or La Niña is expected. Agricultural market is predominantly supply-driven. Weather is the biggest factor that leads to supply shock and price spike. Even if future climate condition may impact the choice of crops, as we have witnessed how global warming encourages farmers to grow grains in Siberia, we can easily modify the list of crops we are monitoring with the assistance of agronomists. In reality, big farms normally implement protection measures in advance, e.g. better irrigation system to fight against drought. This can be easily embedded into the cost of planting certain type of crops.

* No sudden surge and plunge of domestic demand. This assumption eradicates the demand side in the model so we can derive an analytical solution from the supply side. The domestic demand for each type of crops is determined by the population and the disposable income. Beyond Meat and Impossible Whopper are absolutely overhyped. The rise of veganism will merely increase the plantation of soybeans in the long run. Moreover, crops are primarily for culinary consumption. Some crops such as corn and sugar cane are the raw material to generate ethanol for biofuel. Other crops such as acorn and oat are essential feed for livestock (cereals for your favorite prosciutto di Parma). They are relatively niche compared to culinary consumption. Nonetheless, we can always use multiple layers to prove that both industrial and livestock demands are fundamentally driven by the population and the disposable income.

* No major upgrades of agricultural technology. AgriTech covers a lot of topics including satellite image monitoring, drone pesticide spreading, robotic fruit picking, crop gene engineering, etc. To be honest, IoT sensors, AI management or automated machinery do not really matter to the model. This assumption just focuses on the expected yield of crops. Any technology progress that improves the adaptability of seeds and the fertility of soil should be our concerns. In the next chapter, the scarcity of arable land will be one of the constraints that make farmers rational. Advancements like vertical farming can easily distort the model since the expected yield of crops fully depend on the number of storeys.

* No arbitrage between domestic and international market. Oui, oui, we all know international trade is a big deal. Here, we are creating a utopian closed-system where self-sufficiency is achieved. Later in the discussion, we will expand the naïve model to a more general form to somewhat relax the assumption. Apparently, the pain point is data availability. To map out the arbitrage, the freight cost and the tariff should be taken into consideration. Given the complexity of tax systems and the variety of trade routes, this assumption makes our life easier. 

* No logistic bottleneck and liquidity issue. First of all, all crops are shipped to the nearest buyers to preserve the freshness so the low cost of the cargo can be ignored. Second, probably one of the most controversial assumptions, all crops will be absorbed by the market. Those who cannot be consumed locally will be shipped to the nearest available market.  Those who cannot be consumed domestically will be shipped to the international market. According to my business intelligence, the undersupply caused by weather disruption is the common phenomenon. However, <a href=https://calmatters.org/california-divide/2020/04/california-farmers-coronavirus-food-supply-food-bank>most of the farmers disced excess crops back into the ground during COVID-19</a>. The commies will be like, ‘this is the inherent evilness of capitalism, why not donate surplus load to the food bank before rotting?’ The raison d’être is always the cost, the cost of harvest and transportation.

* No premium and penalty for heterogenous crop quality. We are assuming all crops within the defined category is identical and sells at the same market price. There is no Michelin-restaurant grade Basmati rice, Charlotte potato or blood orange. This is another assumption caused by data availability. Agricultural products have far more sophisticated grades than other commodities. Different origins usually refer to different percentages of nutrients (like Brent or WTI). Different varieties lead to different tastes (blueberry/blackberry/raspberry). Then you have labels of organic, conventional or gene-modified. Even brand premiums! See that Zespri on your sungold kiwis? Homogeneity greatly reduces the workload of price collection.

### Theoretical Framework

As we have mentioned in the assumptions, the objective of the farmers is straight forward, profit maximization. The profit equals to unit revenue minus unit cost then times the quantity. Inevitably farmers would love to increase as much output as possible since they gain no control over the unit cost. There is only one small faux pas, too much supply can damage the crop price which ultimately leads to the decrease of the total revenue. Hence, farmers have to strike a delicate balance to plant each type of crop. When facing oversupply of one type of crop, farmers need to decide whether the greater market share can compensate the loss from the crop price, or it is wise to switch to another type of crop.

Nevertheless, the game isn’t this simple. There is limited supply of arable land inside the system. For the sake of biodiversity, chopping off woods to grow crops requires approval from the local government. Farmers do not have the luxury to grow infinite number of plants. Additionally, each type of crop requires different amount of plantation area (the inverse of the yield). Trees are kept a larger distance from each other to prevent competition for essential nutrients. On the contrary, the field of roots and tubers has higher density. 

Moreover, Farmers need to consider the biological features of the crops. Crops are categorized as annual, biennial and perennial plants. Annual plants grow and die within a year. They are the prime target for crop rotation to improve soil structure and organic matter. Biennial plants grow and die within two years. To make our life easier, we consider biennial plants as annual plants which is a common practice in farms. Perennial plants take years to grow and mature and their lifespan can be longer than Homo Sapiens. Farmers are unlikely to chop off perennial plants which can still bear fruits for the next few years. They have fewer incentives to grow perennial plants which take years to bear fruits. What if this year’s price rally of :apple: turns to a price freefall next year?

Last but not least, there may be government policies. Farmers may be entitled to subsidies if they grow specific types of crops. The government may have mandatory minimum quantity for grains to avoid the food crisis. These non-market behaviors can influence farmers’ choice of crops.

After careful considerations of everything we mention above, we come up with the following framework.

**Objective Function**
maximize total profit regarding supply and demand for all crops

**Constraints**

* limited arable land
* annual crop rotation
* perennial crop lifespan
* government policy

![alt text](https://github.com/je-suis-tm/quant-trading/blob/master/Smart%20Farmers%20project/preview/naive%20model.PNG) 

![alt text](https://github.com/je-suis-tm/quant-trading/blob/master/Smart%20Farmers%20project/preview/pricing%20mechanism.PNG) 

![alt text](https://github.com/je-suis-tm/quant-trading/blob/master/Smart%20Farmers%20project/preview/price%20change%20derivation.PNG) 

![alt text](https://github.com/je-suis-tm/quant-trading/blob/master/Smart%20Farmers%20project/preview/demand%20model.PNG) 

![alt text](https://github.com/je-suis-tm/quant-trading/blob/master/Smart%20Farmers%20project/preview/naive%20model%20matrix.PNG) 

### Data Specification

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

![alt text](https://github.com/je-suis-tm/quant-trading/blob/master/Smart%20Farmers%20project/preview/ricardian%20model.PNG) 

### Further Reading
