import numpy as np


class Pattern:
    def __init__(self, data):
        """Constructor of Pattern class

        Parameters
        ----------
        data : pandas dataframe
            A pandas dataframe, expected to have at least the Open, High, Low, Close, Volume columns

        """
        self.data = data
        self.real_body, self.upper_shadow, self.lower_shadow, self.total_range = self.compute_characteristics()

    def compute_characteristics(self):
        """Computes the following characteristics of candlesticks:
        - real body
        - upper shadow
        - lower shadow
        - total range

        Returns
        -------
        real_body : pandas.Series
            real body for each candlestick, can be either positive or negative
        upper_shadow : pandas.Series
            upper shadow for each candlestick
        lower_shadow : pandas.Series
            lower shadow for each candlestick
        total_range : pandas.Series
            total range, from low to high, for each candlestick
        """

        real_body = self.data.Close - self.data.Open
        upper_shadow = np.minimum(self.data.High - self.data.Close, self.data.High - self.data.Open)
        lower_shadow = np.minimum(self.data.Close - self.data.Low, self.data.Open - self.data.Low)
        total_range = self.data.High - self.data.Close

        return real_body, upper_shadow, lower_shadow, total_range
