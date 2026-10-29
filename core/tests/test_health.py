import pytest
from django.test import Client

@pytest.mark.django_db
def test_health_returns_200():
    r = Client().get("/health/")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

@pytest.mark.django_db
def test_readiness_returns_200():
    r = Client().get("/ready/")
    assert r.status_code == 200
    assert r.json()["checks"]["database"] == "ok"