# Generated by Django 5.0.1 on 2024-02-03 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("part", "0065_alter_historicalstock_title_alter_stock_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalstock",
            name="title",
            field=models.CharField(blank=True, db_index=True, max_length=200),
        ),
        migrations.AlterField(
            model_name="stock",
            name="title",
            field=models.CharField(blank=True, db_index=True, max_length=200),
        ),
    ]
