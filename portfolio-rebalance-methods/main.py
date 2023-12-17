
import pandas as pd
from portfolio_rebalancer import PortfolioRebalancer

if __name__ == "__main__":

    # Read asset time series data from CSV
    asset_ts = pd.read_csv('data/example-data.csv', index_col=0, parse_dates=['timestamp'])

    # Define initial allocation weights and rebalance frequency
    allocation = [0.333, 0.333, 0.334]
    reb_freq = 'Q'
    
    # Specify weights type
    weights_type = 'static'  # Change this to 'risk_parity' if needed

    # Create PortfolioRebalancer instance
    rebalancer = PortfolioRebalancer(asset_prices=asset_ts, weights_type=weights_type, rebalance_frequency=reb_freq, static_weights=allocation)

    # Calculate portfolio metrics
    result_equity, result_allocations = rebalancer.calculate_portfolio()

    # Save results to CSV files with weights type in filenames
    equity_filename = f'equity_{weights_type}.csv'
    allocations_filename = f'allocations_{weights_type}.csv'
    
    result_equity.to_csv(equity_filename, sep=';')
    result_allocations.to_csv(allocations_filename, sep=';')

    # Print results
    print("Cumulative Equity:")
    print(result_equity)

    print("\nAsset Allocations:")
    print(result_allocations)
