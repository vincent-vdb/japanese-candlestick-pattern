import pytest
import pandas as pd

from patterns import GravestoneDoji

@pytest.fixture
def mock_dataset():
    """Return a mock dataframe as pattern input"""
    return pd.read_csv('patterns/test/mock_dataframe_input.csv')

def test_gravestone_doji_init(mock_dataset):
    """Test the GravestoneDoji init"""
    # Default GravestoneDoji init
    gdoji = GravestoneDoji(mock_dataset)
    assert isinstance(gdoji.data, pd.DataFrame)
    assert gdoji.doji_threshold == .003
    assert gdoji.total_range_change_threshold == .02

    # Default doji_threshold set
    doji_threshold = 0.1
    total_range_change_threshold = 0.1
    gdoji = GravestoneDoji(data=mock_dataset,
                           doji_threshold=doji_threshold,
                           total_range_change_threshold=total_range_change_threshold)
    assert gdoji.doji_threshold == doji_threshold
    assert gdoji.total_range_change_threshold == total_range_change_threshold

    # Test percent change computation
    pd.testing.assert_series_equal(gdoji.total_range_percent_change,
                                   gdoji.compute_total_range_percent_change())
