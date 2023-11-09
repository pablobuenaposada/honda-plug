# Generated by Django 4.1.3 on 2023-10-18 18:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("part", "0048_image_stocks"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="image",
            name="stock",
        ),
        migrations.AlterField(
            model_name="image",
            name="stocks",
            field=models.ManyToManyField(to="part.stock"),
        ),
    ]