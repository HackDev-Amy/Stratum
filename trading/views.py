from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from .models import Order, Transaction, PortfolioAsset
from .serializers import OrderSerializer, TransactionSerializer, AssetSerializer
from .services import TradingService
from core.exceptions import AppError


class MarketOrderView(APIView):
    def post(self, request):
        symbol = request.data.get("symbol")
        side = request.data.get("side", "").upper()
        try:
            qty = Decimal(str(request.data.get("quantity", 0)))
        except Exception:
            raise AppError("Invalid quantity")
        if side not in ("BUY", "SELL") or qty <= 0:
            raise AppError("Invalid side or quantity")
        order = TradingService.place_market_order(request.user, symbol, side, qty)
        return Response(OrderSerializer(order).data)


class AdvancedOrderView(APIView):
    def post(self, request):
        d = request.data
        order = TradingService.place_limit_or_stop(
            request.user, d["symbol"], d["side"].upper(),
            Decimal(str(d["quantity"])), d["order_type"],
            Decimal(str(d["trigger_price"])),
        )
        return Response(OrderSerializer(order).data)


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).select_related("stock")


class CancelOrderView(APIView):
    def post(self, request, pk):
        o = Order.objects.filter(pk=pk, user=request.user, status="PENDING").first()
        if not o:
            raise AppError("Order not found or not cancellable", code="not_cancellable", status=404)
        o.status = "CANCELLED"
        o.save()
        return Response({"ok": True})


class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).select_related("stock")


class PortfolioDetailView(APIView):
    def get(self, request):
        cache_key = f"portfolio:{request.user.id}"
        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        p = request.user.portfolio
        assets = PortfolioAsset.objects.filter(portfolio=p).select_related("stock")
        total = float(p.cash)
        out = []
        for a in assets:
            a_data = AssetSerializer(a).data
            mv = float(a.quantity) * float(a.stock.last_price)
            a_data["market_value"] = mv
            total += mv
            out.append(a_data)
        payload = {"cash": float(p.cash), "assets": out, "total_value": total}
        cache.set(cache_key, payload, 5)
        return Response(payload)


from django.core.cache import cache