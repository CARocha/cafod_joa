from django.shortcuts import render
from django.views.generic import ListView
from .models import SubirArchivos


# Create your views here.
class ArchivosList(ListView):
    model = SubirArchivos
    template_name = 'subirarchivos_list.html'


