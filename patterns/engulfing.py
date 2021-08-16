import numpy as np

from patterns.pattern import Pattern


class Engulfing(Pattern):
    def __init__(self, data, trend_threshold: float = 0.03):
        """Constructor of Engulfing class

        Parameters
        ----------
        data : pandas dataframe
            A pandas dataframe, expected to have at least the Open, High, Low, Close, Volume columns
        trend_threshold : float
            The absolute relative threshold above which the trend is considered non neutral.
            e.g. with the default value of 0.03, there has to be a relative trend of at least 3% to be considered.
            See Pattern documentation for relative trend computation details.
        """
        super().__init__(data)
        self.trend = self.compute_relative_trend()
        self.trend_threshold = trend_threshold

    def compute_pattern(self):
        """
        Computes if a candlestick is an engulfing.
        Conditions are the following from Steve Nison:
        - market should be in clear trend (either bullish or bearish): this condition won't be tested here
        - two adjacent candles of opposite color
        - the second candle is engulfing the first (since crypto is 24/7, we assume last close == current open,
        thus no need to check engulfing per se, just to test real body heights)

        Engulfing strength is computed according to the following rules of Nison:
        - The bigger the second candle real body, the higher the strength
        - The higher the second candle volume, the higher the strength (here computed relatively to first candle)

        Warning, this does not check the trend, which is a very important part of engulfing patterns!

        Returns
        -------
        self.data : pandas.DataFrame
            the input dataframe, with two new columns:
                - 'engulfing' with bool
                - 'engulfing_strength' that is either 0 (when no engulfing, see above),
                positive when bullish engulfing, negative when bearing engulfing
        """
        # Compute the volume ratio
        volume_ratio = self.data.Volume / self.data.Volume.shift()
        # Compute the candle ratio
        candle_ratio = (self.real_body / self.real_body.shift())
        # Three conditions to meet for engulfing to True:
        # - If candle ratio < -1, meaning this is an engulfing candle
        # - If the trend is in opposite direction of last candle real body
        # - If the trend is above the threshold, to make sure there is an actual trend
        engulfing = np.all([candle_ratio < -1,
                            self.trend * self.real_body < 0,
                            np.abs(self.trend) > self.trend_threshold],
                           axis=0)
        # Compute the engulfing strength: candle ratio times volume ratio
        engulfing_strength = volume_ratio * candle_ratio
        # Log those values in the data
        self.data['engulfing'] = engulfing
        self.data['engulfing_strength'] = np.abs(engulfing_strength) * engulfing * np.sign(self.real_body)

        return self.data
