from django.urls import path
from . import views

urlpatterns = [
    path("configs/", views.StrategyListCreateView.as_view()),
    path("configs/<int:pk>/", views.StrategyDetailView.as_view()),
]