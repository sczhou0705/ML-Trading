import math
import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt

from util import get_data, plot_data

#
def author():
	return 'szhou401'
def All_Plots():
    symbols = ['JPM']
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2009,12,31)
    dates = pd.date_range(start_date, end_date)
    lookback = 14

    prices = get_data(symbols, dates).drop(['SPY'], axis=1)

    # sma(prices, lookback, True)
    bbp(prices, True)
    macd(prices, True)
    # # macd(prices,False)
    #return series
    golden_cross(prices,short_window=50, long_window=200, make_plot=True)
    # return series
    rsi(prices,lookback,True)
    #return series
    momentum(prices, lookback, make_plot=True)

# The first indicator is Golden cross function that call sma function
def sma(prices, lookback, make_plot):
    # Calculate the Simple Moving Average (SMA) for the given lookback period
    sma_df = prices.rolling(window=lookback, min_periods=lookback).mean()
    sma_normalized = sma_df.copy()

    # Normalize the SMA values relative to the first price
    sma_normalized.iloc[lookback - 1:] /= prices.iloc[0]
    sma_normalized.rename(columns={'JPM': 'SMA'}, inplace=True)

    # Normalize the prices
    sma_normalized['Prices'] = prices / prices.iloc[0]

    if make_plot:
        fig, ax = plt.subplots(figsize=(12, 6))
        sma_normalized.plot(ax=ax, title='Simple Moving Average Normalized for JPM', fontsize=12, grid=True)
        ax.set_xlabel('Date')
        ax.set_ylabel('Normalized Value')
        ax.fill_between(sma_normalized.index, sma_normalized['Prices'], sma_normalized['SMA'],
                        where=(sma_normalized['Prices'] > sma_normalized['SMA']), color='green', alpha=0.3,
                        interpolate=True)
        ax.fill_between(sma_normalized.index, sma_normalized['Prices'], sma_normalized['SMA'],
                        where=(sma_normalized['Prices'] <= sma_normalized['SMA']), color='red', alpha=0.3,
                        interpolate=True)
        plt.savefig('images/SMA.png')
# will update it if it will be used in p8
    return sma_df, sma_normalized

def golden_cross(prices, short_window=50, long_window=200, make_plot=True):
    # Compute the short 50 and long-term SMAs 200
    #https://www.investopedia.com/terms/g/goldencross.asp
    short_sma, _ = sma(prices, short_window, False)
    long_sma, _ = sma(prices, long_window, False)

    # Initialize a DataFrame to store signals
    signals = pd.DataFrame(index=prices.index)
    signals['Price'] = prices
    signals['Short_SMA'] = short_sma
    signals['Long_SMA'] = long_sma

    # Initialize the signal column with zeros
    signals['Signal'] = 0.0
    signals['Signal'][short_window:] = np.where(
        signals['Short_SMA'][short_window:] > signals['Long_SMA'][short_window:], 1.0, 0.0)
    signals['positions'] = signals['Signal'].diff()
    # print(signals['positions'])
    if make_plot:
        ax = signals[['Price', 'Short_SMA', 'Long_SMA']].plot(title='Golden Cross And Death Cross for JPM', fontsize=12,
                                                              grid=True)
        ax.plot(signals[signals['positions'] == 1.0].index, signals['Long_SMA'][signals['positions'] == 1.0], '^',
                markersize=10, color='b', label='Golden Cross')
        ax.plot(signals[signals['positions'] == -1.0].index, signals['Long_SMA'][signals['positions'] == -1.0], 'v',
                markersize=10, color='r', label='Death Cross')
        plt.legend()
        plt.savefig('images/Golden Cross.png')
    return signals['positions']


#
#https://www.investopedia.com/terms/b/bollingerbands.asp
def bbp(prices, make_plot=True):
    lookback = 20

    # Ensure 'prices' is a Series
    if isinstance(prices, pd.DataFrame):
        prices = prices.squeeze()

    sma_df, _ = sma(prices, lookback, False)
    rolling_std = prices.rolling(window=lookback).std()
    top_band = sma_df + (2 * rolling_std)
    bottom_band = sma_df - (2 * rolling_std)

    bbp_series = (prices - bottom_band) / (top_band - bottom_band)

    if make_plot:
        figure, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=(10, 8))
        prices.plot(ax=ax1, label="Price", fontsize=12, grid=True)
        top_band.plot(ax=ax1, label="Upper Band", color='green')
        bottom_band.plot(ax=ax1, label="Lower Band", color='red')
        sma_df.plot(ax=ax1, label="SMA", color='blue')

        ax1.fill_between(prices.index, bottom_band, top_band, color='grey', alpha=0.2)

        bbp_series.plot(ax=ax2, fontsize=12, grid=True, color='purple', label='Bollinger Band %')
        ax2.fill_between(bbp_series.index, 0, 1, where=(bbp_series > 1), color='green', alpha=0.3)
        ax2.fill_between(bbp_series.index, 0, 1, where=(bbp_series < 0), color='red', alpha=0.3)

        ax1.set_title('Bollinger Bands for JPM Price Data')
        ax1.legend(prop={'size':'10'}, loc=4)
        ax1.set(ylabel='Value')

        ax2.set_title('B %')
        ax2.legend(prop={'size':'10'}, loc=4)
        ax2.set(ylabel='% Value')

        plt.xlabel('Date')
        plt.tight_layout()
        plt.savefig('images/BBP.png')

    return bbp_series


#
#https://www.investopedia.com/terms/m/macd.asp
#https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html
def macd(prices, make_plot):
    ema_26 = prices.ewm(span=26, min_periods=26, adjust=False).mean()
    ema_12 = prices.ewm(span=12, min_periods=12, adjust=False).mean()

    macd_df = ema_12 - ema_26
    macd_df.rename(columns={'JPM':'MACD'}, inplace=True)
    ema_9 = macd_df.ewm(span=9, min_periods=1, adjust=False).mean() # ema of macd graph (signal line)
    macd_df['Signal Line'] = ema_9
    # print(macd_df)
    if make_plot:
        ax = macd_df.plot(title='Moving Average Convergence Divergence for JPM', fontsize=12, grid=True)
        ax.fill_between(macd_df.index, macd_df['MACD'] - macd_df['Signal Line'],
                        where=(macd_df['MACD'] >= macd_df['Signal Line']), color='g', alpha=0.3)
        ax.fill_between(macd_df.index, macd_df['MACD'] - macd_df['Signal Line'],
                        where=(macd_df['MACD'] < macd_df['Signal Line']), color='r', alpha=0.3)
        ax.set_xlabel('Date')
        ax.set_ylabel('Normalized $ Value')

    plt.savefig('images/MACD.png')
# Return a dataframe , will update if it will be used in P8
    return macd_df
#     return macd_df['MACD'].values
#
#https://www.investopedia.com/terms/r/rsi.asp
def rsi(prices, lookback, make_plot=True):
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)
    avg_gain = gain.rolling(window=lookback).mean()
    avg_loss = loss.rolling(window=lookback).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    if isinstance(rsi, pd.DataFrame):
        rsi = rsi.squeeze()
    # print(type(rsi))
    # return series
    if make_plot:
        fig, ax = plt.subplots(figsize=(12, 6))  # Create a new figure and axis
        rsi.plot(ax=ax, title='RSI for JPM', fontsize=12, grid=True)

        ax.axhline(y=70, color='r', label="Overbought (70)")
        ax.axhline(y=30, color='g', label="Oversold (30)")
        ax.fill_between(rsi.index, 70, rsi.values, where=(rsi > 70), color='red', alpha=0.3, interpolate=True)
        ax.fill_between(rsi.index, 30, rsi.values, where=(rsi < 30), color='green', alpha=0.3, interpolate=True)

        ax.set_xlabel('Date')
        ax.set_ylabel('RSI Value')
        ax.legend()

        plt.savefig('images/RSI.png')

    return rsi

#https://www.investopedia.com/articles/technical/081501.asp
def momentum(prices, lookback, make_plot=True):
    # Ensure that prices is a Series
    if isinstance(prices, pd.DataFrame):
        prices = prices.iloc[:, 0]

    # Normalize the prices
    normalized_prices = prices / prices.iloc[0]
    momentum = normalized_prices - normalized_prices.shift(lookback)
    if make_plot:
        plt.figure(figsize=(12, 6))
        momentum.plot(title=f'Momentum Indicator (lookback={lookback}) using Normalized Prices', fontsize=12,
                             grid=True)

        # Fill areas above and below the zero line
        plt.fill_between(momentum.index, momentum, where=(momentum > 0), color='g', alpha=0.4,
                         label='Positive Momentum')
        plt.fill_between(momentum.index, momentum, where=(momentum < 0), color='r', alpha=0.4,
                         label='Negative Momentum')
        plt.axhline(0, color='black', linestyle='--', linewidth=1)
        plt.xlabel('Date')
        plt.ylabel('Momentum')
        plt.legend()
        plt.savefig('images/Momentum.png')
    return momentum

#
# #
if __name__ == '__main__':
    All_Plots()
