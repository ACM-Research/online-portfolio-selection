from typing import *
import numpy as np
from .mdp import MarketDataProvider
from ..strategies.strategy import Strategy
from ..strategies.bah_strategy import BAHStrategy
from ..datasources.datasource import DataSource


class TradingMarketStrategyInfo(TypedDict):
    strategies: List[Strategy]
    datasource_factory: Callable[[np.array], List[DataSource]]
    frequencies: List[int]
    market_step_size: int


class TradingMarket:
    def __init__(self, strategy_info: TradingMarketStrategyInfo, merged_data_path: str) -> None:
        # Initialize strategies
        self.strategies = strategy_info['strategies']
        # Initialize MarketDataProvider and extract timestamps
        self.data_provider = MarketDataProvider(merged_data_path)
        self.start_timestamp = self.data_provider.min_fill_time
        self.idx = self.data_provider.data.index.get_loc(self.start_timestamp)
        # Assign indices to assets in price vectors that are passed downstream to DataSources
        self.asset_indices = {}
        i = 0
        for asset in sorted(self.data_provider.assets):
            self.asset_indices[asset] = i
            i += 1
        self.current_prices = np.zeros((len(self.data_provider.assets),))
        # Backfill prices
        self.__backfill_prices()
        # Pass in the backfilled prices as initial prices to all datasources
        self.datasources = strategy_info['datasource_factory'](
            self.current_prices
        )
        # Store strategy frequencies
        self.frequencies = strategy_info['frequencies']
        # Store start offset (which will be used to determine exact timestamp)
        self.offset = 0
        # Store step size (the max amount to incremement the offset in any one call to `advance()`.)
        self.step = strategy_info['market_step_size']

    def timestamp(self) -> int:
        '''
        Return the current timestamp the TradingMarket is at.
        '''
        return self.start_timestamp + self.offset

    def __set_current_price(self, asset_name: str, price: float) -> None:
        '''
        Set the current price of an asset by name.
        Note that this does NOT run any strategies.
        '''
        if asset_name not in self.asset_indices:
            raise ValueError('Unknown asset name')
        idx = self.asset_indices[asset_name]
        self.current_prices[idx] = price

    def __backfill_prices(self):
        '''
        Backfills prices from the start timestamp to get the starting prices of assets.
        '''
        idx: int = self.idx
        seen_assets = set()
        # Iterate backwards until all assets are seen or we reach the beginning of the data
        while idx > 0 and len(seen_assets) < len(self.data_provider.assets):
            row = self.data_provider.data.iloc[idx]
            if row['ticker'] not in seen_assets:
                self.__set_current_price(row['ticker'], row['ask'])
            seen_assets.add(row['ticker'])
            idx -= 1

    def advance(self):
        '''
        Run one step in the market.
        Returns `True` if the market could run one step.
        '''
        # If we're past the limit of our data, return
        if self.idx > len(self.data_provider.data):
            return ValueError('No data left to advance')
        # Get price data
        returned_max, prices = self.data_provider.get_data(
            self.timestamp(), threshold=self.step
        )
        # Update prices if needed
        updated = False
        if prices is not None and len(prices) > 0:
            updated = True
            prices.apply(lambda row: self.__set_current_price(
                row['ticker'], row['ask']
            ), axis=1)
        # Check if strategies need to be executed
        for idx, freq in enumerate(self.frequencies):
            if self.offset % freq == 0:
                ds = self.datasources[idx]
                ds.add_prices(self.current_prices)
                strat = self.strategies[idx]
                strat.update(ds)
                print('===\nprices', self.current_prices)
                print('cumulative wealth', strat.cumulative_wealth[-1])
                # input()
        # Update offset
        self.offset += self.step
        # if returned_max is None:
        #     self.offset += self.step
        # else:
        #     self.offset = max(
        #         self.timestamp() + self.offset,
        #         returned_max
        #     ) - self.timestamp()
        return updated


if __name__ == "__main__":
    info: TradingMarketStrategyInfo = {
        'strategies': [BAHStrategy(6)],
        'datasource_factory': lambda initial_prices: [DataSource(initial_prices)],
        'frequencies': [1e9],
        'market_step_size': 1e7
    }
    tm = TradingMarket(
        info, 'data/03-29-2021/merged/AAPL-BBY-DIS-TSLA-TWTR-UBER.csv'
    )
    advanced = True
    while advanced:
        updated = tm.advance()
        # if updated:
        # print(tm.asset_indices)
        # print(tm.current_prices)
