# Generated by Django 4.1.5 on 2023-04-07 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hiveadmin', '0004_remove_transaction_expires'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='expires',
            field=models.DateField(blank=True, null=True),
        ),
    ]
