# Generated by Django 4.1.5 on 2023-06-11 17:53

from django.db import migrations, models
import store.models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0010_product_product_image1_product_product_image2_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="brand",
            name="brand_image",
            field=models.ImageField(
                blank=True, null=True, upload_to=store.models.get_file_path
            ),
        ),
    ]
