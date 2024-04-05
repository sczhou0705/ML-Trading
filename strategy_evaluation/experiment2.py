import math
import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from util import get_data, plot_data
from marketsimcode import compute_portvals
from indicators import rsi, bbp, momentum, golden_cross,macd
from ManualStrategy import ManualStrategy
from StrategyLearner import StrategyLearner
def author(self):
    return 'szhou401'
def compare2(symbol='JPM', sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), impact=0.0):
    sl = StrategyLearner(impact=impact)
    sl.add_evidence(symbol=symbol, sd=sd, ed=ed, sv=100000)

    trades = sl.testPolicy(symbol=symbol, sd=sd, ed=ed, sv=100000)
    trades['Symbol'] = symbol
    trades['Order'] = 'BUY'

    str_trades = 0

    for date, row in trades.iterrows():
        trades.at[date, 'Order'] = 'SELL' if row['Shares'] == -1000 else 'BUY'
        str_trades += int(row['Shares'] != 0)


    str_portval = compute_portvals(trades, start_val=100000, commission=0.0, impact=impact)

    str_portval.columns = ['Strategy Learner PortVal']
    str_portval /= str_portval.iloc[0]

    return str_portval, str_trades

#
def evaluate_e2(initial_impact=0.000, impact_increment=0.005, iterations=5, start_date=dt.datetime(2008, 1, 1), end_date=dt.datetime(2009, 12, 31)):
    impact = initial_impact
    dfs = []
    trades_data =[]
    print("-------experiment2(In Sample)---------")
    print("Date Range: {} to {}".format(start_date, end_date))

    for i in range(iterations):
        str_portval, str_trades = compare2(impact=impact)
        trades_data.append((impact,str_trades))
        # strategy learner values
        str_cr = (str_portval.iloc[-1].at['Strategy Learner PortVal'] / str_portval.iloc[0].at['Strategy Learner PortVal']) - 1
        str_adr = str_portval.pct_change(1).mean()['Strategy Learner PortVal']
        str_sddr = str_portval.pct_change(1).std()['Strategy Learner PortVal']


        print(f"Cumulative Return of Strategy (Impact: {impact}): {str_cr}")
        print(f"Standard Deviation of Strategy (Impact: {impact}): {str_adr}")
        print(f"Average Daily Return of Strategy (Impact: {impact}): {str_sddr}")
        print(f"Number of Trades for Strategy (Impact: {impact}): {str_trades}")
        str_portval.rename(columns={"Strategy Learner PortVal": f"Impact: {impact}"}, inplace=True)
        dfs.append(str_portval)

        impact += impact_increment

    portval_df = pd.concat(dfs, axis=1)
    #graph1
    portval_graph = portval_df.plot(title="Strategy Learner Impact Sensitivity", fontsize=12, grid=True)
    portval_graph.set_xlabel("Date")
    portval_graph.set_ylabel("Normalized Portfolio Value")
    plt.savefig("images/experiment2_1.png")
    #graph2
    trades_df = pd.DataFrame(trades_data, columns=['Impact', 'Number of Trades'])
    trades_graph = trades_df.plot(x='Impact', y='Number of Trades', kind='bar', title="Number of Trades for Different Impacts", fontsize=12, grid=True)
    trades_graph.set_xlabel("Impact")
    trades_graph.set_ylabel("Number of Trades")
    trades_graph.set_xticklabels(trades_graph.get_xticklabels(), rotation=45)
    plt.savefig("images/experiment2_2.png")