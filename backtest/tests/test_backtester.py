import pandas as pd
import pytest
from backtest.services import run_backtest, compute_metrics


def _synthetic_prices(n=200, start=100.0):
    idx = pd.date_range("2024-01-01", periods=n, freq="1h")
    prices = [start + i * 0.5 for i in range(n)]
    return pd.DataFrame({
        "Open": prices, "High": prices, "Low": prices,
        "Close": prices, "Volume": [1000] * n,
    }, index=idx)


class TestBacktester:
    def test_returns_metrics(self):
        r = run_backtest(_synthetic_prices(), initial_capital=10000)
        assert "metrics" in r
        for k in ("total_return_pct", "sharpe_ratio", "max_drawdown_pct"):
            assert k in r["metrics"]

    def test_empty_df_returns_error(self):
        r = run_backtest(pd.DataFrame())
        assert "error" in r

    def test_equity_curve_length_matches_data(self):
        df = _synthetic_prices()
        r = run_backtest(df)
        assert len(r["equity_curve"]) == len(df)

    def test_metrics_zero_on_flat(self):
        m = compute_metrics(
            [{"time": "t1", "equity": 10000}, {"time": "t2", "equity": 10000}],
            10000, 10000, []
        )
        assert m["total_return_pct"] == 0
        assert m["max_drawdown_pct"] == 0