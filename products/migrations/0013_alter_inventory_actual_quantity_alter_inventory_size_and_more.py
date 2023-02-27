# Generated by Django 4.1.5 on 2023-02-20 14:33

from django.db import migrations, models
import separatedvaluesfield.models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0012_merge_20230220_1606"),
    ]

    operations = [
        migrations.AlterField(
            model_name="inventory",
            name="actual_quantity",
            field=separatedvaluesfield.models.SeparatedValuesField(max_length=200),
        ),
        migrations.AlterField(
            model_name="inventory",
            name="size",
            field=separatedvaluesfield.models.SeparatedValuesField(
                blank=True, max_length=200, null=True
            ),
        ),
        migrations.AlterField(
            model_name="inventory",
            name="with_size",
            field=models.BooleanField(
                blank=True, choices=[(1, "Yes"), (0, "No")], null=True
            ),
        ),
    ]