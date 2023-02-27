# Generated by Django 4.1.5 on 2023-02-23 08:51

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("wholesalers", "0005_wholesaler_wholesaler_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="wholesaler",
            name="color",
            field=colorfield.fields.ColorField(
                blank=True,
                default=None,
                image_field=None,
                max_length=18,
                null=True,
                samples=None,
            ),
        ),
    ]