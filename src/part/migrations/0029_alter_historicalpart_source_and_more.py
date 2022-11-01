# Generated by Django 4.1 on 2022-11-01 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("part", "0028_alter_historicalpart_source_alter_part_source"),
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
                    ("acuraexpressparts", "www.acuraexpressparts.com"),
                    ("epc-4-00", "EPC 4.00"),
                ],
                max_length=17,
            ),
        ),
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
                    ("clockwise-motion", "www.clockwisemotion.co.uk"),
                    ("hondaspareparts", "www.hondaspareparts.co.uk"),
                    ("pieces-auto-honda", "www.pieces-auto-honda.fr"),
                    ("acuraexpressparts", "www.acuraexpressparts.com"),
                    ("acurapartsforless", "www.acurapartsforless.com"),
                    ("all4honda", "www.a4h-tech.com"),
                ],
                default=None,
                max_length=20,
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
                    ("acuraexpressparts", "www.acuraexpressparts.com"),
                    ("epc-4-00", "EPC 4.00"),
                ],
                max_length=17,
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
                    ("clockwise-motion", "www.clockwisemotion.co.uk"),
                    ("hondaspareparts", "www.hondaspareparts.co.uk"),
                    ("pieces-auto-honda", "www.pieces-auto-honda.fr"),
                    ("acuraexpressparts", "www.acuraexpressparts.com"),
                    ("acurapartsforless", "www.acurapartsforless.com"),
                    ("all4honda", "www.a4h-tech.com"),
                ],
                default=None,
                max_length=20,
            ),
        ),
    ]
