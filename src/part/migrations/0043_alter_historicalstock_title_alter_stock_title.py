# Generated by Django 4.1.3 on 2023-07-18 20:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("part", "0042_alter_historicalstock_url_alter_stock_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalstock",
            name="title",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="stock",
            name="title",
            field=models.CharField(max_length=100),
        ),
    ]
