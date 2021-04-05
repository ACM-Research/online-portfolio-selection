from .strategy import Strategy
from ..datasources.datasource import DataSource
import numpy as np
from scipy import integrate

class UPStrategy(Strategy):
    def update_weights(self, market_data: DataSource) -> None:
        if len(market_data.price_relatives.shape) == 1:
            prv = market_data.price_relatives
        else:
            prv = market_data.price_relatives[:, -1]
        b = prv
        # wealth for b
        """
        0417.pdf has the formula
        """
        # pt = fractional change in stock price
        # wit = wealth in ith stock day t
        # b distribution
        # assujme dub to be one
        # p is prv
        def generate_prvs():
            if len(market_data.price_relatives.shape) == 1:
                yield market_data.price_relatives
            else:
                for row in market_data.price_relatives:
                    yield row

        wb = lambda b: np.prod([b * np.array(prv) for prv in generate_prvs()])
        # only for stock i
        twi = lambda b, i: integrate.quad(b[i]*wb(b), 0, np.inf)
        """
        so this doesn't work in any way yet
        0417.pdf has the formula
        """

        self.weights = np.array([
            twi(b,i)/wb(b)
            for i in range(len(b))
            ])
        # might not be needed
        #self.weights = self.weights / sum(self.weights)
