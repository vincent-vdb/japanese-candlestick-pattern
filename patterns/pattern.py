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
        real_body : ndarray
            real body for each candlestick
        upper_shadow : ndarray
            upper shadow for each candlestick
        lower_shadow : ndarray
            lower shadow for each candlestick
        total_range : ndarray
            total range, from low to high, for each candlestick
        """

        real_body = np.abs(self.data.Open - self.data.Close)
        upper_shadow = np.minimum(self.data.High - self.data.Close, self.data.High - self.data.Open)
        lower_shadow = np.minimum(self.data.Close - self.data.Low, self.data.Open - self.data.Low)
        total_range = self.data.High - self.data.Close

        return real_body, upper_shadow, lower_shadow, total_range
