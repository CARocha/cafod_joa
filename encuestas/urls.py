from django.conf.urls import url
from encuestas import views
from documentos.views import ArchivosList

urlpatterns = [
    url(r'^$', views.indicadores1, name='indicadores1'),
    #otros indicadores
    url(r'^jefe_sexo/$', views.sexo_duenos, name='jefe-sexo'),
    url(r'^escolaridad/$', views.escolaridad, name='escolaridad'),
    url(r'^agua/$', views.agua, name='agua'),
    url(r'^organizaciones/$', views.organizaciones, name='organizaciones'),
    url(r'^tierra/$', views.tierra, name='tierra'),
    url(r'^cultivos/$', views.cultivos, name='tierra'),
    url(r'^practicas/$', views.practicas, name='practicas'),
    url(r'^seguridad/$', views.seguridad, name='seguridad'),
    url(r'^genero/$', views.genero, name='genero'),
    url(r'^semilla/$', views.semilla, name='semilla'),
    url(r'^xls/$', views.save_as_xls, name='salvar_xls'),
    url(r'^documentos/$', ArchivosList.as_view()),

    #filtros por ajax
    url(r'^ajax/depart/$', views.traer_departamento, name='get-depart'),
    url(r'^ajax/organi/$', views.traer_organizacion, name='get-organi'),
    url(r'^ajax/munis/$', views.traer_municipio, name='get-munis'),
    url(r'^ajax/provincies/$', views.traer_provincia, name='get-provincies'),
    url(r'^ajax/comunies/$', views.traer_comunidad, name='get-comunies'),
]
