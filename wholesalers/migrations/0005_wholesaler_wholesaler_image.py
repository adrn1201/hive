# Generated by Django 4.1.5 on 2023-02-22 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wholesalers', '0004_remove_wholesaler_is_retailer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='wholesaler',
            name='wholesaler_image',
            field=models.ImageField(default='products/default.jpg', upload_to='products/'),
        ),
    ]
