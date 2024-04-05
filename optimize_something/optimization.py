""""""  		  	   		  		 		  		  		    	 		 		   		 		  
"""MC1-P2: Optimize a portfolio.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
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
  		  	   		  		 		  		  		    	 		 		   		 		  
Student Name: Shichao Zhou (replace with your name)  		  	   		  		 		  		  		    	 		 		   		 		  
GT User ID: szhou401 (replace with your User ID)  		  	   		  		 		  		  		    	 		 		   		 		  
GT ID: 903948749 (replace with your GT ID)  		  	   		  		 		  		  		    	 		 		   		 		  
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from util import get_data, plot_data
import scipy.optimize as spo
def optimize_portfolio(
    sd=dt.datetime(2008, 1, 1),
    ed=dt.datetime(2009, 1, 1),
    syms=["GOOG", "AAPL", "GLD", "XOM"],
    gen_plot=False):
    """
    This function should find the optimal allocations for a given set of stocks. You should optimize for maximum Sharpe
    Ratio. The function should accept as input a list of symbols as well as start and end dates and return a list of
    floats (as a one-dimensional numpy array) that represents the allocations to each of the equities. You can take
    advantage of routines developed in the optional assess portfolio project to compute daily portfolio value and
    statistics.

    :param sd: A datetime object that represents the start date, defaults to 1/1/2008
    :type sd: datetime
    :param ed: A datetime object that represents the end date, defaults to 1/1/2009
    :type ed: datetime
    :param syms: A list of symbols that make up the portfolio (note that your code should support any
        symbol in the data directory)
    :type syms: list
    :param gen_plot: If True, optionally create a plot named plot.png. The autograder will always call your
        code with gen_plot = False.
    :type gen_plot: bool
    :return: A tuple containing the portfolio allocations, cumulative return, average daily returns,
        standard deviation of daily returns, and Sharpe ratio
    :rtype: tuple
    """

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices_all = prices_all.fillna(method='ffill')  # filling forward incomplete data
    prices_all = prices_all.fillna(method='bfill')  # filling backward incomplete data
    norm_price = normalize_price(prices_all)
    prices = norm_price[syms]  # only portfolio symbols
    prices_SPY = norm_price["SPY"]  # only SPY, for plot comparison later
    # add code here to find the allocations
    allocs = find_optimal_allocations(prices)

    # port_val = prices_SPY  # add code here to compute daily portfolio values
    port_val = compute_daily_portfolio_values(prices, allocs)
    # print(port_val)
    # add code here to compute stats
    cr, adr, sddr, sr = compute_portfolio_stats(port_val)

    # # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        df_temp = df_temp / df_temp.iloc[0]  # normalize the values
        #plot using matplotlib
        df_temp.plot()
        plt.grid()
        plt.title("Daily Portfolio Value VS SPY Value")
        plt.xlabel("Date")
        plt.ylabel("Normalized Value")
        plt.savefig("images/Figure1.png")

    return allocs, cr, adr, sddr, sr

def normalize_price(orinal_px):
    return orinal_px / orinal_px.iloc[0, :]
 # Compute daily portfolio values
def compute_daily_portfolio_values(prices, allocs):
    # normed = prices / prices.iloc[0] # normalized prices
    alloced = prices * allocs # allocated to each
    port_val_t = alloced.sum(axis=1) # daily total value of a portfolio

    return port_val_t

# Portfolio statistics
def compute_portfolio_stats(port_val):
    cr = (port_val.iloc[-1] / port_val.iloc[0]) - 1  # cumulative return : (last value /first value) - 1
    adr = compute_daily_returns(port_val).mean() # average daily return
    sddr = compute_daily_returns(port_val).std(
        ddof=1) # standard deviation daily return # https://stackoverflow.com/questions/27600207/why-does-numpy-std-give-a-different-result-to-matlab-std
    sr = (adr / sddr) * np.sqrt(252)  # daily return sharpe _ ratio : 252 trading days in a year; assuming risk free rate is 0%
    return cr, adr, sddr, sr
def compute_daily_returns(port_val):
    return (port_val / port_val.shift(1)) - 1
# finding the optimal allocations and maximazing the sharpe ratio
def find_optimal_allocations(prices):
    def minimize_neg_sr_val(allocs):
        port_val = compute_daily_portfolio_values(prices, allocs)
        daily_returns = compute_daily_returns(port_val)
        # daily_returns = port_val[1:]
        adr = daily_returns.mean()
        sddr = daily_returns.std(ddof = 1)
        return -(adr / sddr) * np.sqrt(252)  # negative Sharpe Ratio

# def find_optimal_allocations(prices):
    num_stocks = len(prices.count())
    bounds = [(0, 1) for _ in range(num_stocks)]
    constraints = ({'type': 'eq', 'fun': lambda allocs: 1.0 - np.sum(allocs)})
    initial_guess = [1. / num_stocks] * num_stocks
    result = spo.minimize(minimize_neg_sr_val, initial_guess, method='SLSQP', bounds=bounds, constraints=constraints)  # minimizing the negative sharpe ratio, we will effectively maximizing the actual sharpe ratio
    return result.x

def test_code():
    """
    This function WILL NOT be called by the auto grader.
    """

    start_date = dt.datetime(2009, 1, 1)
    end_date = dt.datetime(2010, 1, 1)
    symbols = ["GOOG", "AAPL", "GLD", "XOM", "IBM"]

    # Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(
        sd=start_date, ed=end_date, syms=symbols, gen_plot=False
    )

    # Print statistics
    print(f"Start Date: {start_date}")
    print(f"End Date: {end_date}")
    print(f"Symbols: {symbols}")
    print(f"Allocations:{allocations}")
    print(f"Sharpe Ratio: {sr}")
    print(f"Volatility (stdev of daily returns): {sddr}")
    print(f"Average Daily Return: {adr}")
    print(f"Cumulative Return: {cr}")


if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    # test_code()
    optimize_portfolio(sd='2008-06-01', ed='2009-06-01', syms=['IBM','X', 'GLD', 'JPM'], gen_plot=True)
