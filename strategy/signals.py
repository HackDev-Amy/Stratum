import pandas as pd


def _rsi(close: pd.Series, period: int) -> pd.Series:
    change = close.diff()
    gains = change.clip(lower=0)
    losses = -change.clip(upper=0)
    average_gain = gains.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    average_loss = losses.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    relative_strength = average_gain / average_loss.replace(0, 1e-12)
    return 100 - (100 / (1 + relative_strength))

def enrich(df: pd.DataFrame, short=10, long=30, rsi_period=14) -> pd.DataFrame:
    """Add indicators + signal column. Expects df with Open/High/Low/Close/Volume."""
    if df.empty:
        return df
    df = df.copy()
    df["sma_short"] = df["Close"].rolling(short).mean()
    df["sma_long"] = df["Close"].rolling(long).mean()
    df["rsi"] = _rsi(df["Close"], rsi_period)

    df["signal"] = 0
    cross_up = (df["sma_short"] > df["sma_long"]) & (
        df["sma_short"].shift(1) <= df["sma_long"].shift(1)
    )
    cross_dn = (df["sma_short"] < df["sma_long"]) & (
        df["sma_short"].shift(1) >= df["sma_long"].shift(1)
    )
    df.loc[cross_up & (df["rsi"] < 70), "signal"] = 1
    df.loc[cross_dn & (df["rsi"] > 30), "signal"] = -1
    return df