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
CHOICE_MIEMBRO_FAMILIA = (
                (1, 'Hombres mayores 31 años'),
                (2, 'Mujeres mayores 31 años'),
                (3, 'Hombre joven de 19 a 30 años'),
                (4, 'Mujer joven de 19 a 30 años'),
                (5, 'Hombre adolescente 13 a 18 años'),
                (6, 'Mujer adolescente 13 a 18 años'),
                (7, 'Niños 5 a 12 años'),
                (8, 'Niñas 5 a 12 años '),
              )
CHOICE_MEDIDA = (
                (1, 'Quintal'),
                (2, 'Libras'),
                (3, 'Docena'),
                (4, 'Cien'),
                (5, 'Cabeza'),
                (6, 'Litro'),
                (7, 'Unidad'),
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
        unique_together = (("nombre", "cedula"),)
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


CHOICES_DECISIONES = ((1,'Esposo'),(2,'Esposa'),(3,'Padre'),
                                              (4,'Madre'),(5,'Ambos'),(6,'Hijos'),
                                              (7,'La familia en conjunto'),)

class DetalleMiembros(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    decisiones = models.IntegerField(choices=CHOICES_DECISIONES, verbose_name='1.3-¿Quién toma las decisiones en la UPF')
    cantidad = models.IntegerField('1.4-Cantidad de personas que habitan en el hogar')
    cantidad_dependen = models.IntegerField('1.5-Cantidad de personas que dependen economicamente en la UPF')

    def __unicode__(self):
        return u'%s' % (self.get_decisiones_display())

    class Meta:
        verbose_name_plural = ''

CHOICE_PARENTESCO = ((1,'Esposo'),
                     (2,'Esposa'),
                     (3,'Hijo'),
                     (4,'Hija'),
                     (5,'Suegra'),
                     (6,'Suegro'),
                     (7,'Tia'),
                     (8,'Tio'),
                     (9,'Pariente'),
                     (10,'Otro'),
                     )

CHOICE_ESCOLARIDAD = ((1,'Ningún estudio'),
                     (2,'Primaria incompleta'),
                     (3,'Primaria completa'),
                     (4,'Secundaria incompleta'),
                     (5,'Secundaria completa (o bachiller)'),
                     (6,'“1” años de carrera universitaria'),
                     (7,'“2” años de carrera universitaria'),
                     (8,'“3” años de carrera universitaria'),
                     (9,'“4” años de carrera universitaria'),
                     (10,'5” años de carrera universitaria'),
                     )

class Idiomas(models.Model):
    nombre = models.CharField(max_length=250)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Idiomas'


class CondicionesVida(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    parentesco = models.IntegerField(choices=CHOICE_PARENTESCO)
    sexo = models.IntegerField(choices=CHOICE_SEXO1)
    edad = models.IntegerField()
    escolaridad = models.IntegerField(choices=CHOICE_ESCOLARIDAD)
    idioma = models.ForeignKey(Idiomas, verbose_name='idiomas que habla')


    def __unicode__(self):
        return u'%s' % (self.get_sexo_display())

    class Meta:
        verbose_name_plural = '2.1- Indicar la cantidad de miembros de la familia y su escolaridad'


class AguaConsumo(models.Model):
    nombre = models.CharField(max_length=250)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Agua para consumo'
        verbose_name_plural = 'Agua para consumo'


class AccesoAgua(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    agua = models.ManyToManyField(AguaConsumo)

    class Meta:
        verbose_name_plural = '2.2.1-Indique la forma que accede al agua para consumo humano'


CHOICE_DISPONIBILIDAD = (
                (1, 'Todo el tiempo'),
                (2, 'Ocacionalmente'),
                (3, 'Casi nunca'),
                (4, 'Solo época lluviosa')
              )


class DisponibilidadAgua(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    disponibilidad = models.IntegerField(choices=CHOICE_DISPONIBILIDAD)

    class Meta:
        verbose_name_plural = '2.2.2-Mencione la disponibilidad del agua para consumo humano)'


CHOICE_OTRO_USO = (
                (1, 'Uso doméstico'),
                (2, 'Uso agrícola'),
                (3, 'Uso turístico'),
                (4, 'Crianza de peces'),
                (5, 'Para animales')
              )

class UsosAgua(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    uso = MultiSelectField(choices=CHOICE_OTRO_USO, verbose_name='2.2.3-Indique qué otros usos le dan al agua en la UPF')
    tiempo_invertido = models.FloatField(verbose_name='2.2.4-Tiempo invertido para acarrrear agua desde la fuente')

    class Meta:
        verbose_name_plural = ''

class OrgComunitarias(models.Model):
    nombre = models.CharField(max_length=250)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name='Organización comunitaria'
        verbose_name_plural='Organizaciones comunitarias'


class BeneficiosOrganizados(models.Model):
    nombre = models.CharField(max_length=250)

    def __unicode__(self):
        return self.nombre

    class Meta:
        verbose_name_plural='Beneficios de estar organizado'

class OrganizacionSocialProductiva(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    pertenece = models.IntegerField(choices=CHOICE_JEFE, verbose_name='3.1-Pertenece a alguna organización')
    caso_si = models.ManyToManyField(OrgComunitarias, verbose_name='3.1.1-Qué organización comunitaria pertenece',blank=True)
    cuales_beneficios = models.ManyToManyField(BeneficiosOrganizados,
                            verbose_name='3.1.2-Cuáles son los beneficio de estar organizado',
                            blank=True)
    capacitacion = models.IntegerField(choices=CHOICE_JEFE, verbose_name='3.1.3-Ha recibido capacitación por parte de las org.comunitaria')

class Descripcion(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    area = models.FloatField('3.2.1-Cuál es el área aproximada de la UPF?')

    class Meta:
        verbose_name_plural='Distribución de la UPF'


CHOICE_TIERRA = (
        (1,'Bosque natural'),
        (2,'Potrero y pastos'),
        (3,'Plantación forestal'),
        (4,'Cultivos anuales'),
        (5,'Cultivos perennes'),
        (6,'Huertos'),
    )

class Distribucionupf(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    tierra = models.IntegerField(choices=CHOICE_TIERRA, verbose_name='3.2.2-Distribución de la tierra en la UPF')
    manzanas = models.FloatField(help_text='en Ha', verbose_name='hectáreas')

class Cultivos(models.Model):
    codigo = models.CharField(max_length=4)
    nombre = models.CharField(max_length=250)
    unidad_medida = models.IntegerField(choices=CHOICE_MEDIDA)
    calorias = models.FloatField(null=True, blank=True)
    proteinas = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        return u'%s - %s - %s' % (self.codigo, self.nombre, self.get_unidad_medida_display())

    class Meta:
        verbose_name_plural='Codigo cultivos anuales'

class CultivosAnuales(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    cultivo = models.ForeignKey(Cultivos)
    area_sembrada = models.FloatField('Area sembrada (Ha)')
    area_cosechada = models.FloatField('Area cosechada (Ha)')
    cantidad_cosechada = models.FloatField()
    consumo_familia = models.FloatField('Consumo de la familia')
    consumo_animal = models.FloatField()
    venta = models.FloatField()

    class Meta:
        verbose_name_plural = '3.2.3-Cultivos anuales (5 principales) producido en la UPF'

class CultivosHuertos(models.Model):
    codigo = models.CharField(max_length=4)
    nombre = models.CharField(max_length=250)
    unidad_medida = models.IntegerField(choices=CHOICE_MEDIDA)
    calorias = models.FloatField(null=True, blank=True)
    proteinas = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        return u'%s - %s - %s' % (self.codigo, self.nombre, self.get_unidad_medida_display())

    class Meta:
        verbose_name_plural='Codigo cultivos de huertos'


class CultivosHuerto(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    cultivo = models.ForeignKey(CultivosHuertos)
    area_sembrada = models.FloatField('Area sembrada (Ha)')
    area_cosechada = models.FloatField('Area cosechada (Ha)')
    cantidad_cosechada = models.FloatField()
    consumo_familia = models.FloatField('Consumo de la familia')
    consumo_animal = models.FloatField()
    venta = models.FloatField()

    class Meta:
        verbose_name_plural = '3.2.4-Cultivos de huertos (5 principales) en la UPF'

class Frutas(models.Model):
    codigo = models.CharField(max_length=4)
    nombre = models.CharField(max_length=250)
    unidad_medida = models.IntegerField(choices=CHOICE_MEDIDA)
    calorias = models.FloatField(null=True, blank=True)
    proteinas = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        return u'%s - %s - %s' % (self.codigo, self.nombre, self.get_unidad_medida_display())

    class Meta:
        verbose_name_plural='Codigo frutas y perennes'

class FrutasCultivosPerennes(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    cultivo = models.ForeignKey(Frutas)
    cantidad_cosechada = models.FloatField()
    consumo_familia = models.FloatField('Consumo de la familia')
    consumo_animal = models.FloatField()
    venta = models.FloatField()

    class Meta:
        verbose_name_plural = '3.2.5-Frutales y cultivos perennes en la UPF'


class Animales(models.Model):
    codigo = models.CharField(max_length=4)
    nombre = models.CharField(max_length=250)

    def __unicode__(self):
        return u'%s-%s' % (self.codigo, self.nombre)

    class Meta:
        verbose_name_plural = 'Codigo animales'

class Ganaderia(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    animal = models.ForeignKey(Animales)
    cantidad = models.IntegerField('Cantidad de animales hace un año')
    cantidad_actual = models.IntegerField('Cantidad de animales hoy en dia')
    consumo = models.IntegerField('Consumo durante ultimos 12 meses')
    cantidad_vendida = models.IntegerField('Comercialización durante ultimos 12 meses', null=True, blank=True)

    class Meta:
        verbose_name_plural = '3.2.6 Inventario de ganaderia mayor y menor'

CHOICE_PRACTICAS = (
            ('A','Fabricación y uso de abono orgánico'),
            ('B','Labranza mínima'),
            ('C','Control ecológico de plagas'),
            ('D','Ahoyado de frutales'),
            ('E','Obras de consevación de suelos'),
            ('F','Uso de abonos verdes'),
            ('G','Selección de semillas nativas'),
            ('H','Asociación de cultivos'),
            ('I','Rotación de cultivos'),
            ('J','Cobertura de suelos'),
        )

class PracticasAgroecologicas(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    si_no = models.IntegerField(choices=CHOICE_JEFE,
                                                      verbose_name='3.2.7-En la UPF usan practicas de manejo agroecológicas')
    responde_si = MultiSelectField(choices=CHOICE_PRACTICAS, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Prácticas agroecológicas'

CHOICE_AGROFORESTAL = (
            ('A','Árboles en potreras'),
            ('B','Asocio de árboles con cultivos anuales'),
            ('C','Árboles en callejones'),
            ('D','Asocio de árboles con cultivos perennes'),
            ('E','Bosques de galería'),
            ('F','Plantación energética'),
            ('G','Cercas vivas'),
            ('H','Establecimiento de viveros forestales'),
            ('I','Cortinas rompevientos'),
            ('J','Protección de bosque comunal'),
        )

class ManejoAgroforestal(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    si_no = models.IntegerField(choices=CHOICE_JEFE,
                                                      verbose_name='3.2.8-En la UPF usan practicas de manejo agroforestal')
    responde_si = MultiSelectField(choices=CHOICE_AGROFORESTAL, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Prácticas agroforestales'


CHOICE_AGRICOLAS_ANCESTRALES = (
            ('A','Tomar en cuenta fase de la luna'),
            ('B','Trueque de productos y semillas'),
            ('C','Espiritualidad en selección de semillas'),
            ('D','Transhumancia'),
            ('E','Espiritualidad en cuanto al maíz'),
            ('F','Predicción climática'),
            ('G','Pedir permiso  a cerros y valles'),
            ('H','Manejo de piso ecológico'),
            ('I','Trabajo colectivo'),
            ('J','Abono jiraguano'),
            ('K','Uso de semillas nativas'),
            ('L','Participación mujeres en ciertos cultivos'),
        )

class PracticasAgricolasAncestrales(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    si_no = models.IntegerField(choices=CHOICE_JEFE,
                                                      verbose_name='3.2.9-En la UPF usan practicas agricolas ancestrales')
    responde_si = MultiSelectField(choices=CHOICE_AGRICOLAS_ANCESTRALES, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Prácticas agricolas ancestrales'

class FormaGobernanza(models.Model):
    nombre = models.CharField(max_length=250)

    def __unicode__(self):
        return u'%s' % (self.nombre)

    class Meta:
        verbose_name_plural = 'Algunas formas de gobernanza indígenas'


class PerteneceGobernanza(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    si_no = models.IntegerField(choices=CHOICE_JEFE,
                                                      verbose_name='3.2.10-Pertenece a alguna forma de gobernanza indígena')
    responde_si = models.ManyToManyField(FormaGobernanza, blank=True)

CHOICE_ESCASEZ = (
            ('A','Busca trabajo fuera de la UPF'),
            ('B','Recibe remesas familiares'),
            ('C','Se endeuda'),
            ('D','Vende algún bien'),
            ('E','Pide donación de alimentos al estado o iglesia'),
            ('F','Pide alimentos a familiares'),
            ('G','Pasa hambre'),
        )

class SeguridadAlimentaria(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    porcentaje = models.FloatField('4.1-Qué porcentaje de los alimentos que consume en su hogar provienen de la misma UPF?')
    disponen = models.IntegerField(choices=CHOICE_JEFE,
                     verbose_name='4.2-Dispone de suficiente recursos economicos para manejar su UPF')
    escasez = MultiSelectField(choices=CHOICE_ESCASEZ,
                                                    null=True,
                                                    blank=True,
                                                    verbose_name='4.3-Qué es lo que hace cuando hay escasez de alimentos en la familia')

CHOICE_FENOMENOS = (
            ('A','Sequía'),
            ('B','Inundación'),
            ('C','Deslizamiento'),
            ('D','Incendios'),
            ('E','Heladas/Granizo'),
        )
CHOICE_AGRICOLA = (
            ('A','Falta o perdida de semilla'),
            ('B','Mala calidad de la semilla'),
            ('C','Falta de riego'),
            ('D','Poca Tierra o baja fertilidad'),
            ('E','Plagas y enfermedades'),
        )
CHOICE_ECONOMICAS = (
            ('A','Bajo precio de sus productos  agrícolas en el mercado'),
            ('B','Falta de mercado'),
            ('C','Falta de credito'),
            ('D','Falta de mano de obra'),
        )


class EscasezAlimentos(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    considera = models.IntegerField(choices=CHOICE_JEFE,
        verbose_name='4.4-Considera que su familia cuenta siempre con suficiente alimentos producidos en la UPF para consumo diario del hogar?')
    fenomeno = MultiSelectField(choices=CHOICE_FENOMENOS, null=True, blank=True)
    agricola = MultiSelectField(choices=CHOICE_AGRICOLA, null=True, blank=True)
    economica = MultiSelectField(choices=CHOICE_ECONOMICAS, null=True, blank=True)

CHOICE_SEMILLAS = (
            ('A','Nativas'),
            ('B','Acriolladas'),
            ('C','Mejoradas/certificadas'),
            ('D','Falta de mano de obra'),
        )

class UsoSemilla(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    tipo_semilla = MultiSelectField(choices=CHOICE_SEMILLAS,
                                                            null=True,
                                                            blank=True,
                                                            verbose_name='4.5.1-Tipos de semilla usadas en UPF')
    semillas_producidas = models.FloatField('4.5.2-Porcentaje de semillas producidas en la UPF')
    semillas_conseguidas = models.FloatField('4.5.2-Porcentaje de semillas conseguidas en la UPF')
    banco_semilla = models.IntegerField(choices=CHOICE_JEFE,
        verbose_name='4.5.3-Usted tiene banco de semillas familiar')
    compradas_agroservicio = models.FloatField('4.5.3-Compradas en un agroservicio')
    sabe = models.IntegerField(choices=CHOICE_JEFE,
        verbose_name='4.5.4-Sabe si existe un registro comunitario de semillas')

CHOICE_ACTIVIDADES_MUJERES = (
            ('A','Cuidado de animales'),
            ('B','Cuidado del huerto'),
            ('C','Preparación del suelo'),
            ('D','Siembra'),
            ('D','Limpia'),
            ('D','Fertilización'),
            ('D','Manejo de plagas'),
            ('D','Cosecha'),
            ('D','Conservación de semilla'),
            ('D','Tranformación'),
            ('D','Venta'),
        )

class GeneroOrgComunitaria(models.Model):
    nombre = models.CharField(max_length=250)

    def __unicode__(self):
        return u'%s' % (self.nombre)

    class Meta:
        verbose_name_plural = 'Organizaciones comunitarias para genero'

class GeneroActividadesComunitaria(models.Model):
    nombre = models.CharField(max_length=250)

    def __unicode__(self):
        return u'%s' % (self.nombre)

    class Meta:
        verbose_name_plural = 'Actividades comunitarias'

class Genero(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    actividades = MultiSelectField(choices=CHOICE_ACTIVIDADES_MUJERES,
                                                            null=True,
                                                            blank=True,
                                                            verbose_name='5.1-Actividades productivas participan las mujeres')
    porcentaje = models.FloatField('5.2-En que porcentaje participa la mujer en generar ingresos y alimentos en la UPF')
    animales = models.IntegerField(choices=CHOICE_JEFE,
        verbose_name='Tiene a nombre de la mujer animales')
    equipos = models.IntegerField(choices=CHOICE_JEFE,
        verbose_name='Tiene a nombre de la mujer equipos electrodomesticos')
    transporte = models.IntegerField(choices=CHOICE_JEFE,
        verbose_name='Tiene a nombre de la mujer equipos transporte')
    tierra = models.IntegerField(choices=CHOICE_JEFE,
        verbose_name='Tiene a nombre de la mujer tierra')
    pertenece = models.IntegerField(choices=CHOICE_JEFE,
        verbose_name='Las mujeres de la UPF pertenece algun tipo de org. comunitaria')
    cual_comunitaria = models.ManyToManyField(GeneroOrgComunitaria, verbose_name='Cual(es)')
    actividad = models.IntegerField(choices=CHOICE_JEFE,
        verbose_name='Las mujeres de la UPF realizan alguna comunitaria')
    cual_actvidad = models.ManyToManyField(GeneroActividadesComunitaria, verbose_name='Cual(es)')
