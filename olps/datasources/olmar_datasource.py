from typing import *
from math import log10
from .datasource import DataSource
import numpy as np


class OLMARDataSource(DataSource):
    # A matrix of price relative vectors.
    # Each column is a logarithmic PRV, and the time increases from left to right.
    window : int
    predictedPRV : np.array

    def __init__(self, initial_prices: np.array, window = 2):
        """
        Initialize the data source with the price of all assets at the beginning of strategy execution.
        """
        super().__init__(initial_prices=initial_prices)
        self.log_price_relatives = None
        self.last_log_price_relatives = None
        self.window = window
        self.predictedPRV = np.empty(len(self.prices),)
    
    def predict_PRV(self) -> None:
        """
        Use moving average over a sliding window frame of prices to calculate the the future
        PRV
        """

        for i in range(len(self.prices)):
            #Calculate moving averages for each asset
            movingAvg = 0
            for j in range(self.window):
                movingAvg += self.prices[i, j]
            movingAvg = movingAvg / self.window
    
            # Predict future PRVs
            future_PRV = movingAvg / self.prices[i, -1]
            self.predictedPRV[i] = future_PRV
        