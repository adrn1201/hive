# Generated by Django 4.1.5 on 2023-02-23 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wholesalers", "0006_wholesaler_color"),
    ]

    operations = [
        migrations.AlterField(
            model_name="wholesaler",
            name="color",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
