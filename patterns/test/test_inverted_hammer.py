"""InvertedHammer test file"""
import pandas as pd

from patterns import InvertedHammer


def test_inverted_hammer_init(mock_dataset):
    """Test the InvertedHammer init"""
    # Default InvertedHammer init
    inv_hammer = InvertedHammer(mock_dataset)
    assert isinstance(inv_hammer.data, pd.DataFrame)
    assert inv_hammer.trend_threshold == .03

    # Set init values
    trend_threshold = 0.1
    inv_hammer = InvertedHammer(data=mock_dataset, trend_threshold=trend_threshold)
    assert inv_hammer.trend_threshold == trend_threshold

    # Test percent change computation
    pd.testing.assert_series_equal(inv_hammer.trend, inv_hammer.compute_relative_trend())
