# Generated by Django 4.1.5 on 2023-03-04 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hiveadmin', '0004_remove_transaction_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailtenant',
            name='created',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='created',
            field=models.DateField(auto_now_add=True),
        ),
    ]
