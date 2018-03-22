# -*- coding: utf-8 -*-
from django.db import models
from lugar.models import Pais, Departamento, Municipio, Comunidad, Microcuenca
from multiselectfield import MultiSelectField
from sorl.thumbnail import ImageField
from smart_selects.db_fields import ChainedForeignKey
from django.contrib.auth.models import User

# Create your models here.

#CHOICES ESTATICOS
CHOICE_SEXO = (
                (1, 'Mujer'),
                (2, 'Hombre'),
                (3, 'Ambos'),
              )
CHOICE_SEXO1 = (
                (1, 'Mujer'),
                (2, 'Hombre'),
                (3, 'Ambos'),
              )
CHOICE_JEFE = (
                (1, 'Si'),
                (2, 'No'),
              )
CHOICE_DUENO_SI = (
                (1, 'A nombre del hombre'),
                (2, 'A nombre de la mujer'),
                (3, 'A nombre de ambos'),
                (4, 'A nombre de los hijos'),
                (5, 'A nombre de los hijas'),
                (6, 'A nombre de parientes'),
                (7, 'A nombre de otros'),
              )
CHOICE_DUENO_NO = (
                (1, 'Arrendada'),
                (2, 'Promesa de venta'),
                (3, 'Prestada'),
                (4, 'Tierra Indígena/Comunal'),
                (5, 'Sin escritura'),
                (6, 'Colectivo/Cooperativa'),
              )
CHOICE_EDAD = (
                (1, 'Hombres > 31 años'),
                (2, 'Mujeres > 31 años'),
                (3, 'Ancianos > 64 años'),
                (4, 'Ancianas > 64 años'),
                (5, 'Mujer joven de 19 a 30 años'),
                (6, 'Hombre joven de 19 a 30 años'),
                (7, 'Mujer adolescente 13 a 18 años'),
                (8, 'Hombre adolescente 13 a 18 años'),
                (9, 'Niñas 5 a 12 años'),
                (10, 'Niños 5 a 12 años '),
                (11, 'Niñas 0 a 4 años '),
                (12, 'Niños 0 a 4 años'),
              )
CHOICE_ESCOLARIDAD = (
                (1, 'Hombres mayores 31 años'),
                (2, 'Mujeres mayores 31 años'),
                (3, 'Hombre joven de 19 a 30 años'),
                (4, 'Mujer joven de 19 a 30 años'),
                (5, 'Hombre adolescente 13 a 18 años'),
                (6, 'Mujer adolescente 13 a 18 años'),
                (7, 'Niños 5 a 12 años'),
                (8, 'Niñas 5 a 12 años '),
              )
# FIN DE CHOICES ESTATICOS


class Encuestadores(models.Model):
    nombre = models.CharField(max_length=250)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Encuestador'
        verbose_name_plural = 'Encuestadores'


class OrganizacionResp(models.Model):
    nombre = models.CharField(max_length=250)
    pais = models.ForeignKey(Pais, null=True)
    departamento = ChainedForeignKey(
        Departamento,
        chained_field="pais",
        chained_model_field="pais",
        show_all=False,
        auto_choose=True,
        null=True
    )
    municipio = ChainedForeignKey(
        Municipio,
        chained_field="departamento",
        chained_model_field="departamento",
        show_all=False,
        auto_choose=True,
        null=True
    )

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Organización responsable'
        verbose_name_plural = 'Organizaciones responsables'


class Entrevistados(models.Model):
    nombre = models.CharField('Nombre Completo', max_length=250)
    cedula = models.CharField('No. Cédula/DPI', max_length=50, null=True, blank=True)
    ocupacion = models.CharField('Ocupación', max_length=150)
    sexo = models.IntegerField(choices=CHOICE_SEXO)
    jefe = models.IntegerField(choices=CHOICE_JEFE, verbose_name='Jefe del hogar')
    edad = models.IntegerField()
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null= True, blank=True)
    pais = models.ForeignKey(Pais)
    departamento = ChainedForeignKey(
        Departamento,
        chained_field="pais",
        chained_model_field="pais",
        show_all=False,
        auto_choose=True
    )
    municipio = ChainedForeignKey(
        Municipio,
        chained_field="departamento",
        chained_model_field="departamento",
        show_all=False,
        auto_choose=True
    )
    comunidad = ChainedForeignKey(
        Comunidad,
        chained_field="municipio",
        chained_model_field="municipio",
        show_all=False,
        auto_choose=True,
        null=True,
        blank=True,
        verbose_name='Provincia'
    )
    microcuenca = ChainedForeignKey(
        Microcuenca,
        chained_field="comunidad",
        chained_model_field="comunidad",
        show_all=False,
        auto_choose=True,
        null=True,
        blank=True,
        verbose_name='Comunidad/Cantón'
    )

    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Base de datos Productor'
        verbose_name_plural = 'Base de datos Productores'


class Encuesta(models.Model):
    fecha = models.DateField()
    encuestador = models.ForeignKey(Encuestadores)
    org_responsable = models.ForeignKey(OrganizacionResp, verbose_name='Nombre de la organización responsable')
    entrevistado = models.ForeignKey(Entrevistados)
    dueno = models.IntegerField(choices=CHOICE_JEFE,
                    verbose_name='¿1.2-La UPF es propiedad de su familia?')

    year = models.IntegerField(editable=False, verbose_name='Año')
    user = models.ForeignKey(User)

    def save(self):
        self.year = self.fecha.year
        super(Encuesta, self).save()

    def __unicode__(self):
        return u'%s' % (self.entrevistado.nombre)

    class Meta:
        verbose_name_plural = 'ENCUESTAS'

class DuenoSi(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    si = models.IntegerField(choices=CHOICE_DUENO_SI)

    def __unicode__(self):
        return u'%s' % (self.get_si_display())

    class Meta:
        verbose_name_plural = '1.2.1-En el caso SI, indique a nombre de quien está'


class DuenoNo(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    no = models.IntegerField(choices=CHOICE_DUENO_NO)

    def __unicode__(self):
        return u'%s' % (self.get_no_display())

    class Meta:
        verbose_name_plural = '1.2.2-En el caso que diga NO, especifique la situación'


CHOICES_DECISIONES = ((1,'Esposo'),(2,'Esposa'),(3,'Padre'),(4,'Madre'),(5,'Ambos'),)

class DetalleMiembros(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    decisiones = models.IntegerField(choices=CHOICES_DECISIONES, verbose_name='1.3-¿Quién toma las decisiones en la UPF')
    cantidad = models.IntegerField('1.4-Cantidad de personas que habitan en el hogar')
    cantidad_dependen = models.IntegerField('1.5-Cantidad de personas que dependen economicamente en la UPF')

    def __unicode__(self):
        return u'%s' % (self.get_decisiones_display())

    class Meta:
        verbose_name_plural = ''
