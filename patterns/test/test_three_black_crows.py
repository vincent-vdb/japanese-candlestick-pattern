import pytest
import pandas as pd

from patterns import ThreeBlackCrows

@pytest.fixture
def mock_dataset():
    """Return a mock dataframe as pattern input"""
    return pd.read_csv('patterns/test/mock_dataframe_input.csv')

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
