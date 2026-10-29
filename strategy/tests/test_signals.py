import pandas as pd
from strategy.signals import enrich


def _prices(n=100):
    idx = pd.date_range("2024-01-01", periods=n, freq="1h")
    p = list(range(100, 100 + n))
    return pd.DataFrame({
        "Open": p, "High": p, "Low": p, "Close": p, "Volume": [1000] * n,
    }, index=idx)


def test_enrich_adds_columns():
    out = enrich(_prices(), short=5, long=20)
    for col in ("sma_short", "sma_long", "rsi", "signal"):
        assert col in out.columns


def test_enrich_empty():
    out = enrich(pd.DataFrame())
    assert out.empty


def test_signal_column_has_expected_values():
    out = enrich(_prices())
    assert set(out["signal"].unique()).issubset({-1, 0, 1})