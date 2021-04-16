from typing import *
from math import log10
from .datasource import DataSource
import numpy as np


class ACDataSource(DataSource):
    # A matrix of price relative vectors.
    # Each column is a logarithmic PRV, and the time increases from left to right.
    log_price_relatives: np.array
    last_log_price_relatives: np.array

    def __init__(self, initial_prices: np.array):
        """
        Initialize the data source with the price of all assets at the beginning of strategy execution.
        """
        super().__init__(initial_prices=initial_prices)
        self.log_price_relatives = None
        self.last_log_price_relatives = None

    def add_prices(self, prices: np.array) -> None:
        """
        Update the data source with new prices. This should only be done right before executing the
        strategy's update() method, as this will use the new prices to calculate PRVs. 
        """
        super().add_prices(prices=prices)
        self.last_log_price_relatives = self.log_price_relatives
        if len(self.price_relatives.shape) == 1:
            prv = self.price_relatives
        else:
            prv = self.price_relatives[:, -1]
        self.log_price_relatives = np.array([log10(rel) for rel in prv])
