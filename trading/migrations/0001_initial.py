from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("market", "0001_initial"),
        ("accounts", "0001_initial"),
    ]
    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order_type", models.CharField(choices=[("MARKET", "MARKET"), ("LIMIT", "LIMIT"), ("STOP_LOSS", "STOP_LOSS")], default="MARKET", max_length=16)),
                ("side", models.CharField(choices=[("BUY", "BUY"), ("SELL", "SELL")], max_length=4)),
                ("quantity", models.DecimalField(decimal_places=8, max_digits=20)),
                ("price", models.DecimalField(blank=True, decimal_places=4, max_digits=16, null=True)),
                ("trigger_price", models.DecimalField(blank=True, decimal_places=4, max_digits=16, null=True)),
                ("status", models.CharField(choices=[("PENDING", "PENDING"), ("EXECUTED", "EXECUTED"), ("CANCELLED", "CANCELLED"), ("FAILED", "FAILED")], default="PENDING", max_length=12)),
                ("filled_price", models.DecimalField(blank=True, decimal_places=4, max_digits=16, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("stock", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="market.stock")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("side", models.CharField(max_length=4)),
                ("quantity", models.DecimalField(decimal_places=8, max_digits=20)),
                ("price", models.DecimalField(decimal_places=4, max_digits=16)),
                ("commission", models.DecimalField(decimal_places=4, default=0, max_digits=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("stock", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="market.stock")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="PortfolioAsset",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quantity", models.DecimalField(decimal_places=8, default=0, max_digits=20)),
                ("portfolio", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="assets", to="accounts.portfolio")),
                ("stock", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="market.stock")),
            ],
            options={"unique_together": {("portfolio", "stock")}},
        ),
    ]
