"""LongleggedDoji test file"""
import pandas as pd

from patterns import LongleggedDoji


def test_longlegged_doji_init(mock_dataset):
    """Test the LongleggedDoji init"""
    # Default LongleggedDoji init
    ldoji = LongleggedDoji(mock_dataset)
    assert isinstance(ldoji.data, pd.DataFrame)
    assert ldoji.doji_threshold == .003
    assert ldoji.total_range_change_threshold == .02

    # Default doji_threshold set
    doji_threshold = 0.1
    total_range_change_threshold = 0.1
    ldoji = LongleggedDoji(data=mock_dataset,
                           doji_threshold=doji_threshold,
                           total_range_change_threshold=total_range_change_threshold)
    assert ldoji.doji_threshold == doji_threshold
    assert ldoji.total_range_change_threshold == total_range_change_threshold

    # Test percent change computation
    pd.testing.assert_series_equal(ldoji.total_range_percent_change,
                                   ldoji.compute_total_range_percent_change())
