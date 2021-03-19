import pytest
from typing import *
from olps.datasources.datasource import DataSource
import numpy as np


class TestDatasource:

    @pytest.fixture
    def basic_datasource(self) -> Dict[str, Union[np.array, DataSource]]:
        """
        Create a basic pytest fixture that will just initialize a data source for testing purposes.
        """
        initial_prices = np.array([137.18, 1827.36, 262.01]).T
        return {
            'initial_prices': initial_prices,
            'next_prices': np.array([136.76, 1893.07, 267.08]).T,
            'ds': DataSource(initial_prices=initial_prices)
        }

    def test_price_storage(self, basic_datasource: DataSource) -> None:
        """
        Ensure the price is stored correctly.
        """
        assert basic_datasource['ds'].prices.shape == basic_datasource['initial_prices'].shape

    def test_price_addition(self, basic_datasource: DataSource) -> None:
        """
        Ensure single price addition works as expected, adding it to the prices matrix and computing
        the appropriate price relatives.
        """
        basic_datasource['ds'].add_prices(basic_datasource['next_prices'])
        assert basic_datasource['ds'].prices.shape == (3, 2)
        assert basic_datasource['ds'].price_relatives is not None
        assert basic_datasource['ds'].price_relatives.shape == (3, )

    def test_multiple_price_addition(self, basic_datasource: DataSource) -> None:
        """
        Ensure multiple price addition works as expected.
        """
        basic_datasource['ds'].add_prices(basic_datasource['next_prices'])
        basic_datasource['ds'].add_prices(basic_datasource['next_prices'])
        assert basic_datasource['ds'].prices.shape == (3, 3)
        assert basic_datasource['ds'].price_relatives is not None
        assert basic_datasource['ds'].price_relatives.shape == (3, 2)
