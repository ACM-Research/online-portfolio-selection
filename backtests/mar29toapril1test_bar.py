import os, json
from olps.market import TradingMarket, TradingMarketStrategyInfo, MarketDataProvider
from olps.strategies import Strategy
from olps.strategies import BAHStrategy
from olps.strategies import BestStockStrategy
from olps.datasources import DataSource
from olps.util import minute, hour
from olps.visualization.brg_visualizer import BarCRGVisualizer
import numpy as np
from pathlib import Path


def main():
    info: TradingMarketStrategyInfo = {
        # strategies array: pass in initialized strategies!
        'strategies': [BAHStrategy(6), BestStockStrategy(6)],
        # datasource factory: initialize datasources with those intial prices inside the array!
        'datasource_factory': lambda initial_prices: [DataSource(initial_prices), DataSource(initial_prices)],
        # frequencies: use the olps.util module to define frequencies!
        'frequencies': [hour(2), hour(2)],
    }

    data_dir = Path('.') / 'data'
    path = data_dir / 'mar29toapril1' / 'merged' / 'AAPL-BBY-DIS-TSLA-TWTR-UBER.csv'
    market = TradingMarket(info, path)
    asset_names = market.data_provider.assets
    while market.can_advance():
        market.advance()
    backtest_name = 'mar29toapril1'
    for strategy in market.strategies:
        name = type(strategy).__name__
        np.savetxt(f'{backtest_name}-wealth-{name}.txt',
                   strategy.cumulative_wealth)

    BarCRGVisualizer.visualize('out.png', market.strategies, asset_names)



if __name__ == "__main__":
    main()