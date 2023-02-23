# Generated by Django 4.1.5 on 2023-02-23 02:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0035_alter_product_with_variation"),
        ("orders", "0002_alter_orderitem_product"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderitem",
            name="variation",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="products.variation",
            ),
        ),
    ]
