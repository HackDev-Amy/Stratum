from django.db import models
from django.conf import settings
from market.models import Stock

class BotConfig(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    strategy_params = models.JSONField(default=dict)   # {"short":10,"long":30,"rsi":14}
    risk_params = models.JSONField(default=dict)       # {"risk_pct":1,"stop_loss_pct":2}
    quantity = models.DecimalField(max_digits=20, decimal_places=8, default=1)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_run = models.DateTimeField(null=True, blank=True)

class BotLog(models.Model):
    bot = models.ForeignKey(BotConfig, on_delete=models.CASCADE, related_name="logs")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)