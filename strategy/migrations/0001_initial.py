from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name="StrategyConfig",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(default="SMA_RSI", max_length=64)),
                ("short_window", models.IntegerField(default=10)),
                ("long_window", models.IntegerField(default=30)),
                ("rsi_period", models.IntegerField(default=14)),
                ("risk_per_trade_pct", models.FloatField(default=1.0)),
                ("stop_loss_pct", models.FloatField(default=2.0)),
                ("take_profit_pct", models.FloatField(default=5.0)),
                ("is_active", models.BooleanField(default=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
