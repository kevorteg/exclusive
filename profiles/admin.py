from django.contrib import admin
from django.utils.html import mark_safe
from .models import Perfil, ConfiguracionAgencia, Tarifa, Galeria

class GaleriaInline(admin.TabularInline):
    model = Galeria
    extra = 10
    fields = ('imagen', 'preview_imagen')
    readonly_fields = ('preview_imagen',)

    def preview_imagen(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="width: 100px; height: auto; border-radius: 4px;" />', obj.imagen.url)
        return "No Image"
    preview_imagen.short_description = "Vista Previa"

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('nombre_preview', 'ciudad', 'tarifa', 'estado', 'verificada', 'activo')
    list_editable = ('estado', 'verificada', 'activo')
    search_fields = ('nombre', 'ciudad')
    list_filter = ('tarifa', 'ciudad', 'estado')
    prepopulated_fields = {'slug': ('nombre',)}
    inlines = [GaleriaInline]

    def nombre_preview(self, obj):
        if obj.foto_principal:
            return mark_safe(f'<img src="{obj.foto_principal.url}" width="50" height="50" style="object-fit:cover; border-radius:50%; margin-right:10px;" /> {obj.nombre}')
        return obj.nombre
    nombre_preview.short_description = "Modelo"

@admin.register(ConfiguracionAgencia)
class ConfiguracionAgenciaAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Evitar crear más de una configuración desde el admin si ya existe una
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(Tarifa)
class TarifaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio_hora', 'incluye_jacuzzi')
