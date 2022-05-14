"""ThreeWhiteSoldiers test file"""
import pandas as pd

from patterns import ThreeWhiteSoldiers


def test_three_white_soldiers_init(mock_dataset):
    """Test the ThreeWhiteSoldiers init"""
    # Default ThreeWhiteSoldiers init
    soldiers = ThreeWhiteSoldiers(mock_dataset)
    assert isinstance(soldiers.data, pd.DataFrame)
    assert soldiers.upper_shadow_threshold == .5

    # Set init values
    upper_shadow_threshold = 0.1
    soldiers = ThreeWhiteSoldiers(data=mock_dataset, upper_shadow_threshold=upper_shadow_threshold)
    assert soldiers.upper_shadow_threshold == upper_shadow_threshold
