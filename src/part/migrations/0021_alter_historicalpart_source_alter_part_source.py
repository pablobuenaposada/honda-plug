# Generated by Django 4.1 on 2022-08-30 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("part", "0020_alter_historicalpart_source_alter_part_source"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalpart",
            name="source",
            field=models.CharField(
                choices=[
                    ("epc-data", "www.epc-data.com"),
                    ("amayama", "www.amayama.com"),
                    ("clockwise-motion", "www.clockwisemotion.co.uk"),
                    ("unknown", "Unknown"),
                    ("pieces-auto-honda", "www.pieces-auto-honda.fr"),
                    ("hondapartsonline", "www.hondapartsonline.net"),
                ],
                max_length=17,
            ),
        ),
        migrations.AlterField(
            model_name="part",
            name="source",
            field=models.CharField(
                choices=[
                    ("epc-data", "www.epc-data.com"),
                    ("amayama", "www.amayama.com"),
                    ("clockwise-motion", "www.clockwisemotion.co.uk"),
                    ("unknown", "Unknown"),
                    ("pieces-auto-honda", "www.pieces-auto-honda.fr"),
                    ("hondapartsonline", "www.hondapartsonline.net"),
                ],
                max_length=17,
            ),
        ),
    ]
