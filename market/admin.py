from django.contrib import admin
from .models import Stock


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("symbol", "name", "last_price", "updated_at")
    search_fields = ("symbol", "name")
    ordering = ("symbol",)
    readonly_fields = ("updated_at",)
