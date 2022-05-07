"""Harami class file"""
import numpy as np
import pandas as pd

from patterns.pattern import Pattern


class Harami(Pattern):
    """Harami class"""

    def __init__(self,
                 data: pd.DataFrame,
                 harami_threshold: float = 2.,
                 percent_change_threshold: float = 0.03):
        """Constructor of Harami class

        Parameters
        ----------
        data : pandas dataframe
            A pandas dataframe expected to have at least the Open, High, Low, Close, Volume columns
        harami_threshold : float
            The minimum ratio between a previous long and current
            short candle to consider it a Harami.
            A value of 2 means we expect the long candle's
            real body to be twice larger then second candle.
        percent_change_threshold : float
            The minimum percent change of the first candle in the Harami pattern.
            e.g. with the default value of 0.03, the first candle has to have a 3% change
            at least to be considered a Harami pattern.
        """
        super().__init__(data)
        self.harami_threshold = harami_threshold
        self.percent_change = self.compute_percent_change()
        self.percent_change_threshold = percent_change_threshold

    def compute_pattern(self) -> pd.DataFrame:
        """
        Computes if a candlestick is a Harami.
        Conditions are the following from Steve Nison:
        - two adjacent candles, the first with long real body (a large percentage change),
         the second with short real body (e.g. at least 2 times shorter than the first one)
        - the two candles do not necessarily have opposite colors, but have to in crypto
        (since 24/7 and almost no gaps)

        Harami strength is computed according to the following rule of Nison:
        - The smaller the second candle real body, the higher the strength
        (best case, cross harami with doji)

        Returns
        -------
        self.data : pandas.DataFrame
            the input dataframe, with two new columns:
                - 'harami' with bool
                - 'harami_strength' that is either 0 (when no engulfing, see above),
                positive when bullish engulfing, negative when bearing engulfing
        """
        harami_strength = self.real_body.shift() / self.real_body
        harami = np.all([np.abs(harami_strength) >= self.harami_threshold,
                         harami_strength < 0,# to make sure the candles are in opposite directions
                         np.abs(self.percent_change.shift()) >= self.percent_change_threshold],
                        axis=0)
        self.data['harami'] = harami
        self.data['harami_strength'] = np.abs(harami_strength) * harami * np.sign(self.real_body)

        return self.data
