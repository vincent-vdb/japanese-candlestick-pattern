import sys
sys.path.append('..')

import pandas as pd
from binance.client import Client

from patterns.hammer import Hammer
from patterns.engulfing import Engulfing
from patterns.harami import Harami
from patterns.three_white_soldiers import ThreeWhiteSoldiers
from patterns.three_black_crows import ThreeBlackCrows

implemented_patterns = {'engulfing': Engulfing,
                        'hammer': Hammer,
                        'harami': Harami,
                        'three_black_crows': ThreeBlackCrows,
                        'three_white_soldiers': ThreeWhiteSoldiers}


class Notifier:
    def __init__(self, binance_public_key: str, binance_secret_key: str,
                 patterns: list, interval: str = '1d', pairs: str = ['BTCBUSD']):
        """
        Constructor of the Notifier

        Parameters
        ----------
        binance_public_key : str
            binance public API key with rights to read
        binance_secret_key : str
            binance secret API key associated to the public key
        patterns : list of str
            List of patterns to get notifications from, among the following:
                engulfing, hammer, harami, three_black_crows, three_white_soldiers
        interval : str
            One of the following 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M.
            Defaults to 1d for 1 day
        pairs : list or str
            An example would be ['BNBBTC', 'BTCBUSD'] for a BNB/BTC and a BTC/BUSD pairs
            Default is ['BTCBUSD'] for the BTC to USD pair.
        """
        self.client = Client(binance_public_key, binance_secret_key)
        self.patterns = patterns
        self.interval = interval
        self.pairs = pairs

    def detect_patterns(self):
        """
        Methods that detects patterns for the given pairs and given interval in the constructor.
        """
        # Loop over all the pairs, get the history candles, detect the patterns
        for pair in self.pairs:
            # Get 5 times the interval of history
            history = int(self.interval[:-1]) * 5
            unit = ' day' if self.interval[-1] == 'd' else self.interval[-1]
            history = str(history) + unit + ' ago UTC'
            # Get the candles
            candles = self.client.get_historical_klines(pair, self.interval, history)
            # Reformat the data to a dataframe
            candles = pd.DataFrame(candles,
                                   columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume',
                                            'Close time', 'Quote asset volume', 'Number of trades',
                                            'Taker buy base vol', 'Taker buy quote vol', 'Ignore'],
                                   dtype=float)
            # Detect the patterns
            for pattern in self.patterns:
                if pattern in implemented_patterns.keys():
                    # Instantiate the pattern
                    pat = implemented_patterns[pattern](candles)
                    # Compute the pattern detection
                    candles = pat.compute_pattern()
                    # Check if the pattern is detected
                    if candles.iloc[-1][pattern]:
                        print('pattern', pattern, 'detected for', pair)
                        if pattern + '_strength' in candles.columns:
                            print('\t with strength:', candles.iloc[-1][pattern + '_strength'])
