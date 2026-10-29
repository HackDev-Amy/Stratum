from django.contrib import admin
from .models import BotConfig, BotLog


@admin.register(BotConfig)
class BotConfigAdmin(admin.ModelAdmin):
    list_display = ("user", "stock", "quantity", "is_active", "last_run")
    list_filter = ("is_active", "created_at")
    search_fields = ("user__username", "stock__symbol")
    readonly_fields = ("created_at", "last_run")


@admin.register(BotLog)
class BotLogAdmin(admin.ModelAdmin):
    list_display = ("bot", "message", "created_at")
    search_fields = ("bot__user__username", "message")
    readonly_fields = ("created_at",)
