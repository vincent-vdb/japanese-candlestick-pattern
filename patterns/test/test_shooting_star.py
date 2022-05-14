"""ShootingStar test file"""
import pandas as pd

from patterns import ShootingStar


def test_shooting_star_init(mock_dataset):
    """Test the ShootingStar init"""
    # Default ShootingStar init
    star = ShootingStar(mock_dataset)
    assert isinstance(star.data, pd.DataFrame)
    assert star.trend_threshold == .03

    # Set init values
    trend_threshold = 0.1
    star = ShootingStar(data=mock_dataset, trend_threshold=trend_threshold)
    assert star.trend_threshold == trend_threshold

    # Test percent change computation
    pd.testing.assert_series_equal(star.trend, star.compute_relative_trend())
