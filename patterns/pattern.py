"""Pattern class file"""
from typing import Tuple

import numpy as np
import pandas as pd


class Pattern:
    """Pattern class"""

    def __init__(self, data: pd.DataFrame):
        """Constructor of Pattern class

        Parameters
        ----------
        data : pandas dataframe
            A pandas dataframe expected to have at least the Open, High, Low, Close, Volume columns
        """
        self.data = data
        self.real_body, \
        self.upper_shadow, \
        self.lower_shadow, \
        self.total_range = self.compute_characteristics()

    def compute_characteristics(self) -> Tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
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
        upper_shadow = np.minimum(self.data.High - self.data.Close,
                                  self.data.High - self.data.Open)
        upper_shadow = pd.Series(upper_shadow, index=self.data.High.index)
        lower_shadow = np.minimum(self.data.Close - self.data.Low,
                                  self.data.Open - self.data.Low)
        lower_shadow = pd.Series(lower_shadow, index=self.data.High.index)
        total_range = self.data.High - self.data.Low

        return real_body, upper_shadow, lower_shadow, total_range

    def compute_total_range_percent_change(self) -> pd.Series:
        """Computes the total range percentage of change per candle.
        Meaning, the computation of (High - Low)/Low.

        Returns
        -------
        change : float
            The total range percentage change per candle
        """
        return (self.data.High - self.data.Low) / self.data.Low

    def compute_percent_change(self) -> pd.Series:
        """Computes the percentage of change per candle.
        Meaning, the computation of (Close - Open)/Open.

        Returns
        -------
        change : float
            The percentage change per candle
        """
        return (self.data.Close - self.data.Open) / self.data.Open

    def compute_relative_trend(self, trend_lookback: int = 5) -> pd.Series:
        """Computes the relative trend: upward or downward, in the trend_lookback period
        The trend is relative in the way it is divided by the value at trend_lookback, thus
        providing a relative increasing or decreasing trend.
        For example, if the average price increases from 100 to 110 in trend_lookback periods, the
        output trend would be (110-100)/100 = 0.1

        Parameters
        ----------
        trend_lookback : int
            Number of time intervals to consider for computing the trend.
            Defaults to 5.
        Returns
        -------
        trend : float
            A trend value:
            - A large positive value for upward/bullish trend
            - A large negative value for downward/bearish trend
            - A close to zero value for a neutral trend
        """
        # Compute the average value between Close and Open
        average = 0.5 * (self.data.Close + self.data.Open)
        # Compute the trend as the diff between those values
        trend = (average - average.shift(trend_lookback)) / average

        return trend
