"""Hammer test file"""
import pandas as pd

from patterns import Hammer


def test_hammer_init(mock_dataset):
    """Test the Hammer init"""
    # Default Hammer init
    hammer = Hammer(mock_dataset)
    assert isinstance(hammer.data, pd.DataFrame)
    assert hammer.trend_threshold == .03

    # Set init values
    trend_threshold = 0.1
    hammer = Hammer(data=mock_dataset, trend_threshold=trend_threshold)
    assert hammer.trend_threshold == trend_threshold

    # Test percent change computation
    pd.testing.assert_series_equal(hammer.trend, hammer.compute_relative_trend())
