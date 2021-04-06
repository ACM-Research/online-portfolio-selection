from .strategy import Strategy
from ..datasources.datasource import DataSource
import numpy as np

class ExpGradStrategy(Strategy):

    learning_rate = 0.1
    def update_weights(self, market_data: DataSource) -> None:
        if len(market_data.price_relatives.shape) == 1:
            prv = market_data.price_relatives
        else:
            prv = market_data.price_relatives[:, -1]
        wealth = np.dot(prv, self.weights)
        self.weights = self.weights * np.exp((self.learning_rate / wealth) * prv)
        weight_sum = sum(self.weights)
        self.weights = self.weights / weight_sum