from .strategy import Strategy
from ..datasources.datasource import DataSource
import numpy as np

class UPStrategy(Strategy):
    def update_weights(self, market_data: DataSource) -> None:
        if len(market_data.price_relatives.shape) == 1:
            prv = market_data.price_relatives
        else:
            prv = market_data.price_relatives[:, -1]
        w = ?
        y1 = log(x[t-2w+1:t-w])
        y2 = log(x[t-w+1:t])
        Mcov(i, j) = (1.0/(w - 1))(y[1:i] -y1mean)T(y2,j - y2mean)
        # might not be needed
        #self.weights = self.weights / sum(self.weights)
