from django.urls import path
from .views import BacktestView

urlpatterns = [path("run/", BacktestView.as_view())]