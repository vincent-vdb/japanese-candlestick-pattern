import numpy as np

from patterns.pattern import Pattern


class Doji(Pattern):
    def __init__(self, data, doji_threshold: float = .003):
        """Constructor of Doji class

        Parameters
        ----------
        data : pandas dataframe
            A pandas dataframe, expected to have at least the Open, High, Low, Close, Volume columns
        doji_threshold : float
            The maximum percentage change threshold below which to consider a candle a Harami.
            A value of 0.003 means a real body absolute relative change of maximum 0.3%.
        """
        super().__init__(data)
        self.doji_threshold = doji_threshold
        self.percent_change = self.compute_percent_change()

    def is_doji(self):
        """
        Returns True if a candlestick is a Doji. False otherwise.

        Returns
        -------
        pandas.Series
            A series of True or False, whether a candle is a doji or not.
        """
        doji_candle = np.abs((self.data.Close - self.data.Open) / self.data.Open) <= self.doji_threshold
        return doji_candle

    def compute_pattern(self):
        """
        Computes if a candlestick is a Doji.
        Condition is the following from Steve Nison:
        - Open and Close are almost the same value.

        Returns
        -------
        self.data : pandas.DataFrame
            the input dataframe, with two new columns:
                - 'doji' with bool

        """

        self.data['doji'] = self.is_doji()

        return self.data