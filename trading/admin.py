from django.contrib import admin
from .models import Order, Transaction, PortfolioAsset


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "stock",
        "side",
        "order_type",
        "quantity",
        "status",
        "filled_price",
        "created_at",
    )
    list_filter = ("status", "side", "order_type", "created_at")
    search_fields = ("user__username", "stock__symbol")
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
    autocomplete_fields = ("stock",)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "stock",
        "side",
        "quantity",
        "price",
        "commission",
        "created_at",
    )
    list_filter = ("side", "created_at")
    search_fields = ("user__username", "stock__symbol")
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
    autocomplete_fields = ("stock",)


@admin.register(PortfolioAsset)
class PortfolioAssetAdmin(admin.ModelAdmin):
    list_display = ("portfolio", "stock", "quantity")
    search_fields = ("portfolio__user__username", "stock__symbol")
    autocomplete_fields = ("stock",)
