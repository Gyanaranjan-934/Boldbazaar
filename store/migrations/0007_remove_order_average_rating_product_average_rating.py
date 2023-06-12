# Generated by Django 4.1.5 on 2023-06-11 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0006_order_average_rating_rating"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="average_rating",
        ),
        migrations.AddField(
            model_name="product",
            name="average_rating",
            field=models.FloatField(blank=True, null=True),
        ),
    ]