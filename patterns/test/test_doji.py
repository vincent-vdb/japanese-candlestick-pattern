"""Doji test file"""
import pandas as pd

from patterns import Doji


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

def test_is_doji():
    """Test is_doji method"""
    # Create a fake dataframe with 2 dojis and one non doji times
    data = pd.DataFrame({'Open': [1, 2, 1000],
                         'High': [2, 3, 1100],
                         'Low': [0, 2 , 900],
                         'Close':[1, 3, 1001]})
    # Expected values
    is_doji_gt = pd.Series(data=[True, False, True])

    # Instantiate
    doji = Doji(data)
    # Compute
    is_doji = doji.is_doji()
    # Test
    pd.testing.assert_series_equal(is_doji, is_doji_gt)
