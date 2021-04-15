from .strategy import Strategy
from ..datasources.ac_datasource import ACDataSource
import numpy as np

class ACStrategy(Strategy):
    def update_weights(self, market_data: ACDataSource) -> None:
        log_prv = market_data.log_price_relatives
        last_log_prv = market_data.last_log_price_relatives
        # possibly change later
        if log_prv is not None and last_log_prv is not None:
            cc = np.correlate(last_log_prv, log_prv, 'same')
            self.weights = self.weights + cc
        self.weights = self.weights / sum(self.weights)
