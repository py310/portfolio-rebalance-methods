# 📈💼 Portfolio Rebalance Methods
Portfolio Rebalance Methods: Explore and implement diverse rebalancing strategies, including Static Weights, Equal Weights, Risk Parity, and Markowitz, to optimize and fine-tune your investment portfolios.

## 🌐 Overview

This repository contains Python scripts for portfolio analysis with various rebalancing methods. The primary script, `portfolio_rebalancer.py`, computes portfolio metrics based on synchronized asset time series data, while the secondary script, `main.py`, demonstrates its usage with example data.

## 🚀 Usage

### Requirements

- Python 3.10.9
- Pandas library 2.0.1

### Example

The `main.py` script serves as an example of how to use the `portfolio_rebalancer` script with sample data.  

To use the portfolio rebalancer, create an instance of the `PortfolioRebalancer` class and specify the required parameters. The following example demonstrates how to use it:
1. Read asset time series data from a CSV file.
2. Define needed parameters.
3. Specify the weights type (risk parity or static).
4. Create a `PortfolioRebalancer` instance.
5. Calculate portfolio metrics.
6. Save results to CSV files.
7. Print the results.

```python
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
```

## 📚 Documentation

### PortfolioRebalancer Class

#### `__init__(self, asset_prices, weights_type='static', rebalance_frequency='Q', static_weights=None, start_deposit=100.0)`

Initialize PortfolioRebalancer.

- `asset_prices` (pd.DataFrame): A DataFrame with synchronized asset prices over time.
- `weights_type` (Literal['risk_parity', 'static']): The type of weights to use ('risk_parity' or 'static').
- `rebalance_frequency` (str): The rebalancing frequency as a pandas frequency string (e.g., 'Q' for quarterly, 'M' for monthly).
- `static_weights` (Optional[List[float]]): A list of static weights for each asset. If not provided and weights_type is 'static', it defaults to equal weights.
- `start_deposit` (float): The initial deposit or starting amount for the portfolio.

#### Function: `get_allocation_weights(self, timestamp) -> pd.Series`

Calculate allocation weights based on the specified type.

Returns:
- `pd.Series[float]`: A Pandas Series of weights for each asset.

#### Function: `calculate_portfolio(self) -> Tuple[pd.DataFrame, pd.DataFrame]`

Calculate portfolio metrics based on synchronized asset time series data using specified parameters.

Returns:
- `Tuple[pd.DataFrame, pd.DataFrame]`:
  - `equity`: DataFrame with cumulative equity.
  - `asset_allocations`: DataFrame with daily asset allocations.


## 📄 License
This project is licensed under the MIT License. See the [LICENSE](https://github.com/py310/portfolio-rebalance-methods/blob/main/LICENSE) file for details.
