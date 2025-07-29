import pytest
from django.urls import reverse
from inventario.models import Categoria, Producto, MovimientoStock
from inventario.services import registrar_movimiento, get_productos_bajo_stock


@pytest.fixture
def categoria(db):
    return Categoria.objects.create(nombre="Bebidas")


@pytest.fixture
def producto(categoria):
    return Producto.objects.create(
        sku="AGUA01",
        nombre="Agua",
        categoria=categoria,
        stock_minimo=5,
    )


@pytest.mark.django_db
def test_registrar_entrada_y_salida(producto):
    registrar_movimiento(producto=producto, tipo=MovimientoStock.Tipo.IN, cantidad=10)
    assert producto.stock_actual == 10

    registrar_movimiento(producto=producto, tipo=MovimientoStock.Tipo.OUT, cantidad=4)
    assert producto.stock_actual == 6


@pytest.mark.django_db
def test_get_productos_bajo_stock(producto):
    registrar_movimiento(producto=producto, tipo=MovimientoStock.Tipo.IN, cantidad=2)
    bajos = get_productos_bajo_stock()
    assert producto in bajos


@pytest.mark.django_db
def test_producto_create_view(client, django_user_model, categoria):
    user = django_user_model.objects.create_user("u1", password="pass12345")
    client.login(username="u1", password="pass12345")

    resp = client.post(
        reverse("inventario:producto_create"),
        {
            "sku": "SKU99",
            "nombre": "Jugo",
            "categoria": categoria.id,
            "stock_minimo": 1,
            "stock_inicial": 3,
            "activo": True,
        },
    )
    assert resp.status_code == 302
    assert Producto.objects.filter(sku="SKU99").exists()
