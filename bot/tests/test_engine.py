import pytest
from decimal import Decimal
from unittest.mock import patch
from django.contrib.auth import get_user_model
from accounts.models import Portfolio
from market.models import Stock
from bot.models import BotConfig, BotLog
from bot.engine import run_bot_once

User = get_user_model()


@pytest.mark.django_db
class TestBotEngine:
    @pytest.fixture
    def setup(self):
        u = User.objects.create_user("botuser", password="pw")
        Portfolio.objects.create(user=u, cash=Decimal("10000"))
        s = Stock.objects.create(symbol="AAPL", last_price=Decimal("100"))
        return u, s

    def test_no_data_logs_error(self, setup):
        u, s = setup
        bot = BotConfig.objects.create(user=u, stock=s, is_active=True)
        with patch("bot.engine.FinancialDataService.fetch_history", return_value=None):
            r = run_bot_once(bot)
        assert "error" in r
        assert BotLog.objects.filter(bot=bot).count() >= 1

    def test_signal_none_returns_none(self, setup):
        u, s = setup
        bot = BotConfig.objects.create(user=u, stock=s, is_active=True)
        import pandas as pd
        df = pd.DataFrame({
            "Open": [100] * 50, "High": [100] * 50, "Low": [100] * 50,
            "Close": [100] * 50, "Volume": [1000] * 50,
        }, index=pd.date_range("2024-01-01", periods=50, freq="1h"))
        with patch("bot.engine.FinancialDataService.fetch_history", return_value=df):
            r = run_bot_once(bot)
        assert r["signal"] == "NONE"
        