# Generated by Django 4.2.4 on 2023-08-09 14:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stocks", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="stock",
            name="price",
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
