import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from accounts.models import Portfolio

User = get_user_model()

@pytest.mark.django_db
class TestAuth:
    def test_register_creates_portfolio(self):
        c = APIClient()
        r = c.post("/api/auth/register/",
                   {"username": "bob", "password": "secret1"},
                   format="json")
        assert r.status_code == 201
        u = User.objects.get(username="bob")
        assert Portfolio.objects.filter(user=u).exists()

    def test_login_returns_tokens(self):
        User.objects.create_user("eve", password="pw12345")
        c = APIClient()
        r = c.post("/api/auth/login/",
                   {"username": "eve", "password": "pw12345"},
                   format="json")
        assert r.status_code == 200
        assert "access" in r.data
        assert "refresh" in r.data