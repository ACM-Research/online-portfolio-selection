import sys
from pathlib import Path
from .pdm import PortfolioDataMerger

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
    files = [x for x in folder.iterdir() if not x.is_dir()
             and not x.name.startswith('.')]
    names = [x.name.split('.')[0] for x in files]
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
    unique_tickers = set(names)
    merged_filename = merged_folder.joinpath(
        f'{"-".join(sorted(unique_tickers))}.csv')
    print(f'Saving merged CSV at {merged_filename}...')
    merged.to_csv(merged_filename)
    # Print out stats on memory usage and data points
    print(merged.info())
