from rest_framework import generics
from .models import StrategyConfig
from .serializers import StrategySerializer

class StrategyListCreateView(generics.ListCreateAPIView):
    serializer_class = StrategySerializer
    def get_queryset(self):
        return StrategyConfig.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class StrategyDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StrategySerializer
    def get_queryset(self):
        return StrategyConfig.objects.filter(user=self.request.user)