# Generated by Django 4.1.5 on 2023-03-06 08:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_tenants.postgresql_backend.base


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Wholesaler",
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
                    "schema_name",
                    models.CharField(
                        db_index=True,
                        max_length=63,
                        unique=True,
                        validators=[
                            django_tenants.postgresql_backend.base._check_schema_name
                        ],
                    ),
                ),
                ("business_name", models.CharField(max_length=255)),
                ("address", models.CharField(blank=True, max_length=255)),
                ("region", models.CharField(blank=True, max_length=255)),
                ("city", models.CharField(blank=True, max_length=255)),
                ("contact_name", models.CharField(max_length=255)),
                ("contact_number", models.CharField(max_length=50)),
                ("is_active", models.BooleanField(default=False)),
                ("color", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "wholesaler_image",
                    models.ImageField(
                        default="products/default.jpg", upload_to="products/"
                    ),
                ),
                ("created", models.DateField(auto_now_add=True)),
                (
                    "user",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="Domain",
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
                    "domain",
                    models.CharField(db_index=True, max_length=253, unique=True),
                ),
                ("is_primary", models.BooleanField(db_index=True, default=True)),
                (
                    "tenant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="domains",
                        to="wholesalers.wholesaler",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
    ]
