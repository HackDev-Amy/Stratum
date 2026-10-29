# views.py
from rest_framework import generics, views
from rest_framework.response import Response
from .models import BotConfig, BotLog
from .serializers import BotSerializer, BotLogSerializer
from .engine import run_bot_once

class BotListCreateView(generics.ListCreateAPIView):
    serializer_class = BotSerializer
    def get_queryset(self):
        return BotConfig.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BotDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BotSerializer
    def get_queryset(self):
        return BotConfig.objects.filter(user=self.request.user)

class BotRunNowView(views.APIView):
    def post(self, request, pk):
        bot = BotConfig.objects.filter(pk=pk, user=request.user).first()
        if not bot:
            return Response({"error": "not found"}, status=404)
        return Response(run_bot_once(bot))

class BotLogsView(generics.ListAPIView):
    serializer_class = BotLogSerializer
    def get_queryset(self):
        return BotLog.objects.filter(bot__user=self.request.user).order_by("-created_at")[:200]