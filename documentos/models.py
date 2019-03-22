from django.db import models
from django.contrib.auth.models import User
from lugar.models import Pais, Departamento, Municipio, Comunidad, Microcuenca
# Create your models here.


class SubirArchivos(models.Model):
    nombre_documento = models.CharField(max_length=250)
    tema = models.CharField(max_length=250)
    descripcion = models.TextField(null=True, blank=True)
    archivo = models.FileField(upload_to='documentos/')
    pais = models.ForeignKey(Pais)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.nombre_documento
