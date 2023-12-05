
import pandas as pd
from static_weights import calculate_portfolio

if __name__ == "__main__":

    # Read asset time series data from CSV
    asset_ts = pd.read_csv('data/example-data.csv', index_col=0, parse_dates=['timestamp'])

    # Define initial allocation weights and rebalance frequency
    reb_freq = 'Q'
    allocation = [0.333, 0.333, 0.334]

    # Calculate portfolio metrics
    result_equity, result_allocations = calculate_portfolio(asset_ts, reb_freq, allocation)

    # Save results to CSV files
    result_equity.to_csv('equity_static_weights.csv', sep=';')
    result_allocations.to_csv('allocations_static_weights.csv', sep=';')

    # Print results
    print("Cumulative Equity:")
    print(result_equity)

    print("\nAsset Allocations:")
    print(result_allocations)