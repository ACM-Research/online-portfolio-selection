from typing import *

import numpy as np


class DataSource:
    # A matrix of price relative vectors.
    # Each column is a PRV, and the time increases from left to right.
    price_relatives: np.array

    # A matrix of prices.
    # Each column is a price, and the time increases from left to right.
    # Note that this matrix will have one extra column.
    prices: np.array

    def __init__(self, initial_prices: np.array):
        """
        Initialize the data source with the price of all assets at the beginning of strategy execution.
        """
        self.prices = initial_prices
        self.price_relatives = None

    def add_prices(self, prices: np.array) -> None:
        """
        Update the data source with new prices. This should only be done right before executing the
        strategy's update() method, as this will use the new prices to calculate PRVs. 
        """
        self.prices = np.column_stack((self.prices, prices))
        prv = self.prices[:, -1] / self.prices[:, -2]
        if self.price_relatives is not None:
            self.price_relatives = np.column_stack((self.price_relatives, prv))
        else:
            self.price_relatives = prv
