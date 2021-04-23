import pytest
from math import isclose
from typing import *
from olps.strategies.correlation_driven_log_optimal_strategy import CorrelationDrivenLogStrategy
from olps.datasources.correlation_driven_datasource import CorrelationDrivenDataSource
import numpy as np

class TestCorrelationDrivenLogStrategy:
    @pytest.fixture
    def correlation_driven_log_optimal_strategy(self) -> CorrelationDrivenLogStrategy:
        """
        Create a basic pytest fixture that will just provide a barebones implementation of Strategy
        """
        return CorrelationDrivenLogStrategy(num_assets=3)
    
    @pytest.fixture
    def cd_datasource(self) -> Dict[str, Union[np.array, CorrelationDrivenDataSource]]:
        """
        Create a basic pytest fixture that will just initialize a data source for testing purposes.
        """
        initial_prices = np.array([137.18, 1827.36, 262.01]).T
        return {
            'initial_prices': initial_prices,
            'next_prices': np.array([136.76, 1893.07, 267.08]).T,
            'third_prices': np.array([136.30, 1826.16, 265.20]).T,
            'fourth_prices': np.array([137.25, 1827.40, 265.02]).T,
            'fifth_prices': np.array([139.75, 1828.03, 262.14]).T,
            'sixth_prices': np.array([139.20, 1828.90, 260.37]).T,
            'very_diff_prices': np.array([69.825, 913.70, 477.036]).T,
            'ds': CorrelationDrivenDataSource(initial_prices=initial_prices, window = 2)
        }
    def test_constructor(self, correlation_driven_log_optimal_strategy: CorrelationDrivenLogStrategy) -> None:
        """
        Check that the constructor initializes the strategy object as expected.
        """
        strat = correlation_driven_log_optimal_strategy
        assert strat.weights.shape == (3, )
        assert strat.cumulative_wealth.shape == (1, )
        assert np.array_equal(strat.weights, np.array([1/3, 1/3, 1/3]).T)

    def test_update_with_price_relatives(self, correlation_driven_log_optimal_strategy: CorrelationDrivenLogStrategy, cd_datasource: Dict[str, Union[np.array, CorrelationDrivenDataSource]]) -> None:
        """
        Check that update() works as expected in updating weights, period, and cumulative return.
        """
        strat = correlation_driven_log_optimal_strategy
        ds = cd_datasource['ds']
        ds.add_prices(cd_datasource['next_prices'])
        ds.add_prices(cd_datasource['third_prices'])
        ds.add_prices(cd_datasource['fourth_prices'])
        ds.add_prices(cd_datasource['fifth_prices'])
        ds.add_prices(cd_datasource['sixth_prices'])
        cumulative_return = strat.update(ds)
        assert isclose(strat.weights[0], 0.33349339415314644)
        assert isclose(strat.weights[1], 0.332156713298505)
        assert isclose(strat.weights[2], 0.33434989254834846)
        assert isclose(cumulative_return, 0.9965960685646182)
        assert strat.cumulative_wealth.shape == (2, )
        assert strat.weights.shape == (3, )