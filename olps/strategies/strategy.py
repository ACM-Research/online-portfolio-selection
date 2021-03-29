from abc import ABC, abstractmethod
from typing import *

import numpy as np
from olps.datasources.datasource import DataSource


class Strategy(ABC):
    """
    Abstract class allowing for implementation of almost any type of online porfolio selection
    strategy.
    Key method to override in child implementations includes the private update_weights method.
    If the strategy requires specially-computed data for each portfolio computation, perform
    and store this data manipulation in a DataSource subclass.
    """

    # Array of weights for each asset in the portfolio.
    weights: np.array
    # Cumulative wealth at every time step the strategy is run.
    cumulative_wealth: np.array

    def __init__(self, num_assets: int) -> None:
        """
        Initialize the strategy based on the number of assets.
        Note that the weights are set to 1 / num_assets as specified in the paper.
        """
        self.weights = np.ones((num_assets, )) / num_assets
        self.cumulative_wealth = np.ones((1,))

    @abstractmethod
    def update_weights(self, market_data: DataSource) -> None:
        """
        Abstract private method to update weights.
        Should be overridden in client strategy classes.
        """
        pass

    def update_wealth(self, current_return: float) -> float:
        """
        Private method to compute strategy's cumulative return.
        Stores in cumulative wealth and returns the current cumulative return value.
        """
        cumulative_return = self.cumulative_wealth[-1] * current_return
        self.cumulative_wealth = np.append(
            self.cumulative_wealth, cumulative_return
        )
        return cumulative_return

    def get_return(self, price_relatives: np.array) -> float:
        """
        Get the return from the previous trading period based on the price relatives provided.
        """
        ret: np.float64 = np.dot(self.weights, price_relatives)
        if not isinstance(ret, np.float64):
            raise ValueError('Price relative is not of expected shape')
        return float(ret)

    @final
    def update(self, market_data: DataSource) -> float:
        """
        Standard final method to update weights based on a data source and update wealth so far.
        """
        if market_data.price_relatives is None:
            raise ValueError(
                'Data source does not have price relative vector to update on.')
        # Get last price relative
        last_price_relative = None
        if len(market_data.price_relatives.shape) == 1:
            # If the price relative is still a 1D array, we only have 1 price relative
            last_price_relative = market_data.price_relatives
        else:
            # Otherwise, get the last price relative in the PRV history matrix
            last_price_relative = market_data.price_relatives[:, -1]
        # Calculate period return b_t * x_t
        period_return = self.get_return(last_price_relative)
        # Calculate cumulative return: S_{t-1} * (current period return)
        cumulative_return = self.update_wealth(period_return)
        self.update_weights(market_data)
        return cumulative_return
