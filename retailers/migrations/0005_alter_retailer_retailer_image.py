# Generated by Django 4.1.5 on 2023-02-16 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("retailers", "0004_retailer_retailer_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="retailer",
            name="retailer_image",
            field=models.ImageField(blank=True, null=True, upload_to=""),
        ),
    ]
