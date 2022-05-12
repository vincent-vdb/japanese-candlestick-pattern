"""COnfiguration of test file"""
import pytest
import pandas as pd

@pytest.fixture(scope='module')
def mock_dataset():
    """Return a mock dataframe as pattern input"""
    return pd.read_csv('patterns/test/mock_dataframe_input.csv')
