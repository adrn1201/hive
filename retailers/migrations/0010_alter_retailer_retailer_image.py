# Generated by Django 4.1.5 on 2023-02-20 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("retailers", "0009_alter_retailer_retailer_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="retailer",
            name="retailer_image",
            field=models.ImageField(
                default="products/default.jpg", upload_to="products/"
            ),
        ),
    ]
