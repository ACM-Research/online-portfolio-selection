from typing import *
import numpy as np
from .mdp import MarketDataProvider
from ..strategies.strategy import Strategy
from ..strategies.bah_strategy import BAHStrategy
from ..datasources.datasource import DataSource


class TradingMarketStrategyInfo(TypedDict):
    '''
    An object to configure a TradingMarket.
    '''
    # An array of Strategies to run.
    strategies: List[Strategy]
    # A function to instantiate a list of DataSources.
    datasource_factory: Callable[[np.array], List[DataSource]]
    # An array of strategy frequencies (in nanoseconds).
    frequencies: List[int]


class TradingMarket:
    '''
    Key abstraction that enables backtesting of strategies in an equities market.
    '''

    def __init__(self, strategy_info: TradingMarketStrategyInfo, merged_data_path: str) -> None:
        # Initialize strategies
        self.strategies = strategy_info['strategies']
        # Initialize MarketDataProvider and extract timestamps
        self.data_provider = MarketDataProvider(merged_data_path)
        self.start_timestamp = self.data_provider.min_fill_time
        self.idx = self.data_provider.get_min_fill_idx()
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

    def execute_strategy(self, idx: int) -> None:
        '''
        Executes a strategy by the index of it inside `self.strategies`.
        '''
        ds = self.datasources[idx]
        ds.add_prices(self.current_prices)
        strat = self.strategies[idx]
        strat.update(ds)
        print('prices', self.current_prices)
        print('cumulative wealth', strat.cumulative_wealth[-1])

    def can_advance(self):
        '''
        Returns True if there are ticks left to iterate through.
        '''
        return self.idx < len(self.data_provider.data)

    def advance(self):
        '''
        Run until the next thing in the market.
        Returns `True` if the market could run one step.
        '''
        # If we're past the limit of our data. throw an error
        if not self.can_advance():
            raise ValueError('No data left to advance')
        # Get the next tick
        next_ts = self.data_provider.data.index[self.idx]
        changes = self.data_provider.get_time(next_ts)
        # Check in the interval between the current tick and the next tick
        # Check if we need to run a strategy within that interval & run it
        interval_start = self.offset
        interval_end = changes.index.max() - self.start_timestamp
        for idx, freq in enumerate(self.frequencies):
            a = (interval_start // freq) * freq
            while a < interval_end:
                if interval_start <= a < interval_end:
                    name = type(self.strategies[idx]).__name__
                    print(
                        f'===\nExecuting strategy {name} at {idx}, time {(self.timestamp() + a):.0f}, tick index {self.idx}')
                    self.execute_strategy(idx)
                a += freq
        # Display multi-stock tick alerts
        if len(changes) > (len(self.asset_indices) // 2):
            print(
                f'!! interesting! we have a big n={len(changes)} multi-stock change at idx {self.idx}, time {changes.index[0]} !!')
        # Update the current price with the next tick
        for _, val in changes.iterrows():
            self.__set_current_price(val['ticker'], val['ask'])
        self.offset = interval_end
        self.idx += len(changes)
