from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="portfolio")
    cash = models.DecimalField(max_digits=16, decimal_places=2, default=10000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s portfolio"