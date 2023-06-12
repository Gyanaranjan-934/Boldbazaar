# Generated by Django 4.1.5 on 2023-06-11 15:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0007_remove_order_average_rating_product_average_rating"),
    ]

    operations = [
        migrations.AddField(
            model_name="rating",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="rating",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]