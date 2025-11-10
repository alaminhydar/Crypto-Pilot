# paper_trader/paper_bot.py
from risk.risk import position_size, sl_tp_levels
from typing import Optional, Dict

class PaperBroker:
    def __init__(self, initial_balance: float = 1000.0, leverage: float = 5.0):
        self.balance = float(initial_balance)
        self.used_margin = 0.0
        self.position = 0.0
        self.entry_price: Optional[float] = None
        self.stop_loss: Optional[float] = None
        self.take_profit: Optional[float] = None
        self.side: Optional[str] = None
        self.leverage = float(leverage)
        self.fee_rate = 0.0005
        self.last_pnl: float = 0.0
        self.cooldown_bars = 0

    def _apply_fee(self, notional: float) -> float:
        return notional * self.fee_rate

    def open_long(self, price: float, atr: float, risk_pct: float = 0.01) -> Optional[Dict]:
        if self.position != 0 or self.cooldown_bars > 0:
            return None

        units = position_size(self.balance, price, atr, risk_pct=risk_pct, leverage=self.leverage)
        if units <= 0:
            return None

        margin_required = (units * price) / self.leverage
        if margin_required > self.balance:
            margin_required = self.balance * 0.999
            units = (margin_required * self.leverage) / price

        self.balance -= margin_required
        self.used_margin += margin_required
        self.position = units
        self.entry_price = price
        # dynamic SL/TP
        sl_mult = 1.0
        tp_mult = 2.0 if atr < price * 0.005 else 3.0
        self.stop_loss, self.take_profit = sl_tp_levels(price, atr, sl_mult, tp_mult)
        self.side = 'long'
        return {'type': 'open_long', 'units': units, 'price': price, 'margin': margin_required, 'balance': self.balance}

    def open_short(self, price: float, atr: float, risk_pct: float = 0.01) -> Optional[Dict]:
        if self.position != 0 or self.cooldown_bars > 0:
            return None

        units = position_size(self.balance, price, atr, risk_pct=risk_pct, leverage=self.leverage)
        if units <= 0:
            return None

        margin_required = (units * price) / self.leverage
        if margin_required > self.balance:
            margin_required = self.balance * 0.999
            units = (margin_required * self.leverage) / price

        self.balance -= margin_required
        self.used_margin += margin_required
        self.position = units
        self.entry_price = price
        sl_mult = 1.0
        tp_mult = 2.0 if atr < price * 0.005 else 3.0
        self.take_profit = price - atr * tp_mult
        self.stop_loss = price + atr * sl_mult
        self.side = 'short'
        return {'type': 'open_short', 'units': units, 'price': price, 'margin': margin_required, 'balance': self.balance}

    def close_position(self, price: float) -> Optional[Dict]:
        if self.position == 0 or self.entry_price is None:
            return None

        units = self.position
        entry = self.entry_price
        margin_released = (units * entry) / self.leverage

        if self.side == 'long':
            pnl = (price - entry) * units
        else:
            pnl = (entry - price) * units

        fee = self._apply_fee(price * units) + self._apply_fee(entry * units)
        pnl_after_fee = pnl - fee
        self.last_pnl = pnl_after_fee

        self.balance += margin_released + pnl_after_fee
        self.used_margin -= margin_released

        result = {'type': 'close', 'side': self.side, 'units': units, 'entry': entry, 'exit': price, 'pnl': pnl_after_fee, 'balance': self.balance}

        self.position = 0.0
        self.entry_price = None
        self.stop_loss = None
        self.take_profit = None
        self.side = None

        # cooldown if loss
        self.cooldown_bars = 2 if pnl_after_fee < 0 else 0
        return result

    def check_sl_tp(self, high: float, low: float) -> Optional[Dict]:
        if self.position == 0 or self.entry_price is None:
            if self.cooldown_bars > 0:
                self.cooldown_bars -= 1
            return None

        if self.side == 'long':
            if self.take_profit is not None and high >= self.take_profit:
                return self.close_position(self.take_profit)
            if self.stop_loss is not None and low <= self.stop_loss:
                return self.close_position(self.stop_loss)
        elif self.side == 'short':
            if self.take_profit is not None and low <= self.take_profit:
                return self.close_position(self.take_profit)
            if self.stop_loss is not None and high >= self.stop_loss:
                return self.close_position(self.stop_loss)
        return None
