from .strategy import Strategy
from ..datasources.datasource import DataSource
import numpy as np

class BAHStrategy(Strategy):
    def update_weights(self, market_data: DataSource) -> None:
        if len(market_data.price_relatives.shape) == 1:
            prv = market_data.price_relatives
        else:
            prv = market_data.price_relatives[:, -1]
        wealth = np.dot(prv, self.weights)
        self.weights = self.weights * prv
        self.weights = self.weights / sum(self.weights)
