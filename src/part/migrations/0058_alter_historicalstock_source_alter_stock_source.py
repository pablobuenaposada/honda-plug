# Generated by Django 4.1.3 on 2023-11-25 11:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("part", "0057_alter_historicalstock_source_alter_stock_source"),
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
                    ("clockwise-motion", "www.clockwisemotion.co.uk"),
                    ("hondaspareparts", "www.hondaspareparts.co.uk"),
                    ("pieces-auto-honda", "www.pieces-auto-honda.fr"),
                    ("acuraexpressparts", "www.acuraexpressparts.com"),
                    ("acurapartsforless", "www.acurapartsforless.com"),
                    ("all4honda", "www.a4h-tech.com"),
                    ("cms", "www.cmsnl.com"),
                    ("nengun", "www.nengun.com"),
                    ("akr", "www.akr-performance.com"),
                    ("online-teile", "www.online-teile.com"),
                    ("japserviceparts", "www.japserviceparts.co.uk"),
                    ("icb", "www.icbmotorsport.com"),
                    ("ipgparts", "www.ipgparts.com"),
                    ("bernardiparts", "www.bernardiparts.com"),
                    ("alvadi", "www.alvadi.ee"),
                    ("rywerksparts", "www.rywerksparts.com"),
                    ("myhondaoemparts", "www.myhondaoemparts.com"),
                    ("hondapartsforless", "www.hondapartsforless.com"),
                    ("oemhondapartswarehouse", "www.oemhondapartswarehouse.com"),
                    ("hondapartsconnection", "www.hondapartsconnection.com"),
                    ("desertcart", "www.desertcart.ae"),
                    ("coxmotorparts", "www.coxmotorparts.co.uk"),
                    ("dreamshop-airport-honda", "dreamshop.honda.com - Airport Honda"),
                    (
                        "dreamshop-airport-marina-honda",
                        "dreamshop.honda.com - Airport Marina Honda",
                    ),
                    (
                        "dreamshop-all-star-honda",
                        "dreamshop.honda.com - All Star Honda",
                    ),
                    (
                        "dreamshop-anderson-honda",
                        "dreamshop.honda.com - Anderson Honda",
                    ),
                    (
                        "dreamshop-antrim-way-honda",
                        "dreamshop.honda.com - Antrim Way Honda",
                    ),
                    ("dreamshop-apple-honda", "dreamshop.honda.com - Apple Honda"),
                    (
                        "dreamshop-apple-tree-honda",
                        "dreamshop.honda.com - Apple Tree Honda",
                    ),
                    (
                        "dreamshop-apple-valley-honda",
                        "dreamshop.honda.com - Apple Valley Honda",
                    ),
                    (
                        "dreamshop-arrowhead-honda",
                        "dreamshop.honda.com - Arrowhead Honda",
                    ),
                    (
                        "dreamshop-ascension-honda",
                        "dreamshop.honda.com - Ascension Honda",
                    ),
                    ("dreamshop-atamian-honda", "dreamshop.honda.com - Atamian Honda"),
                    (
                        "dreamshop-atlantic-honda",
                        "dreamshop.honda.com - Atlantic Honda",
                    ),
                    ("dreamshop-auburn-honda", "dreamshop.honda.com - Auburn Honda"),
                    (
                        "dreamshop-autonation-honda-104",
                        "dreamshop.honda.com - AutoNation Honda 104",
                    ),
                    (
                        "dreamshop-autonation-honda-385",
                        "dreamshop.honda.com - AutoNation Honda 385",
                    ),
                    (
                        "dreamshop-autonation-honda-bel-air-mall",
                        "dreamshop.honda.com - AutoNation Honda at Bel Air Mall",
                    ),
                    (
                        "dreamshop-autonation-honda-chandler",
                        "dreamshop.honda.com - AutoNation Honda Chandler",
                    ),
                    (
                        "dreamshop-autonation-honda-clearwater",
                        "dreamshop.honda.com - AutoNation Honda Clearwater",
                    ),
                    (
                        "dreamshop-autonation-honda-columbus",
                        "dreamshop.honda.com - AutoNation Honda Columbus",
                    ),
                    (
                        "dreamshop-autonation-honda-costa-mesa",
                        "dreamshop.honda.com - AutoNation Honda Costa Mesa",
                    ),
                    (
                        "dreamshop-autonation-covington-pike",
                        "dreamshop.honda.com - AutoNation Honda Covington Pike",
                    ),
                ],
                db_index=True,
                max_length=39,
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
                    ("cms", "www.cmsnl.com"),
                    ("nengun", "www.nengun.com"),
                    ("akr", "www.akr-performance.com"),
                    ("online-teile", "www.online-teile.com"),
                    ("japserviceparts", "www.japserviceparts.co.uk"),
                    ("icb", "www.icbmotorsport.com"),
                    ("ipgparts", "www.ipgparts.com"),
                    ("bernardiparts", "www.bernardiparts.com"),
                    ("alvadi", "www.alvadi.ee"),
                    ("rywerksparts", "www.rywerksparts.com"),
                    ("myhondaoemparts", "www.myhondaoemparts.com"),
                    ("hondapartsforless", "www.hondapartsforless.com"),
                    ("oemhondapartswarehouse", "www.oemhondapartswarehouse.com"),
                    ("hondapartsconnection", "www.hondapartsconnection.com"),
                    ("desertcart", "www.desertcart.ae"),
                    ("coxmotorparts", "www.coxmotorparts.co.uk"),
                    ("dreamshop-airport-honda", "dreamshop.honda.com - Airport Honda"),
                    (
                        "dreamshop-airport-marina-honda",
                        "dreamshop.honda.com - Airport Marina Honda",
                    ),
                    (
                        "dreamshop-all-star-honda",
                        "dreamshop.honda.com - All Star Honda",
                    ),
                    (
                        "dreamshop-anderson-honda",
                        "dreamshop.honda.com - Anderson Honda",
                    ),
                    (
                        "dreamshop-antrim-way-honda",
                        "dreamshop.honda.com - Antrim Way Honda",
                    ),
                    ("dreamshop-apple-honda", "dreamshop.honda.com - Apple Honda"),
                    (
                        "dreamshop-apple-tree-honda",
                        "dreamshop.honda.com - Apple Tree Honda",
                    ),
                    (
                        "dreamshop-apple-valley-honda",
                        "dreamshop.honda.com - Apple Valley Honda",
                    ),
                    (
                        "dreamshop-arrowhead-honda",
                        "dreamshop.honda.com - Arrowhead Honda",
                    ),
                    (
                        "dreamshop-ascension-honda",
                        "dreamshop.honda.com - Ascension Honda",
                    ),
                    ("dreamshop-atamian-honda", "dreamshop.honda.com - Atamian Honda"),
                    (
                        "dreamshop-atlantic-honda",
                        "dreamshop.honda.com - Atlantic Honda",
                    ),
                    ("dreamshop-auburn-honda", "dreamshop.honda.com - Auburn Honda"),
                    (
                        "dreamshop-autonation-honda-104",
                        "dreamshop.honda.com - AutoNation Honda 104",
                    ),
                    (
                        "dreamshop-autonation-honda-385",
                        "dreamshop.honda.com - AutoNation Honda 385",
                    ),
                    (
                        "dreamshop-autonation-honda-bel-air-mall",
                        "dreamshop.honda.com - AutoNation Honda at Bel Air Mall",
                    ),
                    (
                        "dreamshop-autonation-honda-chandler",
                        "dreamshop.honda.com - AutoNation Honda Chandler",
                    ),
                    (
                        "dreamshop-autonation-honda-clearwater",
                        "dreamshop.honda.com - AutoNation Honda Clearwater",
                    ),
                    (
                        "dreamshop-autonation-honda-columbus",
                        "dreamshop.honda.com - AutoNation Honda Columbus",
                    ),
                    (
                        "dreamshop-autonation-honda-costa-mesa",
                        "dreamshop.honda.com - AutoNation Honda Costa Mesa",
                    ),
                    (
                        "dreamshop-autonation-covington-pike",
                        "dreamshop.honda.com - AutoNation Honda Covington Pike",
                    ),
                ],
                db_index=True,
                max_length=39,
            ),
        ),
    ]
