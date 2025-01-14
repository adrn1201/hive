# Generated by Django 4.1.5 on 2023-03-17 03:51

from django.db import migrations, models
import django.db.models.deletion
import products.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wholesalers", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("name", models.CharField(max_length=200, unique=True)),
                ("sold", models.IntegerField(default=0)),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        primary_key=True,
                        serialize=False,
                        unique=True,
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
            options={"verbose_name_plural": "Categories",},
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("product_name", models.CharField(max_length=200)),
                (
                    "actual_stocks",
                    models.IntegerField(blank=True, default=0, null=True),
                ),
                ("tempo_stocks", models.IntegerField(blank=True, default=0, null=True)),
                (
                    "price",
                    models.FloatField(
                        error_messages={"invalid": "Please enter a valid price."},
                        validators=[products.models.positive_validator],
                    ),
                ),
                (
                    "with_variation",
                    models.BooleanField(choices=[(1, "Yes"), (0, "No")]),
                ),
                ("sold", models.IntegerField(default=0)),
                ("description", models.TextField(max_length=200)),
                (
                    "min_orders",
                    models.IntegerField(
                        default=models.IntegerField(blank=True, default=0, null=True)
                    ),
                ),
                (
                    "product_image",
                    models.ImageField(
                        default="products/default.jpg", upload_to="products/"
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("analytics_date", models.DateField(blank=True, null=True)),
                (
                    "id",
                    models.CharField(
                        max_length=5, primary_key=True, serialize=False, unique=True
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="products",
                        to="products.category",
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
            options={"verbose_name_plural": "Products", "ordering": ["-created"],},
        ),
        migrations.CreateModel(
            name="Variation",
            fields=[
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                ("actual_stocks_var", models.IntegerField(default=0)),
                (
                    "tempo_stocks_var",
                    models.IntegerField(blank=True, default=0, null=True),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("analytics_date", models.DateField(blank=True, null=True)),
                (
                    "id",
                    models.CharField(
                        max_length=5, primary_key=True, serialize=False, unique=True
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="products.product",
                    ),
                ),
            ],
            options={"verbose_name_plural": "Sizes", "ordering": ["created"],},
        ),
    ]
