from django.contrib import admin
from django.urls import path
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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
