from rest_framework import serializers
from .models import StrategyConfig

class StrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = StrategyConfig
        fields = "__all__"
        read_only_fields = ("user",)