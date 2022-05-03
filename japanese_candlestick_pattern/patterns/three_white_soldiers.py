"""ThreeWhiteSoldiers class file"""
import numpy as np
import pandas as pd

from patterns.pattern import Pattern


class ThreeWhiteSoldiers(Pattern):
    """ThreeWhiteSoldiers class"""

    def __init__(self, data: pd.DataFrame, upper_shadow_threshold: float = 0.5):
        """Constructor of ThreeWhiteSoldiers class

        Parameters
        ----------
        data : pandas dataframe
            A pandas dataframe expected to have at least the Open, High, Low, Close, Volume columns
        upper_shadow_threshold : float
            The threshold ratio above which the upper shadow is not small enough
        """
        super().__init__(data)
        self.upper_shadow_threshold = upper_shadow_threshold

    def compute_pattern(self) -> pd.DataFrame:
        """
        Computes if a candlestick is a three white soldiers patterns.
        Conditions are the following from Steve Nison:
        - three positive candles, with tall real body
        - short or no upper shadow (threshold if 50% of real body by default,
        quite high but can be adjusted)
        - ideally, open of candles 2 and 3 is inside the real body of the previous one,
        but won't happen much in crypto

        Returns
        -------
        self.data : pandas.DataFrame
            the input dataframe, with two new columns:
                - 'three_white_soldiers' with bool
        """
        # Three positive candles in a row
        three_positive = np.all([self.real_body > 0,
                                 self.real_body.shift() > 0,
                                 self.real_body.shift(2) > 0],
                                axis=0)
        # Three short upper shadows in a row
        upper_shadows = np.all([self.upper_shadow / self.real_body < self.upper_shadow_threshold,
                                self.upper_shadow.shift() / self.real_body.shift() <
                                self.upper_shadow_threshold,
                                self.upper_shadow.shift(2) / self.real_body.shift(2) <
                                self.upper_shadow_threshold],
                               axis=0)

        self.data['three_white_soldiers'] = np.logical_and(three_positive, upper_shadows)

        return self.data
