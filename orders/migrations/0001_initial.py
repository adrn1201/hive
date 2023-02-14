# Generated by Django 4.1.5 on 2023-02-13 09:45

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("products", "0001_initial"),
        ("retailers", "0003_remove_retailer_is_retailer_and_more"),
        ("wholesalers", "0004_remove_wholesaler_is_retailer_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
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
                    "reference_number",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("business_name", models.CharField(max_length=255)),
                ("total_paid", models.DecimalField(decimal_places=2, max_digits=5)),
                ("mode_of_payment", models.CharField(max_length=255)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("preparing", "Preparing"),
                            ("shipped", "Shipped"),
                            ("confirmed", "Confirmed"),
                        ],
                        max_length=255,
                    ),
                ),
                ("is_received", models.BooleanField(default=False)),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "retailer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="retailers.retailer",
                    ),
                ),
                (
                    "wholesaler",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="wholesalers.wholesaler",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrderItem",
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
                ("price", models.DecimalField(decimal_places=2, max_digits=5)),
                ("quantity", models.PositiveIntegerField(default=1)),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="orders.order",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order_items",
                        to="products.inventory",
                    ),
                ),
            ],
        ),
    ]