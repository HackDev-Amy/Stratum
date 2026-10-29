from rest_framework import serializers
from .models import Order, Transaction, PortfolioAsset
from market.serializers import StockSerializer

class OrderSerializer(serializers.ModelSerializer):
    stock = StockSerializer(read_only=True)
    symbol = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ("user", "status", "filled_price", "created_at", "stock")

class TransactionSerializer(serializers.ModelSerializer):
    stock = StockSerializer(read_only=True)
    class Meta:
        model = Transaction
        fields = "__all__"

class AssetSerializer(serializers.ModelSerializer):
    stock = StockSerializer(read_only=True)
    class Meta:
        model = PortfolioAsset
        fields = "__all__"