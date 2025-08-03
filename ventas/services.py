from django.db import transaction
from decimal import Decimal
from inventario.services import registrar_movimiento
from inventario.models import MovimientoStock
from .models import Factura, LineaVenta


@transaction.atomic
def crear_factura(*, cliente, line_items, usuario=None):
    """
    Crea una factura y descuenta stock.

    line_items = [
        {"producto": prod_obj, "cantidad": 2, "precio": Decimal("15000")},
        ...
    ]
    """
    factura = Factura.objects.create(cliente=cliente)
    total = Decimal("0")

    for item in line_items:
        # Evitar error si 'factura' viene en item
        item.pop('factura', None)  
        
        LineaVenta.objects.create(factura=factura, **item)
        total += item["precio"] * item["cantidad"]

        # registrar movimiento de salida
        registrar_movimiento(
            producto=item["producto"],
            tipo=MovimientoStock.Tipo.OUT,
            cantidad=item["cantidad"],
            referencia=f"Venta #{factura.id}",
            usuario=usuario,
        )

    factura.total = total
    factura.save()
    return factura

