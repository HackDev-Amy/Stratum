# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.BotListCreateView.as_view()),
    path("<int:pk>/", views.BotDetailView.as_view()),
    path("<int:pk>/run/", views.BotRunNowView.as_view()),
    path("logs/", views.BotLogsView.as_view()),
]