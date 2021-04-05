import pytest
from math import isclose
from typing import *
from olps.strategies.up_strategy import UPStrategy
from olps.datasources.datasource import DataSource
import numpy as np


class TestUPStrategy:

    @pytest.fixture
    def bah_strategy(self) -> UPStrategy:
        """
        Create a basic pytest fixture that will create a UPStrategy with three assets
        """
        return UPStrategy(num_assets=3)

    @pytest.fixture
    def fake_datasource(self) -> Dict[str, Union[np.array, DataSource]]:
        """
        Create a basic pytest fixture that will just initialize a data source for testing purposes.
        """
        initial_prices = np.array([1., 1., 1.]).T
        next_prices = np.array([2., 2., 2.]).T
        return {
            'initial_prices': initial_prices,
            'next_prices': next_prices,
            'ds': DataSource(initial_prices=initial_prices)
        }

    def test_constructor(self, bah_strategy: UPStrategy) -> None:
        """
        Check that the constructor initializes the strategy object as expected.
        """
        strat = bah_strategy
        assert strat.weights.shape == (3, )
        assert strat.cumulative_wealth.shape == (1, )
        assert np.array_equal(strat.weights, np.array([1/3, 1/3, 1/3]).T)

    def test_update_with_price_relatives(self, bah_strategy: UPStrategy, fake_datasource: Dict[str, Union[np.array, DataSource]]) -> None:
        """
        Check that update() works as expected in updating weights, period, and cumulative return.
        """
        strat = bah_strategy
        ds = fake_datasource['ds']
        ds.add_prices(fake_datasource['next_prices'])
        cumulative_return = strat.update(ds)
        assert np.array_equal(strat.weights, np.array([1/3, 1/3, 1/3]).T)
        assert isclose(cumulative_return, 2.)
        assert strat.cumulative_wealth.shape == (2, )
        assert strat.weights.shape == (3, )
