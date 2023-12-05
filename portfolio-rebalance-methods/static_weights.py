import pandas as pd
from typing import List, Optional, Tuple

def calculate_portfolio(
    asset_prices: pd.DataFrame,
    rebalance_frequency: str = 'Q',    
    allocation_weights: Optional[List[float]] = None,
    start_deposit: float = 100.0
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Calculate portfolio metrics based on synchronized asset time series data.

    Parameters:
    - asset_prices (pd.DataFrame): A DataFrame with synchronized asset prices over time.
    - rebalance_frequency (str): The rebalancing frequency as a pandas frequency string (e.g., 'Q' for quarterly, 'M' for monthly).
    - allocation_weights (Optional[List[float]]): A list of initial allocation percentages for each asset.
      If not provided, equal weights will be assigned to every instrument in the asset_prices DataFrame.
    - start_deposit (float): The initial deposit or starting amount for the portfolio.

    Returns:
    - Tuple[pd.DataFrame, pd.DataFrame]:
        - equity: DataFrame with cumulative equity.
        - asset_allocations: DataFrame with daily asset allocations.
    """
    if not isinstance(asset_prices, pd.DataFrame) or asset_prices.empty:
        raise ValueError("Input DataFrame 'asset_prices' is empty or not a valid DataFrame.")

    # Generate rebalancing dates
    rebalance_dates = pd.date_range(start=asset_prices.index[0], end=asset_prices.index[-1], freq=rebalance_frequency)

    # Initialize DataFrames for net asset values (nav), returns (returns), and allocations (asset_allocations)
    nav = pd.DataFrame(0, index=asset_prices.index, columns=asset_prices.columns)
    returns = pd.DataFrame(0, index=asset_prices.index, columns=asset_prices.columns)
    asset_allocations = pd.DataFrame(0, index=asset_prices.index, columns=asset_prices.columns)

    # If allocation_weights are not provided, assign equal weights
    if allocation_weights is None:
        allocation_weights = [1 / len(asset_prices.columns)] * len(asset_prices.columns)

    # Set trading deposit
    deposit = start_deposit

    # Set start prices
    rebalance_prices = asset_prices.iloc[0]
    
    # Iterate through each timestamp in the asset time series
    for timestamp, asset_prices_row in asset_prices.iterrows():
        # Calculate net asset values (nav) for each asset
        nav.loc[timestamp] = (asset_prices_row - rebalance_prices) / rebalance_prices * allocation_weights * deposit

        # Calculate asset allocations (asset_allocations) for each asset
        asset_allocations.loc[timestamp] = allocation_weights + (asset_prices_row - rebalance_prices) / rebalance_prices * allocation_weights
        asset_allocations.loc[timestamp] = asset_allocations.loc[timestamp] / asset_allocations.loc[timestamp].sum()

        # Check if the current timestamp is a rebalancing date
        if timestamp in rebalance_dates:
            # Calculate returns during rebalancing (returns) for each asset
            returns.loc[timestamp] = (asset_prices_row - rebalance_prices) / rebalance_prices * allocation_weights * deposit

            # Update deposit based on returns for each asset
            deposit = deposit + returns.loc[timestamp].sum()

            # Update open prices
            rebalance_prices = asset_prices.loc[timestamp]

    # Calculate total net asset values and returns
    nav['total'] = nav.sum(axis=1)
    returns['total'] = returns.sum(axis=1)

    # Calculate cumulative equity (equity)
    equity = start_deposit + returns['total'].cumsum() + nav['total'] - returns['total']
    equity = equity.to_frame()

    return equity, asset_allocations
