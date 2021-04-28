from olps.market import TradingMarket, TradingMarketStrategyInfo
from olps.strategies import Strategy
from olps.strategies import BAHStrategy
from olps.strategies import BestStockStrategy
from olps.datasources import DataSource
from olps.util import hour
from olps.visualization.animated_crg_visualizer import AnimatedCRGVisualizer
import numpy as np
from pathlib import Path

# Use this as a template to backtest strategies!


def main():
    info: TradingMarketStrategyInfo = {
        # strategies array: pass in initialized strategies!
        'strategies': [BAHStrategy(7), BestStockStrategy(7)],
        # datasource factory: initialize datasources with those intial prices inside the array!
        'datasource_factory': lambda initial_prices: [DataSource(initial_prices), DataSource(initial_prices)],
        # frequencies: use the olps.util module to define frequencies!
        'frequencies': [hour(2), hour(2)],
    }

    # Define a data directory
    data_dir = Path('.') / 'data'
    # Define the path. You should change this depending on what portfolio you're backtesting.
    path = data_dir / 'yearlong' / 'merged' / 'ABBV-AMC-BGS-GME-NHI-WMT-XOM.csv'
    # Create a market object with the info and path.
    market = TradingMarket(info, path)
    # Main loop: run through all the ticks
    while market.can_advance():
        market.advance()
    # Save the return
    backtest_name = 'yearlong'  # make sure to change this for every new backtest!
    for strategy in market.strategies:
        name = type(strategy).__name__
        np.savetxt(f'{backtest_name}-wealth-{name}.txt',
                   strategy.cumulative_wealth)

    AnimatedCRGVisualizer.visualize('out.mp4', market.strategies)



if __name__ == "__main__":
    main()
