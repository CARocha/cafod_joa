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

    unvalid_keys = []
    for key in params:
        if not params[key]:
            unvalid_keys.append(key)

    for key in unvalid_keys:
        del params[key]

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
            #request.session['encuestados'] = len(_queryset_filtrado(request))

        else:
            centinela = 0
            mensaje = "Todo fallo ni modo :("
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
    anio = request.session['fecha']

    filtro1 = filtro.count()

    cantidad_habitan = filtro.aggregate(t=Avg('detallemiembros__cantidad'))['t']
    cantidad_dependen = filtro.aggregate(t=Avg('detallemiembros__cantidad_dependen'))['t']

    tabla_parentesco = OrderedDict()
    for e in CHOICE_PARENTESCO:
        objeto = filtro.filter(
                condicionesvida__parentesco=e[0]).count()
        if objeto > 0:
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
        if objeto > 0:
            tabla_idioma[e.nombre] = objeto

    dicc_escolaridad[anio] = (tabla_parentesco,tabla_sexo,tabla_educacion,
                                    filtro1,cantidad_habitan,cantidad_dependen,
                                    tabla_idioma)

    return render(request, template, locals())

def agua(request, template="indicadores/agua.html"):
    filtro = _queryset_filtrado(request)
    anio = request.session['fecha']

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

    dicc_agua[anio] = (grafo_agua_consumo,grafo_agua_disponibilidad,
                            grafo_agua_usos,filtro1,promedio_acarreo)

    return render(request, template, locals())

def organizaciones(request, template="indicadores/organizaciones.html"):
    filtro = _queryset_filtrado(request)
    anio = request.session['fecha']

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

    dicc_organizacion[anio] = (grafo_pertenece,grafo_org_comunitarias, grafo_beneficios,filtro1,grafo_capacitacion)

    return render(request, template, locals())

def tierra(request, template="indicadores/tierra.html"):
    filtro = _queryset_filtrado(request)
    anio = request.session['fecha']

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

    dicc_tierra[anio] = (uno_num,seis_num,diez_mas,promedio_mz,grafo_distribucion_tierra,filtro1)


    return render(request, template, locals())

def cultivos(request, template='indicadores/productividad.html'):
    filtro = _queryset_filtrado(request)
    anio = request.session['fecha']
    filtro1 = filtro.count()

    dicc_anuales = OrderedDict()
    for obj in Cultivos.objects.all():
        cultivo = filtro.filter(cultivosanuales__cultivo=obj)
        total_area_sembrada = cultivo.aggregate(t=Sum('cultivosanuales__area_sembrada'))['t']
        total_cantidad_cosechada = cultivo.aggregate(t=Sum('cultivosanuales__cantidad_cosechada'))['t']
        total_consumo_familia = cultivo.aggregate(t=Sum('cultivosanuales__consumo_familia'))['t']
        total_consumo_animal = cultivo.aggregate(t=Sum('cultivosanuales__consumo_animal'))['t']
        total_venta = cultivo.aggregate(t=Sum('cultivosanuales__venta'))['t']

        dicc_anuales[obj] = {'unidad':obj.get_unidad_medida_display(),
                            'total_area_sembrada':total_area_sembrada,
                            'total_cantidad_cosechada':total_cantidad_cosechada,
                            'total_consumo_familia':total_consumo_familia,
                            'total_consumo_animal':total_consumo_animal,
                            'total_venta':total_venta}

    dicc_huertos = OrderedDict()
    for obj in CultivosHuertos.objects.all():
        cultivo = filtro.filter(cultivoshuerto__cultivo=obj)
        total_area_sembrada = cultivo.aggregate(t=Sum('cultivoshuerto__area_sembrada'))['t']
        total_cantidad_cosechada = cultivo.aggregate(t=Sum('cultivoshuerto__cantidad_cosechada'))['t']
        total_consumo_familia = cultivo.aggregate(t=Sum('cultivoshuerto__consumo_familia'))['t']
        total_consumo_animal = cultivo.aggregate(t=Sum('cultivoshuerto__consumo_animal'))['t']
        total_venta = cultivo.aggregate(t=Sum('cultivoshuerto__venta'))['t']

        dicc_huertos[obj] = {'unidad':obj.get_unidad_medida_display(),
                            'total_area_sembrada':total_area_sembrada,
                            'total_cantidad_cosechada':total_cantidad_cosechada,
                            'total_consumo_familia':total_consumo_familia,
                            'total_consumo_animal':total_consumo_animal,
                            'total_venta':total_venta}

    dicc_frutas = OrderedDict()
    for obj in Frutas.objects.all():
        cultivo = filtro.filter(frutascultivosperennes__cultivo=obj)
        total_cantidad_cosechada = cultivo.aggregate(t=Sum('frutascultivosperennes__cantidad_cosechada'))['t']
        total_consumo_familia = cultivo.aggregate(t=Sum('frutascultivosperennes__consumo_familia'))['t']
        total_consumo_animal = cultivo.aggregate(t=Sum('frutascultivosperennes__consumo_animal'))['t']
        total_venta = cultivo.aggregate(t=Sum('frutascultivosperennes__venta'))['t']

        dicc_frutas[obj] = {'unidad':obj.get_unidad_medida_display(),
                            'total_cantidad_cosechada':total_cantidad_cosechada,
                            'total_consumo_familia':total_consumo_familia,
                            'total_consumo_animal':total_consumo_animal,
                            'total_venta':total_venta}

    dicc_ganaderia = OrderedDict()
    for obj in Animales.objects.all():
        cultivo = filtro.filter(ganaderia__animal=obj)
        total_cantidad_cosechada = cultivo.aggregate(t=Sum('ganaderia__cantidad'))['t']
        total_consumo_familia = cultivo.aggregate(t=Sum('ganaderia__cantidad_actual'))['t']
        total_consumo_animal = cultivo.aggregate(t=Sum('ganaderia__consumo'))['t']
        total_venta = cultivo.aggregate(t=Sum('ganaderia__cantidad_vendida'))['t']

        dicc_ganaderia[obj] = {'total_cantidad_cosechada':total_cantidad_cosechada,
                            'total_consumo_familia':total_consumo_familia,
                            'total_consumo_animal':total_consumo_animal,
                            'total_venta':total_venta}


    return render(request, template, locals())

def practicas(request, template="indicadores/practicas.html"):
    filtro = _queryset_filtrado(request)
    anio = request.session['fecha']

    dicc_practicas = OrderedDict()

    filtro1 = filtro.count()
    grafo_practicas_sino_agroecologica = {}
    for obj in CHOICE_JEFE:
        valor = filtro.filter(practicasagroecologicas__si_no=obj[0]).count()
        grafo_practicas_sino_agroecologica[obj[1]] =  valor

    grafo_practica_agroecologica_si = {}
    for obj in CHOICE_PRACTICAS:
        valor = filtro.filter(practicasagroecologicas__responde_si__icontains=obj[0]).count()
        grafo_practica_agroecologica_si[obj[1]] = valor

    grafo_practicas_sino_agroforestal = {}
    for obj in CHOICE_JEFE:
        valor = filtro.filter(manejoagroforestal__si_no=obj[0]).count()
        grafo_practicas_sino_agroforestal[obj[1]] =  valor

    grafo_practica_agroforestal_si = {}
    for obj in CHOICE_AGROFORESTAL:
        valor = filtro.filter(manejoagroforestal__responde_si__icontains=obj[0]).count()
        grafo_practica_agroforestal_si[obj[1]] = valor

    grafo_practicas_sino_ancentral = {}
    for obj in CHOICE_JEFE:
        valor = filtro.filter(practicasagricolasancestrales__si_no=obj[0]).count()
        grafo_practicas_sino_ancentral[obj[1]] =  valor

    grafo_practica_ancestral_si = {}
    for obj in CHOICE_AGRICOLAS_ANCESTRALES:
        valor = filtro.filter(practicasagricolasancestrales__responde_si__icontains=obj[0]).count()
        grafo_practica_ancestral_si[obj[1]] = valor

    grafo_practicas_sino_gobernanza = {}
    for obj in CHOICE_JEFE:
        valor = filtro.filter(pertenecegobernanza__si_no=obj[0]).count()
        grafo_practicas_sino_gobernanza[obj[1]] =  valor

    grafo_practica_gobernanza_si = {}
    for obj in FormaGobernanza.objects.all():
        valor = filtro.filter(pertenecegobernanza__responde_si=obj).count()
        grafo_practica_gobernanza_si[obj.nombre] = valor


    dicc_practicas[anio] = (grafo_practicas_sino_agroecologica,grafo_practica_agroecologica_si,
                                grafo_practicas_sino_agroforestal,grafo_practica_agroforestal_si,
                                grafo_practicas_sino_ancentral,grafo_practica_ancestral_si,
                                grafo_practicas_sino_gobernanza,grafo_practica_gobernanza_si,
                                filtro1)

    return render(request, template, locals())

def seguridad(request, template="indicadores/seguridad.html"):
    filtro = _queryset_filtrado(request)
    anio = request.session['fecha']

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

    grafo_considera = {}
    for obj in CHOICE_JEFE:
        valor = filtro.filter(escasezalimentos__considera=obj[0]).count()
        grafo_considera[obj[1]] =  valor


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


    dicc_seguridad[anio] = (grafo_disponen,
                                 grafo_escasez,
                                conteo_fenomeno,
                                conteo_agricola,
                                conteo_economica,
                                filtro1,
                                grafo_considera)

    return render(request, template, locals())

def genero(request, template="indicadores/genero.html"):
    filtro = _queryset_filtrado(request)
    anio = request.session['fecha']

    dicc_genero = OrderedDict()

    filtro1 = filtro.count()

    grafo_genero_actividades = {}
    for obj in CHOICE_ACTIVIDADES_MUJERES:
        valor = filtro.filter(genero__actividades__icontains=obj[0]).count()
        grafo_genero_actividades[obj[1]] = valor

    grafo_genero_animal = {}
    for obj in CHOICE_JEFE:
        valor = filtro.filter(genero__animales=obj[0]).count()
        grafo_genero_animal[obj[1]] =  valor

    grafo_genero_equipo = {}
    for obj in CHOICE_JEFE:
        valor = filtro.filter(genero__equipos=obj[0]).count()
        grafo_genero_equipo[obj[1]] =  valor

    grafo_genero_transporte = {}
    for obj in CHOICE_JEFE:
        valor = filtro.filter(genero__transporte=obj[0]).count()
        grafo_genero_transporte[obj[1]] =  valor

    grafo_genero_tierra = {}
    for obj in CHOICE_JEFE:
        valor = filtro.filter(genero__tierra=obj[0]).count()
        grafo_genero_tierra[obj[1]] =  valor

    grafo_genero_pertenece = {}
    for obj in CHOICE_JEFE:
        valor = filtro.filter(genero__pertenece=obj[0]).count()
        grafo_genero_pertenece[obj[1]] =  valor

    mujer_organizacion = {}
    for obj in GeneroOrgComunitaria.objects.all():
        dato = filtro.filter(genero__cual_comunitaria=obj).count()
        if dato > 0:
            mujer_organizacion[obj] = dato

    grafo_genero_actividad = {}
    for obj in CHOICE_JEFE:
        valor = filtro.filter(genero__actividad=obj[0]).count()
        grafo_genero_actividad[obj[1]] =  valor

    grafo_genero_cual_actividad = {}
    for obj in GeneroActividadesComunitaria.objects.all():
        dato = filtro.filter(genero__cual_actvidad=obj).count()
        if dato > 0:
            grafo_genero_cual_actividad[obj] = dato

    dicc_genero[anio] = (grafo_genero_actividades,grafo_genero_animal,
                              grafo_genero_equipo,grafo_genero_transporte,
                              grafo_genero_tierra,grafo_genero_pertenece,
                              mujer_organizacion,grafo_genero_actividad,
                              grafo_genero_cual_actividad,filtro1
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

