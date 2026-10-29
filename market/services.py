import os, logging
import requests
import pandas as pd
from datetime import datetime, timezone
from django.conf import settings
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

logger = logging.getLogger(__name__)

class InfluxService:
    _client = None
    @classmethod
    def client(cls):
        if cls._client is None:
            cls._client = InfluxDBClient(
                url=settings.INFLUX_URL, token=settings.INFLUX_TOKEN, org=settings.INFLUX_ORG
            )
        return cls._client

    @classmethod
    def write_price(cls, symbol: str, o, h, l, c, v, ts: datetime):
        pt = (
            Point("stock_price")
            .tag("symbol", symbol)
            .field("open", float(o)).field("high", float(h))
            .field("low", float(l)).field("close", float(c))
            .field("volume", float(v))
            .time(ts, WritePrecision.S)
        )
        try:
            cls.client().write_api(write_options=SYNCHRONOUS).write(
                bucket=settings.INFLUX_BUCKET, record=pt
            )
        except Exception as exc:
            logger.warning("Influx price write failed for %s: %s", symbol, exc)

    @classmethod
    def query_history(cls, symbol: str, minutes: int = 1440) -> pd.DataFrame:
        q = f'''
        from(bucket: "{settings.INFLUX_BUCKET}")
          |> range(start: -{minutes}m)
          |> filter(fn: (r) => r._measurement == "stock_price" and r.symbol == "{symbol}")
          |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
        '''
        tables = cls.client().query_api().query(q)
        rows = []
        for t in tables:
            for rec in t.records:
                rows.append({
                    "timestamp": rec["_time"],
                    "Open": rec.get("open", 0), "High": rec.get("high", 0),
                    "Low": rec.get("low", 0), "Close": rec.get("close", 0),
                    "Volume": rec.get("volume", 0),
                })
        df = pd.DataFrame(rows)
        if not df.empty:
            df = df.set_index("timestamp").sort_index()
        return df


class FinancialDataService:
    BASE = "https://finnhub.io/api/v1"

    @classmethod
    def fetch_quote(cls, symbol: str) -> dict | None:
        key = settings.FINNHUB_API_KEY
        if key:
            try:
                r = requests.get(
                    f"{cls.BASE}/quote",
                    params={"symbol": symbol, "token": key},
                    timeout=5,
                )
                r.raise_for_status()
                data = r.json()
                if data.get("c"):
                    return {"symbol": symbol, "price": data["c"],
                            "high": data.get("h"), "low": data.get("l"),
                            "open": data.get("o"), "prev_close": data.get("pc")}
            except Exception as e:
                logger.warning(f"Finnhub quote failed for {symbol}: {e}")

        # fallback yfinance (delayed but free)
        try:
            import yfinance as yf
            t = yf.Ticker(symbol)
            hist = t.history(period="1d", interval="1m")
            if not hist.empty:
                last = hist.iloc[-1]
                return {"symbol": symbol, "price": float(last["Close"]),
                        "high": float(last["High"]), "low": float(last["Low"]),
                        "open": float(last["Open"]), "prev_close": None}
        except Exception as e:
            logger.error(f"yfinance fallback failed for {symbol}: {e}")
        return None

    @classmethod
    def fetch_history(cls, symbol: str, period="5d", interval="5m") -> pd.DataFrame:
        try:
            import yfinance as yf
            df = yf.Ticker(symbol).history(period=period, interval=interval)
            if df.empty:
                return pd.DataFrame()
            df = df.rename(columns={"Open": "Open", "High": "High", "Low": "Low",
                                    "Close": "Close", "Volume": "Volume"})
            return df[["Open", "High", "Low", "Close", "Volume"]]
        except Exception as e:
            logger.error(f"history fetch failed {symbol}: {e}")
            return pd.DataFrame()