from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError

class ConfiguracionAgencia(models.Model):
    whatsapp_central = models.CharField(max_length=20, help_text="Número central de la agencia (Ej: 573001234567)")
    email_reservas = models.EmailField(blank=True, null=True)
    # logo = models.ImageField(upload_to='agencia/', blank=True, null=True) # Puedes descomentar si añades manejo de logo

    def save(self, *args, **kwargs):
        if not self.pk and ConfiguracionAgencia.objects.exists():
             raise ValidationError('Solo puede existir una configuración de agencia')
        return super(ConfiguracionAgencia, self).save(*args, **kwargs)

    def __str__(self):
        return "Configuración de Agencia"

    class Meta:
        verbose_name = "Configuración Agencia"
        verbose_name_plural = "Configuración Agencia"

class Tarifa(models.Model):
    CATEGORIAS = [
        ('BASIC', 'Estándar'),
        ('GOLD', 'Gold'),
        ('PLATINUM', 'Platino'),
    ]
    nombre = models.CharField(max_length=10, choices=CATEGORIAS)
    precio_hora = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Precio x Hora")
    precio_30_min = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Precio x 30 Min", null=True, blank=True)
    precio_servicio_completo = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    incluye_jacuzzi = models.BooleanField(default=False)

    def __str__(self):
        return self.get_nombre_display()

class Perfil(models.Model):
    # Datos Básicos
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    edad = models.PositiveIntegerField()
    ciudad = models.CharField(max_length=50, default="Cali")
    
    # Relaciones y Negocio
    tarifa = models.ForeignKey(Tarifa, on_delete=models.PROTECT, related_name='perfiles', null=True, blank=True)
    descripcion_corta = models.CharField(max_length=200, help_text="Frase gancho para el card", default="Modelo Exclusiva")
    biografia_larga = models.TextField(verbose_name="Biografía Detallada", default="Información detallada pendiente.")
    
    # Media
    foto_principal = models.ImageField(upload_to='fotos_perfiles/')
    
    # Estado
    ESTADOS = [
        ('DISPONIBLE', 'Disponible'),
        ('OCUPADA', 'Ocupada'),
        ('DESCANSO', 'En Descanso'),
        ('NO_DISPONIBLE', 'No Disponible'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADOS, default='NO_DISPONIBLE', verbose_name="Estado Actual")
    verificada = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super(Perfil, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} ({self.tarifa})"

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"

class Galeria(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='fotos')
    imagen = models.ImageField(upload_to='galeria_perfiles/')
    
    def __str__(self):
        return f"Foto de {self.perfil.nombre}"
