import pytest
from math import isclose
from typing import *
from olps.strategies.strategy import Strategy
from olps.datasources.datasource import DataSource
import numpy as np


class TestStrategy:

    @pytest.fixture
    def fake_strategy(self) -> Strategy:
        """
        Create a basic pytest fixture that will just provide a barebones implementation of Strategy.
        """
        class FakeStrategy(Strategy):
            def update_weights(self, market_data: DataSource) -> None:
                return

        return FakeStrategy(num_assets=3)

    @pytest.fixture
    def fake_datasource(self) -> Dict[str, Union[np.array, DataSource]]:
        """
        Create a basic pytest fixture that will just initialize a data source for testing purposes.
        """
        initial_prices = np.array([137.18, 1827.36, 262.01]).T
        return {
            'initial_prices': initial_prices,
            'next_prices': np.array([136.76, 1893.07, 267.08]).T,
            'ds': DataSource(initial_prices=initial_prices)
        }

    def test_constructor(self, fake_strategy: Strategy) -> None:
        """
        Check that the constructor initializes the strategy object as expected.
        """
        strat = fake_strategy
        assert strat.weights.shape == (3, )
        assert strat.cumulative_wealth.shape == (1, )
        assert np.array_equal(strat.weights, np.array([1/3, 1/3, 1/3]).T)

    def test_update_with_price_relatives(self, fake_strategy: Strategy, fake_datasource: Dict[str, Union[np.array, DataSource]]) -> None:
        """
        Check that update() works as expected in updating weights, period, and cumulative return.
        """
        strat = fake_strategy
        ds = fake_datasource['ds']
        ds.add_prices(fake_datasource['next_prices'])
        cumulative_return = strat.update(ds)
        assert np.array_equal(strat.weights, np.array([1/3, 1/3, 1/3]).T)
        assert isclose(cumulative_return, 1.017415905)
        assert strat.cumulative_wealth.shape == (2, )
        assert strat.weights.shape == (3, )
