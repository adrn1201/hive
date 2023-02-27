# Generated by Django 4.1.5 on 2023-02-22 05:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0022_rename_actual_stocks_variation_actual_stocks_var_and_more"),
        ("cart", "0009_remove_cart_db_products_cart_db_products"),
    ]

    operations = [
        migrations.RemoveField(model_name="cart_db", name="products",),
        migrations.AddField(
            model_name="cart_db",
            name="products",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="products_cart",
                to="products.product",
            ),
        ),
    ]