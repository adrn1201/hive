# Generated by Django 4.1.5 on 2023-04-06 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hiveadmin', '0002_transaction_expires'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='expires',
            field=models.DateField(blank=True, null=True),
        ),
    ]