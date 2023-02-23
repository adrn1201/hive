# Generated by Django 4.1.5 on 2023-02-21 12:52

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0002_remove_cart_db_size_cart_db_variation"),
    ]

    operations = [
        migrations.RemoveField(model_name="cart_db", name="variation",),
        migrations.AddField(
            model_name="cart_db",
            name="variation_id",
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
    ]
