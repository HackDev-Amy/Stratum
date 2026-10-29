from django.contrib import admin
from .models import StrategyConfig


@admin.register(StrategyConfig)
class StrategyConfigAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "name",
        "short_window",
        "long_window",
        "rsi_period",
        "is_active",
    )
    list_filter = ("is_active", "user")
    search_fields = ("user__username", "name")
