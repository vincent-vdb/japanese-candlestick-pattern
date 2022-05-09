![Pylint](https://github.com/vincent-vdb/japanese-candlestick-pattern/actions/workflows/pylint.yml/badge.svg)
![pytest](https://github.com/vincent-vdb/japanese-candlestick-pattern/actions/workflows/python-package.yml/badge.svg)
# japanese-candlestick-pattern

# Install
`pip install japanese-candlestick` 

# Usage

Assuming having a pandas DataFrame `candles` with the following columns:
- `'Open'`
- `'High`
- `'Low'`
- `'Close'`

One can compute the japanese candlestick pattern Engulfing as follow:
```python
from patterns import Engulfing

# Instantiate the pattern, with the candles dataframe as arg
engulfing = Engulfing(candles)

# Perform pattern detection
output_df = engulfing.compute_pattern()
```
The pattern detection value (a bool) is stored in a column having the same name as the pattern (lower case).
In above example, the results would be in `output_df['engulfing']`.

# Available patterns

The patterns are computed based on the book 'Japanese Candlestick Charting Techniques', by Steve Nison.

The currently available patterns are the following:
- Doji
- DragonflyDoji
- Engulfing
- GraveswtoneDoji
- Hammer
- HangingMan
- Harami
- InvertedHammer
- LongleggedDoji
- ShootingStar
- ThreeWhiteSoldiers
- ThreeBlackCrows

They are all to be imported from `patterns`, and all with the same usage (and sometimes parameters), i.e.:

```python
# First import
from patterns import Hammer
# Then instantiate
hammer = Hammer(candles)
# Finally compute detection
output_df = hammer.compute_pattern()
```

# Additional

One can make a telegram bot and configure telegram-send using 
[this tuto](https://medium.com/@robertbracco1/how-to-write-a-telegram-bot-to-send-messages-with-python-bcdf45d0a580).

