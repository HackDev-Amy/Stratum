import time
import pytest
from market.rate_limiter import TokenBucket, RetryBackoff


class TestTokenBucket:
    def test_allows_up_to_capacity(self):
        bucket = TokenBucket(rate_per_min=10)
        # Drain capacity
        for _ in range(10):
            assert bucket.acquire() is True

    def test_non_blocking_returns_false_when_empty(self):
        bucket = TokenBucket(rate_per_min=2)
        bucket.acquire(); bucket.acquire()
        assert bucket.acquire(block=False) is False

    def test_refills_over_time(self):
        bucket = TokenBucket(rate_per_min=60)  # 1/s
        for _ in range(60):
            bucket.acquire()
        time.sleep(1.1)
        assert bucket.acquire(block=False) is True


class TestRetryBackoff:
    def test_succeeds_after_retry(self):
        attempts = {"n": 0}
        def flaky():
            attempts["n"] += 1
            if attempts["n"] < 2:
                raise Exception("429 rate limit")
            return "ok"
        r = RetryBackoff(max_retries=3, base=0.01).run(flaky)
        assert r == "ok"
        assert attempts["n"] == 2

    def test_non_rate_error_raises(self):
        def boom():
            raise ValueError("bad input")
        with pytest.raises(ValueError):
            RetryBackoff(max_retries=2, base=0.01).run(boom)
            