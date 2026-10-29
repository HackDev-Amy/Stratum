from decimal import Decimal
from django.db import transaction
from django.core.cache import cache
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from market.models import Stock
from market.services import FinancialDataService
from core.exceptions import (
    InsufficientFunds, InsufficientShares, SymbolNotFound, MarketDataUnavailable,
)
from .broker_adapter import get_broker
from .models import Order, Transaction, PortfolioAsset

COMMISSION_RATE = Decimal("0.001")


class TradingService:
    @staticmethod
    def _get_asset(portfolio, stock):
        obj, _ = PortfolioAsset.objects.get_or_create(portfolio=portfolio, stock=stock)
        return obj

    @classmethod
    def place_market_order(cls, user, symbol, side, quantity):
        stock = Stock.objects.filter(symbol=symbol.upper()).first()
        if not stock:
            raise SymbolNotFound(f"Unknown symbol: {symbol}")

        quote = FinancialDataService.fetch_quote(stock.symbol)
        if not quote:
            raise MarketDataUnavailable(f"No price for {symbol}")

        price = Decimal(str(quote["price"]))

        with transaction.atomic():
            order = Order.objects.create(
                user=user, stock=stock, order_type="MARKET",
                side=side, quantity=quantity, status="PENDING",
            )
            cls._execute(order, price)

        cache.delete(f"portfolio:{user.id}")
        cls._broadcast_portfolio(user, order)
        return order

    @classmethod
    def _execute(cls, order, price):
        broker = get_broker()
        portfolio = order.user.portfolio
        commission = (price * order.quantity * COMMISSION_RATE).quantize(Decimal("0.0001"))
        cost = price * order.quantity

        if order.side == "BUY":
            if portfolio.cash < cost + commission:
                order.status = "FAILED"
                order.save()
                raise InsufficientFunds(
                    f"Need ${cost + commission:.2f}, have ${portfolio.cash:.2f}"
                )
            broker.buy(order.stock.symbol, float(order.quantity))
            portfolio.cash -= cost + commission
            asset = cls._get_asset(portfolio, order.stock)
            asset.quantity += order.quantity
            asset.save()
        else:
            asset = cls._get_asset(portfolio, order.stock)
            if asset.quantity < order.quantity:
                order.status = "FAILED"
                order.save()
                raise InsufficientShares(
                    f"Have {asset.quantity}, trying to sell {order.quantity}"
                )
            broker.sell(order.stock.symbol, float(order.quantity))
            asset.quantity -= order.quantity
            asset.save()
            portfolio.cash += cost - commission

        portfolio.save()
        order.status = "EXECUTED"
        order.filled_price = price
        order.save()
        Transaction.objects.create(
            user=order.user, stock=order.stock, side=order.side,
            quantity=order.quantity, price=price, commission=commission,
        )

    @classmethod
    def place_limit_or_stop(cls, user, symbol, side, quantity, order_type, trigger_price):
        stock = Stock.objects.filter(symbol=symbol.upper()).first()
        if not stock:
            raise SymbolNotFound(symbol)
        return Order.objects.create(
            user=user, stock=stock, order_type=order_type, side=side,
            quantity=quantity, trigger_price=trigger_price, status="PENDING",
        )

    @classmethod
    def _broadcast_portfolio(cls, user, order):
        layer = get_channel_layer()
        async_to_sync(layer.group_send)(
            f"portfolio_{user.id}",
            {"type": "portfolio.update", "order_id": order.id, "status": order.status},
        )