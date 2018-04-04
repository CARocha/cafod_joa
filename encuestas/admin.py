from django.contrib import admin
from .models import *
from .forms import *


class InlineDuenoSi(admin.TabularInline):
    model = DuenoSi
    extra = 1
    max_num = 1

class InlineDuenoNo(admin.TabularInline):
    model = DuenoNo
    extra = 1
    max_num = 1

class InlineDetalleMiembros(admin.TabularInline):
    model = DetalleMiembros
    extra = 1

class InlineCondicionesVida(admin.TabularInline):
    model = CondicionesVida
    extra = 1

class InlineAccesoAgua(admin.TabularInline):
    model = AccesoAgua
    extra = 1
    max_num = 1

class InlineDisponibilidadAgua(admin.TabularInline):
    model = DisponibilidadAgua
    extra = 1
    max_num = 1

class InlineUsosAgua(admin.TabularInline):
    model = UsosAgua
    extra = 1
    max_num = 5

class InlineOrganizacionComunitaria(admin.TabularInline):
    model = OrganizacionSocialProductiva
    extra = 1
    max_num = 1

class InlineDescripcion(admin.TabularInline):
    model = Descripcion
    extra = 1
    max_num = 1

class InlineDistribucionupf(admin.TabularInline):
    model = Distribucionupf
    extra = 1
    max_num = 6

class InlineCultivosAnuales(admin.TabularInline):
    model = CultivosAnuales
    extra = 1

class InlineCultivosHuerto(admin.TabularInline):
    model = CultivosHuerto
    extra = 1

class InlineFrutasCultivosPerennes(admin.TabularInline):
    model = FrutasCultivosPerennes
    extra = 1

class InlineGanaderia(admin.TabularInline):
    model = Ganaderia
    extra = 1

class InlinePracticasAgroecologicas(admin.TabularInline):
    model = PracticasAgroecologicas
    extra = 1
    max_num = 1

class InlineManejoAgroforestal(admin.TabularInline):
    model = ManejoAgroforestal
    extra = 1
    max_num = 1

class InlinePracticasAgricolasAncestrales(admin.TabularInline):
    model = PracticasAgricolasAncestrales
    extra = 1
    max_num = 1

class InlinePerteneceGobernanza(admin.TabularInline):
    model = PerteneceGobernanza
    extra = 1
    max_num = 1

class InlineSeguridadAlimentaria(admin.TabularInline):
    model = SeguridadAlimentaria
    extra = 1
    max_num = 1

class InlineEscasezAlimentos(admin.TabularInline):
    model = EscasezAlimentos
    extra = 1
    max_num = 1

class InlineUsoSemilla(admin.TabularInline):
    model = UsoSemilla
    extra = 1
    max_num = 1

class InlineGenero(admin.TabularInline):
    model = Genero
    extra = 1
    max_num = 1

class OrganizacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'pais', 'departamento', 'municipio')

class EntrevistadoAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
      obj.user = request.user
      obj.save()

    exclude = ('user',)
    list_display = ('nombre', 'sexo', 'jefe', 'pais', 'departamento')
    list_filter = ('sexo','pais','departamento')
    search_fields = ('nombre',)


class AdminEncuesta(admin.ModelAdmin):
    form = ProductorAdminForm
    fields = (('entrevistado','fecha'),('encuestador'), 'org_responsable','dueno',)
    def queryset(self, request):
        if request.user.is_superuser:
            return Encuesta.objects.all()
        return Encuesta.objects.filter(user=request.user)

    def save_model(self, request, obj, form, change):
      obj.user = request.user
      obj.save()

    exclude = ('user',)
    inlines = [InlineDuenoSi,InlineDuenoNo,InlineDetalleMiembros,InlineCondicionesVida,
                InlineAccesoAgua,InlineDisponibilidadAgua,InlineUsosAgua,
                InlineOrganizacionComunitaria,InlineDescripcion,InlineDistribucionupf,
                InlineCultivosAnuales,InlineCultivosHuerto,InlineFrutasCultivosPerennes,
                InlineGanaderia,InlinePracticasAgroecologicas,InlineManejoAgroforestal,
                InlinePracticasAgricolasAncestrales,InlinePerteneceGobernanza,
                InlineSeguridadAlimentaria,InlineEscasezAlimentos,InlineUsoSemilla,
                InlineGenero]

    list_display = ('entrevistado','dueno','org_responsable','get_municipio','get_comunidad' ,'year')
    list_filter = ('org_responsable','year','entrevistado__pais','entrevistado__pais__departamento')
    search_fields = ('entrevistado__nombre',)

    def get_departamento(self, obj):
        return obj.entrevistado.departamento
    get_departamento.short_description = 'Departamento'
    #get_departamento.admin_order_field = 'entrevistado__departamento'

    def get_municipio(self, obj):
        return obj.entrevistado.municipio
    get_municipio.short_description = 'Municipio'
    get_municipio.admin_order_field = 'entrevistado__departamento__municipio'

    def get_comunidad(self, obj):
        return obj.entrevistado.comunidad
    get_comunidad.short_description = 'Comunidad'
    get_comunidad.admin_order_field = 'entrevistado__departamento__municipio__comunidad'

    # class Media:
    #     css = {
    #         "all": ("css/my_styles_admin.css",)
    #     }
    #     js = ("js/code_admin.js",)

# Register your models here.
admin.site.register(Encuestadores)
admin.site.register(OrganizacionResp, OrganizacionAdmin)
admin.site.register(Entrevistados, EntrevistadoAdmin)
admin.site.register(Encuesta, AdminEncuesta)
admin.site.register(Idiomas)
admin.site.register(AguaConsumo)
admin.site.register(OrgComunitarias)
admin.site.register(BeneficiosOrganizados)
admin.site.register(Cultivos)
admin.site.register(CultivosHuertos)
admin.site.register(Frutas)
admin.site.register(Animales)
admin.site.register(FormaGobernanza)
admin.site.register(GeneroOrgComunitaria)
admin.site.register(GeneroActividadesComunitaria)
