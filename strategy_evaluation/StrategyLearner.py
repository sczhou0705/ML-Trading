""""""  		  	   		  		 		  		  		    	 		 		   		 		  
"""  		  	   		  		 		  		  		    	 		 		   		 		  
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		  		 		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		  	   		  		 		  		  		    	 		 		   		 		  
All Rights Reserved  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		  		 		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		  	   		  		 		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		  	   		  		 		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		  	   		  		 		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		  	   		  		 		  		  		    	 		 		   		 		  
or edited.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		  	   		  		 		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		  	   		  		 		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		  		 		  		  		    	 		 		   		 		  
GT honor code violation.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Student Name: Tucker Balch (replace with your name)  		  	   		  		 		  		  		    	 		 		   		 		  
GT User ID: tb34 (replace with your User ID)  		  	   		  		 		  		  		    	 		 		   		 		  
GT ID: 900897987 (replace with your GT ID)  		  	   		  		 		  		  		    	 		 		   		 		  
"""  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
import datetime as dt  		  	   		  		 		  		  		    	 		 		   		 		  
import random  		  	   		  		 		  		  		    	 		 		   		 		  
from QLearner import QLearner 		  	   		  		 		  		  		    	 		 		   		 		  
import pandas as pd  		  	   		  		 		  		  		    	 		 		   		 		  
import util as ut  		  	   		  		 		  		  		    	 		 		   		 		  
from indicators import rsi, bbp, momentum, golden_cross,macd	  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
class StrategyLearner(object):  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    A strategy learner that can learn a trading policy using the same indicators used in ManualStrategy.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		  		 		  		  		    	 		 		   		 		  
        If verbose = False your code should not generate ANY output.  		  	   		  		 		  		  		    	 		 		   		 		  
    :type verbose: bool  		  	   		  		 		  		  		    	 		 		   		 		  
    :param impact: The market impact of each transaction, defaults to 0.0  		  	   		  		 		  		  		    	 		 		   		 		  
    :type impact: float  		  	   		  		 		  		  		    	 		 		   		 		  
    :param commission: The commission amount charged, defaults to 0.0  		  	   		  		 		  		  		    	 		 		   		 		  
    :type commission: float  		  	   		  		 		  		  		    	 		 		   		 		  
    """  
    def author(self):
        return 'szhou401'  	   		  		 		  		  		    	 		 		   		 		  
    # constructor  		  	   		  		 		  		  		    	 		 		   		 		  
    def __init__(self, verbose=False, impact=0.0, commission=0.0):  		  	   		  		 		  		  		    	 		 		   		 		  
        """  		  	   		  		 		  		  		    	 		 		   		 		  
        Constructor method  		  	   		  		 		  		  		    	 		 		   		 		  
        """  		  	   		  		 		  		  		    	 		 		   		 		  
        self.verbose = verbose  		  	   		  		 		  		  		    	 		 		   		 		  
        self.impact = impact  		  	   		  		 		  		  		    	 		 		   		 		  
        self.commission = commission  	
        self.ql = QLearner(num_states=1000, num_actions=3, rar=0)	  	   		  		 		  		  		    	 		 		   		 		  
	  	   		  		 		  		  		    	 		 		   		 		  
   		  	   		  		 		  		  		    	 		 		   		 		  
    def add_evidence(  		  	   		  		 		  		  		    	 		 		   		 		  
        self,  		  	   		  		 		  		  		    	 		 		   		 		  
        symbol="IBM",  		  	   		  		 		  		  		    	 		 		   		 		  
        sd=dt.datetime(2008, 1, 1),  		  	   		  		 		  		  		    	 		 		   		 		  
        ed=dt.datetime(2009, 1, 1),  		  	   		  		 		  		  		    	 		 		   		 		  
        sv=100000,  		  	   		  		 		  		  		    	 		 		   		 		  
    ):  		  	   		  		 		  		  		    	 		 		   		 		  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
        syms = [symbol]
        dates = pd.date_range(sd - dt.timedelta(days=60), ed)
        prices = ut.get_data(syms, dates).drop(['SPY'], axis=1)

        if self.verbose:
            print(prices)		  	   		  		 		  		  		    	 		 		   		 		  
        combined_df = self._prepare_indicators_and_combine(prices, symbol, sd, sv)
        bins = 10 
        combined_df["rsi_bins"] = pd.qcut(combined_df["rsi"], bins, labels=False, duplicates='drop')
        # combined_df["momentum_bins"] = pd.qcut(combined_df["momentum"], bins, labels=False, duplicates='drop')
        combined_df["bbp_bins"] = pd.qcut(combined_df["bbp"], bins, labels=False, duplicates='drop')
        combined_df["macd_bins"] = pd.qcut(combined_df["macd"], bins, labels=False, duplicates='drop')
        # combined_df["golden_cross_bins"] = pd.qcut(combined_df["golden_cross"], bins, labels=False, duplicates='drop')
        self.state_train = (combined_df["bbp_bins"] * 100) + (combined_df["macd_bins"] * 10) + combined_df["rsi_bins"]
        
        iterations = 0

        trades = prices.copy()
        trades = trades.assign(Shares=0).drop([symbol], axis=1)
        
        
        MAX_ITERATIONS = 600
        CONVERGENCE_THRESHOLD = 10
        trades_copy = trades.copy()      
        net_holdings = 0
        action = 0
        for iterations in range(MAX_ITERATIONS):
            # Initialize a flag to check for convergence
            converged = True

            self.ql.querysetstate(self.state_train.iloc[0])

            for idx in range(len(combined_df)):
                date = combined_df.index[idx]
                daily_return_adjusted = combined_df.at[date, "Daily Return"] - (net_holdings * self.impact)

                if action == 0:  # long
                    trade_amount = 1000 if net_holdings != 1000 else 0
                else:  # short
                    trade_amount = -1000 if net_holdings != -1000 else 0

                if idx > CONVERGENCE_THRESHOLD and trade_amount != 0:
                    converged = False

                trades_copy.at[date, 'Shares'] = trade_amount
                net_holdings += trade_amount
                action = self.ql.query(int(self.state_train[date]), daily_return_adjusted)

            if converged:
                break

       
        trades = trades_copy

        self.trades = trades
        # print(self.trades)
    def testPolicy(self, symbol = "IBM", sd=dt.datetime(2009,1,1), ed=dt.datetime(2010,1,1), sv = 100000):
        syms = [symbol]
        dates = pd.date_range(sd - dt.timedelta(days=60), ed)
        prices = ut.get_data(syms, dates).drop(['SPY'], axis=1)

        if self.verbose:
            print(prices)	
        combined_df = self._prepare_indicators_and_combine(prices, symbol, sd, sv)
   
        bins = 10  
        combined_df["rsi_bins"] = pd.qcut(combined_df["rsi"], bins, labels=False, duplicates='drop')
        # combined_df["momentum_bins"] = pd.qcut(combined_df["momentum"], bins, labels=False, duplicates='drop')
        # combined_df["golden_cross_bins"] = pd.qcut(combined_df["golden_cross"], bins, labels=False, duplicates='drop')
        combined_df["macd_bins"] = pd.qcut(combined_df["macd"], bins, labels=False, duplicates='drop')
        combined_df["bbp_bins"] = pd.qcut(combined_df["bbp"], bins, labels=False, duplicates='drop')
        self.state_train = (combined_df["bbp_bins"] * 100) + (combined_df["macd_bins"] * 10) + combined_df["rsi_bins"]
    
        iterations = 0

        trades = prices.copy()
        trades = trades.assign(Shares=0).drop([symbol], axis=1)

        net_holdings = 0

        for date, row in combined_df.iterrows():
            action = self.ql.querysetstate(int(self.state_train[date]))
            trade_amount = 0
            if action == 0: 
                if net_holdings <= 0:  
                    trade_amount = 1000
            elif action == 1:  
                if net_holdings >= 0:  
                    trade_amount = -1000
            trades.at[date, 'Shares'] = trade_amount
            net_holdings += trade_amount

        return trades
    def _prepare_indicators_and_combine(self, prices, symbol, start_date, sv):
        # Get indicators
        rsi_tuple = rsi(prices, 14, symbol, False)
        # momentum_tuple = momentum(prices, 14, symbol, False)
        bbp_tuple = bbp(prices, make_plot=False)
        # golden_cross_tuple = golden_cross(prices,symbol,make_plot=False)
        macd_tuple = macd(prices,symbol,False)
        # Slice indicators from start_date onwards
        rsi_df = rsi_tuple[start_date:]
        # momentum_df = momentum_tuple[start_date:]
        bbp_df = bbp_tuple[start_date:]
        # golden_cross_df = golden_cross_tuple[start_date:]
        macd_df = macd_tuple[start_date:]
        # Adjust prices dataframe and capture daily returns
        prices = prices[start_date:]
        daily_returns, portfolio_value = self.calculate_portfolio_stats(prices, symbol, sv)

        # Combine data into overall dataframe
        combined_df = prices.copy()
        combined_df["rsi"] = rsi_df
        # combined_df["momentum"] = momentum_df
        combined_df["bbp"] = bbp_df
        # combined_df["golden_cross"] = golden_cross_df
        combined_df["macd"] = macd_df['MACD Histogram']
        combined_df["Portfolio"] = portfolio_value
        combined_df["Daily Return"] = daily_returns

        return combined_df
    def calculate_portfolio_stats(self, price_data, symbol, sv):
        normalized_prices = price_data.copy()
        normalized_prices[symbol] = price_data[symbol] / float(price_data[symbol].iloc[0])
        portfolio_value = normalized_prices.sum(axis=1)
        daily_returns = (portfolio_value / portfolio_value.shift(1)) - 1
        daily_returns.iloc[0] = 0
        portfolio_value *= sv   
        return daily_returns, portfolio_value
        	  	   		  		 		  		  		    	 		 		   		 		   		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		  		 		  		  		    	 		 		   		 		  
    print("One does not simply think up a strategy")  		  	   		  		 		  		  		    	 		 		   		 		  
