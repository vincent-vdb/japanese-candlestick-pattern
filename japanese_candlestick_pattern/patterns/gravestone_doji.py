"""GravestoneDoji class file"""
import numpy as np
import pandas as pd

from patterns.doji import Doji


class GravestoneDoji(Doji):
    """GravestoneDoji class"""

    def __init__(self,
                 data: pd.DataFrame,
                 doji_threshold: float = .003,
                 total_range_change_threshold: float = 0.02):
        """Constructor of GravestoneDoji class

        Parameters
        ----------
        data : pandas dataframe
            A pandas dataframe expected to have at least the Open, High, Low, Close, Volume columns
        doji_threshold : float
            The maximum percentage change threshold below which to consider a candle a Doji.
            A value of 0.003 means a real body absolute relative change of maximum 0.3%.
        total_range_change_threshold : float
            The minimum total range threshold above which to consider a candle a gravestone doji.
            A value of 0.02 means a total candle range (High - Low) absolute
            relative change of minimum 2%.
        """
        super().__init__(data, doji_threshold)
        self.total_range_change_threshold = total_range_change_threshold
        self.total_range_percent_change = self.compute_total_range_percent_change()

    def compute_pattern(self) -> pd.DataFrame:
        """
        Computes if a candlestick is a gravestone doji.
        Condition is the following from Steve Nison:
        - Open and Close are almost the same value (regular doji condition)
        - Long upper shadow
        - No or very small lower shadow

        Since the long upper shadow and small lower shadow are not perfectly explicit,
        it is proposed to be computed the following way:
        - A total range above a given threshold, e.g. 2%
        - An upper shadow of at least 80% of the total range

        Returns
        -------
        self.data : pandas.DataFrame
            the input dataframe, with two new columns:
                - 'gravestone_doji' with bool

        """
        gravestone_doji = np.all([self.is_doji(),
                                  self.upper_shadow > 0.8 * self.total_range,
                                  np.abs(self.total_range_percent_change) >
                                  self.total_range_change_threshold],
                                 axis=0)
        self.data['gravestone_doji'] = gravestone_doji

        return self.data
