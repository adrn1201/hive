# Generated by Django 4.1.5 on 2023-04-08 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wholesalers', '0012_wholesaler_expiry_date_wholesaler_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='wholesaler',
            name='transaction_status',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
