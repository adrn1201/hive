# Generated by Django 4.1.5 on 2023-02-22 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0031_alter_product_with_variation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="with_variation",
            field=models.BooleanField(null=True),
        ),
    ]
