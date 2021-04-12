from .strategy import Strategy
from ..datasources.kernel_based_datasource import KernelBasedDataSource
import math
import numpy as np
class KernelBasedLogStrategy(Strategy):
     
    def update_weights(self, market_data: KernelBasedDataSource) -> None:
        similarity_set = market_data.sample_selection
        largestSummation = -100000
        bestPortfolio = None
        # if there are no windows close enough to the final window or the window size was too large, use CRP update
        if similarity_set is None:
            pass
        # utility log function
        for j in range(similarity_set.size):
            #getting the prvs which correspond to the set of index from sample selection
            i = similarity_set[j]
            currPRV = market_data.price_relatives[:,i]
            logBX = self.weights * currPRV
            # doing log() on every element in the current vector
            for k in range(logB.size)):
                logBX[k] = math.log10(logBX[k])
            if sum(logBX) > largestSummation:
                largestSummation = sum(logBX)
                bestPortfilio = logBX
        self.weights = bestPortfolio
            
          

         

        
