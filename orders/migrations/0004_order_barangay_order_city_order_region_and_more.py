# Generated by Django 4.1.5 on 2023-03-15 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_order_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='barangay',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='city',
            field=models.CharField(default='Zamboanga City', editable=False, max_length=255),
        ),
        migrations.AddField(
            model_name='order',
            name='region',
            field=models.CharField(default='Zamboanga Peninsula', editable=False, max_length=255),
        ),
        migrations.AlterField(
            model_name='order',
            name='business_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
