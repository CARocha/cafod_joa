# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import smart_selects.db_fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lugar', '0005_auto_20180322_2134'),
    ]

    operations = [
        migrations.CreateModel(
            name='Encuestadores',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'Encuestador',
                'verbose_name_plural': 'Encuestadores',
            },
        ),
        migrations.CreateModel(
            name='Entrevistados',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=250, verbose_name=b'Nombre Completo')),
                ('cedula', models.CharField(max_length=50, null=True, verbose_name=b'No. C\xc3\xa9dula/DPI', blank=True)),
                ('ocupacion', models.CharField(max_length=150, verbose_name=b'Ocupaci\xc3\xb3n')),
                ('sexo', models.IntegerField(choices=[(1, b'Mujer'), (2, b'Hombre'), (3, b'Ambos')])),
                ('jefe', models.IntegerField(verbose_name=b'Jefe del hogar', choices=[(1, b'Si'), (2, b'No')])),
                ('edad', models.IntegerField()),
                ('latitud', models.FloatField(null=True, blank=True)),
                ('longitud', models.FloatField(null=True, blank=True)),
                ('comunidad', smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'municipio', chained_field=b'municipio', blank=True, auto_choose=True, to='lugar.Comunidad', null=True)),
                ('departamento', smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'pais', chained_field=b'pais', auto_choose=True, to='lugar.Departamento')),
                ('microcuenca', smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'comunidad', chained_field=b'comunidad', blank=True, auto_choose=True, to='lugar.Microcuenca', null=True)),
                ('municipio', smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'departamento', chained_field=b'departamento', auto_choose=True, to='lugar.Municipio')),
                ('pais', models.ForeignKey(to='lugar.Pais')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Base de datos Productor',
                'verbose_name_plural': 'Base de datos Productores',
            },
        ),
        migrations.CreateModel(
            name='OrganizacionResp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=250)),
                ('departamento', smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'pais', to='lugar.Departamento', chained_field=b'pais', null=True, auto_choose=True)),
                ('municipio', smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'departamento', to='lugar.Municipio', chained_field=b'departamento', null=True, auto_choose=True)),
                ('pais', models.ForeignKey(to='lugar.Pais', null=True)),
            ],
            options={
                'verbose_name': 'Organizaci\xf3n responsable',
                'verbose_name_plural': 'Organizaciones responsables',
            },
        ),
    ]
