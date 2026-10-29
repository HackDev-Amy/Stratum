from django.urls import path
from . import views

urlpatterns = [
    path("orders/market/", views.MarketOrderView.as_view()),
    path("orders/advanced/", views.AdvancedOrderView.as_view()),
    path("orders/", views.OrderListView.as_view()),
    path("orders/<int:pk>/cancel/", views.CancelOrderView.as_view()),
    path("transactions/", views.TransactionListView.as_view()),
    path("portfolio/", views.PortfolioDetailView.as_view()),
]