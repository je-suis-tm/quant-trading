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

&nbsp;

**Objective Function**

Maximize total profit regarding supply and demand for each type of crop

**Constraints**

* Government intervention 
* Annual crop rotation
* Perennial crop lifespan
* Limited arable land

&nbsp;

![alt text](https://github.com/je-suis-tm/quant-trading/blob/master/Smart%20Farmers%20project/preview/naive%20model.PNG) 

As we have mentioned in the assumptions, the objective of the farmers is straight forward, profit maximization. The profit equals to unit revenue minus unit cost then times the quantity. Inevitably farmers would love to increase as much output as possible since they gain no control over the unit cost. There is only one small faux pas, too much supply can damage the crop price which ultimately leads to the decrease of the total revenue. Hence, farmers have to strike a delicate balance to plant each type of crop. When facing oversupply of one type of crop, farmers need to decide whether the greater market share can compensate the loss from the crop price, or it is wise to switch to another type of crop. Translated to mathematics, the entire decision on choice of crops becomes the pricing mechanism of each type of crop. We will expand on the topic of pricing later. For the moment, let’s just quickly scan over the main equation. The objective function can be broken down into four parts. The first one is the declaration of maximization. Next, Σ denotes a sum over each type of crop. The first term after Σ is price (everything inside the parenthesis) times production of crop i. The second term after Σ is cost times production of crop i. 

For the cost, it is tricky. If you read <a href=http://www.fao.org/3/ca6411en/ca6411en.pdf>FAO handbook</a>, you will be astonished by the overloaded dimension of the cost data, how are you supposed to collect so much data? According to <a href=https://usda.library.cornell.edu/concern/publications/qz20ss48r>US farm production expenditure summary</a>, the biggest cost is labor (what happened to illegal immigrants?), land, fertilizer and seed. Rents, tractors, trucks, repairs and other fixed costs are always there in spite of the crop choice. The same applies to the labor. Unless the farmers decide to switch crops, they should have plenty of seeds produced by the existing crops. The good news is we are only left with fertilizers and pesticides. There are plenty of free data on the website of <a href=https://www.ifastat.org>IFA</a>. It’s still a pain in the ass given that each type of crop requires a unique intensity of NPK compound fertilizers. After weeks of brainstorming with my friend, it suddenly came to my mind that cost doesn’t have much impact mathematically when we study the aggregated farmer behavior (for individual farmer it’s a huge one). Later, you will see that both inequality and equality constraints are the major factors. At this point, the cost can be simply calculated via production-weighted profit.

Nevertheless, the game isn’t this simple. We cannot ignore the intervention of government policies. Farmers may be entitled to subsidies if they grow specific types of crops. We all know at least one-third of EU budget goes to every EU farmer who meets the requirement of environment, sustainability and biodiversity (<a href=https://www.europeandatajournalism.eu/eng/News/Data-news/1.6-million-farmers-receive-almost-85-percent-of-the-EU-s-agricultural-subsidies>375 € per hectare</a>, younger gets more). Some of the governments in the world maintain food stockpiles in case of a famine. To suffice the government requirement, there must be mandatory minimum production of grains to avoid the food crisis. After all, Hannibal the Cannibal is a real nightmare. These non-market behaviors can influence farmers’ choice of crops. Therefore, this creates our first inequality constraint, the government intervention. It can take the form of either non-negative production or minimum required production of crop i.

Moreover, Farmers need to consider the biological features of the crops. Crops are categorized as <a href=https://en.wikipedia.org/wiki/Annual_plant>annual</a>, <a href=https://en.wikipedia.org/wiki/Biennial_plant>biennial</a> and <a href=https://en.wikipedia.org/wiki/Perennial_plant>perennial</a> plants. Annual plants grow and die within a year. They are the prime target for <a href=https://rodaleinstitute.org/why-organic/organic-farming-practices/crop-rotations>crop rotation</a> to improve soil structure and organic matter. Biennial plants grow and die within two years. To make our life easier, we consider biennial plants as annual plants which is a common practice in farms. Perennial plants take years to grow and mature and their lifespan can be longer than Homo Sapiens. Farmers are unlikely to replace perennial plants which can still bear fruits for the next few years. They have fewer incentives to grow perennial plants which take years to bear fruits. What if this year’s price rally of :apple: turns to a price freefall next year?

Thus, the second inequality constraint is born. For both annual and perennial plants, they are bounded by upper and lower thresholds. The lower threshold of annual plants is determined by the inertia. Even though the farmers have free wills to choose commercially viable crops, their decision will be limited by their knowledge domain and soil suitability. Different crops require different level of soil acidity and other measures. Needless to say, the knowledge takes time to learn. Furthermore, the drainage condition may affect the choice of crops. That’s why we introduce the inertia coefficient ψ, which controls how much hectare of crop i will remain intact. The inertia coefficient ψ is set at 0.8 by default. As observed throughout the dataset, farmers hardly ever experiment new crops above 20% of their plantation area in a single year. 

The upper threshold of annual plants is determined by the crop rotation. Monoculture ends up with the same pest and weed community each year. Crop rotation creates a diverse environment and utilizes the ecosystem service to build up the resilience of the farm. With crop rotation, the theoretical largest plantation area of crop i next year equals to this year’s maximum arable land minus this year’s plantation area of crop i. In another word, the theoretical maximum plantation area of crop i equals to sum of this year’s plantation area of any crops apart from crop i. 

The lower threshold of perennial plants is its long economic lifespan. The biggest issue is that nobody knows the exact age distribution of crop i aside from the actual owner of the farm. At this time, we assume a uniform distribution. Each year only a fraction of crop i reaches the end of their economic lifespan and the rest keeps nourishing. The farmers merely need to decide on the choice of that fraction, replace the old with the new or cut off and try others. To be more precise, that fraction equals to one over ωL where ω denotes the economic lifecycle coefficient (I consulted my agronomist friend and she suggested 0.7) and L denotes the average lifespan of crop i. 

The upper threshold of perennial plants is its long growth period. Some trees take years to bear fruits. Even if we plan to increase the plantation of perennial plants ridiculously, we will only be capable of harvesting so many fruits next year. To be more precise, we can only harvest (ωL+1)/ωL at maximum. Assuming no perennial plants exceed their economic lifespan this year, the plantation increment of crop i should be the same as the fraction that we would’ve chopped off (the fraction in the lower threshold), since the age of crop i is uniformly distributed.

Last but not least, there is limited supply of arable land inside the system. For the sake of ESG, deforestation requires approval from the local government (didn’t stop the notorious palm oil apartheid between EU and Malaysia). Farmers do not have the luxury to grow infinite number of plants. Additionally, each type of crop requires different amount of plantation area. Social distancing is a must for planting trees to prevent competition for sunlight and water. On the contrary, the field of roots and tubers can have higher density. We will take the historic average of the inverse of the yield to get the required hectare per each expected tonne of crop i. This computation allows us to take discount from weather risk, which indicates no bias towards a good year or a bad year.

Hence, we derive the equality constraint, the total available land area for plantation. It is rather difficult to predict how much land area will increase by the issued permits or decrease by the natural disasters. We can only do two things to get around the trouble, take the last available number or create scenarios with inputs from agricultural experts. However, the big malaise of the equality constraint is the life cycle of some annual plants. Some of the crops grow and mature within several months even several weeks. Yet, the time horizon of the whole model is on an annual basis, which implies harvest area of some plants is repeatedly taken into account. The sum of cropland is inevitably larger than the maximum arable land. It is something worth exploring. With no solutions in sight, we have to turn a blind eye for now.

After we set things straight at the objective function and the constraints, we can move onto the core part of the model, the pricing mechanism. Let’s borrow the concept of market equilibrium from microeconomics. Alfred Marshall introduced the idea of supply demand model into economics. Where supply curve with negative slope and demand curve with positive slope intercepts denotes the equilibrium price.

![alt text](https://github.com/je-suis-tm/quant-trading/blob/master/Smart%20Farmers%20project/preview/pricing%20mechanism.PNG) 

By using linear approximation, we obtain the equation above. Price of crop i equals to the equilibrium price plus the mismatch between supply and demand. When supply exceeds demand, the market condition is oversupply. The difference between demand and supply is undisputedly negative. After multiplied by pricing coefficient α, the difference converts from several hundred tonnes to the scale of US dollar per tonne. The equation easily generates a downward pressure on the equilibrium price, and vice versa. With some random disturbance ε (force majeure), the linear regression emerges.

Now that we obtain the pricing mechanism, we plug it back into the original objective function. Because the income per crop is estimated via last available price, the expected unit revenue equals to the latest price plus the change of the price caused by supply fluctuation through the pricing mechanism. The price change can be easily derived via the first order difference of price at time t and t-1. We already know the number of this year’s supply but want to get the answer of next year’s, so we use next year’s supply minus this year’s supply instead of the abbreviation of ∆Q. What is ∆D though?

![alt text](https://github.com/je-suis-tm/quant-trading/blob/master/Smart%20Farmers%20project/preview/price%20change%20derivation.PNG) 

Let’s solve the final piece of the puzzle. Prior to our assumptions of demand, demand is driven by the population and the disposable income. Disposable income is slightly complicated to compute but we can easily find its substitute, GDP per capita. Intuitively we can create a regression model like the pricing mechanism. The only problem is we cannot directly observe the value of demand which bridges the gap between two regression models.

![alt text](https://github.com/je-suis-tm/quant-trading/blob/master/Smart%20Farmers%20project/preview/demand%20model.PNG) 

Fortunately, there is an econometric tool called <a href=https://en.wikipedia.org/wiki/Instrumental_variables_estimation>instrumental variable</a>. By using 2-Stage Least Square, it creates the possibility of making causal inferences with observational data. A valid instrumental variable has a causal effect on unobserved variable but no confounding for the direct effect on the dependent variable. Both population and GDP per capita make brilliant instrumental variables. In layman’s terms, population and GDP per capita have no direct power over the crop price. They can only influence the crop price indirectly through the change of demand. Voila, the only unknown variable inside the framework is expected production of each type of crop.

In order to get the optimal production of each type of crop, we steal something called quadratic programming from the toolbox of convex optimization. We have to transform the equations above into the matrix form below. While using `CVXOPT`, a couple of things are moderately modified. First, we will minimize the negative version of the objective function rather than maximize the objective function. Then, the inequality constraint must follow the form of not-larger-than. Many smaller-than inequalities are converted to the negative version of not-larger-than. At last, we ought to construct block matrix to satisfy the requirement of a single inequality constraint. 

![alt text](https://github.com/je-suis-tm/quant-trading/blob/master/Smart%20Farmers%20project/preview/naive%20model%20matrix.PNG) 

Splendid, all :raised_hands: on deck, it’s about time to move towards the next chapter!

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

1. Angrist JD, Krueger AB (2001) <a href=https://economics.mit.edu/files/18>Instrumental Variables and the Search for Identification: From Supply and Demand to Natural Experiments</a>

2. Komareka AM et al. (2017) <a href=https://www.sciencedirect.com/science/article/pii/S0308521X16304942>Agricultural Household Effects of Fertilizer Price Changes for Smallholder Farmers in Central Malawi</a>

3. Louhichi K et al. (2010) <a href=https://ec.europa.eu/jrc/en/publication/articles-journals/fssim-bio-economic-farm-model-simulating-response-eu-farming-systems-agricultural-and-environmental>FSSIM, A Bio-economic Farm Model for Simulating the Response of EU Farming Systems to Agricultural and Environmental Policies</a>

4. Louhichi K, Gomez y Paloma S (2013) <a href=https://ec.europa.eu/jrc/en/publication/eur-scientific-and-technical-research-reports/modelling-agri-food-policy-impact-farm-household-level-developing-countries-fssim-dev>Modelling Agri-Food Policy Impact at Farm-household Level in Developing Countries (FSSIM-Dev)</a>

5. Marshall A (1890) <a href=http://files.libertyfund.org/files/1676/Marshall_0197_EBk_v6.0.pdf>Principles of Economics</a>

6. Ricardo D (1817) <a href=http://ricardo.ecn.wfu.edu/~cottrell/ecn265/Principles.pdf>On the Principles of Political Economy and Taxation</a>
