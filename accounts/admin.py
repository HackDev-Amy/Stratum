from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Portfolio

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ("user", "cash", "created_at")