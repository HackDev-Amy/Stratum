from celery import shared_task
import logging
from datetime import datetime, timezone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Stock
from .services import FinancialDataService, InfluxService

logger = logging.getLogger(__name__)

@shared_task
def refresh_quotes():
    layer = get_channel_layer()
    for stock in Stock.objects.all():
        q = FinancialDataService.fetch_quote(stock.symbol)
        if not q:
            continue
        stock.last_price = q["price"]
        stock.save(update_fields=["last_price", "updated_at"])

        # write to InfluxDB
        try:
            InfluxService.write_price(
                stock.symbol, q["open"] or q["price"], q["high"] or q["price"],
                q["low"] or q["price"], q["price"], 0,
                datetime.now(timezone.utc),
            )
        except Exception as e:
            logger.error(f"Influx write error {stock.symbol}: {e}")

        async_to_sync(layer.group_send)(
            "prices", {"type": "price.update",
                       "symbol": stock.symbol, "price": float(stock.last_price)}
        )