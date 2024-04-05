""""""  		  	   		  		 		  		  		    	 		 		   		 		  
"""MC2-P1: Market simulator.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
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
  		  	   		  		 		  		  		    	 		 		   		 		  
Student Name: Shichao Zhou(replace with your name)  		  	   		  		 		  		  		    	 		 		   		 		  
GT User ID: szhou401 (replace with your User ID)  		  	   		  		 		  		  		    	 		 		   		 		  
GT ID: 900897987 (replace with your GT ID)  		  	   		  		 		  		  		    	 		 		   		 		  
"""

import datetime as dt
# import os

import numpy as np

import pandas as pd
from util import get_data, plot_data


def compute_portvals(
        orders_file="./orders/orders.csv",
        start_val=1000000,
        commission=9.95,
        impact=0.005,
):
    """
    Computes the portfolio values.

    :param orders_file: Path of the order file or the file object
    :type orders_file: str or file object
    :param start_val: The starting value of the portfolio
    :type start_val: int
    :param commission: The fixed amount in dollars charged for each transaction (both entry and exit)
    :type commission: float
    :param impact: The amount the price moves against the trader compared to the historical data at each transaction
    :type impact: float
    :return: the result (portvals) as a single-column dataframe, containing the value of the portfolio for each trading day in the first column from start_date to end_date, inclusive.
    :rtype: pandas.DataFrame
    """
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # TODO: Your code here
    df = pd.read_csv(orders_file, index_col='Date', parse_dates=True, na_values=['nan'])
    order_dts = df.index
    start_dt = df.index[0]
    end_dt = df.index[-1]

    portvals = get_data(['SPY'], pd.date_range(start_dt, end_dt), addSPY=True, colname='Adj Close')
    portvals = portvals.rename(columns={'SPY': 'value'})
    dates = portvals.index

    curr_cash = start_val
    positions = {}
    tickers = {}

    def process_order(order, curr_cash, positions, tickers, dt, end_dt, commission, impact):
        ticker = order.loc['Symbol']
        action = order.loc['Order']
        quantity = order.loc['Shares']
        return update_positions(ticker, action, quantity, curr_cash, positions, tickers, dt, end_dt, commission, impact)

    for dt in dates:
        if dt in order_dts:
            order_details = df.loc[dt]

            # If there are multiple orders on the same day
            if isinstance(order_details, pd.DataFrame):
                for _, row in order_details.iterrows():
                    curr_cash, positions, tickers = process_order(row, curr_cash, positions, tickers, dt, end_dt,
                                                                  commission, impact)
            else:
                curr_cash, positions, tickers = process_order(order_details, curr_cash, positions, tickers, dt, end_dt,
                                                              commission, impact)

        # Calculate porfolio value
        mktVal = 0
        for posi in positions:
            mktVal += tickers[posi].loc[dt].loc[posi] * positions[posi]
        portvals.loc[dt, 'value'] = mktVal + curr_cash

    return portvals


def update_positions(ticker, action, quantity, current_cash, holding_shares, tickers, curr_dt, end_dt, commission,
                     impact):
    if ticker not in tickers:
        df = get_data([ticker], pd.date_range(curr_dt, end_dt), addSPY=True, colname='Adj Close')
        df = df.ffill()
        df = df.bfill()
        tickers[ticker] = df

    action_multipliers = {
        'BUY': (1, 1 + impact),
        'SELL': (-1, 1 - impact)
    }

    if action in action_multipliers:
        multiplier, cash_multiplier = action_multipliers[action]
        share_change = multiplier * quantity
        cash_change = -multiplier * tickers[ticker].loc[curr_dt, ticker] * cash_multiplier * quantity
    else:
        print("Action type is not supported.")

    holding_shares[ticker] = holding_shares.get(ticker, 0) + share_change
    current_cash += (cash_change - commission)

    return current_cash, holding_shares, tickers


def author():
    return "szhou401"


def test_code():
    """
    Helper function to test code
    """
    # # this is a helper function you can use to test your code
    # # note that during autograding his function will not be called.
    # # Define input parameters
    #
    # # of = "./additional_orders/orders.csv"
    # of = "./additional_orders/orders2.csv"
    # # of = "./additional_orders/orders-short.csv"
    # sv = 1000000
    #
    # # Process orders
    # portvals = compute_portvals(orders_file=of, start_val=sv,commission=20,impact=0.01)
    # if isinstance(portvals, pd.DataFrame):
    #     portvals = portvals[
    #         portvals.columns[0]]  # just get the first column
    # else:
    #     "warning, code did not return a DataFrame"
    #
    # print(portvals)
    # # Get portfolio stats
    # # Here we just fake the data. you should use your code from previous assignments.
    # start_date = dt.datetime(2011, 1, 10)
    # end_date = dt.datetime(2011, 12, 20)
    # # cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [
    # #     0.2,
    # #     0.01,
    # #     0.02,
    # #     1.5,
    # # ]
    # cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [
    #     0.2,
    #     0.01,
    #     0.02,
    #     1.5,
    # ]
    # d_returns = portvals.copy()
    # d_returns = (portvals[1:]/portvals.shift(1) - 1)
    # d_returns.iloc[0] = 0
    # d_returns = d_returns[1:]
    # cum_ret = portvals[-1] / portvals[0] - 1
    # avg_daily_ret = d_returns.mean()
    # std_daily_ret = d_returns.std()
    # daily_rfr = (1.0)**(1/252) - 1
    # sr = (d_returns - daily_rfr).mean() / std_daily_ret
    # sharpe_ratio = sr * (252**0.5)
    #
    # # Compare portfolio against $SPX
    # print(f"Date Range: {start_date} to {end_date}")
    # print()
    # print(f"Sharpe Ratio of Fund: {sharpe_ratio}")
    # print(f"Sharpe Ratio of SPY : {sharpe_ratio_SPY}")
    # print()
    # print(f"Cumulative Return of Fund: {cum_ret}")
    # print(f"Cumulative Return of SPY : {cum_ret_SPY}")
    # print()
    # print(f"Standard Deviation of Fund: {std_daily_ret}")
    # print(f"Standard Deviation of SPY : {std_daily_ret_SPY}")
    # print()
    # print(f"Average Daily Return of Fund: {avg_daily_ret}")
    # print(f"Average Daily Return of SPY : {avg_daily_ret_SPY}")
    # print()
    # print(f"Final Portfolio Value: {portvals[-1]}")


if __name__ == "__main__":
    test_code()  		  	   		  		 		  		  		    	 		 		   		 		  
