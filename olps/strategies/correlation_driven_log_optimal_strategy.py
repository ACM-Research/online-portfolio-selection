from .strategy import Strategy
from ..datasources.correlation_driven_datasource import CorrelationDrivenDataSource
import math
import numpy as np

class CorrelationDrivenLogStrategy(Strategy):
     
    def update_weights(self, market_data: CorrelationDrivenDataSource) -> None:
        
        market_data.sample_selection()
        similarity_set = market_data.similarity_set
        similarity_set_size = market_data.similarity_set_size

        # if there are no windows close enough to the final window or the window size was too large, use CRP update
        if similarity_set is None or market_data.window > len(market_data.prices):
            self.weights = self.weights
        elif (similarity_set_size == 1):
            # Compute the weights based off of the single similar PRC
            i = similarity_set[0]
            currPRV = market_data.price_relatives[:, i]
            logBX = self.weights * currPRV
            for k in range(logBX.size):
                logBX[k] = math.log10(logBX[k])
            self.weights = logBX / sum(logBX)
        # Handling more than two windows
        else:
            largestSummation = -100000
            bestPortfolio = None
            winningI = -1
            for j in range(similarity_set_size):
            # getting the prvs which correspond to the set of index from sample selection
                i = similarity_set[j]
                currPRV = market_data.price_relatives[:, i]
                logBX =  self.weights * currPRV
                for k in range(logBX.size):
                    logBX[k] = math.log10(logBX[k])
                if sum(logBX) > largestSummation:
                    largestSummation = sum(logBX)
                    bestPortfolio = logBX
                    winningI = i
            self.weights = bestPortfolio/ sum(bestPortfolio)