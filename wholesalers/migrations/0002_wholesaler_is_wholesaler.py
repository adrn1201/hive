# Generated by Django 4.1.5 on 2023-02-09 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wholesalers", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="wholesaler",
            name="is_wholesaler",
            field=models.BooleanField(default=True),
        ),
    ]
