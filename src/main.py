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
    binance_public_key = #Add binance public key here
    binance_secret_key = #Add binance private key here
    # Instantiate the notifier
    notif = Notifier(binance_public_key, binance_secret_key, patterns, interval, pairs, telegram_notif=True)
    # Run the notifier periodically
    notif.launch_scheduler()

