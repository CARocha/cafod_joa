# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('encuestas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='distribucionupf',
            name='manzanas',
            field=models.FloatField(help_text=b'en Ha', verbose_name=b'hect\xc3\xa1reas'),
        ),
        migrations.AlterField(
            model_name='escasezalimentos',
            name='considera',
            field=models.IntegerField(verbose_name=b'4.4-Considera que su familia cuenta siempre con suficiente alimentos producidos en la UPF para consumo diario del hogar?', choices=[(1, b'Si'), (2, b'No')]),
        ),
        migrations.AlterField(
            model_name='usosagua',
            name='uso',
            field=multiselectfield.db.fields.MultiSelectField(max_length=9, verbose_name=b'2.2.3-Indique qu\xc3\xa9 otros usos le dan al agua en la UPF', choices=[(1, b'Uso dom\xc3\xa9stico'), (2, b'Uso agr\xc3\xadcola'), (3, b'Uso tur\xc3\xadstico'), (4, b'Crianza de peces'), (5, b'Para animales')]),
        ),
    ]
