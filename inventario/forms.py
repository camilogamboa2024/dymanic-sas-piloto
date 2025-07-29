from django import forms
from .models import Producto, MovimientoStock
from .services import crear_producto, registrar_movimiento


class ProductoForm(forms.ModelForm):
    stock_inicial = forms.IntegerField(min_value=0, initial=0)

    class Meta:
        model = Producto
        fields = ("sku", "nombre", "categoria", "stock_minimo", "activo")

    def save(self, usuario=None, commit=True):
        data = self.cleaned_data
        return crear_producto(
            sku=data["sku"],
            nombre=data["nombre"],
            categoria=data["categoria"],
            stock_inicial=data["stock_inicial"],
            stock_minimo=data["stock_minimo"],
            usuario=usuario,
        )


class MovimientoForm(forms.ModelForm):
    class Meta:
        model = MovimientoStock
        fields = ("producto", "tipo", "cantidad", "referencia")

    def save(self, usuario=None, commit=True):
        return registrar_movimiento(usuario=usuario, **self.cleaned_data)
