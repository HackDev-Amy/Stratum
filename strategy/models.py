from django.db import models
from django.conf import settings

class StrategyConfig(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, default="SMA_RSI")
    short_window = models.IntegerField(default=10)
    long_window = models.IntegerField(default=30)
    rsi_period = models.IntegerField(default=14)
    risk_per_trade_pct = models.FloatField(default=1.0)
    stop_loss_pct = models.FloatField(default=2.0)
    take_profit_pct = models.FloatField(default=5.0)
    is_active = models.BooleanField(default=True)