# Generated by Django 4.1.5 on 2023-02-22 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0013_cart_db_subtotal"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="cart_db", options={"ordering": ["created"]},
        ),
    ]
