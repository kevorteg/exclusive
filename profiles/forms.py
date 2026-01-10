from django import forms
from .models import Tarifa

class TarifaAdminForm(forms.ModelForm):
    # Campos de texto para permitir puntos (Ej: 400.000)
    precio_hora = forms.CharField(label="Precio x Hora", help_text="Puedes usar puntos. Ej: 400.000")
    precio_30_min = forms.CharField(label="Precio x 30 Min", required=False, help_text="Puedes usar puntos. Ej: 200.000")
    precio_servicio_completo = forms.CharField(label="Precio Servicio Completo", required=False, help_text="Puedes usar puntos. Ej: 600.000")

    class Meta:
        model = Tarifa
        fields = '__all__'

    def clean_price_field(self, value):
        if not value:
            return None
        # Eliminar puntos y espacios
        clean_value = value.replace('.', '').replace(' ', '')
        # Si usan comas para decimales, reemplazar o quitar según lógica (asumimos entero)
        clean_value = clean_value.replace(',', '.') 
        try:
            return float(clean_value)
        except ValueError:
            raise forms.ValidationError("Por favor ingresa un número válido.")

    def clean_precio_hora(self):
        return self.clean_price_field(self.cleaned_data.get('precio_hora'))

    def clean_precio_30_min(self):
        return self.clean_price_field(self.cleaned_data.get('precio_30_min'))

    def clean_precio_servicio_completo(self):
        return self.clean_price_field(self.cleaned_data.get('precio_servicio_completo'))
