# Portfolio Rebalance Methods
Portfolio Rebalance Methods: Explore and implement diverse rebalancing strategies, including Static Weights, Risk Parity, and Markowitz, to optimize and fine-tune your investment portfolios.

## Overview

This repository contains Python scripts for portfolio analysis with various rebalancing methods. The primary script, `static_weights.py`, computes portfolio metrics based on synchronized asset time series data, while the secondary script, `main.py`, demonstrates its usage with example data.

## `main.py`

### Usage

The `main.py` script serves as an example of how to use the `static_weights` script with sample data.

### Example

The example provided in `main.py` reads asset time series data, defines allocation weights and rebalance frequency, and calculates portfolio metrics. Results are saved to CSV files and printed to the console.

## `static_weights.py`

### Function: `calculate_portfolio`

The `static_weights` script contains a function to compute portfolio metrics based on provided parameters.

#### Parameters:

- `asset_prices` (pd.DataFrame): DataFrame with synchronized asset prices.
- `rebalance_frequency` (str): Rebalancing frequency as a pandas frequency string.
- `allocation_weights` (Optional[List[float]]): List of initial allocation percentages for each asset.
- `start_deposit` (float): Initial deposit or starting amount for the portfolio.

#### Returns:

- Tuple[pd.DataFrame, pd.DataFrame]: Cumulative equity and daily asset allocations.

### Example Usage:

```python
import pandas as pd
from static_weights import calculate_portfolio

# Input data
asset_prices = pd.DataFrame(...)
allocation_weights = [0.4, 0.3, 0.3]
rebalance_frequency = 'Q'
start_deposit = 100.0

# Calculate portfolio metrics
equity, allocations = calculate_portfolio(asset_prices, rebalance_frequency, allocation_weights, start_deposit)

# Print or use the results
print("Cumulative Equity:")
print(equity)

print("\nAsset Allocations:")
print(allocations)
```

## License
This project is licensed under the [MIT License](LICENSE). See the [LICENSE](https://github.com/py310/portfolio-rebalance-methods/blob/main/LICENSE) file for details.

