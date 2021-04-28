from .strategy import Strategy
from ..datasources.olmar_datasource import OLMARDataSource
import numpy as np

class OLMARStrategy(Strategy):

    epsilon : float
    
    def __init__(self, num_assets: int, epsilon = 0.999999999999999999999):
        """
        Add initialization of senstivity parameter to constructor
        """
        super().__init__(num_assets=num_assets)
        self.epsilon = epsilon

    def update_weights(self, market_data: OLMARDataSource) -> None:
        
        if(len(self.cumulative_wealth) < market_data.window):
            self.weights = self.weights
        else:
            market_data.predict_PRV()
            futurePRVArr = market_data.predictedPRV

            identity = np.identity(len(futurePRVArr)).T

            numeratorF = identity @ futurePRVArr
            f = numeratorF / 2

            innerLambda = ((self.epsilon - np.dot(self.weights, futurePRVArr)) / np.linalg.norm(futurePRVArr - f))

            lg = 0

            if (innerLambda > 0):
                lg = innerLambda

            if (market_data.price_relatives.ndim == 1):
                weights = self.weights + lg * (market_data.price_relatives[-1] - f)
            else:
                weights = self.weights + lg * (market_data.price_relatives[:, -1] - f)
            weights = weights / sum(weights)
            self.weights = weights
