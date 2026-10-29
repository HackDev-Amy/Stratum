# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Stock
from .serializers import StockSerializer
from .services import FinancialDataService, InfluxService

class StockListView(generics.ListCreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

class QuoteView(APIView):
    def get(self, request, symbol):
        q = FinancialDataService.fetch_quote(symbol.upper())
        return Response(q or {"error": "not found"}, status=200 if q else 404)

class HistoryView(APIView):
    def get(self, request, symbol):
        df = FinancialDataService.fetch_history(symbol.upper(), period="5d", interval="5m")
        if df.empty:
            # try InfluxDB as fallback
            df = InfluxService.query_history(symbol.upper())
        return Response(df.reset_index().to_dict("records") if not df.empty else [])