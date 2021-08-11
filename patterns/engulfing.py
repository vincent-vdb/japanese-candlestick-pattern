import numpy as np

from patterns.pattern import Pattern


class Engulfing(Pattern):
    def __init__(self, data):
        """Constructor of Engulfing class

        Parameters
        ----------
        data : pandas dataframe
            A pandas dataframe, expected to have at least the Open, High, Low, Close, Volume columns
        """
        super().__init__(data)

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
        - The higher the second candle volume, the higher the strength (not yet taken into account)engulfing.py

        Warning, this does not check the trend, which is a very important part of engulfing patterns!

        Returns
        -------
        self.data : pandas.DataFrame
            the input dataframe, with two new columns:
                - 'Engulfing' with bool
                - 'Engulfing_strength' that is either 0 (when no engulfing, see above),
                positive when bullish engulfing, negative when bearing engulfing
        """
        engulfing_strength = self.real_body / self.real_body.shift()
        engulfing = engulfing_strength < -1
        self.data['Engulfing'] = engulfing
        self.data['Engulfing_strength'] = np.abs(engulfing_strength) * engulfing * np.sign(self.real_body)

        return self.data
