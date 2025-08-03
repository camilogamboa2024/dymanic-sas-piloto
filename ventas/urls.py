from django.urls import path
from .views import FacturaCreate, FacturaDetail, VentasResumen

app_name = "ventas"

urlpatterns = [
    path("nueva/", FacturaCreate.as_view(), name="factura_create"),
    path("<int:pk>/", FacturaDetail.as_view(), name="factura_detail"),
    path("resumen/", VentasResumen.as_view(), name="resumen"),  # para /ventas/resumen/
]
