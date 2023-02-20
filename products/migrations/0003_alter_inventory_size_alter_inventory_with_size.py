# Generated by Django 4.1.5 on 2023-02-17 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_inventory_with_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='size',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='with_size',
            field=models.BooleanField(blank=True, choices=[('1', 'Yes'), ('0', 'No')], default=0, null=True),
        ),
    ]