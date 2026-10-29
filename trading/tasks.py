from celery import shared_task
from decimal import Decimal
import logging
from .models import Order
from .services import TradingService
from market.services import FinancialDataService

logger = logging.getLogger(__name__)

@shared_task
def process_pending_orders():
    for order in Order.objects.filter(status="PENDING").exclude(order_type="MARKET"):
        quote = FinancialDataService.fetch_quote(order.stock.symbol)
        if not quote:
            continue
        price = Decimal(str(quote["price"]))
        trig = order.trigger_price
        if trig is None:
            continue
        hit = (
            (order.order_type == "LIMIT" and order.side == "BUY" and price <= trig) or
            (order.order_type == "LIMIT" and order.side == "SELL" and price >= trig) or
            (order.order_type == "STOP_LOSS" and order.side == "SELL" and price <= trig)
        )
        if hit:
            try:
                TradingService._execute(order, price)
                logger.info(f"Executed pending order {order.id}")
            except Exception as e:
                logger.error(f"Failed pending order {order.id}: {e}")