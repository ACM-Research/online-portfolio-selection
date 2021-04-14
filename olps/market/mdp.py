from typing import *
import pandas as pd
from pandas.core.frame import DataFrame


class MarketDataProvider:
    def __init__(self, merged_csv_path: str) -> None:
        df = pd.read_csv(merged_csv_path)
        df['time'] = pd.to_datetime(df['time'])
        df.set_index('time', inplace=True)
        self.stocks = df['ticker'].unique()
        self.data = df

    def min_time(self) -> int:
        return self.data.index.min().timestamp() * 1e9

    def max_time(self) -> int:
        return self.data.index.max().timestamp() * 1e9

    def get_data(self, ns_timestamp: int, threshold=1e9) -> Tuple[int, DataFrame]:
        view = self.data.loc[
            (self.data.index.astype('int64') >= ns_timestamp) &
            (self.data.index.astype('int64') <= (ns_timestamp + threshold))
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
            max_time = view.index.max().timestamp() * 1e9
        return (max_time, prices)


if __name__ == "__main__":
    dp = MarketDataProvider(
        'data/03-29-2021/merged/AAPL-BBY-DIS-TSLA-TWTR-UBER.csv')
    ts = dp.min_time()
    max_time = dp.max_time()
    STEP = 1e9
    while ts <= max_time:
        returned_max, prices = dp.get_data(ts, STEP)
        if prices is not None and len(prices) > 0:
            print(f'timestamp: {ts:.0f}')
            print(prices.to_numpy())
        if returned_max is None:
            returned_max = 0
        ts = max(ts + STEP, returned_max)
