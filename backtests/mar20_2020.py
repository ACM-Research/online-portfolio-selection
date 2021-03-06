from olps.market import TradingMarket, TradingMarketStrategyInfo
from olps.strategies import BAHStrategy
from olps.strategies import BestStockStrategy
from olps.strategies import ACStrategy
from olps.strategies import CorrelationDrivenLogStrategy
from olps.strategies import CRPStrategy
from olps.strategies import ExpGradStrategy
from olps.strategies import KernelBasedLogStrategy
from olps.strategies import KernelBasedSemiLogStrategy
from olps.strategies import OLMARStrategy
from olps.datasources import DataSource
from olps.datasources import ACDataSource
from olps.datasources import CorrelationDrivenDataSource
from olps.datasources import KernelBasedDataSource
from olps.datasources import OLMARDataSource
from olps.visualization.brg_visualizer import BarCRGVisualizer
from olps.visualization.crg_visualizer import CRGVisualizer
from olps.util import minute, hour
import numpy as np
from pathlib import Path

# Use this as a template to backtest strategies!

def main():
    info: TradingMarketStrategyInfo = {
        # strategies array: pass in initialized strategies!
        'strategies': [BAHStrategy(6), BestStockStrategy(6), 
        ACStrategy(6), CorrelationDrivenLogStrategy(6), CRPStrategy(6), 
        ExpGradStrategy(6), OLMARStrategy(6, epsilon=0.9), KernelBasedLogStrategy(6), 
        KernelBasedSemiLogStrategy(6)],
        # datasource factory: initialize datasources with those intial prices inside the array!
        'datasource_factory': lambda initial_prices: [DataSource(initial_prices), DataSource(initial_prices), 
        ACDataSource(initial_prices), CorrelationDrivenDataSource(initial_prices), DataSource(initial_prices), 
        DataSource(initial_prices), OLMARDataSource(initial_prices), KernelBasedDataSource(initial_prices, window = 4), 
        KernelBasedDataSource(initial_prices, window= 4)],
        # frequencies: use the olps.util module to define frequencies!
        'frequencies': [minute(10), minute(10), minute(10), minute(10), minute(10), minute(10), 
        minute(10), minute(10), minute(10)],
    }
    # Define a data directory
    data_dir = Path('.') / 'data'
    # Define the path. You should change this depending on what portfolio you're backtesting.
    path = data_dir / 'mar20_2020' / 'merged' / 'AAPL-AMZN-OXY-PEP-SPY-VXX.csv'
    # Create a market object with the info and path.
    market = TradingMarket(info, path)
    asset_names = market.data_provider.assets
    # Main loop: run through all the ticks
    while market.can_advance():
        market.advance()
    # Save the return
    backtest_name = 'mar20_2020_testV1'  # make sure to change this for every new backtest!
    for strategy in market.strategies:
        name = type(strategy).__name__
        np.savetxt(f'{backtest_name}-wealth-{name}.txt',
                   strategy.cumulative_wealth)

    BarCRGVisualizer.visualize('bar_out_mar20_2020.png', market.strategies, asset_names)

if __name__ == "__main__":
    main()
