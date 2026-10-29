from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
import redis


def health(request):
    """Liveness probe — returns 200 if the process is alive."""
    return JsonResponse({"status": "ok"})


def readiness(request):
    """Readiness probe — checks DB + Redis."""
    checks = {}
    ok = True

    try:
        with connection.cursor() as c:
            c.execute("SELECT 1")
        checks["database"] = "ok"
    except Exception as e:
        checks["database"] = str(e)
        ok = False

    try:
        cache.set("_ping", 1, 5)
        assert cache.get("_ping") == 1
        checks["redis"] = "ok"
    except Exception as e:
        checks["redis"] = str(e)
        ok = False

    return JsonResponse(
        {"status": "ready" if ok else "degraded", "checks": checks},
        status=200 if ok else 503,
    )
