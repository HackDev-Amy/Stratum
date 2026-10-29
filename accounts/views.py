from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, PortfolioSerializer
from .models import Portfolio

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class PortfolioView(APIView):
    def get(self, request):
        portfolio, _ = Portfolio.objects.get_or_create(user=request.user)
        return Response(PortfolioSerializer(portfolio).data)