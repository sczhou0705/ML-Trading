"""Analyze a portfolio."""

import datetime as dt

import numpy as np

import matplotlib.pyplot as plt
import pandas as pd
# from util import get_data, plot_data
from util import get_data
import scipy.optimize as spo

# This is the function that will be tested by the autograder
# The student must updaSte this code to properly implement the functionality
def assess_portfolio(
        sd=dt.datetime(2008, 1, 1),
        ed=dt.datetime(2009, 1, 1),
        syms=["GOOG", "AAPL", "GLD", "XOM"],
        allocs=[0.1, 0.2, 0.3, 0.4],
        gen_plot=False
):
    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices_all = prices_all.fillna(method='ffill')  # filling forward incomplete data
    prices_all = prices_all.fillna(method='bfill')  # filling backward incomplete data
    norm_price = normalize_price(prices_all)
    prices = norm_price[syms]  # only portfolio symbols

    prices_SPY = norm_price["SPY"]  # only SPY, for plot comparison later

    # find the allocations for the optimal portfolio
    # note that the values here ARE NOT meant to be correct for a test case
    # allocs = np.asarray(
    #     [0.2, 0.2, 0.3, 0.3]
    # )
    # add code here to find the allocations
    # optimal_allocs = find_optimal_allocations(prices)

    # port_val = prices_SPY  # add code here to compute daily portfolio values
    port_val = compute_daily_portfolio_values(prices, allocs)
    # print(port_val)
    # add code here to compute stats
    cr, adr, sddr, sr = compute_portfolio_stats(port_val)

    # # Compare daily portfolio value with SPY using a normalized plot
    # if gen_plot:
    #     df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
    #     df_temp = df_temp / df_temp.iloc[0]  # normalize the values
    #     # plot using matplotlib
    #     df_temp.plot(figsize=(12, 6))
    #     plt.grid()
    #     plt.title("Daily Portfolio Value VS SPY Value")
    #     plt.xlabel("Date")
    #     plt.ylabel("Normalized Value")
    #     plt.savefig("images/Figure1.png")

    return cr, adr, sddr, sr


def normalize_price(orinal_px):
    return orinal_px / orinal_px.iloc[0, :]
#
#
#
# Compute daily portfolio values
def compute_daily_portfolio_values(prices, allocs):
    alloced = prices * allocs  # allocated to each
    daily_port_val = alloced.sum(axis=1)  # daily total value of a portfolio
    return daily_port_val


# Portfolio statistics
def compute_portfolio_stats(port_value):
    cr = (port_value.iloc[-1] / port_value.iloc[0]) - 1  # cumulative return : (last value /first value) - 1
    adr = compute_daily_returns(port_value).mean()  # average daily return
    sddr = compute_daily_returns(port_value).std(
        ddof=1)  # standard deviation daily return # https://stackoverflow.com/questions/27600207/why-does-numpy-std-give-a-different-result-to-matlab-std
    sr = (adr / sddr) * np.sqrt(
        252)  # daily return sharpe _ ratio : 252 trading days in a year; assuming risk free rate is 0%
    return cr, adr, sddr, sr


def compute_daily_returns(port_value):
    return (port_value / port_value.shift(1)) - 1


def test_code():
    """
    Performs a test of your code and prints the results
    """
    # This code WILL NOT be tested by the auto grader
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!
    start_date = dt.datetime(2009, 1, 1)
    end_date = dt.datetime(2010, 1, 1)
    symbols = ["GOOG", "AAPL", "GLD", "XOM"]
    allocations = [0.2, 0.3, 0.4, 0.1]
    # start_val = 1000000
    # risk_free_rate = 0.0
    # sample_freq = 252

    # Assess the portfolio
    # cr, adr, sddr, sr, ev = assess_portfolio(
    #     sd=start_date,
    #     ed=end_date,
    #     syms=symbols,
    #     # allocs=allocations,
    #     # sv=start_val,
    #     gen_plot=False,
    # )
    # Assess the portfolio
    allocations,cr, adr, sddr, sr = assess_portfolio(
        sd=start_date, ed=end_date, syms=symbols, gen_plot=False
    )
    # Print statistics
    print(f"Start Date: {start_date}")
    print(f"End Date: {end_date}")
    print(f"Symbols: {symbols}")
    print(f"Allocations: {allocations}")
    print(f"Sharpe Ratio: {sr}")
    print(f"Volatility (stdev of daily returns): {sddr}")
    print(f"Average Daily Return: {adr}")
    print(f"Cumulative Return: {cr}")


if __name__ == "__main__":
    test_code()