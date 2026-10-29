from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("market", "0001_initial"),
    ]
    operations = [
        migrations.CreateModel(
            name="BotConfig",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("strategy_params", models.JSONField(default=dict)),
                ("risk_params", models.JSONField(default=dict)),
                ("quantity", models.DecimalField(decimal_places=8, default=1, max_digits=20)),
                ("is_active", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_run", models.DateTimeField(blank=True, null=True)),
                ("stock", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="market.stock")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="BotLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("message", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("bot", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="logs", to="bot.botconfig")),
            ],
        ),
    ]
