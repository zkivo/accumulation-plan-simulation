# Accumulation Plan Simulations
Dollar Cost Averaging or Simple Market Timing? Once you have a salary and start asking yourself whether you should invest regularly part of your paycheck into some world indices, or wait for a drop, you should know what you are getting into. In this project, I am doing a simulation between simple dollar cost averaging, i.e., investing in an index every month when the paycheck is received, and simple market timing. For example, since we cannot forecast the future, a simple strategy can consist on waiting until a drop of the market to invest. The drop can be 5%, 10%, or 15%.

The code can be "easily" changed to simulate different markets. However, a good passive investor, in my opinion, should know how these simple strategies work with one of the simplest and most boring market, i.e., the world market.

![msci-graph](https://github.com/zkivo/accumulation-plan-simulation/assets/58048638/0c7bbdab-1f3b-44c7-b046-8bf35156facc)

Simulation: buying with all the accumulated salaries at each 5% drop from all-time high.

The simulation suggests that investing regularly (Dollar Cost Averaging) without trying to market timing by waiting a drop of 5%, it provides better outcomes.

Example output
```
Processing file: MSCI World Historical Data.csv
market timing / dca = [0.8113798287646228]
unused salaries in market timing =  29
```

Also 29 salaries were unused by waiting a drop of 5% in this simulation. This can also be seen in the graphs above. For two years there has been one drop of 5% from all-time high. 
