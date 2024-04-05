import pandas as pd
from util import get_data


def compute_portvals(
        df,
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
    start_dt = df.index[0]
    end_dt = df.index[-1]
    portvals = get_data(['SPY'], pd.date_range(start_dt, end_dt), addSPY=True, colname = 'Adj Close')
    portvals = portvals.rename(columns={'SPY': 'value'})
    dates = portvals.index

    curr_cash = start_val
    positions = {}
    tickers = {}

    ticker = df.columns[0]

    for dt in dates:
        trade_qty = df.loc[dt].Shares
        if trade_qty != 0:
            if trade_qty < 0:
                action = 'SELL'
                qty = abs(trade_qty)
            else:
                action = 'BUY'
                qty = trade_qty
            curr_cash, positions, tickers = update_positions(ticker, action, qty, curr_cash, positions, tickers, dt, end_dt, commission, impact)

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