from olps.market import TradingMarket, TradingMarketStrategyInfo
from olps.strategies import BAHStrategy
from olps.strategies.ac_strategy import ACStrategy
from olps.strategies.best_stock_strategy import BestStockStrategy
from olps.strategies.crp_strategy import CRPStrategy
from olps.strategies.exp_grad_strategy import ExpGradStrategy
from olps.strategies.kernel_based_log_optimal_strategy import KernelBasedLogStrategy
from olps.strategies.kernel_based_log_optimal_strategy import KernelBasedDataSource
from olps.strategies.kernel_based_semi_log_optimal_strategy import KernelBasedSemiLogStrategy
from olps.strategies.kernel_based_semi_log_optimal_strategy import KernelBasedDataSource
from olps.datasources import DataSource
from olps.datasources.ac_datasource import ACDataSource
from olps.util import minute, hour
from olps.visualization.visualizer import Visualizer
import numpy as np
from pathlib import Path

# Use this as a template to backtest strategies!


def main():
    info: TradingMarketStrategyInfo = {
        # strategies array: pass in initialized strategies!
        # kernel based log not working or semi
        'strategies': [ACStrategy(6), CRPStrategy(6), ExpGradStrategy(6), BestStockStrategy(6), BAHStrategy(6)],
        # datasource factory: initialize datasources with those intial prices inside the array!
        'datasource_factory': lambda initial_prices: [ACDataSource(initial_prices), DataSource(initial_prices), DataSource(initial_prices), DataSource(initial_prices), DataSource(initial_prices)],
        # frequencies: use the olps.util module to define frequencies!
        'frequencies': [minute(15)] * 5,
    }
    # Define a data directory
    data_dir = Path('.') / 'data'
    # Define the path. You should change this depending on what portfolio you're backtesting.
    path = data_dir / 'mar29test' / 'merged' / 'AAPL-BBY-DIS-TSLA-TWTR-UBER.csv'
    # Create a market object with the info and path.
    market = TradingMarket(info, path)
    # Main loop: run through all the ticks
    while market.can_advance():
        market.advance()
    # Save the return
    backtest_name = 'mar29test'  # make sure to change this for every new backtest!
    for strategy in market.strategies:
        name = type(strategy).__name__
        np.savetxt(f'{backtest_name}-wealth-{name}.txt',
                   strategy.cumulative_wealth)

    v = Visualizer('vis.png', market.strategies)
    v.visualize()


if __name__ == "__main__":
    main()
