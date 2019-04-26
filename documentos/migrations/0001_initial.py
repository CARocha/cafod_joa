# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lugar', '0006_auto_20180322_2235'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubirArchivos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre_documento', models.CharField(max_length=250)),
                ('tema', models.CharField(max_length=250)),
                ('descripcion', models.TextField(null=True, blank=True)),
                ('archivo', models.FileField(upload_to=b'documentos/')),
                ('pais', models.ForeignKey(to='lugar.Pais')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
