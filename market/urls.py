# urls.py
from django.urls import path
from . import views
urlpatterns = [
    path("stocks/", views.StockListView.as_view()),
    path("stocks/<str:symbol>/history/", views.HistoryView.as_view()),
    path("stocks/<str:symbol>/quote/", views.QuoteView.as_view()),
]