# alerts/telegram_alerts.py
import os
import time
import pandas as pd
import telebot
from datetime import datetime
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_IDS

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

_last_alert = None
_last_alert_time = 0
_MIN_SECONDS_DUP = 2
_MAX_MSG_LEN = 350  # keep messages short to avoid "message too long" and reduce rate

def _now_ts():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

def _safe_send(cid: str, message: str):
    """
    Send with small protective measures: truncate long messages and catch rate errors.
    """
    try:
        if len(message) > _MAX_MSG_LEN:
            message = message[:_MAX_MSG_LEN - 3] + "..."
        bot.send_message(cid, message)
    except Exception as e:
        # print error but don't crash
        print(f"Telegram send error to {cid}: {e}")

def send_alert(message: str, force: bool = False):
    """
    Send alert with dedupe protection and minimal length.
    """
    global _last_alert, _last_alert_time
    now = time.time()
    if not force and message == _last_alert and (now - _last_alert_time) < _MIN_SECONDS_DUP:
        return
    _last_alert = message
    _last_alert_time = now

    for cid in TELEGRAM_CHAT_IDS:
        cid = str(cid).strip()
        if not cid:
            continue
        _safe_send(cid, message)

def log_trade(trade_data: dict, file='trade_log.csv'):
    """
    Append trade data to CSV. Ensure timestamp column exists.
    """
    df = pd.DataFrame([trade_data])
    # ensure timestamp column exists
    if 'timestamp' not in df.columns:
        df['timestamp'] = _now_ts()
    df.to_csv(file, mode='a', header=not os.path.exists(file), index=False)
