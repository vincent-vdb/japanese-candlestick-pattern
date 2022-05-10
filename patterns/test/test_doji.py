import pytest
import pandas as pd

from patterns import Doji

@pytest.fixture
def mock_dataset():
    """Return a mock dataframe as pattern input"""
    return pd.read_csv('patterns/test/mock_dataframe_input.csv')

def test_doji_init(mock_dataset):
    """Test the Doji init"""
    # Default Doji init
    doji = Doji(mock_dataset)
    assert isinstance(doji.data, pd.DataFrame)
    assert doji.doji_threshold == .003

    # Default doji_threshold set
    doji_threshold = 0.1
    doji = Doji(data=mock_dataset, doji_threshold=doji_threshold)
    assert doji.doji_threshold == doji_threshold

    # Test percent change computation
    pd.testing.assert_series_equal(doji.percent_change, doji.compute_percent_change())