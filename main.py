# main.py
import ccxt
import pandas as pd
import ta
from strategies.strategies import ema_rsi_macd
from data.data_collector import init_bitget, fetch_ohlcv
from paper_trader.paper_bot import PaperBroker
from config import BITGET_API_KEY, BITGET_API_SECRET, BITGET_PASSWORD, INITIAL_BALANCE
from alerts.telegram_alerts import send_alert, log_trade
from datetime import datetime
import time

SYMBOL = "SOL/USDT"   # default pair
TIMEFRAMES = ["4h", "1d"]   # user requested
LIMIT = 2000

LEVERAGE = 5.0
RISK_PCT = 0.01

exchange = init_bitget(BITGET_API_KEY, BITGET_API_SECRET, BITGET_PASSWORD, testnet=True)
exchange.options["defaultType"] = "swap"

def rolling_stats(equity_curve):
    if len(equity_curve) < 2:
        return 0.0, 0.0, 0.0
    returns = pd.Series(equity_curve).pct_change().fillna(0)
    total_return = (equity_curve[-1] / equity_curve[0] - 1) * 100
    win_rate = (returns > 0).sum() / len(returns) * 100 if len(returns) else 0.0
    max_dd = ((pd.Series(equity_curve).cummax() - pd.Series(equity_curve)) / pd.Series(equity_curve).cummax()).max() * 100
    return total_return, win_rate, max_dd

for tf in TIMEFRAMES:
    try:
        df = fetch_ohlcv(exchange, SYMBOL, timeframe=tf, limit=LIMIT)
    except Exception as e:
        print(f"Error fetching {SYMBOL} {tf}: {e}")
        continue

    df = ema_rsi_macd(df)
    df['ATR'] = ta.volatility.AverageTrueRange(df['high'], df['low'], df['close'], window=14).average_true_range()
    # use recommended ffill to avoid FutureWarning
    df['ATR'] = df['ATR'].ffill().fillna(0.0)
    # compute EMA50 used by strategies if needed (safe)
    df['EMA50'] = df['close'].ewm(span=50, adjust=False).mean()

    broker = PaperBroker(initial_balance=INITIAL_BALANCE, leverage=LEVERAGE)
    equity_curve = []

    for idx, row in df.iterrows():
        price = float(row['close'])
        atr = float(row['ATR']) if row['ATR'] > 0 else max(1.0, price * 0.001)
        signal = int(row.get('signal', 0))

        # check SL/TP first
        ev = broker.check_sl_tp(row['high'], row['low'])
        if ev:
            ev.update({'symbol': SYMBOL, 'timeframe': tf, 'timestamp': row['timestamp']})
            log_trade(ev)
            equity_curve.append(ev['balance'])
            tr, wr, dd = rolling_stats(equity_curve)
            send_alert(f"⚡ SL/TP | {SYMBOL} | {tf} | {ev['type'].upper()} | PnL: {ev.get('pnl',0):.6f} | Bal: {ev['balance']:.2f} | TR: {tr:.2f}% | WR: {wr:.2f}% | DD: {dd:.2f}%")

        # open long
        if signal == 1 and broker.position == 0:
            ev = broker.open_long(price=price, atr=atr, risk_pct=RISK_PCT)
            if ev:
                ev.update({'symbol': SYMBOL, 'timeframe': tf, 'timestamp': row['timestamp']})
                log_trade(ev)
                equity_curve.append(broker.balance)
                tr, wr, dd = rolling_stats(equity_curve)
                send_alert(f"💰 OPEN LONG | {SYMBOL} | {tf} | Price: {price:.2f} | Units: {ev['units']:.8f} | Margin: {ev['margin']:.2f} | Bal: {ev['balance']:.2f} | TR: {tr:.2f}%")

        # open short
        elif signal == -1 and broker.position == 0:
            ev = broker.open_short(price=price, atr=atr, risk_pct=RISK_PCT)
            if ev:
                ev.update({'symbol': SYMBOL, 'timeframe': tf, 'timestamp': row['timestamp']})
                log_trade(ev)
                equity_curve.append(broker.balance)
                tr, wr, dd = rolling_stats(equity_curve)
                send_alert(f"💰 OPEN SHORT | {SYMBOL} | {tf} | Price: {price:.2f} | Units: {ev['units']:.8f} | Margin: {ev['margin']:.2f} | Bal: {ev['balance']:.2f} | TR: {tr:.2f}%")

        # neutral signal -> close
        elif signal == 0 and broker.position != 0:
            ev = broker.close_position(price=price)
            if ev:
                ev.update({'symbol': SYMBOL, 'timeframe': tf, 'timestamp': row['timestamp']})
                log_trade(ev)
                equity_curve.append(broker.balance)
                tr, wr, dd = rolling_stats(equity_curve)
                send_alert(f"🔒 CLOSE | {SYMBOL} | {tf} | Side: {ev['side']} | Price: {ev['exit']:.2f} | PnL: {ev['pnl']:.6f} | Bal: {ev['balance']:.2f} | TR: {tr:.2f}%")

    final = {'symbol': SYMBOL, 'timeframe': tf, 'final_balance': broker.balance, 'final_position': broker.position}
    print(f"📊 Final Summary | {SYMBOL} | {tf} | Balance: {broker.balance:.2f} | Position: {broker.position}")
    send_alert(f"📊 Final Summary | {SYMBOL} | {tf} | Balance: {broker.balance:.2f} | Position: {broker.position}")
    # small pause between timeframes to avoid rate-limit bursts
    time.sleep(1.0)
