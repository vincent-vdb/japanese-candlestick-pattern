"""Engulfing test file"""
import pandas as pd

from patterns import Engulfing


def test_engulfing_init(mock_dataset):
    """Test the Engulfing init"""
    # Default Engulfing init
    engulfing = Engulfing(mock_dataset)
    assert isinstance(engulfing.data, pd.DataFrame)
    assert engulfing.trend_threshold == .03
    assert engulfing.stop_loss_shift == .02

    # Set init values
    trend_threshold = 0.1
    stop_loss_shift = 0.5
    engulfing = Engulfing(data=mock_dataset,
                          trend_threshold=trend_threshold,
                          stop_loss_shift=stop_loss_shift)
    assert engulfing.trend_threshold == trend_threshold
    assert engulfing.stop_loss_shift == stop_loss_shift

    # Test percent change computation
    pd.testing.assert_series_equal(engulfing.trend, engulfing.compute_relative_trend())
