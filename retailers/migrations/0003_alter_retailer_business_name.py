# Generated by Django 4.1.5 on 2023-03-11 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retailers', '0002_retailer_barangay_alter_retailer_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='retailer',
            name='business_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
