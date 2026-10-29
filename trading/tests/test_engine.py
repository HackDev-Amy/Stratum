import pytest
from decimal import Decimal
from unittest.mock import patch
from django.contrib.auth import get_user_model
from accounts.models import Portfolio
from market.models import Stock
from trading.models import Order, Transaction, PortfolioAsset
from trading.services import TradingService

User = get_user_model()


def _fake_quote(symbol):
    return {"symbol": symbol, "price": 100.0, "high": 101, "low": 99, "open": 100, "prev_close": 99}


@pytest.mark.django_db
class TestMarketOrder:
    @pytest.fixture
    def user(self):
        u = User.objects.create_user("alice", password="pw")
        Portfolio.objects.create(user=u, cash=Decimal("10000"))
        return u

    @pytest.fixture
    def stock(self):
        return Stock.objects.create(symbol="AAPL", name="Apple", last_price=Decimal("100"))

    def test_buy_success(self, user, stock):
        with patch("trading.services.FinancialDataService.fetch_quote",
                   side_effect=_fake_quote):
            order = TradingService.place_market_order(user, "AAPL", "BUY", Decimal("5"))
        assert order.status == "EXECUTED"
        assert order.filled_price == Decimal("100")
        user.portfolio.refresh_from_db()
        assert user.portfolio.cash == Decimal("10000") - Decimal("500.5000")
        asset = PortfolioAsset.objects.get(portfolio=user.portfolio, stock=stock)
        assert asset.quantity == Decimal("5")
        assert Transaction.objects.filter(user=user).count() == 1

    def test_buy_insufficient_cash(self, user, stock):
        user.portfolio.cash = Decimal("10"); user.portfolio.save()
        with patch("trading.services.FinancialDataService.fetch_quote",
                   side_effect=_fake_quote):
            with pytest.raises(ValueError, match="Insufficient cash"):
                TradingService.place_market_order(user, "AAPL", "BUY", Decimal("5"))

    def test_sell_insufficient_shares(self, user, stock):
        with patch("trading.services.FinancialDataService.fetch_quote",
                   side_effect=_fake_quote):
            with pytest.raises(ValueError, match="Insufficient shares"):
                TradingService.place_market_order(user, "AAPL", "SELL", Decimal("3"))

    def test_round_trip_preserves_cash_minus_fees(self, user, stock):
        with patch("trading.services.FinancialDataService.fetch_quote",
                   side_effect=_fake_quote):
            TradingService.place_market_order(user, "AAPL", "BUY", Decimal("10"))
            TradingService.place_market_order(user, "AAPL", "SELL", Decimal("10"))
        user.portfolio.refresh_from_db()
        assert user.portfolio.cash == Decimal("10000") - Decimal("2.0000")

    def test_portfolio_cache_invalidated(self, user, stock):
        from django.core.cache import cache
        cache.set(f"portfolio:{user.id}", {"dummy": True}, 60)
        with patch("trading.services.FinancialDataService.fetch_quote",
                   side_effect=_fake_quote):
            TradingService.place_market_order(user, "AAPL", "BUY", Decimal("1"))
        assert cache.get(f"portfolio:{user.id}") is None