import time
from threading import Lock


class TokenBucket:
    def __init__(self, rate_per_min, capacity=None):
        self.rate = rate_per_min / 60.0
        self.capacity = float(capacity or rate_per_min)
        self.tokens = self.capacity
        self.updated_at = time.monotonic()
        self.lock = Lock()

    def _refill(self):
        now = time.monotonic()
        self.tokens = min(
            self.capacity, self.tokens + (now - self.updated_at) * self.rate
        )
        self.updated_at = now

    def acquire(self, block=True):
        while True:
            with self.lock:
                self._refill()
                if self.tokens >= 1:
                    self.tokens -= 1
                    return True
            if not block:
                return False
            time.sleep(max(0.01, 1 / self.rate))


class RetryBackoff:
    def __init__(self, max_retries=3, base=0.5):
        self.max_retries = max_retries
        self.base = base

    def run(self, function, *args, **kwargs):
        for attempt in range(self.max_retries + 1):
            try:
                return function(*args, **kwargs)
            except Exception as exc:
                if "rate limit" not in str(exc).lower() or attempt >= self.max_retries:
                    raise
                time.sleep(self.base * (2**attempt))
