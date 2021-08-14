import numpy as np

from patterns.pattern import Pattern


class Harami(Pattern):
    def __init__(self, data, harami_threshold: float = 2.):
        """Constructor of Harami class

        Parameters
        ----------
        data : pandas dataframe
            A pandas dataframe, expected to have at least the Open, High, Low, Close, Volume columns
        harami_threshold : float
            The minimum ratio between a previous long and current short candle to consider it a Harami
        """
        super().__init__(data)
        self.harami_threshold = harami_threshold

    def compute_pattern(self):
        """
        Computes if a candlestick is a Harami.
        Conditions are the following from Steve Nison:
        - two adjacent candles, the first with long real body, the second
        with short real body (e.g. at least 2 times shorter than the first one)
        - the two candles do not necessarily opposite colors, but have to in crypto (since 24/7 and almost no gaps)

        Harami strength is computed according to the following rule of Nison:
        - The smaller the second candle real body, the higher the strength (best case, cross harami with doji)

        Returns
        -------
        self.data : pandas.DataFrame
            the input dataframe, with two new columns:
                - 'harami' with bool
                - 'harami_strength' that is either 0 (when no engulfing, see above),
                positive when bullish engulfing, negative when bearing engulfing
        """
        harami_strength = self.real_body.shift() / self.real_body
        harami = harami_strength < -self.harami_threshold
        self.data['harami'] = harami
        self.data['harami_strength'] = np.abs(harami_strength) * harami * np.sign(self.real_body)

        return self.data
