# Generated by Django 4.1.5 on 2023-04-07 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hiveadmin', '0005_transaction_expires'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='expires',
        ),
    ]