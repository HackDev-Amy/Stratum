import pytest
from decimal import Decimal
from unittest.mock import patch
from django.contrib.auth import get_user_model
from accounts.models import Portfolio
from market.models import Stock
from trading.models import Order
from trading.tasks import process_pending_orders

User = get_user_model()


@pytest.mark.django_db
class TestPendingOrders:
    @pytest.fixture
    def setup(self):
        u = User.objects.create_user("bob", password="pw")
        Portfolio.objects.create(user=u, cash=Decimal("10000"))
        s = Stock.objects.create(symbol="TSLA", last_price=Decimal("100"))
        return u, s

    def test_limit_buy_triggers_when_price_below(self, setup):
        u, s = setup
        order = Order.objects.create(
            user=u, stock=s, order_type="LIMIT", side="BUY",
            quantity=Decimal("1"), trigger_price=Decimal("105"),
            status="PENDING",
        )
        with patch("trading.services.FinancialDataService.fetch_quote",
                   return_value={"price": 100.0, "symbol": "TSLA"}):
            with patch("trading.tasks.FinancialDataService.fetch_quote",
                       return_value={"price": 100.0}):
                process_pending_orders()

        order.refresh_from_db()
        assert order.status == "EXECUTED"

    def test_limit_buy_does_not_trigger(self, setup):
        u, s = setup
        order = Order.objects.create(
            user=u, stock=s, order_type="LIMIT", side="BUY",
            quantity=Decimal("1"), trigger_price=Decimal("90"),
            status="PENDING",
        )
        with patch("trading.tasks.FinancialDataService.fetch_quote",
                   return_value={"price": 100.0}):
            process_pending_orders()
        order.refresh_from_db()
        assert order.status == "PENDING"