# Generated by Django 4.1 on 2022-08-13 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("part", "0014_alter_historicalpart_source_alter_part_source"),
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
                    ("amayama", "www.amayama.com"),
                ],
                default=None,
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
                    ("amayama", "www.amayama.com"),
                ],
                default=None,
                max_length=20,
            ),
        ),
    ]
