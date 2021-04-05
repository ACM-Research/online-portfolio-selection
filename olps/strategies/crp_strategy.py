from .strategy import Strategy
from ..datasources.datasource import DataSource

class CRPStrategy(Strategy):
    def update_weights(self, market_data: DataSource) -> None:
        '''
         the weights are held in constant distribution
        '''
        pass
