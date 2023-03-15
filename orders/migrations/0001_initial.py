# Generated by Django 4.1.5 on 2023-03-15 16:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("products", "0001_initial"),
        ("wholesalers", "0001_initial"),
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
                ("reference_number", models.CharField(blank=True, max_length=120)),
                ("business_name", models.CharField(max_length=255)),
                ("address", models.CharField(blank=True, max_length=255, null=True)),
                ("total_paid", models.FloatField()),
                ("mode_of_payment", models.CharField(max_length=255)),
                ("success", models.BooleanField(default=False, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("preparing", "Preparing"),
                            ("shipped", "Shipped"),
                            ("completed", "Completed"),
                        ],
                        max_length=255,
                    ),
                ),
                ("is_received", models.BooleanField(default=False)),
                ("created", models.DateField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
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
                ("price", models.FloatField()),
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
                        to="products.product",
                    ),
                ),
                (
                    "variation",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.variation",
                    ),
                ),
            ],
        ),
    ]
