import pytest
from typing import *
from olps.datasources.olmar_datasource import OLMARDataSource
import numpy as np


class TestOLMARDatasource:

    @pytest.fixture
    def basic_datasource(self) -> Dict[str, Union[np.array, OLMARDataSource]]:
        """
        Create a basic pytest fixture that will just initialize a data source for testing purposes.
        """
        initial_prices = np.array([137.18, 1827.36, 262.01]).T
        return {
            'initial_prices': initial_prices,
            'next_prices': np.array([136.76, 1828.07, 263.08]).T,
            'third_prices': np.array([136.30, 1826.16, 265.20]).T,
            'ds': OLMARDataSource(initial_prices=initial_prices, window = 2)
        }

    def test_price_storage(self, basic_datasource: OLMARDataSource) -> None:
        """
        Ensure the price is stored correctly.
        """
        assert basic_datasource['ds'].prices.shape == basic_datasource['initial_prices'].shape

    def test_price_addition(self, basic_datasource: OLMARDataSource) -> None:
        """
        Ensure single price addition works as expected, adding it to the prices matrix and computing
        the appropriate price relatives.
        """
        basic_datasource['ds'].add_prices(basic_datasource['next_prices'])
        assert basic_datasource['ds'].prices.shape == (3, 2)
        assert basic_datasource['ds'].price_relatives is not None
        assert basic_datasource['ds'].price_relatives.shape == (3, )

    def test_multiple_price_addition(self, basic_datasource: OLMARDataSource) -> None:
        """
        Ensure multiple price addition works as expected.
        """
        basic_datasource['ds'].add_prices(basic_datasource['next_prices'])
        basic_datasource['ds'].add_prices(basic_datasource['third_prices'])
        assert basic_datasource['ds'].prices.shape == (3, 3)
        assert basic_datasource['ds'].price_relatives is not None
        assert basic_datasource['ds'].price_relatives.shape == (3, 2)
    
    def test_future_PRV_prediction(self, basic_datasource: OLMARDataSource) -> None:
        """
        Check that future PRVs are being predicted correctly
        """
        basic_datasource['ds'].add_prices(basic_datasource['next_prices'])
        basic_datasource['ds'].add_prices(basic_datasource['third_prices'])
        basic_datasource['ds'].predict_PRV()
        assert basic_datasource['ds'].predictedPRV is not None
        assert basic_datasource['ds'].predictedPRV.shape == (3, )
