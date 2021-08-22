import numpy as np

from patterns.doji import Doji


class GravestoneDoji(Doji):
    def __init__(self, data, doji_threshold: float = .003, total_range_change_threshold: float = 0.02):
        """Constructor of GravestoneDoji class

        Parameters
        ----------
        data : pandas dataframe
            A pandas dataframe, expected to have at least the Open, High, Low, Close, Volume columns
        doji_threshold : float
            The maximum percentage change threshold below which to consider a candle a Harami.
            A value of 0.003 means a real body absolute relative change of maximum 0.3%.
        """
        super().__init__(data, doji_threshold)
        self.total_range_change_threshold = total_range_change_threshold
        self.total_range_percent_change = self.compute_total_range_percent_change()

    def compute_pattern(self):
        """
        Computes if a candlestick is a gravestone doji.
        Condition is the following from Steve Nison:
        - Open and Close are almost the same value (regular doji condition)
        - Long upper shadow
        - No or very small lower shadow

        Since the long upper shadow and small lower shadow are not perfectly explicit,
        it is proposed to be computed the following way:
        - A total range above a given threshold, e.g. 2%
        - An upper shadow of at least 90% of the total range

        Returns
        -------
        self.data : pandas.DataFrame
            the input dataframe, with two new columns:
                - 'gravestone_doji' with bool

        """
        gravestone_doji = np.all([self.is_doji(),
                                  self.upper_shadow > 0.8 * self.total_range,
                                  np.abs(self.total_range_percent_change) > self.total_range_change_threshold],

                                 axis=0)
        self.data['upper'] = self.upper_shadow
        self.data['total_range'] = self.total_range
        self.data['gravestone_doji'] = gravestone_doji

        return self.data