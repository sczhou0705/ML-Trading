from util import get_data, plot_data
import datetime as dt
import pandas as pd
from marketsimcode import compute_portvals
import matplotlib.pyplot as plt


def author():
	return 'szhou401'
class TheoreticallyOptimalStrategy:
	def testPolicy(self, symbol='AAPL', sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000):
		symbol = symbol[0]
		df = get_data([symbol], pd.date_range(sd, ed))
		px_df = df[[symbol]]
		px_df = px_df.ffill()
		px_df = px_df.bfill()
		dates = px_df.index

		df_trades = pd.DataFrame(0, index=dates, columns=[symbol])
		current_position = 0
		for today, next_day in zip(dates, dates[1:]):
			today_px = px_df.loc[today, symbol]
			next_day_px = px_df.loc[next_day, symbol]

			trade_qty = (1000 if next_day_px > today_px else -1000) - current_position
			df_trades.loc[today, symbol] = trade_qty
			current_position += trade_qty

		# print(df_trades)
		return df_trades


# takes in pd.df and prints stats
def print_stats(benchmark_portvals, strategy_portvals):
	benchmark_portvals, strategy_portvals = benchmark_portvals['value'], strategy_portvals['value']

	# Cumulative return of the benchmark and portfolio
	cr_ben = benchmark_portvals[-1] / benchmark_portvals[0] - 1
	cr_stg = strategy_portvals[-1] / strategy_portvals[0] - 1

	# Daily return in percentage
	dr_ben = (benchmark_portvals / benchmark_portvals.shift(1) - 1).iloc[1:]
	dr_stg = (strategy_portvals / strategy_portvals.shift(1) - 1).iloc[1:]

	# Stdev of daily returns of benchmark and portfolio
	sddr_ben = dr_ben.std()
	sddr_stg = dr_stg.std()

	# Mean of daily returns of benchmark and portfolio
	adr_ben = dr_ben.mean()
	adr_stg = dr_stg.mean()
	# Sharpe Ratio (assuming daily risk free rate = 0, and yearly sampling rate = 252)
	sr_ben = (adr_ben - 0) / sddr_ben * (252 ** 0.5)
	sr_stg = (adr_stg - 0) / sddr_stg * (252 ** 0.5)
	# Create DataFrame for statistics and save to txt
	stats_df = pd.DataFrame({
		'Benchmark': [cr_ben, adr_ben, sddr_ben, sr_ben],
		'Portfolio': [cr_stg, adr_stg, sddr_stg, sr_stg]
	}, index=['Cumulative Return', 'Mean Daily Return', 'Std Daily Return', 'Sharpe Ratio'])
	#Plot a table
	stats_data = {
		'Benchmark': [f'{cr_ben:.6f}', f'{sddr_ben:.6f}', f'{adr_ben:.6f}',f'{sr_ben:.6f}'],
		'Portfolio': [f'{cr_stg:.6f}', f'{sddr_stg:.6f}', f'{adr_stg:.6f}',f'{sr_stg:.6f}']
	}
	stats_df = pd.DataFrame(stats_data)
	stats_df['Stats'] = ['Cumulative Return', 'Stdev of Daily Returns', 'Mean of Daily Returns','Sharpe Ratio']
	cols = list(stats_df.columns)
	cols = [cols[-1]] + cols[:-1]
	stats_df = stats_df[cols]

	header = "+" + "-" * 26 + "+" + "-" * 11 + "+" + "-" * 11 + "+\n"
	row_format = "| {0: <24} | {1: <9} | {2: <9} |\n"
	txt_table = header
	txt_table += row_format.format("Stats", "Benchmark", "Portfolio")
	txt_table += header
	for index, row in stats_df.iterrows():
		txt_table += row_format.format(row[0], row[1], row[2])
		txt_table += header
	with open("p6_results.txt", "w") as f:
		f.write(txt_table)

	print("Portfolio")
	print("Theoretically Optimal Strategy Statistic")
	print(f"Cumulative return: {cr_stg:.6f}")
	print(f"Mean of daily returns: {adr_stg:.6f}")
	print(f"Stdev of daily returns: {sddr_stg:.6f}")
	print(f"Sharpe Ratio: {sr_stg:.6f}")
	print("Benchmark")
	print(f"Cumulative return: {cr_ben:.6f}")
	print(f"Mean of daily returns: {adr_ben:.6f}")
	print(f"Stdev of daily returns: {sddr_ben:.6f}")
	print(f"Sharpe Ratio: {sr_ben:.6f}")
	print("___")


# takes in pd.df and plots graphs
def draw_chart(benchmark_portvals, strategy_portvals):
	benchmark_portvals['value'] = benchmark_portvals['value'] / benchmark_portvals['value'][0]
	strategy_portvals['value'] = strategy_portvals['value'] / strategy_portvals['value'][0]

	plt.figure(figsize=(14, 8))
	plt.title("Theoretically Optimal Strategy")
	plt.xlabel("Date")
	plt.ylabel("Normalized Portfolio Return")
	plt.xticks(rotation=30)
	plt.grid()
	# Set x-axis limit to start at the beginning date
	start_date = benchmark_portvals.index[0]
	plt.xlim(left=start_date)
	plt.plot(benchmark_portvals, label="benchmark", color="purple")
	plt.plot(strategy_portvals, label="tos", color="red")
	plt.legend()
	plt.savefig("images/Benchmark vs TOS.png")
	plt.clf()


def generate_chart_stats():
	# testing conditions
	start_values = 100000
	start_dt = dt.datetime(2008, 1, 1)
	end_dt = dt.datetime(2009, 12, 31)

	# get theoretical performance
	tos = TheoreticallyOptimalStrategy()
	df_trades = tos.testPolicy(['JPM'], start_dt, end_dt, start_values)
	strategy_portvals = compute_portvals(df_trades, start_values, 0.00, 0.00)
	# get benchmark performance
	df_benchmark = get_data(['JPM'], pd.date_range(start_dt, end_dt))
	df_trades_benchmark = pd.DataFrame(0, index=df_benchmark.index, columns=['JPM'])
	df_trades_benchmark.loc[df_trades_benchmark.index[0]] = 1000
	benchmark_portvals = compute_portvals(df_trades_benchmark, start_values, commission=0.00, impact=0.00)

	# get stats
	print_stats(benchmark_portvals, strategy_portvals)

	# plot graph
	draw_chart(benchmark_portvals, strategy_portvals)


if __name__ == "__main__":
	generate_chart_stats()
