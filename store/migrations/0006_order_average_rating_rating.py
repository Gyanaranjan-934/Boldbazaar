# Generated by Django 4.1.5 on 2023-06-11 14:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("store", "0005_alter_order_phone_profile"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="average_rating",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name="Rating",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "rating",
                    models.IntegerField(
                        blank=True,
                        choices=[
                            (1, "1 - Poor"),
                            (2, "2 - Below average"),
                            (3, "3 - Average"),
                            (4, "4 - Good"),
                            (5, "5 - Excellent"),
                        ],
                        null=True,
                    ),
                ),
                ("review", models.TextField(blank=True, null=True)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="store.product"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]