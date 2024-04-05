import math
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt

from util import get_data, plot_data
from marketsimcode import compute_portvals
from ManualStrategy import ManualStrategy
from StrategyLearner import StrategyLearner

def author(self):
    return 'szhou401'
def e1_test_strategy(symbol, sd, ed, impact, is_in_sample=True):
    ms = ManualStrategy()
    sl = StrategyLearner(impact=impact)

    # Manual Strategy 
    manual_orders = ms.testPolicy(symbol, sd=sd, ed=ed)
    manual_portval = compute_portvals(manual_orders, start_val=100000, commission=9.95, impact=0.005)
    manual_portval.columns = ['Manual Strategy PortVal']
    manual_portval /= manual_portval.iloc[0]

    # Strategy Learner 
    sl.add_evidence(symbol=symbol, sd=sd, ed=ed, sv=100000)
    trades = sl.testPolicy(symbol=symbol, sd=sd, ed=ed, sv=100000)
    trades['Symbol'] = symbol
    trades['Order'] = 'BUY'

    strategy_trades = 0

    for date, row in trades.iterrows():
        trades.at[date, 'Order'] = 'SELL' if row['Shares'] == -1000 else 'BUY'
        strategy_trades += 1 if row['Shares'] != 0 else 0

    strategy_portval = compute_portvals(trades, start_val=100000, commission=9.95, impact=0.005)
    strategy_portval.columns = ['Strategy Learner PortVal']
    strategy_portval /= strategy_portval.iloc[0]

    # Benchmark Strategy 
    benchmark_orders = ms.benchmark_policy(symbol=symbol, sd=sd, ed=ed)
    benchmark_portval = compute_portvals(benchmark_orders, start_val=100000, commission=9.95, impact=0.005)
    benchmark_portval.columns = ['Benchmark PortVal']
    benchmark_portval /= benchmark_portval.iloc[0]

    # Plot
    portval_df = pd.concat([strategy_portval, manual_portval, benchmark_portval], axis=1)
    title = f"Exp. 1: {'InSample' if is_in_sample else 'OutofSample'} - Strategy vs Manual vs Benchmark(impact=0.005)"
    portval_graph = portval_df.plot(title=title, fontsize=12, grid=True)
    portval_graph.set_xlabel("Date")
    portval_graph.set_ylabel("Normalized Portfolio Value")
    plt.savefig(f"images/Experiment1_Figure_{'In' if is_in_sample else 'Out'}.png")

    # Performance Metrics
    # Manual Strategy Metrics
    manual_cr = (manual_portval.iloc[-1] / manual_portval.iloc[0]) - 1
    manual_adr = manual_portval.pct_change(1).mean()
    manual_sddr = manual_portval.pct_change(1).std()
    manual_sr = math.sqrt(252.0) * (manual_adr / manual_sddr)

    # Strategy Learner Metrics
    strategy_cr = (strategy_portval.iloc[-1] / strategy_portval.iloc[0]) - 1
    strategy_adr = strategy_portval.pct_change(1).mean()
    strategy_sddr = strategy_portval.pct_change(1).std()
    strategy_sr = math.sqrt(252.0) * (strategy_adr / strategy_sddr)

    # Benchmark Metrics
    benchmark_cr = (benchmark_portval.iloc[-1] / benchmark_portval.iloc[0]) - 1
    benchmark_adr = benchmark_portval.pct_change(1).mean()
    benchmark_sddr = benchmark_portval.pct_change(1).std()
    benchmark_sr = math.sqrt(252.0) * (benchmark_adr / benchmark_sddr)

    # Print Metrics
    print(f"\n{'In-Sample' if is_in_sample else 'Out-of-Sample'} Performance Metrics")
    print("Date Range: {} to {}".format(sd, ed))
    print_metrics("Manual", manual_cr, manual_adr, manual_sddr, manual_sr)
    print_metrics("Strategy Learner", strategy_cr, strategy_adr, strategy_sddr, strategy_sr)
    print_metrics("Benchmark", benchmark_cr, benchmark_adr, benchmark_sddr, benchmark_sr)

def print_metrics(label, cr, adr, sddr, sr):
    print(f"\nMetrics for {label}:")
    print("Cumulative Return: {}".format(cr.iloc[0]))
    print("Average Daily Return: {}".format(adr.iloc[0]))
    print("Standard Deviation of Daily Return: {}".format(sddr.iloc[0]))
    print("Sharpe Ratio: {}".format(sr.iloc[0]))

def compare(symbol='JPM',impact=0.005):
    # In-Sample Test
    e1_test_strategy(symbol, sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), impact=0.005, is_in_sample=True)

    # Out-of-Sample Test
    e1_test_strategy(symbol, sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), impact=0.005, is_in_sample=False)

if __name__ == "__main__":
    compare()
