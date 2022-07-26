# Generated by Django 4.0.6 on 2022-08-07 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("part", "0011_alter_historicalpart_source_alter_part_source"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalstock",
            name="source",
            field=models.CharField(
                choices=[
                    ("hondaautomotiveparts", "www.hondaautomotiveparts.com"),
                    ("hondapartsnow", "www.hondapartsnow.com"),
                    ("hondapartsonline", "www.hondapartsonline.net"),
                    ("tegiwa", "www.tegiwaimports.com"),
                ],
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="stock",
            name="source",
            field=models.CharField(
                choices=[
                    ("hondaautomotiveparts", "www.hondaautomotiveparts.com"),
                    ("hondapartsnow", "www.hondapartsnow.com"),
                    ("hondapartsonline", "www.hondapartsonline.net"),
                    ("tegiwa", "www.tegiwaimports.com"),
                ],
                max_length=20,
            ),
        ),
    ]
