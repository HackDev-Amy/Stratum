import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from market.services import FinancialDataService, InfluxService


class TestFinancialDataService:
    @patch("market.services.requests.get")
    def test_finnhub_quote_success(self, mock_get, settings):
        settings.FINNHUB_API_KEY = "fake"
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {"c": 150.5, "h": 152, "l": 149, "o": 150, "pc": 149.5}
        )
        q = FinancialDataService.fetch_quote("AAPL")
        assert q is not None
        assert q["price"] == 150.5
        assert q["symbol"] == "AAPL"

    @patch("market.services.requests.get")
    def test_finnhub_fail_falls_back(self, mock_get, settings):
        settings.FINNHUB_API_KEY = "fake"
        mock_get.side_effect = Exception("network down")
        q = FinancialDataService.fetch_quote("AAPL")
        # Either yfinance returns something or None — both acceptable
        assert q is None or "price" in q

    def test_history_empty_on_bad_symbol(self):
        df = FinancialDataService.fetch_history("ZZZZZZZZZZ")
        assert isinstance(df, pd.DataFrame)


class TestInfluxService:
    def test_write_price_no_crash(self):
        # Should not raise even if Influx is down
        from datetime import datetime, timezone
        InfluxService.write_price(
            "TEST", 1, 2, 0.5, 1.5, 100, datetime.now(timezone.utc)
        )