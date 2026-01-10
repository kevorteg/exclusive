from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from profiles import views

urlpatterns = [
    # Admin Seguro
    path('gestion-exclusiva/', admin.site.urls), # URL cambiada por seguridad
    
    # Rutas Públicas
    path('', views.home, name='home'),
    path('perfil/<slug:slug>/', views.perfil_detalle, name='perfil_detalle'),
    path('acompanantes/', views.acompañantes, name='acompañantes'),
    path('instalaciones/', views.instalaciones, name='instalaciones'),
    path('contacto/', views.contacto, name='contacto'),
    path('api/status/', views.get_status_updates, name='api_status'),

    # HTMX Partials
    path('partials/profiles-grid/', views.profiles_grid_partial, name='profiles_grid_partial'),
    path('partials/live-panel/', views.live_panel_partial, name='live_panel_partial'),
    
    # Cambio de Idioma
    path('i18n/', include('django.conf.urls.i18n')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
