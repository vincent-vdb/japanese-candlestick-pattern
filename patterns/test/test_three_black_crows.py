"""ThreeBlackCrows test file"""
import pandas as pd

from patterns import ThreeBlackCrows


def test_three_black_crows_init(mock_dataset):
    """Test the ThreeBlackCrows init"""
    # Default ThreeBlackCrows init
    crows = ThreeBlackCrows(mock_dataset)
    assert isinstance(crows.data, pd.DataFrame)
    assert crows.lower_shadow_threshold == .5

    # Set init values
    lower_shadow_threshold = 0.1
    crows = ThreeBlackCrows(data=mock_dataset, lower_shadow_threshold=lower_shadow_threshold)
    assert crows.lower_shadow_threshold == lower_shadow_threshold
