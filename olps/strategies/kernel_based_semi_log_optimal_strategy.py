from .strategy import Strategy
from ..datasources.kernel_based_datasource import KernelBasedDataSource
import math
import numpy as np
class KernelBasedSemiLogStrategy(Strategy):
     
    def update_weights(self, market_data: KernelBasedDataSource) -> None:
        market_data.sample_selection()
        similarity_set = market_data.similarity_set
        # if there are no windows close enough to the final window or the window size was too large, use CRP update
        if similarity_set is None:
            pass
        else:
            largestSummation = None
            bestPortfolio : np.array
            # utility log function
            for j in range(similarity_set.size):
            #getting the prvs which correspond to the set of index from sample selection
                i = similarity_set[0,j]
                currPRV = market_data.price_relatives[:,i]
                logBX = self.weights * currPRV
                # doing second order Taylor expansion of log(BX) on every element in the current vector
                for k in range(logBX.size):
                    logBX[k] =logBX[k] - 1 - (.5 * ((logBX[k] - 1) ** 2))
                if largestSummation is None:
                    largestSummation = sum(logBX)
                    bestPortfolio = logBX
                elif sum(logBX) > largestSummation:
                    largestSummation = sum(logBX)
                    bestPortfolio = logBX
            self.weights = bestPortfolio / sum(bestPortfolio)
        
