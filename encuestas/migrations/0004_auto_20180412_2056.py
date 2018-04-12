# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('encuestas', '0003_auto_20180406_0353'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='distribucionupf',
            options={'verbose_name_plural': 'Ditribuci\xf3n de la tierra en la UPF'},
        ),
        migrations.RemoveField(
            model_name='cultivosanuales',
            name='area_cosechada',
        ),
        migrations.RemoveField(
            model_name='cultivoshuerto',
            name='area_cosechada',
        ),
        migrations.AlterField(
            model_name='condicionesvida',
            name='escolaridad',
            field=models.IntegerField(choices=[(1, b'Ning\xc3\xban estudio'), (2, b'Primaria incompleta'), (3, b'Primaria completa'), (4, b'Secundaria incompleta'), (5, b'Secundaria completa (o bachiller)'), (6, b'carrera universitarios incompleta'), (7, b'carrera universitaria completa')]),
        ),
        migrations.AlterField(
            model_name='cultivos',
            name='unidad_medida',
            field=models.IntegerField(choices=[(1, b'Quintal(100kg)'), (2, b'Libras'), (3, b'Docena'), (4, b'Cien'), (5, b'Cabeza'), (6, b'Litro'), (7, b'Unidad'), (8, b'Kilo')]),
        ),
        migrations.AlterField(
            model_name='cultivosanuales',
            name='consumo_animal',
            field=models.FloatField(verbose_name=b'Semilla'),
        ),
        migrations.AlterField(
            model_name='cultivoshuerto',
            name='consumo_animal',
            field=models.FloatField(verbose_name=b'Semilla'),
        ),
        migrations.AlterField(
            model_name='cultivoshuertos',
            name='unidad_medida',
            field=models.IntegerField(choices=[(1, b'Quintal(100kg)'), (2, b'Libras'), (3, b'Docena'), (4, b'Cien'), (5, b'Cabeza'), (6, b'Litro'), (7, b'Unidad'), (8, b'Kilo')]),
        ),
        migrations.AlterField(
            model_name='detallemiembros',
            name='cantidad_dependen',
            field=models.IntegerField(verbose_name=b'1.5-\xc2\xbfCu\xc3\xa1ntas personas dependen economicamente del encuestado/a?'),
        ),
        migrations.AlterField(
            model_name='duenosi',
            name='si',
            field=models.IntegerField(choices=[(1, b'A nombre del hombre'), (2, b'A nombre de la mujer'), (3, b'A nombre de ambos'), (4, b'A nombre de los hijos'), (5, b'A nombre de los hijas'), (6, b'A nombre de padres'), (7, b'A nombre de otros')]),
        ),
        migrations.AlterField(
            model_name='escasezalimentos',
            name='agricola',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, max_length=9, null=True, verbose_name=b'Razones agr\xc3\xadcolas', choices=[(b'A', b'Falta o perdida de semilla'), (b'B', b'Mala calidad de la semilla'), (b'C', b'Falta de riego'), (b'D', b'Poca Tierra o baja fertilidad'), (b'E', b'Plagas y enfermedades')]),
        ),
        migrations.AlterField(
            model_name='escasezalimentos',
            name='considera',
            field=models.IntegerField(verbose_name=b'4.4-Si no cuenta siempre con suficientes alimentos, indicar las principales razones', choices=[(1, b'Si'), (2, b'No')]),
        ),
        migrations.AlterField(
            model_name='escasezalimentos',
            name='economica',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, max_length=7, null=True, verbose_name=b'Razones econ\xc3\xb3micas', choices=[(b'A', b'Bajo precio de sus productos  agr\xc3\xadcolas en el mercado'), (b'B', b'Falta de mercado'), (b'C', b'Falta de credito'), (b'D', b'Falta de mano de obra')]),
        ),
        migrations.AlterField(
            model_name='escasezalimentos',
            name='fenomeno',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, max_length=9, null=True, verbose_name=b'Fen\xc3\xb3menos naturales', choices=[(b'A', b'Sequ\xc3\xada'), (b'B', b'Inundaci\xc3\xb3n'), (b'C', b'Deslizamiento'), (b'D', b'Incendios'), (b'E', b'Heladas/Granizo')]),
        ),
        migrations.AlterField(
            model_name='frutas',
            name='unidad_medida',
            field=models.IntegerField(choices=[(1, b'Quintal(100kg)'), (2, b'Libras'), (3, b'Docena'), (4, b'Cien'), (5, b'Cabeza'), (6, b'Litro'), (7, b'Unidad'), (8, b'Kilo')]),
        ),
        migrations.AlterField(
            model_name='organizacionsocialproductiva',
            name='cuales_beneficios',
            field=models.ManyToManyField(to='encuestas.BeneficiosOrganizados', verbose_name=b'3.1.2-\xc2\xbfPor qu\xc3\xa9 decidi\xc3\xb3 integrar estas organizaciones?', blank=True),
        ),
        migrations.AlterField(
            model_name='seguridadalimentaria',
            name='escasez',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, max_length=15, null=True, verbose_name=b'4.3-Qu\xc3\xa9 es lo que hace cuando hay escasez de alimentos en la familia', choices=[(b'A', b'Busca trabajo fuera de la UPF'), (b'B', b'Recibe remesas familiares'), (b'C', b'Se endeuda'), (b'D', b'Vende alg\xc3\xban bien'), (b'E', b'Pide donaci\xc3\xb3n de alimentos al estado o iglesia'), (b'F', b'Pide alimentos a familiares'), (b'G', b'Pasa hambre'), (b'H', b'Trueque de productos')]),
        ),
        migrations.AlterField(
            model_name='usosemilla',
            name='compradas_agroservicio',
            field=models.FloatField(verbose_name=b'4.5.2-Compradas en un agroservicio'),
        ),
        migrations.AlterField(
            model_name='usosemilla',
            name='tipo_semilla',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, max_length=5, null=True, verbose_name=b'4.5.1-Tipos de semilla usadas en UPF', choices=[(b'A', b'Nativas'), (b'B', b'Acriolladas'), (b'C', b'Mejoradas/certificadas')]),
        ),
    ]
