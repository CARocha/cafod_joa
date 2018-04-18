# -*- coding: utf-8 -*-
from django import forms
from .models import *
from lookups import *
import selectable.forms as selectable
from lugar.models import *

class ProductorAdminForm(forms.ModelForm):

    class Meta(object):
        model = Encuesta
        fields = '__all__'
        widgets = {
            'entrevistado': selectable.AutoCompleteSelectWidget(lookup_class=ProductorLookup),
        }

def fecha_choice():
    years = []
    for en in Encuesta.objects.order_by('year').values_list('year', flat=True):
        years.append((en,en))
    return list(sorted(set(years)))


class ConsultarForm(forms.Form):
    fecha = forms.ChoiceField(choices=fecha_choice(), label="Años", required=True)
    pais = forms.ModelChoiceField(queryset=Pais.objects.all(), required=True)
    departamento = forms.ModelMultipleChoiceField(queryset=Departamento.objects.filter(entrevistados__gt=1).distinct(), required=False)
    organizacion = forms.ModelMultipleChoiceField(queryset=OrganizacionResp.objects.all(), required=False)
    municipio = forms.ModelMultipleChoiceField(queryset=Municipio.objects.all(), required=False)
    comunidad = forms.ModelMultipleChoiceField(queryset=Comunidad.objects.all(), required=False)




