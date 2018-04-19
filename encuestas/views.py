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

    cantidad_habitan = filtro.aggregate(t=Avg('detallemiembros__cantidad'))['t']
    cantidad_dependen = filtro.aggregate(t=Avg('detallemiembros__cantidad_dependen'))['t']

    dicc_sexo_dueno[anio] = (si_dueno,no_dueno,a_nombre,situacion,detalle_edad,filtro1,cantidad_habitan,cantidad_dependen)

    return render(request, template, locals())

def escolaridad(request, template="indicadores/escolaridad.html"):
    filtro = _queryset_filtrado(request)

    dicc_escolaridad = OrderedDict()
    dicc_grafo_tipo_educacion = OrderedDict()

    filtro1 = filtro.count()
    cantidad_miembros_hombres = filtro.filter(
                                entrevistado__departamento=request.session['departamento'],
                                entrevistado__sexo=2,
                                entrevistado__jefe=1).aggregate(num_total = Sum('escolaridad__total'))['num_total']

    cantidad_miembros_mujeres = filtro.filter(
                                entrevistado__departamento=request.session['departamento'],
                                entrevistado__sexo=1,
                                entrevistado__jefe=1).aggregate(num_total = Sum('escolaridad__total'))['num_total']

    grafo_educacion_hombre = filtro.filter(
                                entrevistado__departamento=request.session['departamento'],
                                entrevistado__sexo=2,
                                entrevistado__jefe=1).aggregate(
                                no_sabe_leer = Sum('escolaridad__no_leer'),
                                primaria_incompleta = Sum('escolaridad__pri_incompleta'),
                                primaria_completa = Sum('escolaridad__pri_completa'),
                                secundaria_incompleta = Sum('escolaridad__secu_incompleta'),
                                bachiller = Sum('escolaridad__bachiller'),
                                universitario = Sum('escolaridad__uni_tecnico'),
                            )

    grafo_educacion_mujer = filtro.filter(
                                entrevistado__sexo=1,
                                entrevistado__jefe=1).aggregate(
                                no_sabe_leer = Sum('escolaridad__no_leer'),
                                primaria_incompleta = Sum('escolaridad__pri_incompleta'),
                                primaria_completa = Sum('escolaridad__pri_completa'),
                                secundaria_incompleta = Sum('escolaridad__secu_incompleta'),
                                bachiller = Sum('escolaridad__bachiller'),
                                universitario = Sum('escolaridad__uni_tecnico'),
                            )

    tabla_educacion_hombre = []
    for e in CHOICE_ESCOLARIDAD:
        objeto = filtro.filter(escolaridad__sexo = e[0],
                entrevistado__sexo=2,
                entrevistado__jefe=1).aggregate(num_total = Sum('escolaridad__total'),
                no_leer = Sum('escolaridad__no_leer'),
                p_incompleta = Sum('escolaridad__pri_incompleta'),
                p_completa = Sum('escolaridad__pri_completa'),
                s_incompleta = Sum('escolaridad__secu_incompleta'),
                bachiller = Sum('escolaridad__bachiller'),
                universitario = Sum('escolaridad__uni_tecnico'),

                )

        fila = [e[1], objeto['num_total'],
                saca_porcentajes(objeto['no_leer'], objeto['num_total'], False),
                saca_porcentajes(objeto['p_incompleta'], objeto['num_total'], False),
                saca_porcentajes(objeto['p_completa'], objeto['num_total'], False),
                saca_porcentajes(objeto['s_incompleta'], objeto['num_total'], False),
                saca_porcentajes(objeto['bachiller'], objeto['num_total'], False),
                saca_porcentajes(objeto['universitario'], objeto['num_total'], False),
                ]
        tabla_educacion_hombre.append(fila)

    #tabla para cuando la mujer es jefe

    tabla_educacion_mujer = []
    for e in CHOICE_ESCOLARIDAD:
        objeto = filtro.filter(
                escolaridad__sexo = e[0],
                entrevistado__sexo=1,
                entrevistado__jefe=1).aggregate(num_total = Sum('escolaridad__total'),
                no_leer = Sum('escolaridad__no_leer'),
                p_incompleta = Sum('escolaridad__pri_incompleta'),
                p_completa = Sum('escolaridad__pri_completa'),
                s_incompleta = Sum('escolaridad__secu_incompleta'),
                bachiller = Sum('escolaridad__bachiller'),
                universitario = Sum('escolaridad__uni_tecnico'),

                )
        fila = [e[1], objeto['num_total'],
                saca_porcentajes(objeto['no_leer'], objeto['num_total'], False),
                saca_porcentajes(objeto['p_incompleta'], objeto['num_total'], False),
                saca_porcentajes(objeto['p_completa'], objeto['num_total'], False),
                saca_porcentajes(objeto['s_incompleta'], objeto['num_total'], False),
                saca_porcentajes(objeto['bachiller'], objeto['num_total'], False),
                saca_porcentajes(objeto['universitario'], objeto['num_total'], False),
                ]
        tabla_educacion_mujer.append(fila)
    dicc_escolaridad[year[1]] = (tabla_educacion_hombre,tabla_educacion_mujer,filtro1)
    dicc_grafo_tipo_educacion[year[1]] = (grafo_educacion_hombre, grafo_educacion_mujer, cantidad_miembros_hombres, cantidad_miembros_mujeres)

    return render(request, template, locals())

def energia(request, template="indicadores/energia.html"):
    filtro = _queryset_filtrado(request)

    dicc_energia = OrderedDict()

    filtro1 = filtro.count()
    grafo_tipo_energia = {}
    for obj in Energia.objects.all():
        valor = filtro.filter(tipoenergia__tipo=obj).count()
        grafo_tipo_energia[obj] =  valor

    grafo_panel_solar = {}
    for obj in CHOICE_PANEL_SOLAR:
        valor = filtro.filter(panelsolar__panel=obj[0]).count()
        grafo_panel_solar[obj[1]] =  valor

    grafo_fuente_energia = {}
    for obj in FuenteEnergia.objects.all():
        valor = filtro.filter(energiasolarcocinar__fuente=obj).count()
        grafo_fuente_energia[obj] =  valor

    grafo_tipo_cocina = {}
    for obj in Cocinas.objects.all():
        valor = filtro.filter(tipococinas__cocina=obj).count()
        grafo_tipo_cocina[obj] =  valor

    dicc_energia[year[1]] = (grafo_tipo_energia,grafo_panel_solar,grafo_fuente_energia,grafo_tipo_cocina,filtro1)

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

    grafo_agua_calidad = {}
    for obj in CHOICE_CALIDAD_AGUA:
        valor = filtro.filter(calidadagua__calidad=obj[0]).count()
        grafo_agua_calidad[obj[1]] =  valor

    grafo_agua_contaminada = {}
    for obj in TipoContamindaAgua.objects.all():
        valor = filtro.filter(contaminada__contaminada=obj).count()
        grafo_agua_contaminada[obj] =  valor

    grafo_agua_tratamiento = {}
    for obj in CHOICE_TRATAMIENTO:
        valor = filtro.filter(tratamientoagua__tratamiento=obj[0]).count()
        grafo_agua_tratamiento[obj[1]] =  valor

    grafo_agua_usos = {}
    for obj in CHOICE_OTRO_USO:
        valor = filtro.filter(usosagua__uso=obj[0]).count()
        grafo_agua_usos[obj[1]] =  valor

    dicc_agua['reparar'] = (grafo_agua_consumo,grafo_agua_disponibilidad,grafo_agua_calidad,grafo_agua_contaminada,grafo_agua_tratamiento,grafo_agua_usos,filtro1)

    return render(request, template, locals())

def organizaciones(request, template="indicadores/organizaciones.html"):
    filtro = _queryset_filtrado(request)

    dicc_organizacion = OrderedDict()

    filtro1 = filtro.count()
    grafo_pertenece = {}
    for obj in CHOICE_JEFE:
        valor = filtro.filter(organizacioncomunitaria__pertenece=obj[0]).count()
        grafo_pertenece[obj[1]] =  valor

    grafo_org_comunitarias = {}
    for obj in OrgComunitarias.objects.all():
        valor = filtro.filter(organizacioncomunitaria__caso_si=obj).count()
        if valor > 0:
            grafo_org_comunitarias[obj] =  valor

    grafo_beneficios = {}
    for obj in BeneficiosOrganizados.objects.all():
        valor = filtro.filter(organizacioncomunitaria__cuales_beneficios=obj).count()
        if valor > 0:
            grafo_beneficios[obj] =  valor

    dicc_organizacion['repaarar'] = (grafo_pertenece,grafo_org_comunitarias, grafo_beneficios,filtro1)

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

def seguridad(request, template="indicadores/seguridad.html"):
    filtro = _queryset_filtrado(request)

    dicc_seguridad = OrderedDict()

    filtro1 = filtro.count()
    grafo_economico = {}
    for obj in CHOICE_JEFE:
        valor = filtro.filter(seguridadalimentaria__economico=obj[0]).count()
        grafo_economico[obj[1]] =  valor

    grafo_secado = {}
    for obj in CHOICE_JEFE:
        valor = filtro.filter(seguridadalimentaria__secado=obj[0]).count()
        grafo_secado[obj[1]] =  valor

    grafo_tipo_secado = {}
    for obj in TipoSecado.objects.all():
        valor = filtro.filter(seguridadalimentaria__tipo_secado=obj).count()
        grafo_tipo_secado[obj] =  valor

    grafo_plan_cosecha = {}
    for obj in CHOICE_JEFE:
        valor = filtro.filter(seguridadalimentaria__plan_cosecha=obj[0]).count()
        grafo_plan_cosecha[obj[1]] =  valor

    grafo_ayuda = {}
    for obj in CHOICE_JEFE:
        valor = filtro.filter(seguridadalimentaria__ayuda=obj[0]).count()
        grafo_ayuda[obj[1]] =  valor

    grafo_suficiente_alimento = {}
    for obj in CHOICE_JEFE:
        valor = filtro.filter(seguridadalimentaria__suficiente_alimento=obj[0]).count()
        grafo_suficiente_alimento[obj[1]] =  valor

    grafo_consumo_diario = {}
    for obj in CHOICE_JEFE:
        valor = filtro.filter(seguridadalimentaria__consumo_diario=obj[0]).count()
        grafo_consumo_diario[obj[1]] =  valor


    conteo_fenomeno = {}
    for obj in CHOICE_FENOMENOS:
        valor = filtro.filter(respuestano41__fenomeno=obj[0]).count()
        conteo_fenomeno[obj[1]] =  valor

    conteo_agricola = {}
    for obj in CHOICE_AGRICOLA:
        valor = filtro.filter(respuestano41__agricola=obj[0]).count()
        conteo_agricola[obj[1]] =  valor

    conteo_mercado = {}
    for obj in CHOICE_MERCADO:
        valor = filtro.filter(respuestano41__mercado=obj[0]).count()
        conteo_mercado[obj[1]] =  valor

    conteo_inversion = {}
    for obj in CHOICE_INVERSION:
        valor = filtro.filter(respuestano41__inversion=obj[0]).count()
        conteo_inversion[obj[1]] =  valor

    grafo_adquiere_agua = {}
    for obj in AdquiereAgua.objects.all():
        valor = filtro.filter(otrasseguridad__adquiere_agua=obj).count()
        grafo_adquiere_agua[obj] =  valor

    grafo_tratamiento_agua = {}
    for obj in CHOICE_JEFE:
        valor = filtro.filter(otrasseguridad__tratamiento=obj[0]).count()
        grafo_tratamiento_agua[obj[1]] =  valor

    grafo_tipo_tratamientos = {}
    for obj in TrataAgua.objects.all():
        valor = filtro.filter(otrasseguridad__tipo_tratamiento=obj).count()
        grafo_tipo_tratamientos[obj] =  valor

    dicc_seguridad['repaara'] = (grafo_economico,
                                grafo_secado,
                                grafo_tipo_secado,
                                grafo_plan_cosecha,
                                grafo_ayuda,
                                grafo_suficiente_alimento,
                                grafo_consumo_diario,
                                conteo_fenomeno,
                                conteo_agricola,
                                conteo_mercado,
                                conteo_inversion,
                                grafo_adquiere_agua,
                                grafo_tratamiento_agua,
                                grafo_tipo_tratamientos,
                                filtro1)

    return render(request, template, locals())

def genero(request, template="indicadores/genero.html"):
    filtro = _queryset_filtrado(request)

    dicc_genero = OrderedDict()

    filtro1 = filtro.count()
    porcentaje_aporta_mujer = OrderedDict()
    for obj in CHOICER_INGRESO:
        porcentaje_aporta_mujer[obj[1]] = OrderedDict()
        for obj2 in CHOICE_PORCENTAJE:
            valor = filtro.filter(genero__tipo=obj[0], genero__porcentaje=obj2[0]).count()
            if valor > 0:
                porcentaje_aporta_mujer[obj[1]][obj2[1]] =  valor


    grafo_credito_mujer = {}
    for obj in CHOICE_JEFE:
        valor = filtro.filter(genero1__tipo=obj[0]).count()
        grafo_credito_mujer[obj[1]] =  valor

    grafo_bienes_mujer = {}
    for obj in CHOICER_COSAS_MUJER:
        valor_si = filtro.filter(genero2__pregunta=obj[0], genero2__respuesta=1).count()
        valor_no = filtro.filter(genero2__pregunta=obj[0], genero2__respuesta=2).count()
        grafo_bienes_mujer[obj[1]] =  (valor_si, valor_no)

    grafo_organizacion_mujer = {}
    for obj in CHOICE_JEFE:
        valor = filtro.filter(genero3__respuesta=obj[0]).count()
        grafo_organizacion_mujer[obj[1]] =  valor

    mujer_organizacion = {}
    for obj in OrgComunitarias.objects.all():
        dato = filtro.filter(organizacioncomunitaria__caso_si=obj,entrevistado__jefe=1).count()
        if dato > 0:
            mujer_organizacion[obj] = dato


    nivel_educacion_mujer = OrderedDict()
    for obj in CHOICER_NIVEL_MUJER:
        valor = filtro.filter(genero4__opcion=obj[0]).count()
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

