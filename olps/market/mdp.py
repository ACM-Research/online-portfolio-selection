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
