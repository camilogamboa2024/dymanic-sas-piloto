# reportes/services.py

from datetime import date
from django.db.models import Sum, Q, F, FloatField, Value, Case, When
from django.db.models.functions import Coalesce
from inventario.models import Producto


def top_productos(start: date, end: date, limit: int = 5):
    """
    Retorna los productos más vendidos entre start y end.
    """
    return (
        Producto.objects.annotate(
            vendidos=Coalesce(
                Sum(
                    'lineaventa__cantidad',
                    filter=Q(lineaventa__factura__fecha__range=(start, end))
                ),
                0
            )
        )
        .filter(vendidos__gt=0)
        .order_by('-vendidos')[:limit]
    )


def rotacion_inventario(start: date, end: date):
    """
    Calcula rotación = ventas_totales / stock_promedio para cada producto.
    """
    qs = (
        Producto.objects.annotate(
            vendidos=Coalesce(
                Sum(
                    'lineaventa__cantidad',
                    filter=Q(lineaventa__factura__fecha__range=(start, end))
                ),
                0
            ),
            stock_inicial=Coalesce(
                Sum(
                    'movimientos__cantidad',
                    filter=Q(movimientos__timestamp__lt=start)
                ),
                0
            ),
            stock_final=Coalesce(
                Sum(
                    'movimientos__cantidad',
                    filter=Q(movimientos__timestamp__lte=end)
                ),
                0
            ),
        )
        .annotate(
            stock_promedio=(F('stock_inicial') + F('stock_final')) / Value(2),
            rotacion=Case(
                When(stock_promedio__gt=0, then=F('vendidos') / F('stock_promedio')),
                default=Value(0),
                output_field=FloatField(),
            ),
        )
        .order_by('-rotacion')
    )
    return qs
