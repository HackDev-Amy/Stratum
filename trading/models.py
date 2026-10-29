from django.db import models
from django.conf import settings
from market.models import Stock

class PortfolioAsset(models.Model):
    portfolio = models.ForeignKey("accounts.Portfolio", on_delete=models.CASCADE, related_name="assets")
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=20, decimal_places=8, default=0)

    class Meta:
        unique_together = ("portfolio", "stock")

class Order(models.Model):
    ORDER_TYPE = [("MARKET", "MARKET"), ("LIMIT", "LIMIT"), ("STOP_LOSS", "STOP_LOSS")]
    SIDE = [("BUY", "BUY"), ("SELL", "SELL")]
    STATUS = [("PENDING", "PENDING"), ("EXECUTED", "EXECUTED"),
              ("CANCELLED", "CANCELLED"), ("FAILED", "FAILED")]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    order_type = models.CharField(max_length=16, choices=ORDER_TYPE, default="MARKET")
    side = models.CharField(max_length=4, choices=SIDE)
    quantity = models.DecimalField(max_digits=20, decimal_places=8)
    price = models.DecimalField(max_digits=16, decimal_places=4, null=True, blank=True)
    trigger_price = models.DecimalField(max_digits=16, decimal_places=4, null=True, blank=True)
    status = models.CharField(max_length=12, choices=STATUS, default="PENDING")
    filled_price = models.DecimalField(max_digits=16, decimal_places=4, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    side = models.CharField(max_length=4)
    quantity = models.DecimalField(max_digits=20, decimal_places=8)
    price = models.DecimalField(max_digits=16, decimal_places=4)
    commission = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    created_at = models.DateTimeField(auto_now_add=True)