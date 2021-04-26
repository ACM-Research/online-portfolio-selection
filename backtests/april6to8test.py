from olps.market import TradingMarket, TradingMarketStrategyInfo
from olps.strategies import KernelBasedLogStrategy
from olps.strategies import ExpGradStrategy
from olps.strategies import BestStockStrategy
from olps.strategies import BAHStrategy
from olps.datasources import KernelBasedDataSource
from olps.datasources import DataSource
from olps.util import minute
import numpy as np
from pathlib import Path

# Use this as a template to backtest strategies!


def main():
    info: TradingMarketStrategyInfo = {
        # strategies array: pass in initialized strategies!
        'strategies': [KernelBasedLogStrategy(5),BAHStrategy(5), ExpGradStrategy(5), BestStockStrategy(5)],
        # datasource factory: initialize datasources with those intial prices inside the array!
        'datasource_factory': lambda initial_prices: [KernelBasedDataSource(initial_prices,3), DataSource(initial_prices),DataSource(initial_prices),DataSource(initial_prices)],
        # frequencies: use the olps.util module to define frequencies!
        'frequencies': [minute(5),minute(5),minute(5),minute(5)],
    }
    # Define a data directory
    data_dir = Path('.') / 'data'
    # Define the path. You should change this depending on what portfolio you're backtesting.
    path = data_dir / 'april6to8' / 'merged' / 'CL-COST-DAL-KO-T.csv'
    # Create a market object with the info and path.
    market = TradingMarket(info, path)
    # Main loop: run through all the ticks
    while market.can_advance():
        market.advance()
    # Save the return
    backtest_name = 'april6to8test'  # make sure to change this for every new backtest!
    for strategy in market.strategies:
        name = type(strategy).__name__
        np.savetxt(f'{backtest_name}-wealth-{name}.txt',
                   strategy.cumulative_wealth)


if __name__ == "__main__":
    main()
