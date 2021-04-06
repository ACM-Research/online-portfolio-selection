from .strategy import Strategy
from ..datasources.datasource import DataSource
import numpy as np

class BestStockStrategy(Strategy):
    def update_weights(self, market_data: DataSource) -> None:
        if len(market_data.price_relatives.shape) == 1:
            prv = market_data.price_relatives
        else:
            prv = market_data.price_relatives[:, -1]
        wealth = np.dot(prv, self.weights)
        best_stock_prv = 0
        best_stock_index = 0
        for i in range(len(prv)):
          if prv[i] <= best_stock_prv:
            self.weights[i] = 0
          else:
            best_stock_prv = prv[i]
            self.weights[best_stock_index] = 0 
            best_stock_index = i
            self.weights[i] = 1