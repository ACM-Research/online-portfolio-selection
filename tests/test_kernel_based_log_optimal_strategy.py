import pytest
from math import isclose
from typing import *
from olps.strategies.kernel_based_log_optimal_strategy import KernelBasedLogStrategy
from olps.datasources.kernel_based_datasource import KernelBasedDataSource
import numpy as np

class TestKernelBasedLogStrategy:
    @pytest.fixture
    def kernel_based_log_optimal_strategy(self) -> KernelBasedLogStrategy:
        """
        Create a basic pytest fixture that will just provide a barebones implementation of Strategy
        """
        return KernelBasedLogStrategy(num_assets=3)
    
    @pytest.fixture
    def fake_datasource(self) -> Dict[str, Union[np.array, KernelBasedDataSource]]:
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
            'very_diff_prices': np.array([50.00, 700.00, 300.00]).T,
            'ds': KernelBasedDataSource(initial_prices=initial_prices, window = 2)
        }
    def test_constructor(self, kernel_based_log_optimal_strategy: KernelBasedLogStrategy) -> None:
        """
        Check that the constructor initializes the strategy object as expected.
        """
        strat = kernel_based_log_optimal_strategy
        assert strat.weights.shape == (3, )
        assert strat.cumulative_wealth.shape == (1, )
        assert np.array_equal(strat.weights, np.array([1/3, 1/3, 1/3]).T)

    def test_update_with_price_relatives(self, kernel_based_log_optimal_strategy: KernelBasedLogStrategy, fake_datasource: Dict[str, Union[np.array, KernelBasedDataSource]]) -> None:
        """
        Check that update() works as expected in updating weights, period, and cumulative return.
        """
        strat = kernel_based_log_optimal_strategy
        ds = fake_datasource['ds']
        ds.add_prices(fake_datasource['next_prices'])
        ds.add_prices(fake_datasource['third_prices'])
        ds.add_prices(fake_datasource['fourth_prices'])
        ds.add_prices(fake_datasource['fifth_prices'])
        ds.add_prices(fake_datasource['sixth_prices'])
        cumulative_return = strat.update(ds)
        assert isclose(strat.weights[0],0.3286011017)
        assert isclose(strat.weights[1],0.3339856391)
        assert isclose(strat.weights[2],0.3374132592)
        assert isclose(cumulative_return,0.9965960685)
        assert strat.cumulative_wealth.shape == (2, )
        assert strat.weights.shape == (3, )

