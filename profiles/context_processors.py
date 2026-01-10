from .models import Perfil, Tarifa, ConfiguracionAgencia

def global_context(request):
    """
    Context processor to make common data available across all templates.
    Used for the global Floating Action Buttons (Live Panel & Rates).
    """
    agencia = ConfiguracionAgencia.objects.first()
    
    # We need lists for the Live Panel
    perfiles_activos = Perfil.objects.filter(activo=True).select_related('tarifa')
    # For the panel, we typically show those "In Real Time" or just grouped by status/tariff
    # The home view filtered by 'DISPONIBLE' for 'en_linea_gold' lists.
    # Let's replicate the logic from home view so the panel works the same way everywhere.
    
    disponibles = perfiles_activos.filter(estado='DISPONIBLE')
    
    return {
        'global_agencia': agencia, # Renamed to avoid basic conflict, though 'agencia' is used in base.html
        'en_linea_gold': disponibles.filter(tarifa__nombre='GOLD'),
        'en_linea_platinum': disponibles.filter(tarifa__nombre='PLATINUM'),
        'tarifas_gold': Tarifa.objects.filter(nombre='GOLD').first(),
        'tarifas_platinum': Tarifa.objects.filter(nombre='PLATINUM').first(),
    }
