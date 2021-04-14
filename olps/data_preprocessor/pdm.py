from typing import *
import pandas as pd
import os
import sys
from pathlib import Path


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
        df['time'] = pd.to_datetime(
            df['time'], format=PortfolioDataMerger.DATE_FORMAT
        )
        df['ticker'] = ticker
        df.set_index('time', inplace=True)
        return df


if __name__ == "__main__":
    # Runs the CLI version to generate merged CSVs
    print('Portfolio Data Merging Utility')
    if len(sys.argv) <= 1:
        print('You must pass in a folder name of stock CSVs.', file=sys.stderr)
        sys.exit(1)
    folder = Path(sys.argv[1])
    if not folder.is_dir():
        print('You must pass in a folder, not a file.', file=sys.stderr)
        sys.exit(1)
    # Get all files and stock names
    files = [x for x in folder.iterdir() if not x.is_dir()]
    names = [str(x).replace('data/03-29-2021/', '').split('.')[0]
             for x in files]
    # Merge portfolios
    merged = PortfolioDataMerger.merge_portfolio(files, names)
    # Find the merged folder and create it if it doesn't exist
    merged_folder = folder.joinpath('merged')
    if merged_folder.exists() and not merged_folder.is_dir():
        print(
            f'The merged folder path {merged_folder} already exists and is a file?')
    elif not merged_folder.exists():
        print('Creating folder to store merged CSV...')
        merged_folder.mkdir()
    # Save the CSV in the merged folder
    merged_filename = merged_folder.joinpath(f'{"-".join(sorted(names))}.csv')
    print(f'Saving merged CSV at {merged_filename}...')
    merged.to_csv(merged_filename)
    # Print out stats on memory usage and data points
    print(merged.info())
