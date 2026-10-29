# serializers.py
from rest_framework import serializers
from .models import BotConfig, BotLog

class BotSerializer(serializers.ModelSerializer):
    symbol = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = BotConfig
        fields = "__all__"
        read_only_fields = ("user", "last_run", "created_at")

    def create(self, validated_data):
        from market.models import Stock

        symbol = validated_data.pop("symbol").upper()
        stock, _ = Stock.objects.get_or_create(symbol=symbol, defaults={"name": symbol})
        return BotConfig.objects.create(stock=stock, **validated_data)

    def update(self, instance, validated_data):
        from market.models import Stock

        symbol = validated_data.pop("symbol", None)
        if symbol:
            stock, _ = Stock.objects.get_or_create(
                symbol=symbol.upper(), defaults={"name": symbol.upper()}
            )
            instance.stock = stock
        return super().update(instance, validated_data)

class BotLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotLog
        fields = "__all__"