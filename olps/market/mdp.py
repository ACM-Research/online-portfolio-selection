from typing import Tuple
import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame


class MarketDataProvider:
    assets: np.array
    data: DataFrame
    min_fill_time: int

    def __init__(self, merged_csv_path: str) -> None:
        # Load in CSV and convert time to DatetimeIndex
        expected_dtypes = {
            'time': 'int64',
            'ask': 'float',
            'bid': 'float',
            'ticker': 'category'
        }
        df = pd.read_csv(
            merged_csv_path,
            dtype=expected_dtypes,
            index_col='time'
        )
        # Get a list of assets in this combined portfolio dataframe
        self.assets = df['ticker'].cat.categories.to_numpy()
        self.data = df
        self.min_fill_time = self.__calc_min_fill_time()

    def __calc_min_fill_time(self) -> int:
        max_time = None
        for stock in self.assets:
            index = self.data[self.data['ticker'] == stock].index[0]
            if max_time is None:
                max_time = index
            else:
                max_time = max(max_time, index)
        return max_time

    def min_time(self) -> int:
        return self.data.index.min()

    def max_time(self) -> int:
        return self.data.index.max()

    def get_data(self, timestamp: int, threshold=1e7) -> Tuple[int, DataFrame]:
        view = self.data.loc[
            (self.data.index > timestamp) &
            (self.data.index <= (timestamp + threshold))
        ]
        grouped = view.groupby(['ticker'])
        prices = None
        try:
            prices = pd.concat(map(
                lambda gr: gr[1].loc[gr[1].index ==
                                     gr[1].index.max()], grouped
            ))
        except ValueError:
            pass
        max_time = None
        if len(view) > 0:
            max_time = view.index.max()
        return (max_time, prices)


if __name__ == "__main__":
    dp = MarketDataProvider(
        'data/03-29-2021/merged/AAPL-BBY-DIS-TSLA-TWTR-UBER.csv')
    print(dp.min_fill_time)
    print(dp.assets)
    ts = dp.min_fill_time
    max_time = dp.max_time()
    STEP = 1e7
    while ts <= max_time:
        returned_max, prices = dp.get_data(ts, STEP)
        if prices is not None and len(prices) > 0:
            print(f'timestamp: {ts:.0f}')
            print(prices)
            # input()
        if returned_max is None:
            returned_max = 0
        ts = max(ts + STEP, returned_max)
