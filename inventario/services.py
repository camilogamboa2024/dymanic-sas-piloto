from django.db import transaction
from .models import Producto, MovimientoStock

@transaction.atomic
def crear_producto(*, sku, nombre, categoria, stock_inicial=0, stock_minimo=0, usuario=None):
    producto = Producto.objects.create(
        sku=sku, nombre=nombre, categoria=categoria, stock_minimo=stock_minimo
    )
    if stock_inicial:
        registrar_movimiento(
            producto=producto,
            tipo=MovimientoStock.Tipo.IN,
            cantidad=stock_inicial,
            referencia="Stock inicial",
            usuario=usuario,
        )
    return producto


def registrar_movimiento(*, producto, tipo, cantidad, referencia="", usuario=None):
    if tipo == MovimientoStock.Tipo.OUT and cantidad > 0:
        cantidad = -cantidad  # salidas se guardan negativas
    return MovimientoStock.objects.create(
        producto=producto,
        tipo=tipo,
        cantidad=cantidad,
        referencia=referencia,
        usuario=usuario,
    )


def get_productos_bajo_stock():
    from django.db.models import Sum, F, Value as V
    from django.db.models.functions import Coalesce

    return (
        Producto.objects.annotate(
            disponible=Coalesce(Sum("movimientos__cantidad"), V(0))
        ).filter(disponible__lte=F("stock_minimo"))
    )
