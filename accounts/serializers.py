from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Portfolio

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    class Meta:
        model = User
        fields = ("username", "email", "password")
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Portfolio.objects.create(user=user)
        return user

class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ("cash", "created_at")