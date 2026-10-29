from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Stock",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("symbol", models.CharField(max_length=16, unique=True)),
                ("name", models.CharField(blank=True, max_length=128)),
                ("last_price", models.DecimalField(decimal_places=4, default=0, max_digits=16)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
