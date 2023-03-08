# Generated by Django 4.1.5 on 2023-03-06 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminRetailerLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wholesaler', models.CharField(max_length=255)),
                ('retailer', models.CharField(max_length=255)),
                ('domain', models.CharField(max_length=255)),
                ('action', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='AdminWholesalerLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wholesaler', models.CharField(max_length=255)),
                ('domain', models.CharField(max_length=255)),
                ('action', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmailTenant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=255)),
                ('status', models.BooleanField(default=False)),
                ('created', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_number', models.CharField(blank=True, max_length=120)),
                ('business_name', models.CharField(max_length=255)),
                ('payment_method', models.CharField(max_length=255)),
                ('amount', models.FloatField()),
                ('payment_status', models.CharField(max_length=255)),
                ('subscription_id', models.CharField(blank=True, max_length=255, null=True)),
                ('created', models.DateField(auto_now_add=True)),
            ],
        ),
    ]