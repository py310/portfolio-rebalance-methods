import pandas as pd
from typing import Literal, Optional

class PortfolioRebalancer:
    def __init__(
        self,
        asset_prices: pd.DataFrame,
        weights_type: Literal['risk_parity', 'static'] = 'static',
        rebalance_frequency: str = 'Q',
        static_weights: Optional[list[float]] = None,
        start_deposit: float = 100.0
    ) -> None:
        """
        Initialize PortfolioRebalancer.

        Parameters:
        - asset_prices (pd.DataFrame): A DataFrame with synchronized asset prices over time.
        - weights_type (Literal['risk_parity', 'static']): The type of weights to use ('risk_parity' or 'static').
        - rebalance_frequency (str): The rebalancing frequency as a pandas frequency string
                                    (e.g., 'Q' for quarterly, 'M' for monthly).
        - static_weights (Optional[list[float]]): A list of static weights for each asset. 
                                                   If not provided and weights_type is 'static', it defaults to equal weights.
        - start_deposit (float): The initial deposit or starting amount for the portfolio.
        """
        self.asset_prices = asset_prices
        self.weights_type = weights_type
        self.rebalance_frequency = rebalance_frequency
        self.start_deposit = start_deposit

        if weights_type == 'risk_parity' and static_weights is not None:
            raise ValueError("Static weights should not be provided for risk parity. Use weights_type='static' for static weights.")

        if weights_type == 'static':
            self.allocation_weights = static_weights or [1 / len(asset_prices.columns)] * len(asset_prices.columns)
        else:
            # Initial allocation_weights if weights_type is not 'static' (equal weights for the first rebalance)
            self.allocation_weights = [1 / len(asset_prices.columns)] * len(asset_prices.columns)


    def get_allocation_weights(self, timestamp: pd.Timestamp) -> pd.Series | list[float]:
        """
        Calculate allocation weights based on the specified type.

        Returns:
        - pd.Series[float]: A Pandas Series of weights for each asset.
        """
        if self.weights_type == 'risk_parity':
            volatilities = self.asset_prices.loc[:timestamp].pct_change().fillna(0).std()
            inv_volatilities = 1 / volatilities
            weights = inv_volatilities / inv_volatilities.sum()
        elif self.weights_type == 'static':
            weights = self.allocation_weights
        else:
            raise ValueError("Invalid weights_type. Use 'risk_parity' or 'static'.")

        return weights

    def calculate_portfolio(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Calculate portfolio metrics based on synchronized asset time series data using specified weights.

        Returns:
        - tuple[pd.DataFrame, pd.DataFrame]:
            - equity: DataFrame with cumulative equity.
            - asset_allocations: DataFrame with daily asset allocations.
        """
        if not isinstance(self.asset_prices, pd.DataFrame) or self.asset_prices.empty:
            raise ValueError("Input DataFrame 'asset_prices' is empty or not a valid DataFrame.")

        # Generate rebalancing dates
        rebalance_dates = pd.date_range(start=self.asset_prices.index[0], end=self.asset_prices.index[-1],
                                       freq=self.rebalance_frequency)

        # Initialize DataFrames for net asset values (nav), returns (returns), and allocations (asset_allocations)
        nav = pd.DataFrame(0, index=self.asset_prices.index, columns=self.asset_prices.columns)
        returns = pd.DataFrame(0, index=self.asset_prices.index, columns=self.asset_prices.columns)
        asset_allocations = pd.DataFrame(0, index=self.asset_prices.index, columns=self.asset_prices.columns)

        # Set trading deposit
        deposit = self.start_deposit

        # Set start prices
        rebalance_prices = self.asset_prices.iloc[0]

        # Iterate through each timestamp in the asset time series
        for timestamp, asset_prices_row in self.asset_prices.iterrows():
            # Calculate net asset values (nav) for each asset
            nav.loc[timestamp] = (asset_prices_row - rebalance_prices) / rebalance_prices * self.allocation_weights * deposit

            # Calculate asset allocations (asset_allocations) for each asset
            asset_allocations.loc[timestamp] = self.allocation_weights + \
                                               (asset_prices_row - rebalance_prices) / rebalance_prices * self.allocation_weights
            asset_allocations.loc[timestamp] = asset_allocations.loc[timestamp] / asset_allocations.loc[timestamp].sum()

            # Check if the current timestamp is a rebalancing date
            if timestamp in rebalance_dates:
                # Calculate returns during rebalancing (returns) for each asset
                returns.loc[timestamp] = (asset_prices_row - rebalance_prices) / rebalance_prices * \
                                          self.allocation_weights * deposit

                # Update deposit based on returns for each asset
                deposit = deposit + returns.loc[timestamp].sum()

                # Update open prices
                rebalance_prices = self.asset_prices.loc[timestamp]

                # Update allocation weights based on specified type
                self.allocation_weights = self.get_allocation_weights(timestamp)

        # Calculate total net asset values and returns
        nav['total'] = nav.sum(axis=1)
        returns['total'] = returns.sum(axis=1)

        # Calculate cumulative equity (equity)
        equity = self.start_deposit + returns['total'].cumsum() + nav['total'] - returns['total']
        equity = equity.to_frame()

        return equity, asset_allocations
