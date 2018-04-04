# -*- coding: utf-8 -*-
from django import forms
from .models import *
from lookups import *
import selectable.forms as selectable

class ProductorAdminForm(forms.ModelForm):

    class Meta(object):
        model = Encuesta
        fields = '__all__'
        widgets = {
            'entrevistado': selectable.AutoCompleteSelectWidget(lookup_class=ProductorLookup),
        }
