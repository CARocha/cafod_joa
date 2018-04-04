# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields
import multiselectfield.db.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lugar', '0006_auto_20180322_2235'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccesoAgua',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name_plural': '2.2.1-Indique la forma que accede al agua para consumo humano',
            },
        ),
        migrations.CreateModel(
            name='AguaConsumo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'Agua para consumo',
                'verbose_name_plural': 'Agua para consumo',
            },
        ),
        migrations.CreateModel(
            name='Animales',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=4)),
                ('nombre', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name_plural': 'Codigo animales',
            },
        ),
        migrations.CreateModel(
            name='BeneficiosOrganizados',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name_plural': 'Beneficios de estar organizado',
            },
        ),
        migrations.CreateModel(
            name='CondicionesVida',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parentesco', models.IntegerField(choices=[(1, b'Esposo'), (2, b'Esposa'), (3, b'Hijo'), (4, b'Hija'), (5, b'Suegra'), (6, b'Suegro'), (7, b'Tia'), (8, b'Tio'), (9, b'Pariente'), (10, b'Otro')])),
                ('sexo', models.IntegerField(choices=[(1, b'Mujer'), (2, b'Hombre')])),
                ('edad', models.IntegerField()),
                ('escolaridad', models.IntegerField(choices=[(1, b'Ning\xc3\xban estudio'), (2, b'Primaria incompleta'), (3, b'Primaria completa'), (4, b'Secundaria incompleta'), (5, b'Secundaria completa (o bachiller)'), (6, b'\xe2\x80\x9c1\xe2\x80\x9d a\xc3\xb1os de carrera universitaria'), (7, b'\xe2\x80\x9c2\xe2\x80\x9d a\xc3\xb1os de carrera universitaria'), (8, b'\xe2\x80\x9c3\xe2\x80\x9d a\xc3\xb1os de carrera universitaria'), (9, b'\xe2\x80\x9c4\xe2\x80\x9d a\xc3\xb1os de carrera universitaria'), (10, b'5\xe2\x80\x9d a\xc3\xb1os de carrera universitaria')])),
            ],
            options={
                'verbose_name_plural': '2.1- Indicar la cantidad de miembros de la familia y su escolaridad',
            },
        ),
        migrations.CreateModel(
            name='Cultivos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=4)),
                ('nombre', models.CharField(max_length=250)),
                ('unidad_medida', models.IntegerField(choices=[(1, b'Quintal'), (2, b'Libras'), (3, b'Docena'), (4, b'Cien'), (5, b'Cabeza'), (6, b'Litro'), (7, b'Unidad')])),
                ('calorias', models.FloatField(null=True, blank=True)),
                ('proteinas', models.FloatField(null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Codigo cultivos anuales',
            },
        ),
        migrations.CreateModel(
            name='CultivosAnuales',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('area_sembrada', models.FloatField(verbose_name=b'Area sembrada (Ha)')),
                ('area_cosechada', models.FloatField(verbose_name=b'Area cosechada (Ha)')),
                ('cantidad_cosechada', models.FloatField()),
                ('consumo_familia', models.FloatField(verbose_name=b'Consumo de la familia')),
                ('consumo_animal', models.FloatField()),
                ('venta', models.FloatField()),
                ('cultivo', models.ForeignKey(to='encuestas.Cultivos')),
            ],
            options={
                'verbose_name_plural': '3.2.3-Cultivos anuales (5 principales) producido en la UPF',
            },
        ),
        migrations.CreateModel(
            name='CultivosHuerto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('area_sembrada', models.FloatField(verbose_name=b'Area sembrada (Ha)')),
                ('area_cosechada', models.FloatField(verbose_name=b'Area cosechada (Ha)')),
                ('cantidad_cosechada', models.FloatField()),
                ('consumo_familia', models.FloatField(verbose_name=b'Consumo de la familia')),
                ('consumo_animal', models.FloatField()),
                ('venta', models.FloatField()),
            ],
            options={
                'verbose_name_plural': '3.2.4-Cultivos de huertos (5 principales) en la UPF',
            },
        ),
        migrations.CreateModel(
            name='CultivosHuertos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=4)),
                ('nombre', models.CharField(max_length=250)),
                ('unidad_medida', models.IntegerField(choices=[(1, b'Quintal'), (2, b'Libras'), (3, b'Docena'), (4, b'Cien'), (5, b'Cabeza'), (6, b'Litro'), (7, b'Unidad')])),
                ('calorias', models.FloatField(null=True, blank=True)),
                ('proteinas', models.FloatField(null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Codigo cultivos de huertos',
            },
        ),
        migrations.CreateModel(
            name='Descripcion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('area', models.FloatField(verbose_name=b'3.2.1-Cu\xc3\xa1l es el \xc3\xa1rea aproximada de la UPF?')),
            ],
            options={
                'verbose_name_plural': 'Distribuci\xf3n de la UPF',
            },
        ),
        migrations.CreateModel(
            name='DetalleMiembros',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('decisiones', models.IntegerField(verbose_name=b'1.3-\xc2\xbfQui\xc3\xa9n toma las decisiones en la UPF', choices=[(1, b'Esposo'), (2, b'Esposa'), (3, b'Padre'), (4, b'Madre'), (5, b'Ambos'), (6, b'Hijos'), (7, b'La familia en conjunto')])),
                ('cantidad', models.IntegerField(verbose_name=b'1.4-Cantidad de personas que habitan en el hogar')),
                ('cantidad_dependen', models.IntegerField(verbose_name=b'1.5-Cantidad de personas que dependen economicamente en la UPF')),
            ],
            options={
                'verbose_name_plural': '',
            },
        ),
        migrations.CreateModel(
            name='DisponibilidadAgua',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('disponibilidad', models.IntegerField(choices=[(1, b'Todo el tiempo'), (2, b'Ocacionalmente'), (3, b'Casi nunca'), (4, b'Solo \xc3\xa9poca lluviosa')])),
            ],
            options={
                'verbose_name_plural': '2.2.2-Mencione la disponibilidad del agua para consumo humano)',
            },
        ),
        migrations.CreateModel(
            name='Distribucionupf',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tierra', models.IntegerField(verbose_name=b'3.2.2-Distribuci\xc3\xb3n de la tierra en la UPF', choices=[(1, b'Bosque natural'), (2, b'Potrero y pastos'), (3, b'Plantaci\xc3\xb3n forestal'), (4, b'Cultivos anuales'), (5, b'Cultivos perennes'), (6, b'Huertos')])),
                ('manzanas', models.FloatField(help_text=b'en Ha')),
            ],
        ),
        migrations.CreateModel(
            name='DuenoNo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('no', models.IntegerField(choices=[(1, b'Arrendada'), (2, b'Promesa de venta'), (3, b'Prestada'), (4, b'Tierra Ind\xc3\xadgena/Comunal'), (5, b'Sin escritura'), (6, b'Colectivo/Cooperativa')])),
            ],
            options={
                'verbose_name_plural': '1.2.2-En el caso que diga NO, especifique la situaci\xf3n',
            },
        ),
        migrations.CreateModel(
            name='DuenoSi',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('si', models.IntegerField(choices=[(1, b'A nombre del hombre'), (2, b'A nombre de la mujer'), (3, b'A nombre de ambos'), (4, b'A nombre de los hijos'), (5, b'A nombre de los hijas'), (6, b'A nombre de parientes'), (7, b'A nombre de otros')])),
            ],
            options={
                'verbose_name_plural': '1.2.1-En el caso SI, indique a nombre de quien est\xe1',
            },
        ),
        migrations.CreateModel(
            name='Encuesta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField()),
                ('dueno', models.IntegerField(verbose_name=b'\xc2\xbf1.2-La UPF es propiedad de su familia?', choices=[(1, b'Si'), (2, b'No')])),
                ('year', models.IntegerField(verbose_name=b'A\xc3\xb1o', editable=False)),
            ],
            options={
                'verbose_name_plural': 'ENCUESTAS',
            },
        ),
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
                ('comunidad', smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'municipio', chained_field=b'municipio', verbose_name=b'Provincia', blank=True, auto_choose=True, to='lugar.Comunidad', null=True)),
                ('departamento', smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'pais', chained_field=b'pais', auto_choose=True, to='lugar.Departamento')),
                ('microcuenca', smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'comunidad', chained_field=b'comunidad', verbose_name=b'Comunidad/Cant\xc3\xb3n', blank=True, auto_choose=True, to='lugar.Microcuenca', null=True)),
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
            name='EscasezAlimentos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('considera', models.IntegerField(verbose_name=b'4.4-Considera que su familia cuenta siempre con suficiente alimentos', choices=[(1, b'Si'), (2, b'No')])),
                ('fenomeno', multiselectfield.db.fields.MultiSelectField(blank=True, max_length=9, null=True, choices=[(b'A', b'Sequ\xc3\xada'), (b'B', b'Inundaci\xc3\xb3n'), (b'C', b'Deslizamiento'), (b'D', b'Incendios'), (b'E', b'Heladas/Granizo')])),
                ('agricola', multiselectfield.db.fields.MultiSelectField(blank=True, max_length=9, null=True, choices=[(b'A', b'Falta o perdida de semilla'), (b'B', b'Mala calidad de la semilla'), (b'C', b'Falta de riego'), (b'D', b'Poca Tierra o baja fertilidad'), (b'E', b'Plagas y enfermedades')])),
                ('economica', multiselectfield.db.fields.MultiSelectField(blank=True, max_length=7, null=True, choices=[(b'A', b'Bajo precio de sus productos  agr\xc3\xadcolas en el mercado'), (b'B', b'Falta de mercado'), (b'C', b'Falta de credito'), (b'D', b'Falta de mano de obra')])),
                ('encuesta', models.ForeignKey(to='encuestas.Encuesta')),
            ],
        ),
        migrations.CreateModel(
            name='FormaGobernanza',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name_plural': 'Algunas formas de gobernanza ind\xedgenas',
            },
        ),
        migrations.CreateModel(
            name='Frutas',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=4)),
                ('nombre', models.CharField(max_length=250)),
                ('unidad_medida', models.IntegerField(choices=[(1, b'Quintal'), (2, b'Libras'), (3, b'Docena'), (4, b'Cien'), (5, b'Cabeza'), (6, b'Litro'), (7, b'Unidad')])),
                ('calorias', models.FloatField(null=True, blank=True)),
                ('proteinas', models.FloatField(null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Codigo frutas y perennes',
            },
        ),
        migrations.CreateModel(
            name='FrutasCultivosPerennes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad_cosechada', models.FloatField()),
                ('consumo_familia', models.FloatField(verbose_name=b'Consumo de la familia')),
                ('consumo_animal', models.FloatField()),
                ('venta', models.FloatField()),
                ('cultivo', models.ForeignKey(to='encuestas.Frutas')),
                ('encuesta', models.ForeignKey(to='encuestas.Encuesta')),
            ],
            options={
                'verbose_name_plural': '3.2.5-Frutales y cultivos perennes en la UPF',
            },
        ),
        migrations.CreateModel(
            name='Ganaderia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.IntegerField(verbose_name=b'Cantidad de animales hace un a\xc3\xb1o')),
                ('cantidad_actual', models.IntegerField(verbose_name=b'Cantidad de animales hoy en dia')),
                ('consumo', models.IntegerField(verbose_name=b'Consumo durante ultimos 12 meses')),
                ('cantidad_vendida', models.IntegerField(null=True, verbose_name=b'Comercializaci\xc3\xb3n durante ultimos 12 meses', blank=True)),
                ('animal', models.ForeignKey(to='encuestas.Animales')),
                ('encuesta', models.ForeignKey(to='encuestas.Encuesta')),
            ],
            options={
                'verbose_name_plural': '3.2.6 Inventario de ganaderia mayor y menor',
            },
        ),
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('actividades', multiselectfield.db.fields.MultiSelectField(blank=True, max_length=21, null=True, verbose_name=b'5.1-Actividades productivas participan las mujeres', choices=[(b'A', b'Cuidado de animales'), (b'B', b'Cuidado del huerto'), (b'C', b'Preparaci\xc3\xb3n del suelo'), (b'D', b'Siembra'), (b'D', b'Limpia'), (b'D', b'Fertilizaci\xc3\xb3n'), (b'D', b'Manejo de plagas'), (b'D', b'Cosecha'), (b'D', b'Conservaci\xc3\xb3n de semilla'), (b'D', b'Tranformaci\xc3\xb3n'), (b'D', b'Venta')])),
                ('porcentaje', models.FloatField(verbose_name=b'5.2-En que porcentaje participa la mujer en generar ingresos y alimentos en la UPF')),
                ('animales', models.IntegerField(verbose_name=b'Tiene a nombre de la mujer animales', choices=[(1, b'Si'), (2, b'No')])),
                ('equipos', models.IntegerField(verbose_name=b'Tiene a nombre de la mujer equipos electrodomesticos', choices=[(1, b'Si'), (2, b'No')])),
                ('transporte', models.IntegerField(verbose_name=b'Tiene a nombre de la mujer equipos transporte', choices=[(1, b'Si'), (2, b'No')])),
                ('tierra', models.IntegerField(verbose_name=b'Tiene a nombre de la mujer tierra', choices=[(1, b'Si'), (2, b'No')])),
                ('pertenece', models.IntegerField(verbose_name=b'Las mujeres de la UPF pertenece algun tipo de org. comunitaria', choices=[(1, b'Si'), (2, b'No')])),
                ('actividad', models.IntegerField(verbose_name=b'Las mujeres de la UPF realizan alguna comunitaria', choices=[(1, b'Si'), (2, b'No')])),
            ],
        ),
        migrations.CreateModel(
            name='GeneroActividadesComunitaria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name_plural': 'Actividades comunitarias',
            },
        ),
        migrations.CreateModel(
            name='GeneroOrgComunitaria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name_plural': 'Organizaciones comunitarias para genero',
            },
        ),
        migrations.CreateModel(
            name='Idiomas',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name_plural': 'Idiomas',
            },
        ),
        migrations.CreateModel(
            name='ManejoAgroforestal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('si_no', models.IntegerField(verbose_name=b'3.2.8-En la UPF usan practicas de manejo agroforestal', choices=[(1, b'Si'), (2, b'No')])),
                ('responde_si', multiselectfield.db.fields.MultiSelectField(blank=True, max_length=19, null=True, choices=[(b'A', b'\xc3\x81rboles en potreras'), (b'B', b'Asocio de \xc3\xa1rboles con cultivos anuales'), (b'C', b'\xc3\x81rboles en callejones'), (b'D', b'Asocio de \xc3\xa1rboles con cultivos perennes'), (b'E', b'Bosques de galer\xc3\xada'), (b'F', b'Plantaci\xc3\xb3n energ\xc3\xa9tica'), (b'G', b'Cercas vivas'), (b'H', b'Establecimiento de viveros forestales'), (b'I', b'Cortinas rompevientos'), (b'J', b'Protecci\xc3\xb3n de bosque comunal')])),
                ('encuesta', models.ForeignKey(to='encuestas.Encuesta')),
            ],
            options={
                'verbose_name_plural': 'Pr\xe1cticas agroforestales',
            },
        ),
        migrations.CreateModel(
            name='OrganizacionResp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=250)),
                ('departamento', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, to='lugar.Departamento', chained_model_field=b'pais', chained_field=b'pais', null=True)),
                ('municipio', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, to='lugar.Municipio', chained_model_field=b'departamento', chained_field=b'departamento', null=True)),
                ('pais', models.ForeignKey(to='lugar.Pais', null=True)),
            ],
            options={
                'verbose_name': 'Organizaci\xf3n responsable',
                'verbose_name_plural': 'Organizaciones responsables',
            },
        ),
        migrations.CreateModel(
            name='OrganizacionSocialProductiva',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pertenece', models.IntegerField(verbose_name=b'3.1-Pertenece a alguna organizaci\xc3\xb3n', choices=[(1, b'Si'), (2, b'No')])),
                ('capacitacion', models.IntegerField(verbose_name=b'3.1.3-Ha recibido capacitaci\xc3\xb3n por parte de las org.comunitaria', choices=[(1, b'Si'), (2, b'No')])),
            ],
        ),
        migrations.CreateModel(
            name='OrgComunitarias',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'Organizaci\xf3n comunitaria',
                'verbose_name_plural': 'Organizaciones comunitarias',
            },
        ),
        migrations.CreateModel(
            name='PerteneceGobernanza',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('si_no', models.IntegerField(verbose_name=b'3.2.10-Pertenece a alguna forma de gobernanza ind\xc3\xadgena', choices=[(1, b'Si'), (2, b'No')])),
                ('encuesta', models.ForeignKey(to='encuestas.Encuesta')),
                ('responde_si', models.ManyToManyField(to='encuestas.FormaGobernanza', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PracticasAgricolasAncestrales',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('si_no', models.IntegerField(verbose_name=b'3.2.9-En la UPF usan practicas agricolas ancestrales', choices=[(1, b'Si'), (2, b'No')])),
                ('responde_si', multiselectfield.db.fields.MultiSelectField(blank=True, max_length=23, null=True, choices=[(b'A', b'Tomar en cuenta fase de la luna'), (b'B', b'Trueque de productos y semillas'), (b'C', b'Espiritualidad en selecci\xc3\xb3n de semillas'), (b'D', b'Transhumancia'), (b'E', b'Espiritualidad en cuanto al ma\xc3\xadz'), (b'F', b'Predicci\xc3\xb3n clim\xc3\xa1tica'), (b'G', b'Pedir permiso  a cerros y valles'), (b'H', b'Manejo de piso ecol\xc3\xb3gico'), (b'I', b'Trabajo colectivo'), (b'J', b'Abono jiraguano'), (b'K', b'Uso de semillas nativas'), (b'L', b'Participaci\xc3\xb3n mujeres en ciertos cultivos')])),
                ('encuesta', models.ForeignKey(to='encuestas.Encuesta')),
            ],
            options={
                'verbose_name_plural': 'Pr\xe1cticas agricolas ancestrales',
            },
        ),
        migrations.CreateModel(
            name='PracticasAgroecologicas',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('si_no', models.IntegerField(verbose_name=b'3.2.7-En la UPF usan practicas de manejo agroecol\xc3\xb3gicas', choices=[(1, b'Si'), (2, b'No')])),
                ('responde_si', multiselectfield.db.fields.MultiSelectField(blank=True, max_length=19, null=True, choices=[(b'A', b'Fabricaci\xc3\xb3n y uso de abono org\xc3\xa1nico'), (b'B', b'Labranza m\xc3\xadnima'), (b'C', b'Control ecol\xc3\xb3gico de plagas'), (b'D', b'Ahoyado de frutales'), (b'E', b'Obras de consevaci\xc3\xb3n de suelos'), (b'F', b'Uso de abonos verdes'), (b'G', b'Selecci\xc3\xb3n de semillas nativas'), (b'H', b'Asociaci\xc3\xb3n de cultivos'), (b'I', b'Rotaci\xc3\xb3n de cultivos'), (b'J', b'Cobertura de suelos')])),
                ('encuesta', models.ForeignKey(to='encuestas.Encuesta')),
            ],
            options={
                'verbose_name_plural': 'Pr\xe1cticas agroecol\xf3gicas',
            },
        ),
        migrations.CreateModel(
            name='SeguridadAlimentaria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('porcentaje', models.FloatField(verbose_name=b'4.1-Qu\xc3\xa9 porcentaje de los alimentos que consume en su hogar provienen de la misma UPF?')),
                ('disponen', models.IntegerField(verbose_name=b'4.2-Dispone de suficiente recursos economicos para manejar su UPF', choices=[(1, b'Si'), (2, b'No')])),
                ('escasez', multiselectfield.db.fields.MultiSelectField(blank=True, max_length=13, null=True, verbose_name=b'4.3-Qu\xc3\xa9 es lo que hace cuando hay escasez de alimentos en la familia', choices=[(b'A', b'Busca trabajo fuera de la UPF'), (b'B', b'Recibe remesas familiares'), (b'C', b'Se endeuda'), (b'D', b'Vende alg\xc3\xban bien'), (b'E', b'Pide donaci\xc3\xb3n de alimentos al estado o iglesia'), (b'F', b'Pide alimentos a familiares'), (b'G', b'Pasa hambre')])),
                ('encuesta', models.ForeignKey(to='encuestas.Encuesta')),
            ],
        ),
        migrations.CreateModel(
            name='UsosAgua',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uso', models.IntegerField(verbose_name=b'2.2.3-Indique qu\xc3\xa9 otros usos le dan al agua en la UPF', choices=[(1, b'Uso dom\xc3\xa9stico'), (2, b'Uso agr\xc3\xadcola'), (3, b'Uso tur\xc3\xadstico'), (4, b'Crianza de peces'), (5, b'Para ganado')])),
                ('tiempo_invertido', models.FloatField(verbose_name=b'2.2.4-Tiempo invertido para acarrrear agua desde la fuente')),
                ('encuesta', models.ForeignKey(to='encuestas.Encuesta')),
            ],
            options={
                'verbose_name_plural': '',
            },
        ),
        migrations.CreateModel(
            name='UsoSemilla',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo_semilla', multiselectfield.db.fields.MultiSelectField(blank=True, max_length=7, null=True, verbose_name=b'4.5.1-Tipos de semilla usadas en UPF', choices=[(b'A', b'Nativas'), (b'B', b'Acriolladas'), (b'C', b'Mejoradas/certificadas'), (b'D', b'Falta de mano de obra')])),
                ('semillas_producidas', models.FloatField(verbose_name=b'4.5.2-Porcentaje de semillas producidas en la UPF')),
                ('semillas_conseguidas', models.FloatField(verbose_name=b'4.5.2-Porcentaje de semillas conseguidas en la UPF')),
                ('banco_semilla', models.IntegerField(verbose_name=b'4.5.3-Usted tiene banco de semillas familiar', choices=[(1, b'Si'), (2, b'No')])),
                ('compradas_agroservicio', models.FloatField(verbose_name=b'4.5.3-Compradas en un agroservicio')),
                ('sabe', models.IntegerField(verbose_name=b'4.5.4-Sabe si existe un registro comunitario de semillas', choices=[(1, b'Si'), (2, b'No')])),
                ('encuesta', models.ForeignKey(to='encuestas.Encuesta')),
            ],
        ),
        migrations.AddField(
            model_name='organizacionsocialproductiva',
            name='caso_si',
            field=models.ManyToManyField(to='encuestas.OrgComunitarias', verbose_name=b'3.1.1-Qu\xc3\xa9 organizaci\xc3\xb3n comunitaria pertenece', blank=True),
        ),
        migrations.AddField(
            model_name='organizacionsocialproductiva',
            name='cuales_beneficios',
            field=models.ManyToManyField(to='encuestas.BeneficiosOrganizados', verbose_name=b'3.1.2-Cu\xc3\xa1les son los beneficio de estar organizado', blank=True),
        ),
        migrations.AddField(
            model_name='organizacionsocialproductiva',
            name='encuesta',
            field=models.ForeignKey(to='encuestas.Encuesta'),
        ),
        migrations.AddField(
            model_name='genero',
            name='cual_actvidad',
            field=models.ManyToManyField(to='encuestas.GeneroActividadesComunitaria', verbose_name=b'Cual(es)'),
        ),
        migrations.AddField(
            model_name='genero',
            name='cual_comunitaria',
            field=models.ManyToManyField(to='encuestas.GeneroOrgComunitaria', verbose_name=b'Cual(es)'),
        ),
        migrations.AddField(
            model_name='genero',
            name='encuesta',
            field=models.ForeignKey(to='encuestas.Encuesta'),
        ),
        migrations.AddField(
            model_name='encuesta',
            name='encuestador',
            field=models.ForeignKey(to='encuestas.Encuestadores'),
        ),
        migrations.AddField(
            model_name='encuesta',
            name='entrevistado',
            field=models.ForeignKey(to='encuestas.Entrevistados'),
        ),
        migrations.AddField(
            model_name='encuesta',
            name='org_responsable',
            field=models.ForeignKey(verbose_name=b'Nombre de la organizaci\xc3\xb3n responsable', to='encuestas.OrganizacionResp'),
        ),
        migrations.AddField(
            model_name='encuesta',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='duenosi',
            name='encuesta',
            field=models.ForeignKey(to='encuestas.Encuesta'),
        ),
        migrations.AddField(
            model_name='duenono',
            name='encuesta',
            field=models.ForeignKey(to='encuestas.Encuesta'),
        ),
        migrations.AddField(
            model_name='distribucionupf',
            name='encuesta',
            field=models.ForeignKey(to='encuestas.Encuesta'),
        ),
        migrations.AddField(
            model_name='disponibilidadagua',
            name='encuesta',
            field=models.ForeignKey(to='encuestas.Encuesta'),
        ),
        migrations.AddField(
            model_name='detallemiembros',
            name='encuesta',
            field=models.ForeignKey(to='encuestas.Encuesta'),
        ),
        migrations.AddField(
            model_name='descripcion',
            name='encuesta',
            field=models.ForeignKey(to='encuestas.Encuesta'),
        ),
        migrations.AddField(
            model_name='cultivoshuerto',
            name='cultivo',
            field=models.ForeignKey(to='encuestas.CultivosHuertos'),
        ),
        migrations.AddField(
            model_name='cultivoshuerto',
            name='encuesta',
            field=models.ForeignKey(to='encuestas.Encuesta'),
        ),
        migrations.AddField(
            model_name='cultivosanuales',
            name='encuesta',
            field=models.ForeignKey(to='encuestas.Encuesta'),
        ),
        migrations.AddField(
            model_name='condicionesvida',
            name='encuesta',
            field=models.ForeignKey(to='encuestas.Encuesta'),
        ),
        migrations.AddField(
            model_name='condicionesvida',
            name='idioma',
            field=models.ForeignKey(verbose_name=b'idiomas que habla', to='encuestas.Idiomas'),
        ),
        migrations.AddField(
            model_name='accesoagua',
            name='agua',
            field=models.ManyToManyField(to='encuestas.AguaConsumo'),
        ),
        migrations.AddField(
            model_name='accesoagua',
            name='encuesta',
            field=models.ForeignKey(to='encuestas.Encuesta'),
        ),
    ]
