from django.db import models

class Stock(models.Model):
    symbol = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=128, blank=True)
    last_price = models.DecimalField(max_digits=16, decimal_places=4, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.symbol