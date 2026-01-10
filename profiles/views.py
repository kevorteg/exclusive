from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.generic import TemplateView, DetailView, ListView
from .models import Perfil, ConfiguracionAgencia, Tarifa

def get_status_updates(request):
    """API endpoint for real-time status updates"""
    perfiles = Perfil.objects.filter(activo=True).values('id', 'slug', 'estado')
    return JsonResponse({'perfiles': list(perfiles)})

def get_common_context():
    """Helper to get context available globally if needed, or just for specific views."""
    try:
        agencia = ConfiguracionAgencia.objects.first()
    except ConfiguracionAgencia.DoesNotExist:
        agencia = None
    return {'agencia': agencia}

def home(request):
    agencia = ConfiguracionAgencia.objects.first()
    perfiles = Perfil.objects.filter(activo=True).select_related('tarifa')
    
    # Real Time Logic (Disponible = En Tiempo Real)
    disponibles = perfiles.filter(estado='DISPONIBLE')
    
    context = {
        'agencia': agencia,
        'perfiles': perfiles,
        'en_linea_gold': disponibles.filter(tarifa__nombre='GOLD'),
        'en_linea_platinum': disponibles.filter(tarifa__nombre='PLATINUM'),
        'total_gold': disponibles.filter(tarifa__nombre='GOLD').count(),
        'total_platinum': disponibles.filter(tarifa__nombre='PLATINUM').count(),
        'total_presentes': disponibles.count(),
        'count_18_25': disponibles.filter(edad__gte=18, edad__lte=25).count(),
        'count_25_plus': disponibles.filter(edad__gt=25).count(),
        'tarifas_gold': Tarifa.objects.filter(nombre='GOLD').first(),
        'tarifas_platinum': Tarifa.objects.filter(nombre='PLATINUM').first(),
    }
    return render(request, 'home.html', context)

def perfil_detalle(request, slug):
    perfil = get_object_or_404(Perfil, slug=slug, activo=True)
    context = get_common_context()
    context['perfil'] = perfil
    return render(request, 'perfil_detalle.html', context)

def acompañantes(request):
    gold = Perfil.objects.filter(activo=True, tarifa__nombre='GOLD')
    platinum = Perfil.objects.filter(activo=True, tarifa__nombre='PLATINUM')
    context = get_common_context()
    context.update({'gold': gold, 'platinum': platinum})
    return render(request, 'acompañantes.html', context)

def instalaciones(request):
    return render(request, 'instalaciones.html', get_common_context())

def contacto(request):
    return render(request, 'contacto.html', get_common_context())

# HTMX Partials
def profiles_grid_partial(request):
    perfiles = Perfil.objects.filter(activo=True).select_related('tarifa')
    context = {'perfiles': perfiles}
    return render(request, 'partials/profiles_grid.html', context)

def live_panel_partial(request):
    # Re-use logic to get available/online profiles
    perfiles = Perfil.objects.filter(activo=True).select_related('tarifa')
    disponibles = perfiles.filter(estado='DISPONIBLE')
    ocupadas = perfiles.filter(estado='OCUPADA')
    
    context = {
        'en_linea_gold': disponibles.filter(tarifa__nombre='GOLD'),
        'en_linea_platinum': disponibles.filter(tarifa__nombre='PLATINUM'),
        'en_linea_ocupadas': ocupadas,
    }
    return render(request, 'partials/live_panel_content.html', context)
