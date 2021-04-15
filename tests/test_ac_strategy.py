import pytest
from math import isclose
from typing import *
from olps.strategies.ac_strategy import ACStrategy
from olps.datasources.ac_datasource import ACDataSource
import numpy as np


class TestACStrategy:

    @pytest.fixture
    def bah_strategy(self) -> ACStrategy:
        """
        Create a basic pytest fixture that will create a ACStrategy with three assets
        """
        return ACStrategy(num_assets=3)

    @pytest.fixture
    def fake_datasource(self) -> Dict[str, Union[np.array, ACDataSource]]:
        """
        Create a basic pytest fixture that will just initialize a data source for testing purposes.
        """
        initial_prices = np.array([1., 1., 1.]).T
        next_prices = np.array([2., 2., 2.]).T
        return {
            'initial_prices': initial_prices,
            'next_prices': next_prices,
            'ds': ACDataSource(initial_prices=initial_prices)
        }

    def test_constructor(self, bah_strategy: ACStrategy) -> None:
        """
        Check that the constructor initializes the strategy object as expected.
        """
        strat = bah_strategy
        assert strat.weights.shape == (3, )
        assert strat.cumulative_wealth.shape == (1, )
        assert np.array_equal(strat.weights, np.array([1/3, 1/3, 1/3]).T)

    def test_update_with_price_relatives(self, bah_strategy: ACStrategy, fake_datasource: Dict[str, Union[np.array, ACDataSource]]) -> None:
        """
        Check that update() works as expected in updating weights, period, and cumulative return.
        """
        strat = bah_strategy
        ds = fake_datasource['ds']
        ds.add_prices(fake_datasource['next_prices'])
        cumulative_return = strat.update(ds)
        assert np.array_equal(strat.weights, np.array([1/3, 1/3, 1/3]).T)
        for arr in np.array([[1, 1.5, 2], [.5, 2, 3], [1, 1, 1]]):
            ds.add_prices(arr)
            cumulative_return = strat.update(ds)
        assert isclose(cumulative_return, 1.4868526839459266)
        assert strat.cumulative_wealth.shape == (5, )
        assert strat.weights.shape == (3, )
