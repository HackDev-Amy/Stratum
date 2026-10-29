from decimal import Decimal
from django.db import transaction
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.cache import cache
from market.models import Stock
from market.services import FinancialDataService
from .models import Order, Transaction, PortfolioAsset
import logging

logger = logging.getLogger(__name__)
COMMISSION_RATE = Decimal("0.001")  # 0.1%

class TradingService:
    @staticmethod
    def _get_asset(portfolio, stock):
        obj, _ = PortfolioAsset.objects.get_or_create(portfolio=portfolio, stock=stock)
        return obj

    @classmethod
    def place_market_order(cls, user, symbol: str, side: str, quantity: Decimal) -> Order:
        stock = Stock.objects.filter(symbol=symbol.upper()).first()
        if not stock:
            raise ValueError("Unknown symbol")
        quote = FinancialDataService.fetch_quote(stock.symbol)
        if not quote:
            raise ValueError("No market price available")
        price = Decimal(str(quote["price"]))

        with transaction.atomic():
            order = Order.objects.create(
                user=user, stock=stock, order_type="MARKET",
                side=side, quantity=quantity, status="PENDING",
            )
            cls._execute(order, price)

        # realtime portfolio push
        layer = get_channel_layer()
        async_to_sync(layer.group_send)(
            f"portfolio_{user.id}",
            {"type": "portfolio.update", "order_id": order.id, "status": order.status},
        )
        return order

    @classmethod
    def _execute(cls, order: Order, price: Decimal):
        from accounts.models import Portfolio

        portfolio, _ = Portfolio.objects.get_or_create(user=order.user)
        commission = (price * order.quantity * COMMISSION_RATE).quantize(Decimal("0.0001"))
        cost = price * order.quantity

        if order.side == "BUY":
            if portfolio.cash < cost + commission:
                order.status = "FAILED"
                order.save(); raise ValueError("Insufficient cash")
            portfolio.cash -= cost + commission
            asset = cls._get_asset(portfolio, order.stock)
            asset.quantity += order.quantity
            asset.save()
        else:
            asset = cls._get_asset(portfolio, order.stock)
            if asset.quantity < order.quantity:
                order.status = "FAILED"
                order.save(); raise ValueError("Insufficient shares")
            asset.quantity -= order.quantity
            asset.save()
            portfolio.cash += cost - commission

        portfolio.save()
        cache.delete(f"portfolio:{order.user_id}")
        order.status = "EXECUTED"
        order.filled_price = price
        order.save()
        Transaction.objects.create(
            user=order.user, stock=order.stock, side=order.side,
            quantity=order.quantity, price=price, commission=commission,
        )

    @classmethod
    def place_limit_or_stop(cls, user, symbol, side, quantity, order_type, trigger_price):
        stock = Stock.objects.get(symbol=symbol.upper())
        return Order.objects.create(
            user=user, stock=stock, order_type=order_type, side=side,
            quantity=quantity, trigger_price=trigger_price, status="PENDING",
        )