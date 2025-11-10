# strategies/strategies.py
import pandas as pd
import ta

def ema_rsi_macd(df: pd.DataFrame, short=8, long=21, rsi_period=14, macd_fast=12, macd_slow=26, macd_signal=9):
    df = df.copy()
    # Trend filter: long-term EMAs (200) and mid-term EMA (50) for trend strength
    df['EMA_long_term'] = df['close'].ewm(span=200, adjust=False).mean()
    df['EMA50'] = df['close'].ewm(span=50, adjust=False).mean()   # used for optional trend checks
    df['EMA_short'] = df['close'].ewm(span=short, adjust=False).mean()
    df['EMA_long'] = df['close'].ewm(span=long, adjust=False).mean()

    # Momentum indicators
    df['RSI'] = ta.momentum.RSIIndicator(df['close'], window=rsi_period).rsi()
    macd = ta.trend.MACD(df['close'], window_slow=macd_slow, window_fast=macd_fast, window_sign=macd_signal)
    df['MACD'] = macd.macd()
    df['MACD_signal'] = macd.macd_signal()

    # default signal 0 (neutral)
    df['signal'] = 0

    buy = (
        (df['close'] > df['EMA_long_term']) &
        (df['EMA_short'] > df['EMA_long']) &
        (df['RSI'] < 65) &
        (df['MACD'] > df['MACD_signal'])
    )
    sell = (
        (df['close'] < df['EMA_long_term']) &
        (df['EMA_short'] < df['EMA_long']) &
        (df['RSI'] > 35) &
        (df['MACD'] < df['MACD_signal'])
    )

    df.loc[buy, 'signal'] = 1
    df.loc[sell, 'signal'] = -1

    # position marks entry/exit: 1 = entry long, -1 = entry short, 0 = nothing
    df['position'] = df['signal'].diff().fillna(0).astype(int)
    return df
