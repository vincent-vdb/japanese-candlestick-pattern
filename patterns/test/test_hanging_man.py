import pytest
import pandas as pd

from patterns import HangingMan

@pytest.fixture
def mock_dataset():
    """Return a mock dataframe as pattern input"""
    return pd.read_csv('patterns/test/mock_dataframe_input.csv')

def test_hanging_man_init(mock_dataset):
    """Test the HangingMan init"""
    # Default HangingMan init
    hanging = HangingMan(mock_dataset)
    assert isinstance(hanging.data, pd.DataFrame)
    assert hanging.trend_threshold == .03

    # Set init values
    trend_threshold = 0.1
    hanging = HangingMan(data=mock_dataset, trend_threshold=trend_threshold)
    assert hanging.trend_threshold == trend_threshold

    # Test percent change computation
    pd.testing.assert_series_equal(hanging.trend, hanging.compute_relative_trend())
