from django.core.management.base import BaseCommand
from market.models import Stock

DEFAULT = [
    ("AAPL", "Apple Inc."), ("MSFT", "Microsoft"),
    ("GOOGL", "Alphabet"), ("TSLA", "Tesla"),
    ("NVDA", "NVIDIA"), ("AMZN", "Amazon"),
    ("META", "Meta"), ("BTC-USD", "Bitcoin"),
    ("ETH-USD", "Ethereum"),
]

class Command(BaseCommand):
    help = "Seed default stocks"
    def handle(self, *args, **opts):
        for sym, name in DEFAULT:
            Stock.objects.get_or_create(symbol=sym, defaults={"name": name})
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(DEFAULT)} stocks"))