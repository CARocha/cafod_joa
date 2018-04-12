from django.shortcuts import render

# Create your views here.


def _queryset_filtrado(request):
    params = {}

    if request.session['fecha']:
        params['year'] = request.session['fecha']

    # if 'estacion' in request.session:
    #     params['estacion'] = request.session['estacion']

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

    return Encuesta.objects.filter(**params)
