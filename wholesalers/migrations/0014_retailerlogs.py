# Generated by Django 4.1.5 on 2023-03-04 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wholesalers', '0013_alter_wholesaler_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='RetailerLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('retailer', models.CharField(max_length=255)),
                ('action', models.CharField(max_length=255)),
                ('created', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
