# data/data_collector.py
import ccxt
import pandas as pd
from typing import Optional

def init_bitget(api_key=None, api_secret=None, password=None, testnet=False):
    exchange = ccxt.bitget({
        "apiKey": api_key,
        "secret": api_secret,
        "password": password,
    })
    if testnet:
        exchange.set_sandbox_mode(True)
    exchange.options["defaultType"] = "swap"
    return exchange

def fetch_ohlcv(exchange: ccxt.Exchange, symbol: str, timeframe: str = '15m', since: int = None, limit: int = 1000):
    """
    Fetch OHLCV and return a clean pandas DataFrame. Wrap errors so caller can handle missing symbols.
    """
    try:
        raw = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=limit)
        df = pd.DataFrame(raw, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].astype(float)
        return df
    except Exception as e:
        raise RuntimeError(f"Error fetching {symbol} {timeframe}: {e}")
