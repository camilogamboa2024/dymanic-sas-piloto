# ventas/forms.py

from django import forms
from django.forms import inlineformset_factory
from .models import Factura, LineaVenta


class FacturaForm(forms.ModelForm):
    """
    Form para la cabecera de la factura (solo cliente).
    La fecha se asigna automáticamente en el modelo.
    """
    class Meta:
        model = Factura
        fields = ("cliente",)


# Formset para las líneas de venta dentro de la misma factura
LineaFormSet = inlineformset_factory(
    Factura,
    LineaVenta,
    # Usamos el nombre real del campo en tu modelo:
    fields=("producto", "cantidad", "precio"),
    extra=1,
    can_delete=False,
)
