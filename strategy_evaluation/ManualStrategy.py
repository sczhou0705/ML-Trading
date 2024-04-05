import math
import matplotlib.pyplot as plt

from util import get_data, plot_data
from marketsimcode import compute_portvals
from indicators import rsi, bbp, momentum, golden_cross,macd

import pandas as pd
import datetime as dt

class ManualStrategy(object):
    """
    Manual trading strategy using RSI, BBP, and Macd indicators.
    """
    def author(self):
        return 'szhou401'
    def __init__(self):
        self.long_entries = [] 
        self.short_entries = []

    def testPolicy(self, symbol='AAPL', sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31), sv=100000):
        dates = pd.date_range(sd, ed)
        prices = get_data([symbol], dates).drop(['SPY'], axis=1)
        rsi_df= rsi(prices, 14, symbol,False) 
        bbp_df = bbp(prices,False)          
        # momentum_df = momentum(prices, lookback,symbol,False)  
        # golden_cross_df = golden_cross(prices,symbol,make_plot=False) 
        macd_df = macd(prices, symbol, False)
        manual_orders = pd.DataFrame(index=prices.index)
        manual_orders['Symbol'] = symbol
        manual_orders['Order'] = None
        manual_orders['Shares'] = 0
        self.long_entries = [] 
        self.short_entries = []
        net_holdings = 0

        for curr_date in manual_orders.index:
            if curr_date in rsi_df.index and curr_date in bbp_df.index and curr_date in macd_df.index:
                rsi_val = rsi_df.loc[curr_date]
                bbp_val = bbp_df.loc[curr_date]
                macd_val = macd_df.loc[curr_date]['MACD Histogram']
                if (rsi_val >= 59) and (macd_val < 0) and (bbp_val >= 0.8):
                    if net_holdings > 0:
                        manual_orders.at[curr_date, 'Order'] = 'SELL'
                        manual_orders.at[curr_date, 'Shares'] = 1000  
                        net_holdings -= 1000
                        self.short_entries.append(curr_date)
                elif (rsi_val <= 35) and (macd_val > 0) and (bbp_val <= 0.2):
                    if net_holdings <= 0:
                        manual_orders.at[curr_date, 'Order'] = 'BUY'
                        manual_orders.at[curr_date, 'Shares'] = 1000  
                        net_holdings += 1000
                        self.long_entries.append(curr_date)
        # manual_orders.dropna(how='any', inplace=True)
        # print(manual_orders)
        return manual_orders        
                    
                   
    def benchmark_policy(self, symbol='AAPL', sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000):
        """
             The performance of a portfolio starting with $100,000 cash, 
             investing in 1000 shares of the symbol in use on the first trading day,  
             and holding that position. Include transaction costs. 
        """

        dates = pd.date_range(sd, ed)
        prices = get_data([symbol], dates).drop(['SPY'], axis=1)
        actual_start = prices.index[0]

        benchmark_orders = prices.copy()
        benchmark_orders[symbol] = symbol
        benchmark_orders['Order'] = 'BUY'
        benchmark_orders['Shares'] = 0

        benchmark_orders.rename(columns={symbol: 'Symbol'}, inplace=True)
        benchmark_orders.at[actual_start, 'Shares'] = 1000
        return benchmark_orders

    def evaluate_ms(self):
        """
            Manual Strategy approach vs benchmark approach
        """

        # In-Sample
        sd = dt.datetime(2008, 1, 1)
        ed = dt.datetime(2009, 12, 31)

        benchmark_orders = self.benchmark_policy(symbol='JPM', sd=sd, ed=ed)
        benchmark_portval = compute_portvals(benchmark_orders, start_val=100000,commission=9.95, impact=0.005)
        benchmark_portval.columns = ['Benchmark PortVal']
        benchmark_portval /= benchmark_portval.iloc[0]

        manual_orders = self.testPolicy(symbol='JPM', sd=sd, ed=ed)
        manual_portval = compute_portvals(manual_orders, start_val=100000,commission=9.95, impact=0.005)
        manual_portval.columns = ['Manual Strategy PortVal']
        manual_portval /= manual_portval.iloc[0]

        portval_df = pd.concat([benchmark_portval, manual_portval], axis=1)

        portval_graph = portval_df.plot(title="Benchmark vs Manual Strategy Portfolio Value (In-Sample)", fontsize=12,
                                        grid=True, color=['purple', 'red'])
        portval_graph.set_xlabel("Date")
        portval_graph.set_ylabel("Normalized Portfolio Value")

        for date in self.long_entries:
            portval_graph.axvline(x=date, color='blue', linestyle='--', linewidth=1)

        for date in self.short_entries:
            portval_graph.axvline(x=date, color='black', linestyle='--', linewidth=1)
        plt.savefig("images/benchmark_vs_manual_in.png")

        benchmark_cr = (benchmark_portval.iloc[-1].at['Benchmark PortVal'] / benchmark_portval.iloc[0].at[
            'Benchmark PortVal']) - 1
        benchmark_adr = benchmark_portval.pct_change(1).mean()['Benchmark PortVal']
        benchmark_sddr = benchmark_portval.pct_change(1).std()['Benchmark PortVal']
        benchmark_sr = math.sqrt(252.0) * (benchmark_adr / benchmark_sddr)

        manual_cr = (manual_portval.iloc[-1].at['Manual Strategy PortVal'] / manual_portval.iloc[0].at[
            'Manual Strategy PortVal']) - 1
        manual_adr = manual_portval.pct_change(1).mean()['Manual Strategy PortVal']
        manual_sddr = manual_portval.pct_change(1).std()['Manual Strategy PortVal']
        manual_sr = math.sqrt(252.0) * (manual_adr / manual_sddr)

        print("------In Sample------")

        print("Date Range: {} to {}".format(sd, ed))

        print("Cumulative Return of Benchmark: {}".format(benchmark_cr))
        print("Cumulative Return of Manual: {}".format(manual_cr))

        print("Standard Deviation of Benchmark: {}".format(benchmark_sddr))
        print("Standard Deviation of Manual: {}".format(manual_sddr))

        print("Average Daily Return of Benchmark: {}".format(benchmark_adr))
        print("Average Daily Return of Manual: {}".format(manual_adr))

        print("Sharpe Ratio of Benchmark: {}".format(benchmark_sr))
        print("Sharpe Ratio of Manual: {}".format(manual_sr))

     

        # Out of Sample
        sd = dt.datetime(2010, 1, 1)
        ed = dt.datetime(2011, 12, 31)
        benchmark_orders = self.benchmark_policy(symbol='JPM')  
        benchmark_portval = compute_portvals(benchmark_orders, start_val=100000,commission=9.95,impact=0.005)
        benchmark_portval.columns = ['Benchmark PortVal']
        benchmark_portval /= benchmark_portval.iloc[0]

        manual_orders = self.testPolicy(symbol='JPM')
        manual_portval = compute_portvals(manual_orders, start_val=100000,commission=9.95,impact=0.005)
        manual_portval.columns = ['Manual Strategy PortVal']
        manual_portval /= manual_portval.iloc[0]

        portval_df = pd.concat([benchmark_portval, manual_portval], axis=1)

        portval_graph = portval_df.plot(title="Benchmark vs Manual Strategy Portfolio Value (Out-of-Sample)",
                                        fontsize=12, grid=True, color=['purple', 'red'])
        portval_graph.set_xlabel("Date")
        portval_graph.set_ylabel("Normalized Portfolio Value")


        for date in self.long_entries:
            portval_graph.axvline(x=date, color='blue', linestyle='--', linewidth=1)

        for date in self.short_entries:
            portval_graph.axvline(x=date, color='black', linestyle='--', linewidth=1)
        plt.savefig("images/benchmark_vs_manual_out.png")

        benchmark_cr = (benchmark_portval.iloc[-1].at['Benchmark PortVal'] / benchmark_portval.iloc[0].at[
            'Benchmark PortVal']) - 1
        benchmark_adr = benchmark_portval.pct_change(1).mean()['Benchmark PortVal']
        benchmark_sddr = benchmark_portval.pct_change(1).std()['Benchmark PortVal']
        benchmark_sr = math.sqrt(252.0) * (benchmark_adr / benchmark_sddr)

        manual_cr = (manual_portval.iloc[-1].at['Manual Strategy PortVal'] / manual_portval.iloc[0].at[
            'Manual Strategy PortVal']) - 1
        manual_adr = manual_portval.pct_change(1).mean()['Manual Strategy PortVal']
        manual_sddr = manual_portval.pct_change(1).std()['Manual Strategy PortVal']
        manual_sr = math.sqrt(252.0) * (manual_adr / manual_sddr)

   
        print("------Out-of-Sample------")

        print("Date Range: {} to {}".format(sd, ed))

        print("Cumulative Return of Benchmark: {}".format(benchmark_cr))
        print("Cumulative Return of Manual: {}".format(manual_cr))

        print("Standard Deviation of Benchmark: {}".format(benchmark_sddr))
        print("Standard Deviation of Manual: {}".format(manual_sddr))

        print("Average Daily Return of Benchmark: {}".format(benchmark_adr))
        print("Average Daily Return of Manual: {}".format(manual_adr))

        print("Sharpe Ratio of Benchmark: {}".format(benchmark_sr))
        print("Sharpe Ratio of Manual: {}".format(manual_sr))



