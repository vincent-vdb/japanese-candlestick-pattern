import numpy as np
import pandas as pd

from patterns.pattern import Pattern


class ShootingStar(Pattern):
    def __init__(self, data: pd.DataFrame, trend_threshold: float = 0.03):
        """Constructor of ShootingStar class

        Parameters
        ----------
        data : pandas dataframe
            A pandas dataframe, expected to have at least the Open, High, Low, Close, Volume columns
        trend_threshold : float
            The relative threshold above which the trend is considered non neutral.
            e.g. with the default value of 0.03, there has to be a relative trend of
            at least 3% to be considered a Shooting star pattern.
            See Pattern documentation for relative trend computation details.
        """
        super().__init__(data)
        self.trend = self.compute_relative_trend()
        self.trend_threshold = trend_threshold

    def compute_pattern(self) -> pd.DataFrame:
        """
        Computes if a candlestick is a Shooting star

        Definition is following from Steve Nison:
        - Real body is on lower part (no matter the color)
        - Upper shadow should be at least two times the real body
        - No or really small lower shadow, here computed as at most 50% of real body height
        - In an upward/bullish trend

        Returns
        -------
        self.data : pandas.DataFrame
            the input dataframe, with a new column 'shooting_star' with bool
        """

        shooting_star = np.all([self.upper_shadow >= 2 * np.abs(self.real_body),
                                self.lower_shadow <= 0.5 * self.total_range,
                                self.trend >= self.trend_threshold],
                               axis=0)
        self.data['shooting_star'] = shooting_star

        return self.data
