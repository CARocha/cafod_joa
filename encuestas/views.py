from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count, Sum, Avg, Value as V
import json as simplejson
from collections import OrderedDict
from .models import *
from .forms import ConsultarForm
from lugar.models import *
# Create your views here.


def _queryset_filtrado(request):
    params = {}

    if request.session['fecha']:
        params['year'] = request.session['fecha']

    if 'pais' in request.session:
        params['entrevistado__pais'] = request.session['pais']

    if 'departamento' in request.session:
        params['entrevistado__departamento__in'] = request.session['departamento']

    if 'organizacion' in request.session:
        params['org_responsable__in'] = request.session['organizacion']

    if 'municipio' in request.session:
        params['entrevistado__municipio__in'] = request.session['municipio']

    if 'comunidad' in request.session:
        params['entrevistado__comunidad__in'] = request.session['comunidad']

    #if request.session['sexo']:
    #    params['entrevistado__sexo'] = request.session['sexo']

    unvalid_keys = []
    for key in params:
        if not params[key]:
            unvalid_keys.append(key)

    for key in unvalid_keys:
        del params[key]

    print params

    return Encuesta.objects.filter(**params)


def indicadores1(request, template='indicadores1.html'):
    request.session['encuestados'] = 0
    if request.method == 'POST':
        mensaje = None
        form = ConsultarForm(request.POST)
        if form.is_valid():
            request.session['fecha'] = form.cleaned_data['fecha']
            request.session['pais'] = form.cleaned_data['pais']
            request.session['departamento'] = form.cleaned_data['departamento']
            request.session['organizacion'] = form.cleaned_data['organizacion']
            request.session['municipio'] = form.cleaned_data['municipio']
            request.session['comunidad'] = form.cleaned_data['comunidad']

            mensaje = "Todas las variables estan correctamente :)"
            request.session['activo'] = True
            centinela = 1
            request.session['encuestados'] = len(_queryset_filtrado(request))
            print mensaje

        else:
            centinela = 0
            mensaje = "Todo fallo ni modo :("
            print mensaje
    else:
        form = ConsultarForm()
        centinela = 0
        if 'pais' in request.session:
            try:
                del request.session['fecha']
                del request.session['pais']
                del request.session['departamento']
                del request.session['organizacion']
                del request.session['municipio']
                del request.session['comunidad']
            except:
                pass
            request.session['activo'] = False

    return render(request, template, locals())

#FUNCIONES PARA LAS DEMAS SALIDAS DEL SISTEMA

def sexo_duenos(request, template="indicadores/sexo_duenos.html"):
    filtro = _queryset_filtrado(request)

    dicc_sexo_dueno = OrderedDict()
    anio = request.session['fecha']
    filtro1 = filtro.count()
    si_dueno = filtro.filter(dueno=1).count()
    no_dueno = filtro.filter(dueno=2).count()

    a_nombre = {}
    for obj in CHOICE_DUENO_SI:
        conteos = filtro.filter(duenosi__si=obj[0]).count()
        a_nombre[obj[1]] = conteos

    situacion = {}
    for obj in CHOICE_DUENO_NO:
        conteos = filtro.filter(duenono__no=obj[0]).count()
        situacion[obj[1]] = conteos

    detalle_edad = {}
    for obj in CHOICES_DECISIONES:
        conteos = filtro.filter(detallemiembros__decisiones=obj[0]).count()
        if conteos > 0:
            detalle_edad[obj[1]] = conteos

    dicc_sexo_dueno[anio] = (si_dueno,no_dueno,a_nombre,situacion,detalle_edad,filtro1)

    return render(request, template, locals())

def escolaridad(request, template="indicadores/escolaridad.html"):
    filtro = _queryset_filtrado(request)

    dicc_escolaridad = OrderedDict()

    filtro1 = filtro.count()

    cantidad_habitan = filtro.aggregate(t=Avg('detallemiembros__cantidad'))['t']
    cantidad_dependen = filtro.aggregate(t=Avg('detallemiembros__cantidad_dependen'))['t']

    tabla_parentesco = OrderedDict()
    for e in CHOICE_PARENTESCO:
        objeto = filtro.filter(
                condicionesvida__parentesco=e[0]).count()
        tabla_parentesco[e[1]] = objeto

    tabla_sexo = OrderedDict()
    for e in CHOICE_SEXO1:
        objeto = filtro.filter(
                condicionesvida__sexo=e[0]).count()
        tabla_sexo[e[1]] = objeto

    tabla_educacion = OrderedDict()
    for e in CHOICE_ESCOLARIDAD:
        objeto = filtro.filter(
                condicionesvida__escolaridad=e[0]).count()
        tabla_educacion[e[1]] = objeto

    tabla_idioma = OrderedDict()
    for e in Idiomas.objects.all():
        objeto = filtro.filter(
                condicionesvida__idioma=e).count()
        tabla_idioma[e.nombre] = objeto

    dicc_escolaridad['reaparar'] = (tabla_parentesco,tabla_sexo,tabla_educacion,
                                    filtro1,cantidad_habitan,cantidad_dependen,
                                    tabla_idioma)

    return render(request, template, locals())

def agua(request, template="indicadores/agua.html"):
    filtro = _queryset_filtrado(request)

    dicc_agua = OrderedDict()

    filtro1 = filtro.count()
    grafo_agua_consumo = {}
    for obj in AguaConsumo.objects.all():
        valor = filtro.filter(accesoagua__agua=obj).count()
        grafo_agua_consumo[obj] =  valor

    grafo_agua_disponibilidad = {}
    for obj in CHOICE_DISPONIBILIDAD:
        valor = filtro.filter(disponibilidadagua__disponibilidad=obj[0]).count()
        grafo_agua_disponibilidad[obj[1]] =  valor

    grafo_agua_usos = {}
    for obj in CHOICE_OTRO_USO:
        valor = filtro.filter(usosagua__uso__icontains=obj[0]).count()
        grafo_agua_usos[obj[1]] =  valor


    promedio_acarreo = 0

    dicc_agua['reparar'] = (grafo_agua_consumo,grafo_agua_disponibilidad,
                            grafo_agua_usos,filtro1,promedio_acarreo)

    return render(request, template, locals())

def organizaciones(request, template="indicadores/organizaciones.html"):
    filtro = _queryset_filtrado(request)

    dicc_organizacion = OrderedDict()

    filtro1 = filtro.count()
    grafo_pertenece = {}
    for obj in CHOICE_JEFE:
        valor = filtro.filter(organizacionsocialproductiva__pertenece=obj[0]).count()
        grafo_pertenece[obj[1]] =  valor

    grafo_org_comunitarias = {}
    for obj in OrgComunitarias.objects.all():
        valor = filtro.filter(organizacionsocialproductiva__caso_si=obj).count()
        if valor > 0:
            grafo_org_comunitarias[obj] =  valor

    grafo_beneficios = {}
    for obj in BeneficiosOrganizados.objects.all():
        valor = filtro.filter(organizacionsocialproductiva__cuales_beneficios=obj).count()
        if valor > 0:
            grafo_beneficios[obj] =  valor

    grafo_capacitacion = {}
    for obj in CHOICE_JEFE:
        valor = filtro.filter(organizacionsocialproductiva__capacitacion=obj[0]).count()
        grafo_capacitacion[obj[1]] =  valor

    dicc_organizacion['repaarar'] = (grafo_pertenece,grafo_org_comunitarias, grafo_beneficios,filtro1,grafo_capacitacion)

    return render(request, template, locals())

def tierra(request, template="indicadores/tierra.html"):
    filtro = _queryset_filtrado(request)

    dicc_tierra = OrderedDict()
    #tabla distribucion de frecuencia
    filtro1 = filtro.count()
    uno_num = filtro.filter(descripcion__area__range=(0.1,5.99)).count()
    seis_num = filtro.filter(descripcion__area__range=(6,10.99)).count()
    diez_mas = filtro.filter(descripcion__area__gt=11).count()

    #promedio de manzanas por todas las personas
    promedio_mz = filtro.aggregate(promedio=Avg('descripcion__area'))['promedio']

    grafo_distribucion_tierra = {}
    for obj in CHOICE_TIERRA:
        valor = filtro.filter(distribucionupf__tierra=obj[0]).count()
        grafo_distribucion_tierra[obj[1]] =  valor

    dicc_tierra['reparar'] = (uno_num,seis_num,diez_mas,promedio_mz,grafo_distribucion_tierra,filtro1)


    return render(request, template, locals())

def practicas(request, template="indicadores/practicas.html"):
    filtro = _queryset_filtrado(request)

    dicc_practicas = OrderedDict()

    filtro1 = filtro.count()
    grafo_practicas_sino = {}
    for obj in CHOICE_JEFE:
        valor = filtro.filter(practicasagroecologicas__si_no=obj[0]).count()
        grafo_practicas_sino[obj[1]] =  valor

    grafo_manejo = {}
    for obj in CHOICE_MANEJO:
        valor = filtro.filter(practicasagroecologicas__manejo=obj[0]).count()
        grafo_manejo[obj[1]] =  valor

    grafo_traccion = {}
    for obj in CHOICE_TRACCION:
        valor = filtro.filter(practicasagroecologicas__traccion=obj[0]).count()
        grafo_traccion[obj[1]] =  valor

    grafo_fertilidad = {}
    for obj in CHOICE_JEFE:
        valor = filtro.filter(practicasagroecologicas__fertilidad=obj[0]).count()
        grafo_fertilidad[obj[1]] =  valor

    grafo_control = {}
    for obj in CHOICE_JEFE:
        valor = filtro.filter(practicasagroecologicas__control=obj[0]).count()
        grafo_control[obj[1]] =  valor

    dicc_practicas['reparar'] = (grafo_practicas_sino,grafo_manejo,grafo_traccion,grafo_fertilidad,grafo_control,filtro1)

    return render(request, template, locals())

def practicas(request, template="indicadores/practicas.html"):

    return render(request, template, locals())

def seguridad(request, template="indicadores/seguridad.html"):
    filtro = _queryset_filtrado(request)

    dicc_seguridad = OrderedDict()

    filtro1 = filtro.count()

    grafo_disponen = {}
    for obj in CHOICE_JEFE:
        valor = filtro.filter(seguridadalimentaria__disponen=obj[0]).count()
        grafo_disponen[obj[1]] =  valor

    grafo_escasez = {}
    for obj in CHOICE_ESCASEZ:
        valor = filtro.filter(seguridadalimentaria__escasez__icontains=obj[0]).count()
        grafo_escasez[obj[1]] =  valor


    conteo_fenomeno = {}
    for obj in CHOICE_FENOMENOS:
        valor = filtro.filter(escasezalimentos__fenomeno__icontains=obj[0]).count()
        conteo_fenomeno[obj[1]] =  valor

    conteo_agricola = {}
    for obj in CHOICE_AGRICOLA:
        valor = filtro.filter(escasezalimentos__agricola__icontains=obj[0]).count()
        conteo_agricola[obj[1]] =  valor

    conteo_economica = {}
    for obj in CHOICE_ECONOMICAS:
        valor = filtro.filter(escasezalimentos__economica__icontains=obj[0]).count()
        conteo_economica[obj[1]] =  valor


    dicc_seguridad['repaara'] = (grafo_disponen,
                                 grafo_escasez,
                                conteo_fenomeno,
                                conteo_agricola,
                                conteo_economica,
                                filtro1)

    return render(request, template, locals())

def genero(request, template="indicadores/genero.html"):
    filtro = _queryset_filtrado(request)

    dicc_genero = OrderedDict()

    filtro1 = filtro.count()

    grafo_organizacion_animal = {}
    for obj in CHOICE_JEFE:
        valor = filtro.filter(genero__animal=obj[0]).count()
        grafo_organizacion_mujer[obj[1]] =  valor

    mujer_organizacion = {}
    for obj in OrgComunitarias.objects.all():
        dato = filtro.filter(organizacioncomunitaria__caso_si=obj,entrevistado__jefe=1).count()
        if dato > 0:
            mujer_organizacion[obj] = dato


    nivel_educacion_mujer = OrderedDict()
    for obj in CHOICER_NIVEL_MUJER:
        valor = filtro.filter(genero__opcion=obj[0]).count()
        nivel_educacion_mujer[obj[1]] =  valor

    dicc_genero[year[1]] = (porcentaje_aporta_mujer,
                              grafo_credito_mujer,
                              grafo_bienes_mujer,
                              grafo_organizacion_mujer,
                              mujer_organizacion,
                              nivel_educacion_mujer,
                              filtro1,
                              )

    return render(request, template, locals())

def traer_departamento(request):
    ids = request.GET.get('ids', '')
    if ids:
        lista = ids.split(',')
    departamento = Departamento.objects.filter(pais__pk__in=lista, entrevistados__gte=1).distinct().values('id', 'nombre')
    return HttpResponse(simplejson.dumps(list(departamento)), content_type='application/json')

def traer_municipio(request):
    ids = request.GET.get('ids', '')
    dicc = {}
    resultado = []
    if ids:
        lista = ids.split(',')
        for id in lista:
            try:
                encuesta = Encuesta.objects.filter(entrevistado__municipio__departamento__id=id).distinct().values_list('entrevistado__municipio__id', flat=True)
                departamento = Departamento.objects.get(pk=id)
                municipios = Municipio.objects.filter(departamento__id=departamento.pk,id__in=encuesta).order_by('nombre')
                lista1 = []
                for municipio in municipios:
                    muni = {}
                    muni['id'] = municipio.pk
                    muni['nombre'] = municipio.nombre
                    lista1.append(muni)
                    dicc[departamento.nombre] = lista1
            except:
                pass

    #filtrar segun la organizacion seleccionada
    org_ids = request.GET.get('org_ids', '')
    if org_ids:
        lista = org_ids.split(',')
        municipios = [encuesta.municipio for encuesta in Encuesta.objects.filter(organizacion__id__in=lista)]
        #crear los keys en el dicc para evitar KeyError
        for municipio in municipios:
            dicc[municipio.departamento.nombre] = []

        #agrupar municipios por departamento padre
        for municipio in municipios:
            muni = {'id': municipio.id, 'nombre': municipio.nombre}
            if not muni in dicc[municipio.departamento.nombre]:
                dicc[municipio.departamento.nombre].append(muni)

    resultado.append(dicc)

    return HttpResponse(simplejson.dumps(resultado), content_type='application/json')

def traer_organizacion(request):
    ids = request.GET.get('ids', '')
    if ids:
        lista = ids.split(',')
        organizaciones = OrganizacionResp.objects.filter(departamento__id__in = lista).order_by('nombre').values('id', 'nombre')
    return HttpResponse(simplejson.dumps(list(organizaciones)), content_type='application/json')

def traer_comunidad(request):
    ids = request.GET.get('ids', '')
    if ids:
        lista = ids.split(',')
        results = []
        comunies = Comunidad.objects.filter(municipio__pk__in=lista).order_by('nombre').values('id', 'nombre')
    return HttpResponse(simplejson.dumps(list(comunies)), content_type='application/json')

