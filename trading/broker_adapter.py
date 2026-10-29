import os

import requests
from django.conf import settings


class SimulatedAdapter:
    def buy(self, symbol, quantity):
        return {"status": "simulated", "side": "buy", "symbol": symbol, "qty": quantity}

    def sell(self, symbol, quantity):
        return {"status": "simulated", "side": "sell", "symbol": symbol, "qty": quantity}


class AlpacaPaperAdapter:
    def __init__(self):
        self.base_url = os.getenv(
            "ALPACA_BASE_URL", "https://paper-api.alpaca.markets"
        ).rstrip("/")
        self.headers = {
            "APCA-API-KEY-ID": os.getenv("ALPACA_API_KEY", ""),
            "APCA-API-SECRET-KEY": os.getenv("ALPACA_SECRET_KEY", ""),
        }

    def _submit(self, symbol, quantity, side):
        response = requests.post(
            f"{self.base_url}/v2/orders",
            headers=self.headers,
            json={
                "symbol": symbol,
                "qty": str(quantity),
                "side": side,
                "type": "market",
                "time_in_force": "day",
            },
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def buy(self, symbol, quantity):
        return self._submit(symbol, quantity, "buy")

    def sell(self, symbol, quantity):
        return self._submit(symbol, quantity, "sell")


def get_broker():
    if (
        os.getenv("BROKER", "simulated").lower() == "alpaca"
        and os.getenv("ALPACA_API_KEY")
        and os.getenv("ALPACA_SECRET_KEY")
    ):
        return AlpacaPaperAdapter()
    return SimulatedAdapter()
