import pytest
from typing import *
from olps.datasources.correlation_driven_datasource import CorrelationDrivenDataSource
import numpy as np


class TestCorrelationDrivenDatasource:

    @pytest.fixture
    def cd_datasource(self) -> Dict[str, Union[np.array, CorrelationDrivenDataSource]]:
        """
        Create a basic pytest fixture that will just initialize a data source for testing purposes.
        """
        initial_prices = np.array([137.18, 1827.36, 262.01]).T
        return {
            'initial_prices': initial_prices,
            'second_prices': np.array([136.76, 1828.07, 263.08]).T,
            'third_prices': np.array([136.30, 1826.16, 265.20]).T,
            'fourth_prices': np.array([137.25, 1827.40, 265.02]).T,
            'fifth_prices': np.array([139.75, 1828.03, 262.14]).T,
            'sixth_prices': np.array([139.20, 1828.90, 260.37]).T,
            'very_diff_prices': np.array([69.825, 913.70, 477.036]).T,
            'second_pricesv2': np.array([136.719, 1825.43, 262.01]).T,
            'third_pricesv2': np.array([139.167, 1839.97, 265.054]).T,
            'fourth_pricesv2': np.array([140.137, 1841.22, 264.874]).T,
            'fifth_pricesv2': np.array([142.689, 1841.85, 261.996]).T,
            'sixth_pricesv2': np.array([142.127, 1842.73, 260.227]).T,
            'ds': CorrelationDrivenDataSource(initial_prices=initial_prices, window = 2)
        }

    def test_price_storage(self, cd_datasource: CorrelationDrivenDataSource) -> None:
        """
        Ensure the price is stored correctly.
        """
        assert cd_datasource['ds'].prices.shape == cd_datasource['initial_prices'].shape

    def test_price_addition(self, cd_datasource: CorrelationDrivenDataSource) -> None:
        """
        Ensure single price addition works as expected, adding it to the prices matrix and computing
        the appropriate price relatives.
        """
        cd_datasource['ds'].add_prices(cd_datasource['second_prices'])
        assert cd_datasource['ds'].prices.shape == (3, 2)
        assert cd_datasource['ds'].price_relatives is not None
        assert cd_datasource['ds'].price_relatives.shape == (3, )

    def test_multiple_price_addition(self, cd_datasource: CorrelationDrivenDataSource) -> None:
        """
        Ensure multiple price addition works as expected.
        """
        cd_datasource['ds'].add_prices(cd_datasource['second_prices'])
        cd_datasource['ds'].add_prices(cd_datasource['second_prices'])
        assert cd_datasource['ds'].prices.shape == (3, 3)
        assert cd_datasource['ds'].price_relatives is not None
        assert cd_datasource['ds'].price_relatives.shape == (3, 2)
    
    def test_window_too_large(self, cd_datasource: CorrelationDrivenDataSource) ->None:
        """
        Ensure the similarity set is not updated if the window size is too big
        """
        cd_datasource['ds'].add_prices(cd_datasource['second_prices'])
        cd_datasource['ds'].add_prices(cd_datasource['second_prices'])
        assert cd_datasource['ds'].window == 2
        assert cd_datasource['ds'].prices.shape == (3, 3)
        cd_datasource['ds'].sample_selection()
        assert cd_datasource['ds'].similarity_set is None

    def test_sample_selection(self, cd_datasource: CorrelationDrivenDataSource) ->None:
        """
        Ensure sample selection works as expected, creating a 1D vector
        """
        cd_datasource['ds'].add_prices(cd_datasource['second_prices'])
        cd_datasource['ds'].add_prices(cd_datasource['third_prices'])
        cd_datasource['ds'].add_prices(cd_datasource['fourth_prices'])
        cd_datasource['ds'].add_prices(cd_datasource['fifth_prices'])
        cd_datasource['ds'].add_prices(cd_datasource['sixth_prices'])
        assert cd_datasource['ds'].price_relatives.shape == (3, 5)
        assert cd_datasource['ds'].similarity_set is None
        cd_datasource['ds'].sample_selection()
        assert cd_datasource['ds'].similarity_set is not None
        assert cd_datasource['ds'].similarity_set_size == 1
        assert cd_datasource['ds'].similarity_set[0] == 4
    
    def test_drastic_jump_sample_selection(self, cd_datasource: CorrelationDrivenDataSource) ->None:
        """
        Ensure sample selection filters out windows with very high differences by placing a drastically 
        different price in between, which should remove 2 windows from consideration.
        """
        cd_datasource['ds'].add_prices(cd_datasource['second_prices'])
        cd_datasource['ds'].add_prices(cd_datasource['third_prices'])
        cd_datasource['ds'].add_prices(cd_datasource['fourth_prices'])
        cd_datasource['ds'].add_prices(cd_datasource['very_diff_prices'])
        cd_datasource['ds'].add_prices(cd_datasource['fifth_prices'])
        cd_datasource['ds'].add_prices(cd_datasource['sixth_prices'])
        assert cd_datasource['ds'].similarity_set is None
        cd_datasource['ds'].sample_selection()
        assert cd_datasource['ds'].similarity_set is None

    def test_sample_selection_size_over_one(self, cd_datasource: CorrelationDrivenDataSource) -> None:
        """
        Ensure sample selection works for instances with greater than one candidate
        """
        cd_datasource['ds'].add_prices(cd_datasource['second_pricesv2'])
        cd_datasource['ds'].add_prices(cd_datasource['third_pricesv2'])
        cd_datasource['ds'].add_prices(cd_datasource['fourth_pricesv2'])
        cd_datasource['ds'].add_prices(cd_datasource['fifth_pricesv2'])
        cd_datasource['ds'].add_prices(cd_datasource['sixth_pricesv2'])
        assert cd_datasource['ds'].price_relatives.shape == (3, 5)
        assert cd_datasource['ds'].similarity_set is None
        cd_datasource['ds'].sample_selection()
        assert cd_datasource['ds'].similarity_set is not None
        assert cd_datasource['ds'].similarity_set_size == 2