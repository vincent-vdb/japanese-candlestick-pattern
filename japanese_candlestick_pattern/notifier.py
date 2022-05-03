import time

import numpy as np
import pandas as pd
from binance.client import Client
import telegram_send
import schedule  # first time pip install schedule

from patterns.hammer import Hammer
from patterns.hanging_man import HangingMan
from patterns.inverted_hammer import InvertedHammer
from patterns.shooting_star import ShootingStar
from patterns.engulfing import Engulfing
from patterns.harami import Harami
from patterns.three_white_soldiers import ThreeWhiteSoldiers
from patterns.three_black_crows import ThreeBlackCrows
from patterns.doji import Doji
from patterns.dragonfly_doji import DragonflyDoji
from patterns.gravestone_doji import GravestoneDoji
from patterns.longlegged_doji import LongleggedDoji

implemented_patterns = {'engulfing': Engulfing,
                        'hammer': Hammer,
                        'hanging_man': HangingMan,
                        'inverted_hammer': InvertedHammer,
                        'shooting_star': ShootingStar,
                        'harami': Harami,
                        'three_black_crows': ThreeBlackCrows,
                        'three_white_soldiers': ThreeWhiteSoldiers,
                        'doji': Doji,
                        'dragonfly_doji': DragonflyDoji,
                        'gravestone_doji': GravestoneDoji,
                        'longlegged_doji': LongleggedDoji}


class Notifier:
    """Notifier class"""
    def __init__(self,
                 binance_public_key: str,
                 binance_secret_key: str,
                 patterns: list,
                 interval: str = '1d',
                 pairs: list = ['BTCBUSD'],
                 telegram_notif: bool = True):
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
        telegram_notif : bool
            If True, the notif will be output to telegram.
            If False, the notif is on standard output.
        """
        self.client = Client(binance_public_key, binance_secret_key)
        self.patterns = patterns
        self.interval = interval
        self.pairs = pairs
        self.telegram_notif = telegram_notif

    def detect_patterns(self) -> None:
        """
        Methods that detects patterns for the given pairs and given interval in the constructor.
        """
        # Loop over all the pairs, get the history candles, detect the patterns
        for pair in self.pairs:
            # Get 5 + 1 times the interval of history
            history = int(self.interval[:-1]) * 7
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
            # Remove the last line, since this is the current (and unfinished) candle
            candles = candles.iloc[:-1]
            # Detect the patterns
            for pattern in self.patterns:
                if pattern in implemented_patterns.keys():
                    # Instantiate the pattern
                    pat = implemented_patterns[pattern](candles)
                    # Compute the pattern detection
                    candles = pat.compute_pattern()
                    # Check if the pattern is detected
                    if candles.iloc[-1][pattern]:
                        message = pattern + ' pattern detected for ' + pair + ' | interval ' + self.interval
                        if pattern + '_strength' in candles.columns:
                            strength = '\n with strength: ' + "{:.2f}".format(candles.iloc[-1][pattern + '_strength'])
                            message = message + strength
                        if pattern + '_stop_loss' in candles.columns:
                            message = message + '\n stop loss: ' + str(candles.iloc[-1][pattern + '_stop_loss'])
                        # Send the notif
                        if self.telegram_notif:
                            telegram_send.send(messages=[message])
                        else:
                            print(message)

    def launch_scheduler(self) -> None:
        """
        Methods automatically launches the self.detect_patterns() method at the right time.
        e.g. for a 4 hours interval, the pattern detection will be launched every 4 hours.
        """
        # Get the interval information
        time_number = int(self.interval[:-1])
        time_unit = self.interval[-1]

        if time_unit == 'm':
            # In case of minutes, to be sure it launches at minutes:
            # 0, interval, 2*interval...60-interval of every hour
            # Loop over all the minutes you want it to be launched
            for i in np.arange(0, 60, time_number):
                minute_time = str(i)
                if len(minute_time) == 1:
                    minute_time = '0' + minute_time
                minute_time = minute_time + ':01'
                schedule.every(1).hours.at(minute_time).do(self.detect_patterns)
        elif time_unit == 'h':
            # Same as minutes, for example with interval 4h to be sure it launches at
            # 0:00, 4:00, 8:00, 12:00, 16:00, 20:00
            # Make a loop on all those hours
            for i in np.arange(0, 24, time_number):
                hour_time = str(i)
                if len(hour_time) == 1:
                    hour_time = '0' + hour_time
                hour_time = hour_time + ':00:10'
                schedule.every(1).days.at(hour_time).do(self.detect_patterns)
        elif time_unit == 'd':
            schedule.every(time_number).days.at("00:01:00").do(self.detect_patterns)
        elif time_unit == 'w':
            schedule.every(time_number).monday.at("00:01").do(self.detect_patterns)

        # Put the scheduling in a infinite loop
        while True:
            schedule.run_pending()
            time.sleep(1)
