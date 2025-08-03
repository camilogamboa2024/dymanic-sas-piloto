from django.urls import path
from . import views

app_name = "inventario"

urlpatterns = [
    path("productos/", views.ProductoList.as_view(), name="productos"),
    path("productos/nuevo/", views.ProductoCreate.as_view(), name="producto_create"),
    path("productos/<int:pk>/", views.ProductoDetail.as_view(), name="producto_detail"),

    # Rutas nuevas para editar y eliminar
    path("productos/<int:pk>/editar/", views.ProductoUpdate.as_view(), name="producto_update"),
    path("productos/<int:pk>/eliminar/", views.ProductoDelete.as_view(), name="producto_delete"),

    path("movimientos/nuevo/", views.MovimientoCreate.as_view(), name="movimiento_create"),
]


