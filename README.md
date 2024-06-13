# Accumulation Plan Simulations
Dollar Cost Averaging or Simple Market Timing? Once you have a salary and start asking yourself whether you should invest regularly part of your paycheck into some world indices, or wait for a drop, you should know what you are getting into. In this project, I am doing a simulation between simple dollar cost averaging, i.e., investing in an index every month when the paycheck is received, and simple market timing. For example, since we cannot forecast the future, a simple strategy can consist on waiting until a drop of the market to invest. The drop can be 5%, 10%, or 15%.

The code can be "easily" changed to simulate different markets. However, a good passive investor, in my opinion, should know how these simple strategies work with one of the simplest and most boring (but best) market, i.e., the world market.

# Results of simulation

![msci-graph](https://github.com/zkivo/accumulation-plan-simulation/assets/58048638/0c7bbdab-1f3b-44c7-b046-8bf35156facc)

## Table of performance: Market timing / DCA

|market                                  |Drop 5%|Drop 10%|Drop 15%|Drop 20%|
|----------------------------------------|-------|--------|--------|--------|
|FTSE All World Historical Price Data.csv|-22.99% |-18.79%  |-12.16%  |-3.87%   |
|MSCI World Historical Data.csv          |-18.86% |-16.99%  |-9.75%   |-11.51%  |
|S&P 500 Historical Data.csv             |-7.98%  |-20.83%  |-28.63%  |-41.57%  |

## Table of # of unused salaries at the end date

|market                                  |Drop 5%|Drop 10%|Drop 15%|Drop 20%|
|----------------------------------------|-------|--------|--------|--------|
|FTSE All World Historical Price Data.csv|29     |27      |25      |23      |
|MSCI World Historical Data.csv          |29     |28      |25      |24      |
|S&P 500 Historical Data.csv             |2      |0       |14      |156     |

Above are the results of the simulation. This simulation consider two world indicies and one for the USA market, just for comparison.

The first table shows the performace of each strategies compared to the normal DCA, meanwhile the second shows how many salaries are not used at the end of the simulation period. The strategies are shown under the **drop** columns, and as we can see they all underperform the simple DCA strategies. Leaving, also, the investor with many paycheck not invested.  

# data
FTSE All World: daily data starting from 10/14/2013.
MSCI world: daily data starting from 07/09/2012.
S&P 500: daily data starting from 12/26/1979.


