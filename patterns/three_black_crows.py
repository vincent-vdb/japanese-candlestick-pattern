"""ThreeBlackCrows class file"""
import numpy as np
import pandas as pd

from patterns.pattern import Pattern


class ThreeBlackCrows(Pattern):
    """ThreeBlackCrows class file"""

    def __init__(self, data: pd.DataFrame, lower_shadow_threshold: float = 0.5):
        """Constructor of ThreeBlackCrows class

        Parameters
        ----------
        data : pandas dataframe
            A pandas dataframe expected to have at least the Open, High, Low, Close, Volume columns
        lower_shadow_threshold : float
            The threshold ratio above which the lower shadow is not small enough
        """
        super().__init__(data)
        self.lower_shadow_threshold = lower_shadow_threshold

    def compute_pattern(self) -> pd.DataFrame:
        """
        Computes if a candlestick is a three white soldiers patterns.
        Conditions are the following from Steve Nison:
        - three negative candles, with tall real body
        - short or no lower shadow (threshold if 80% of real body by default,
        quite high but can be adjusted)
        - ideally, open of candles 2 and 3 is inside the real body of the previous one,
        but won't happen much in crypto

        Returns
        -------
        self.data : pandas.DataFrame
            the input dataframe, with two new columns:
                - 'three_black_crows' with bool
        """
        # Three positive candles in a row
        three_negative = np.all([self.real_body < 0,
                                 self.real_body.shift() < 0,
                                 self.real_body.shift(2) < 0],
                                axis=0)
        # Three short lower shadows in a row
        lower_shadows = np.all([self.lower_shadow / np.abs(self.real_body) <
                                self.lower_shadow_threshold,
                                self.lower_shadow.shift() / np.abs(self.real_body.shift()) <
                                self.lower_shadow_threshold,
                                self.lower_shadow.shift(2) / np.abs(self.real_body.shift(2)) <
                                self.lower_shadow_threshold],
                               axis=0)

        self.data['three_black_crows'] = np.logical_and(three_negative, lower_shadows)

        return self.data
