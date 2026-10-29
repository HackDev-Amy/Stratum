import pytest
from unittest.mock import patch, MagicMock
from trading.broker_adapter import (
    get_broker, SimulatedAdapter, AlpacaPaperAdapter,
)


class TestSimulatedAdapter:
    def test_buy(self):
        a = SimulatedAdapter()
        r = a.buy("AAPL", 5)
        assert r["status"] == "simulated"
        assert r["side"] == "buy"

    def test_sell(self):
        a = SimulatedAdapter()
        r = a.sell("AAPL", 5)
        assert r["side"] == "sell"


class TestGetBroker:
    @patch.dict("os.environ", {"BROKER": "simulated"})
    def test_simulated_default(self):
        assert isinstance(get_broker(), SimulatedAdapter)

    @patch.dict("os.environ", {"BROKER": "alpaca",
                                "ALPACA_API_KEY": "k",
                                "ALPACA_SECRET_KEY": "s"})
    def test_alpaca_when_configured(self):
        assert isinstance(get_broker(), AlpacaPaperAdapter)

    @patch.dict("os.environ", {"BROKER": "alpaca"})
    def test_alpaca_falls_back_without_keys(self):
        assert isinstance(get_broker(), SimulatedAdapter)


class TestAlpacaAdapter:
    @patch("trading.broker_adapter.requests.post")
    def test_buy_calls_api(self, mock_post):
        mock_post.return_value = MagicMock(
            status_code=200, json=lambda: {"id": "abc", "status": "accepted"}
        )
        with patch.dict("os.environ", {
            "ALPACA_API_KEY": "k", "ALPACA_SECRET_KEY": "s"
        }):
            a = AlpacaPaperAdapter()
            r = a.buy("AAPL", 2)
        assert r["id"] == "abc"
        mock_post.assert_called_once()