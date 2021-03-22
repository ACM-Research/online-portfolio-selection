from .strategy import Strategy
from ..datasources.datasource import DataSource
import numpy as np

class BAHStrategy(Strategy):
    # TODO implement
    def update_weights(self, market_data: DataSource) -> None:
        if len(market_data.price_relatives.shape) == 1:
            prv = market_data.price_relatives
        else:
            prv = market_data.price_relatives[:, -1]
        wealth = np.dot(prv, self.weights)
        print('wealth', wealth)
        self.weights = self.weights * prv
        self.weights = self.weights / sum(self.weights)
        y = self.update_wealth(wealth)
        print('y', y)
        print('cumu', self.cumulative_wealth)

def main():
    data = DataSource(np.array([
        [1],
        [3],
        [9],
        [2]
        ]))
    changes = np.array([
        [1.1, 3, 10, 3],
        [1.4, 3, 12, 5],
        [1.2, 3.1, 20, 8],
        ])
    bahtest = BAHStrategy(4)
    for change in changes:
        data.add_prices(change)
        bahtest.update_weights(data)
        #bahtest.update_wealth(1.0)#TODO what is my return
    print("weights", bahtest.weights)
    print('sum', sum(bahtest.weights))

if __name__ == '__main__':
    main()
