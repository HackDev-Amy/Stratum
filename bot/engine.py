import logging
from decimal import Decimal
from django.utils import timezone
from market.services import FinancialDataService
from strategy.signals import enrich
from trading.services import TradingService
from notifications.services import send_notification
from .models import BotLog

logger = logging.getLogger(__name__)

def run_bot_once(bot):
    """Fetch data → compute signal → maybe trade. Returns dict of result."""
    bot.last_run = timezone.now()
    bot.save(update_fields=["last_run"])

    df = FinancialDataService.fetch_history(bot.stock.symbol, period="5d", interval="15m")
    if df is None or df.empty:
        msg = f"{bot.stock.symbol}: no data"
        BotLog.objects.create(bot=bot, message=msg)
        return {"error": msg}

    df = enrich(df,
                short=bot.strategy_params.get("short", 10),
                long=bot.strategy_params.get("long", 30),
                rsi_period=bot.strategy_params.get("rsi", 14))

    last_signal = int(df["signal"].iloc[-1])
    if last_signal == 0:
        return {"signal": "NONE"}

    side = "BUY" if last_signal == 1 else "SELL"
    try:
        order = TradingService.place_market_order(
            bot.user, bot.stock.symbol, side, Decimal(str(bot.quantity))
        )
        msg = f"{bot.stock.symbol} {side} {bot.quantity} @ {order.filled_price}"
        BotLog.objects.create(bot=bot, message=msg)
        send_notification(f"[BOT] {msg}")
        return {"signal": side, "order_id": order.id, "price": float(order.filled_price)}
    except Exception as e:
        BotLog.objects.create(bot=bot, message=f"Error: {e}")
        send_notification(f"[BOT ERROR] {bot.stock.symbol}: {e}")
        return {"error": str(e)}
    