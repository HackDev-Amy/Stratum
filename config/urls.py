from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from core.health import health, readiness

api_v1 = [
    path("auth/", include("accounts.urls")),
    path("market/", include("market.urls")),
    path("trading/", include("trading.urls")),
    path("strategy/", include("strategy.urls")),
    path("backtest/", include("backtest.urls")),
    path("bot/", include("bot.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_v1)),
    path("api/v1/", include(api_v1)),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
    path("health/", health),
    path("ready/", readiness),
]