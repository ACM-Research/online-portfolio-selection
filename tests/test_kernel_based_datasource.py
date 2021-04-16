import pytest
from typing import *
from olps.datasources.kernel_based_datasource import KernelBasedDataSource
import numpy as np


class TestKernelBasedDatasource:

    @pytest.fixture
    def basic_datasource(self) -> Dict[str, Union[np.array, KernelBasedDataSource]]:
        """
        Create a basic pytest fixture that will just initialize a data source for testing purposes.
        """
        initial_prices = np.array([137.18, 1827.36, 262.01]).T
        return {
            'initial_prices': initial_prices,
            'next_prices': np.array([136.76, 1828.07, 263.08]).T,
            'third_prices': np.array([136.30, 1826.16, 265.20]).T,
            'fourth_prices': np.array([137.25, 1827.40, 265.02]).T,
            'fifth_prices': np.array([139.75, 1828.03, 262.14]).T,
            'sixth_prices': np.array([139.20, 1828.90, 260.37]).T,
            'very_diff_prices': np.array([50.00, 700.00, 300.00]).T,
            'ds': KernelBasedDataSource(initial_prices=initial_prices, window = 2)
        }

    def test_price_storage(self, basic_datasource: KernelBasedDataSource) -> None:
        """
        Ensure the price is stored correctly.
        """
        assert basic_datasource['ds'].prices.shape == basic_datasource['initial_prices'].shape

    def test_price_addition(self, basic_datasource: KernelBasedDataSource) -> None:
        """
        Ensure single price addition works as expected, adding it to the prices matrix and computing
        the appropriate price relatives.
        """
        basic_datasource['ds'].add_prices(basic_datasource['next_prices'])
        assert basic_datasource['ds'].prices.shape == (3, 2)
        assert basic_datasource['ds'].price_relatives is not None
        assert basic_datasource['ds'].price_relatives.shape == (3, )

    def test_multiple_price_addition(self, basic_datasource: KernelBasedDataSource) -> None:
        """
        Ensure multiple price addition works as expected.
        """
        basic_datasource['ds'].add_prices(basic_datasource['next_prices'])
        basic_datasource['ds'].add_prices(basic_datasource['next_prices'])
        assert basic_datasource['ds'].prices.shape == (3, 3)
        assert basic_datasource['ds'].price_relatives is not None
        assert basic_datasource['ds'].price_relatives.shape == (3, 2)
    
    def test_window_too_large(self, basic_datasource: KernelBasedDataSource) ->None:
        """
        Ensure the similarity set is not updated if the window size is too big
        """
        basic_datasource['ds'].add_prices(basic_datasource['next_prices'])
        basic_datasource['ds'].add_prices(basic_datasource['next_prices'])
        assert basic_datasource['ds'].window == 2
        assert basic_datasource['ds'].prices.shape == (3, 3)
        basic_datasource['ds'].sample_selection()
        assert basic_datasource['ds'].similarity_set is None

    def test_sample_selection(self, basic_datasource: KernelBasedDataSource) ->None:
        """
        Ensure sample selection works as expected, creating a 1D vector
        """
        basic_datasource['ds'].add_prices(basic_datasource['next_prices'])
        basic_datasource['ds'].add_prices(basic_datasource['third_prices'])
        basic_datasource['ds'].add_prices(basic_datasource['fourth_prices'])
        basic_datasource['ds'].add_prices(basic_datasource['fifth_prices'])
        basic_datasource['ds'].add_prices(basic_datasource['sixth_prices'])
        assert basic_datasource['ds'].price_relatives.shape == (3, 5)
        assert basic_datasource['ds'].similarity_set is None
        basic_datasource['ds'].sample_selection()
        assert basic_datasource['ds'].similarity_set is not None
        assert basic_datasource['ds'].similarity_set.size == 3
        assert basic_datasource['ds'].similarity_set.shape == (1, 3)
    
    def test_drastic_jump_sample_selection(self, basic_datasource: KernelBasedDataSource) ->None:
        """
        Ensure sample selection filters out windows with very high differences by placing a drastically 
        different price in between, which should remove 2 windows from consideration.
        """
        basic_datasource['ds'].add_prices(basic_datasource['next_prices'])
        basic_datasource['ds'].add_prices(basic_datasource['third_prices'])
        basic_datasource['ds'].add_prices(basic_datasource['very_diff_prices'])
        basic_datasource['ds'].add_prices(basic_datasource['fourth_prices'])
        basic_datasource['ds'].add_prices(basic_datasource['fifth_prices'])
        basic_datasource['ds'].add_prices(basic_datasource['sixth_prices'])
        assert basic_datasource['ds'].similarity_set is None
        basic_datasource['ds'].sample_selection()
        assert basic_datasource['ds'].similarity_set is not None
        assert basic_datasource['ds'].similarity_set.size == 1
