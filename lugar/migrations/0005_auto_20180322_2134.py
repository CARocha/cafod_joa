# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lugar', '0004_auto_20161031_1550'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comunidad',
            options={'ordering': ['nombre'], 'verbose_name': 'Provincia', 'verbose_name_plural': 'Provincias'},
        ),
        migrations.AlterModelOptions(
            name='microcuenca',
            options={'ordering': ['nombre'], 'verbose_name': 'Comunidad/Cant\xf3n', 'verbose_name_plural': 'Comunidades/Cantones'},
        ),
    ]
