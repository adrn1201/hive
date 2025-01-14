# Generated by Django 4.1.5 on 2023-04-07 00:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hiveadmin', '0003_alter_transaction_expires'),
        ('wholesalers', '0003_remove_wholesaler_reference_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='wholesaler',
            name='expires',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wholesaler',
            name='transaction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hiveadmin.transaction'),
        ),
    ]
