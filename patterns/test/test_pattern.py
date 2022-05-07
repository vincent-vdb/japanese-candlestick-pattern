import sys
sys.path.append('japanese_candlestick_pattern')

import pytest
import numpy as np
import pandas as pd

from patterns.pattern import Pattern

@pytest.fixture
def mock_dataset():
    """Return a mock dataframe as pattern input"""
    return pd.read_csv('patterns/test/mock_dataframe_input.csv')


def test_pattern_init(mock_dataset):
    """Test the Pattern init"""
    pattern = Pattern(mock_dataset)

    assert isinstance(pattern.data, pd.DataFrame)
    pd.testing.assert_frame_equal(mock_dataset, pattern.data)


def test_compute_characteristics(mock_dataset):
    """Test the Pattern compute_characteristics method"""
    pattern = Pattern(mock_dataset)

    real_body, upper_shadow, lower_shadow, total_range = pattern.compute_characteristics()

    # Test real_body
    real_body_gt = pattern.data.Close - pattern.data.Open
    pd.testing.assert_series_equal(real_body_gt, real_body)

    # Test upper_shadow
    upper_shadow_gt = np.minimum(pattern.data.High - pattern.data.Close,
                                 pattern.data.High - pattern.data.Open)
    pd.testing.assert_series_equal(upper_shadow_gt, upper_shadow)

    # Test lower_shadow
    lower_shadow_gt = np.minimum(pattern.data.Close - pattern.data.Low,
                                 pattern.data.Open - pattern.data.Low)
    pd.testing.assert_series_equal(lower_shadow_gt, lower_shadow)

    # Test total_range
    total_range_gt = pattern.data.High - pattern.data.Low
    pd.testing.assert_series_equal(total_range_gt, total_range)


def test_compute_total_range_percent_change(mock_dataset):
    """Test the Pattern compute_total_range_percent_change method"""
    pattern = Pattern(mock_dataset)

    tot_range_pct_change = pattern.compute_total_range_percent_change()
    tot_range_pct_change_gt = (pattern.data.High - pattern.data.Low) / pattern.data.Low

    pd.testing.assert_series_equal(tot_range_pct_change_gt, tot_range_pct_change)


def test_compute_percent_change(mock_dataset):
    """Test the Pattern compute_percent_change method"""
    pattern = Pattern(mock_dataset)

    pct_change = pattern.compute_percent_change()
    pct_change_gt = (pattern.data.Close - pattern.data.Open) / pattern.data.Open

    pd.testing.assert_series_equal(pct_change_gt, pct_change)


def test_compute_relative_trend(mock_dataset):
    """Test the Pattern compute_relative_trend method"""
    pattern = Pattern(mock_dataset)

    # Default relative trend lookback test
    relative_trend = pattern.compute_relative_trend()
    average = 0.5 * (pattern.data.Close + pattern.data.Open)
    trend_lookback = 5
    relative_trend_gt = (average - average.shift(trend_lookback)) / average

    pd.testing.assert_series_equal(relative_trend_gt, relative_trend)

    # Set value relative trend lookback test
    trend_lookback = 10
    relative_trend = pattern.compute_relative_trend(trend_lookback=trend_lookback)
    average = 0.5 * (pattern.data.Close + pattern.data.Open)
    relative_trend_gt = (average - average.shift(trend_lookback)) / average

    pd.testing.assert_series_equal(relative_trend_gt, relative_trend)
