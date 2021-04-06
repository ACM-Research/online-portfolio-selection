import pytest
from math import isclose
from typing import *
from olps.strategies.exp_grad_strategy import ExpGradStrategy
from olps.datasources.datasource import DataSource
import numpy as np


class TestExpGradStrategy:

    @pytest.fixture
    def exp_grad_strategy(self) -> ExpGradStrategy:
        """
        Create a basic pytest fixture that will create a BAHStrategy with three assets
        """
        return ExpGradStrategy(num_assets=3)

    @pytest.fixture
    def fake_datasource(self) -> Dict[str, Union[np.array, DataSource]]:
        """
        Create a basic pytest fixture that will just initialize a data source for testing purposes.
        """
        initial_prices = np.array([137.18, 1827.36, 262.01])
        next_prices = np.array([136.76, 1893.07, 267.08])
        return {
            'initial_prices': initial_prices,
            'next_prices': next_prices,
            'ds': DataSource(initial_prices=initial_prices)
        }

    def test_constructor(self, exp_grad_strategy: ExpGradStrategy) -> None:
        """
        Check that the constructor initializes the strategy object as expected.
        """
        strat = exp_grad_strategy
        assert strat.weights.shape == (3, )
        assert strat.cumulative_wealth.shape == (1, )
        assert np.array_equal(strat.weights, np.array([1/3, 1/3, 1/3]))

    def test_update_with_price_relatives(self, exp_grad_strategy: ExpGradStrategy, fake_datasource: Dict[str, Union[np.array, DataSource]]) -> None:
        """
        Check that update() works as expected in updating weights, period, and cumulative return.
        """
        strat = exp_grad_strategy
        ds = fake_datasource['ds']
        ds.add_prices(fake_datasource['next_prices'])
        cumulative_return = strat.update(ds)
        
        assert isclose(cumulative_return, 1.0174159, rel_tol = 1E-5)
        assert isclose(strat.weights[0], 0.3326627, rel_tol = 1E-5)
        assert isclose(strat.weights[1], 0.333941, rel_tol = 1E-5)
        assert strat.cumulative_wealth.shape == (2, )
        assert strat.weights.shape == (3, )
