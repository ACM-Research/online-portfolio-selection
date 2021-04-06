import pytest
from math import isclose
from typing import *
from olps.strategies.best_stock_strategy import BestStockStrategy
from olps.datasources.datasource import DataSource
import numpy as np


class TestBestStocktrategy:

    @pytest.fixture
    def best_stock_strategy(self) -> BestStockStrategy:
        """
        Create a basic pytest fixture that will create a BAHStrategy with three assets
        """
        return BestStockStrategy(num_assets=3)

    @pytest.fixture
    def fake_datasource(self) -> Dict[str, Union[np.array, DataSource]]:
        """
        Create a basic pytest fixture that will just initialize a data source for testing purposes.
        """
        #initial_prices = np.array([137.18, 1827.36, 262.01]).T
        #next_prices = np.array([136.76, 1893.07, 267.08]).T
        initial_prices = np.array([137.18, 1827.36, 262.01])
        next_prices = np.array([136.76, 1893.07, 267.08])
        return {
            'initial_prices': initial_prices,
            'next_prices': next_prices,
            'ds': DataSource(initial_prices=initial_prices)
        }

    def test_constructor(self, best_stock_strategy: BestStockStrategy) -> None:
        """
        Check that the constructor initializes the strategy object as expected.
        """
        strat = best_stock_strategy
        assert strat.weights.shape == (3, )
        assert strat.cumulative_wealth.shape == (1, )
        assert np.array_equal(strat.weights, np.array([1/3, 1/3, 1/3]))

    def test_update_with_price_relatives(self, best_stock_strategy: BestStockStrategy, fake_datasource: Dict[str, Union[np.array, DataSource]]) -> None:
        """
        Check that update() works as expected in updating weights, period, and cumulative return.
        """
        strat = best_stock_strategy
        ds = fake_datasource['ds']
        ds.add_prices(fake_datasource['next_prices'])
        cumulative_return = strat.update(ds)

        full_weight_occurences = np.count_nonzero(strat.weights == 1)
        non_zero_occurences = np.count_nonzero(strat.weights)

        assert full_weight_occurences == non_zero_occurences
        assert strat.weights[1] == 1
        assert isclose(cumulative_return, 1.017415, rel_tol = 1E-5)
        assert strat.cumulative_wealth.shape == (2, )
        assert strat.weights.shape == (3, )
