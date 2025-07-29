from django.urls import path
from . import views

app_name = "inventario"

urlpatterns = [
    path("productos/", views.ProductoList.as_view(), name="productos"),
    path("productos/nuevo/", views.ProductoCreate.as_view(), name="producto_create"),
    path("productos/<int:pk>/", views.ProductoDetail.as_view(), name="producto_detail"),
    path("movimientos/nuevo/", views.MovimientoCreate.as_view(), name="movimiento_create"),
]
