from notifier import Notifier

if __name__ == "__main__":
    # Define the params
    patterns = ['engulfing', 'harami',
                'hammer', 'hanging_man',
                'inverted_hammer', 'shooting_star',
                'three_black_crows', 'three_white_soldiers',
                'doji', 'dragonfly_doji', 'gravestone_doji', 'longlegged_doji']
    interval = '1m'
    pairs = ['BTCBUSD', 'ETHBUSD', 'BNBBUSD', 'ADABUSD', 'CAKEBUSD',
             'LTCBUSD', 'XRPBUSD', 'DOGEBUSD', 'DOTBUSD', 'SOLBUSD']
    binance_public_key = '2td0qxvKzpFokhECn2ekcgvJfpLeqSWqag9fTbooHh4xFTMs75J6eFqpWhE9Mh4V'
    binance_secret_key = 'I3a4sHzAF6gPhFfipFsLFaRSyS3KEEkP7M6Rp6fAtykQMKprojqhgRdg6Oknt3F4'
    # Instantiate the notifier
    notif = Notifier(binance_public_key,
                     binance_secret_key,
                     patterns,
                     interval,
                     pairs,
                     telegram_notif=False)
    # Run the notifier periodically
    notif.launch_scheduler()
