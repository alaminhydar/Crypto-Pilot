# risk/risk.py
from typing import Tuple

def position_size(
    balance: float,
    price: float,
    atr: float,
    risk_pct: float = 0.01,
    sl_multiplier: float = 1.5,
    leverage: float = 5.0,
    max_margin_pct: float = 0.2
) -> float:
    """
    Units to trade. Uses ATR-based stop distance and caps margin usage.
    - risk_pct: percent of balance to risk if SL hit.
    - sl_multiplier: how many ATRs for the stop.
    - max_margin_pct: portion of balance allowed to be used as margin for a single trade.
    """
    if atr <= 0 or price <= 0:
        return 0.0

    risk_amount = balance * risk_pct
    risk_per_unit = atr * sl_multiplier
    if risk_per_unit <= 0:
        return 0.0

    units_by_risk = risk_amount / risk_per_unit
    max_units_by_margin = (balance * max_margin_pct * leverage) / price
    units = min(units_by_risk, max_units_by_margin)
    return max(0.0, float(units))

def sl_tp_levels(entry_price: float, atr: float, sl_multiplier: float = 1.5, tp_multiplier: float = 3.0) -> Tuple[float, float]:
    stop_loss = entry_price - atr * sl_multiplier
    take_profit = entry_price + atr * tp_multiplier
    return stop_loss, take_profit
