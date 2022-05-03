import numpy as np


class Hurst:
    def __init__(self, data, lag: int = 20):
        """Constructor of Pattern class

        Parameters
        ----------
        data : pandas dataframe
            A pandas dataframe, expected to have at least the Open, High, Low, Close, Volume columns

        """
        self.data = data
        self.lag = lag

    def compute_value(self):
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

        # interpretation of return value
        # hurst < 0.5 - input_ts is mean reverting
        # hurst = 0.5 - input_ts is effectively random/geometric brownian motion
        # hurst > 0.5 - input_ts is trending
        tau = []
        lagvec = []
        #  Step through the different lags
        for lag in range(2, self.lag):
            #  produce price difference with lag
            pp = np.subtract(self.data[lag:].values, self.data[:-lag].values)
            #  Write the different lags into a vector
            lagvec.append(lag)
            #  Calculate the variance of the difference vector
            tau.append(np.sqrt(np.std(pp)))
            #  linear fit to double-log graph (gives power)
        m = np.polyfit(np.log10(lagvec), np.log10(tau), 1)
        # calculate hurst
        hurst = m[0] * 2
        print(hurst)
        return hurst


