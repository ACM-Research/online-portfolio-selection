import pytest
from math import isclose
from typing import *
from olps.strategies.olmar_strategy import OLMARStrategy
from olps.datasources.olmar_datasource import OLMARDataSource
import numpy as np


class TestOLMARStrategy:

    @pytest.fixture
    def olmar_strategy(self) -> OLMARStrategy:
        """
        Create a basic pytest fixture that will create a ACStrategy with three assets
        """
        return OLMARStrategy(num_assets=3)

    @pytest.fixture
    def fake_datasource(self) -> Dict[str, Union[np.array, OLMARDataSource]]:
        """
        Create a basic pytest fixture that will just initialize a data source for testing purposes.
        """
        initial_prices = np.array([137.18, 1827.36, 262.01])
        next_prices = np.array([2., 2., 2.]).T
        return {
            'initial_prices': initial_prices,
            'next_prices': np.array([136.76, 1828.07, 263.08]).T,
            'third_prices': np.array([136.30, 1826.16, 265.20]).T,
            'fourth_prices': np.array([136.80, 1826.86, 265.80]).T,
            'ds': OLMARDataSource(initial_prices=initial_prices)
        }

    def test_constructor(self, olmar_strategy: OLMARStrategy) -> None:
        """
        Check that the constructor initializes the strategy object as expected.
        """
        strat = olmar_strategy
        assert strat.weights.shape == (3, )
        assert strat.cumulative_wealth.shape == (1, )
        assert np.array_equal(strat.weights, np.array([1/3, 1/3, 1/3]).T)

    def test_update_with_price_relatives(self, olmar_strategy: OLMARStrategy, fake_datasource: Dict[str, Union[np.array, OLMARDataSource]]) -> None:
        """
        Check that update() works as expected in updating weights, period, and cumulative return.
        """
        strat = olmar_strategy
        ds = fake_datasource['ds']
        ds.add_prices(fake_datasource['next_prices'])
        ds.add_prices(fake_datasource['third_prices'])
        ds.add_prices(fake_datasource['fourth_prices'])
        cumulative_return = strat.update(ds)
        assert strat.weights.shape == (3, )
        assert isclose(strat.weights[0], 0.33333004293691315)
        assert isclose(strat.weights[1], 0.33331832341042444)
        assert isclose(strat.weights[2], 0.3333516336526624)
        assert isclose(sum(strat.weights), 1.0)
        assert strat.cumulative_wealth.shape == (2, )
        assert isclose(cumulative_return, 1.002104713338732)