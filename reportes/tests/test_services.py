import pytest
from datetime import date, timedelta

from inventario.models import Categoria, Producto, MovimientoStock
from ventas.models import Cliente, Factura, LineaVenta
from reportes.services import top_productos, rotacion_inventario

@pytest.mark.django_db
def test_top_productos_devuelve_vacio_si_no_hay_ventas():
    start = date.today() - timedelta(days=7)
    end = date.today()
    qs = top_productos(start, end, limit=5)
    assert list(qs) == []

@pytest.mark.django_db
def test_top_productos_agrupa_y_ordena_correctamente():
    cat = Categoria.objects.create(nombre="Cat A")
    p1 = Producto.objects.create(sku="SKU1", nombre="Producto 1", categoria=cat, stock_minimo=0, activo=True)
    p2 = Producto.objects.create(sku="SKU2", nombre="Producto 2", categoria=cat, stock_minimo=0, activo=True)
    cliente = Cliente.objects.create(nombre="Cliente X")
    f = Factura.objects.create(cliente=cliente, fecha=date.today())
    LineaVenta.objects.create(factura=f, producto=p1, cantidad=3, precio=100)
    LineaVenta.objects.create(factura=f, producto=p2, cantidad=5, precio=200)

    start = date.today() - timedelta(days=1)
    end = date.today() + timedelta(days=1)
    qs = list(top_productos(start, end, limit=2))

    assert qs[0].nombre == "Producto 2"
    assert qs[1].nombre == "Producto 1"
    assert len(qs) == 2

@pytest.mark.django_db
def test_rotacion_inventario_devuelve_vacio_si_no_hay_movimientos():
    start = date.today() - timedelta(days=30)
    end = date.today()
    qs = rotacion_inventario(start, end)
    assert list(qs) == []

@pytest.mark.django_db
def test_rotacion_inventario_calcula_y_orden_por_rotacion():
    cat = Categoria.objects.create(nombre="Cat B")
    prod = Producto.objects.create(sku="SKU3", nombre="Prod B", categoria=cat, stock_minimo=0, activo=True)
    MovimientoStock.objects.create(producto=prod, tipo="sal", cantidad=10)
    MovimientoStock.objects.create(producto=prod, tipo="sal", cantidad=5)

    start = date.today() - timedelta(days=1)
    end = date.today() + timedelta(days=1)
    qs = list(rotacion_inventario(start, end))

    assert len(qs) == 1
    row = qs[0]
    assert hasattr(row, "rotacion")
    row = qs[0]
    assert row.rotacion == 0.0
