# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('encuestas', '0004_auto_20180412_2056'),
    ]

    operations = [
        migrations.AddField(
            model_name='cultivosanuales',
            name='consumo_animals',
            field=models.FloatField(null=True, verbose_name=b'Consumo animal', blank=True),
        ),
        migrations.RemoveField(
            model_name='condicionesvida',
            name='idioma',
        ),
        migrations.AddField(
            model_name='condicionesvida',
            name='idioma',
            field=models.ManyToManyField(to='encuestas.Idiomas', verbose_name=b'idiomas que habla'),
        ),
        migrations.AlterField(
            model_name='cultivosanuales',
            name='consumo_animal',
            field=models.FloatField(verbose_name=b'Guarda para semilla'),
        ),
        migrations.AlterField(
            model_name='cultivoshuerto',
            name='consumo_animal',
            field=models.FloatField(verbose_name=b'Guarda para semilla'),
        ),
        migrations.AlterField(
            model_name='genero',
            name='actividad',
            field=models.IntegerField(verbose_name=b'Las mujeres de la UPF realizan alguna actividad comunitaria', choices=[(1, b'Si'), (2, b'No')]),
        ),
        migrations.AlterField(
            model_name='usosemilla',
            name='semillas_conseguidas',
            field=models.FloatField(verbose_name=b'4.5.2-Porcentaje de semillas conseguidas en la comunidad'),
        ),
    ]
