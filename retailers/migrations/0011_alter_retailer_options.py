# Generated by Django 4.1.5 on 2023-02-23 07:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("retailers", "0010_alter_retailer_retailer_image"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="retailer", options={"ordering": ["business_name"]},
        ),
    ]
