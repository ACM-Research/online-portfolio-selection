from typing import List
import pandas as pd


class PortfolioDataMerger:
    DATE_FORMAT = '%d.%m.%Y %H:%M:%S.%f GMT%z'

    def merge_portfolio(csv_paths: List[str], stock_names: List[str]) -> None:
        '''
        Merges stock data CSVs with the given paths and stock names.
        '''
        csvs = [PortfolioDataMerger.load_csv(path, ticker)
                for path, ticker in zip(csv_paths, stock_names)]
        df = pd.DataFrame().append(csvs)
        print('Sorting by datetime...')
        df.sort_index('index', inplace=True)
        return df

    def load_csv(path, ticker):
        '''
        Preprocesses and loads a raw stock data CSV.
        '''
        print(f'Loading {ticker} at {path}...')
        df = pd.read_csv(
            path,
            # replace column names with our own
            header=0,
            names=['time', 'ask', 'bid'],
            # use a subset of the columns [timestamp, ask, and bid]
            usecols=[0, 1, 2]
        )
        # Convert time column to datetime, then back into nanoseconds
        df['time'] = pd.to_datetime(
            df['time'], format=PortfolioDataMerger.DATE_FORMAT
        )
        df['time'] = df['time'].astype('int64')
        df['ticker'] = ticker
        df.set_index('time', inplace=True)
        return df
