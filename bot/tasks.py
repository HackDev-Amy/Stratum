from celery import shared_task
from .models import BotConfig
from .engine import run_bot_once

@shared_task
def run_all_bots():
    results = []
    for bot in BotConfig.objects.filter(is_active=True).select_related("stock", "user"):
        results.append({"bot": bot.id, **run_bot_once(bot)})
    return results