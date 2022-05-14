"""Harami test file"""
import pandas as pd

from patterns import Harami


def test_harami_init(mock_dataset):
    """Test the Harami init"""
    # Default Harami init
    harami = Harami(mock_dataset)
    assert isinstance(harami.data, pd.DataFrame)
    assert harami.harami_threshold == 2.
    assert harami.percent_change_threshold == .03

    # Set init values
    harami_threshold = 1.5
    percent_change_threshold = .05
    harami = Harami(data=mock_dataset,
                    harami_threshold=harami_threshold,
                    percent_change_threshold=percent_change_threshold)
    assert harami.harami_threshold == harami_threshold
    assert harami.percent_change_threshold == percent_change_threshold

    # Test percent change computation
    pd.testing.assert_series_equal(harami.percent_change, harami.compute_percent_change())
