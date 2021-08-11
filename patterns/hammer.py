import numpy as np

from patterns.pattern import Pattern


class Hammer(Pattern):
    def __init__(self, data):
        """Constructor of Hammer class

        Parameters
        ----------
        data : pandas dataframe
            A pandas dataframe, expected to have at least the Open, High, Low, Close, Volume columns
        """
        super().__init__(data)

    def compute_pattern(self):
        """
        Computes if a candlestick is a Hammer (or Hanging man, since no trend is computed)

        Definition is following from Steve Nison:
        - Real body is on upper part (no matter the color)
        - Lower shadow should be at least two times the real body
        - No or really small upper shadow (actually quite same as condition 1)

        Returns
        -------
        self.data : pandas.DataFrame
            the input dataframe, with a new column 'Hammer' with bool
        """
        self.data['Hammer'] = np.logical_and(self.lower_shadow >= 2 * np.abs(self.real_body),
                                             self.upper_shadow <= 0.05 * self.total_range)

        return self.data
