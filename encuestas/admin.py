from django.contrib import admin
from .models import *


class OrganizacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'pais', 'departamento', 'municipio')

class EntrevistadoAdmin(admin.ModelAdmin):
    def queryset(self, request):
        if request.user.is_superuser:
            return Noticias.objects.all()
        return Noticias.objects.filter(user=request.user)

    def save_model(self, request, obj, form, change):
      obj.user = request.user
      obj.save()

    exclude = ('user',)
    list_display = ('nombre', 'sexo', 'jefe', 'pais', 'departamento')
    list_filter = ('sexo','pais','departamento')
    search_fields = ('nombre',)

# Register your models here.
admin.site.register(Encuestadores)
admin.site.register(OrganizacionResp, OrganizacionAdmin)
admin.site.register(Entrevistados, EntrevistadoAdmin)
