# backtester/backtester.py
import numpy as np
import pandas as pd
from risk.risk import position_size, sl_tp_levels

def compute_metrics(equity):
    returns = pd.Series(equity).pct_change().fillna(0)
    total_return = equity[-1] / equity[0] - 1
    annual_return = (1 + total_return) ** (365.0 / len(equity)) - 1
    sharpe = returns.mean() / (returns.std() + 1e-9) * np.sqrt(365*24)
    peak = pd.Series(equity).cummax()
    drawdown = (pd.Series(equity) - peak) / peak
    max_dd = drawdown.min()
    return {'total_return': total_return, 'annual_return': annual_return, 'sharpe': sharpe, 'max_drawdown': max_dd}

def backtest(df, initial_balance=1000.0):
    balance = initial_balance
    position = 0.0
    entry_price = None
    stop_loss = None
    take_profit = None
    equity_curve = []

    for idx, row in df.iterrows():
        sig = int(row.get('position', 0))
        price = row['close']
        atr = row.get('ATR', 1.0)

        if sig == 1 and position == 0:
            units = position_size(balance, price, atr)
            position = units
            entry_price = price
            balance -= position * price
            stop_loss, take_profit = sl_tp_levels(entry_price, atr)

        if position > 0:
            if row['low'] <= stop_loss or row['high'] >= take_profit or sig == -1:
                exit_price = stop_loss if row['low'] <= stop_loss else (take_profit if row['high'] >= take_profit else price)
                balance += position * exit_price
                position = 0
                entry_price = None
                stop_loss = take_profit = None

        equity_curve.append(balance + position * price)

    df = df.copy()
    df['equity_curve'] = equity_curve
    metrics = compute_metrics(equity_curve)
    return df, metrics
