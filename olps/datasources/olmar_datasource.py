from typing import *
from math import log10
from .datasource import DataSource
import numpy as np


class OLMARDataSource(DataSource):
    # A matrix of price relative vectors.
    # Each column is a logarithmic PRV, and the time increases from left to right.
    window = 2
    predictedPRV : np.array

    def __init__(self, initial_prices: np.array, window):
        """
        Initialize the data source with the price of all assets at the beginning of strategy execution.
        """
        super().__init__(initial_prices=initial_prices)
        self.log_price_relatives = None
        self.last_log_price_relatives = None
        self.window = window

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
    
    def predict_PRV(self, prices: np.array) -> None:
        """
        Use moving average over a sliding window frame of prices to calculate the the future
        PRV
        """

        for i in range(len(self.prices)):
            #Calculate moving averages for each asset
            movingAvg = 0
            for j in range(i - self.window, i):
                movingAvg += self.prices[i][j]
            movingAvg = movingAvg / self.window
    
            # Predict future PRVs
            future_PRV = movingAvg / self.prices[-1]
            self.predictedPRV[j] = future_PRV
        