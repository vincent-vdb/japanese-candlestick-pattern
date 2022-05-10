import pytest
import pandas as pd

from patterns import DragonflyDoji

@pytest.fixture
def mock_dataset():
    """Return a mock dataframe as pattern input"""
    return pd.read_csv('patterns/test/mock_dataframe_input.csv')

def test_dragonfly_doji_init(mock_dataset):
    """Test the Doji init"""
    # Default DragonflyDoji init
    ddoji = DragonflyDoji(mock_dataset)
    assert isinstance(ddoji.data, pd.DataFrame)
    assert ddoji.doji_threshold == .003
    assert ddoji.total_range_change_threshold == .02

    # Default doji_threshold set
    doji_threshold = 0.1
    total_range_change_threshold = 0.1
    ddoji = DragonflyDoji(data=mock_dataset,
                          doji_threshold=doji_threshold,
                          total_range_change_threshold=total_range_change_threshold)
    assert ddoji.doji_threshold == doji_threshold
    assert ddoji.total_range_change_threshold == total_range_change_threshold

    # Test percent change computation
    pd.testing.assert_series_equal(ddoji.total_range_percent_change,
                                   ddoji.compute_total_range_percent_change())