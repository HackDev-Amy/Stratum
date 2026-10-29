from decimal import Decimal
import numpy as np
import pandas as pd
from strategy.signals import enrich

COMMISSION = 0.001  # 0.1%

def run_backtest(df: pd.DataFrame, initial_capital=10000.0,
                 risk_pct=1.0, stop_loss_pct=2.0) -> dict:
    if df.empty:
        return {"error": "No data"}

    df = enrich(df)
    cash = initial_capital
    position = 0.0
    entry_price = 0.0
    stop_loss = 0.0
    trades = []
    equity_curve = []

    for ts, row in df.iterrows():
        price = float(row["Close"])
        signal = int(row.get("signal", 0))

        # exit on stop loss
        if position > 0 and price <= stop_loss:
            proceeds = position * price * (1 - COMMISSION)
            trades.append({"time": str(ts), "side": "SELL(SL)",
                           "qty": position, "price": price})
            cash += proceeds
            position = 0.0

        if signal == 1 and position == 0:
            risk_amount = cash * risk_pct / 100
            sl_price = price * (1 - stop_loss_pct / 100)
            per_share_risk = price - sl_price
            qty = int(risk_amount / per_share_risk) if per_share_risk > 0 else 0
            cost = qty * price * (1 + COMMISSION)
            if qty > 0 and cost <= cash:
                cash -= cost
                position = qty
                entry_price = price
                stop_loss = sl_price
                trades.append({"time": str(ts), "side": "BUY",
                               "qty": qty, "price": price})

        elif signal == -1 and position > 0:
            proceeds = position * price * (1 - COMMISSION)
            trades.append({"time": str(ts), "side": "SELL",
                           "qty": position, "price": price})
            cash += proceeds
            position = 0.0

        equity_curve.append({"time": str(ts), "equity": cash + position * price})

    final_value = cash + position * float(df["Close"].iloc[-1])
    metrics = compute_metrics(equity_curve, initial_capital, final_value, trades)
    return {
        "trades": trades,
        "equity_curve": equity_curve,
        "final_value": final_value,
        "metrics": metrics,
    }


def compute_metrics(equity_curve, initial, final, trades):
    eq = pd.Series([p["equity"] for p in equity_curve])
    if eq.empty or initial == 0:
        return {}

    total_return_pct = (final - initial) / initial * 100

    # daily-ish returns
    returns = eq.pct_change().dropna()
    sharpe = 0.0
    if len(returns) > 1 and returns.std() > 0:
        sharpe = float(np.sqrt(252 * 78) * returns.mean() / returns.std())

    # max drawdown
    running_max = eq.cummax()
    drawdown = (eq - running_max) / running_max
    max_dd = float(drawdown.min() * 100) if not drawdown.empty else 0.0

    # win/loss on realized trades (paired buy→sell)
    wins, losses = 0, 0
    open_buy = None
    for t in trades:
        if t["side"] == "BUY":
            open_buy = t
        elif t["side"].startswith("SELL") and open_buy:
            pnl = (t["price"] - open_buy["price"]) * t["qty"]
            if pnl > 0: wins += 1
            else: losses += 1
            open_buy = None

    return {
        "total_return_pct": round(total_return_pct, 2),
        "sharpe_ratio": round(sharpe, 3),
        "max_drawdown_pct": round(max_dd, 2),
        "win_trades": wins,
        "loss_trades": losses,
        "win_rate_pct": round(wins / (wins + losses) * 100, 2) if (wins + losses) else 0,
        "num_trades": len(trades),
        "final_value": round(final, 2),
    }