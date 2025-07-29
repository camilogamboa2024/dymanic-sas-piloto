from django.urls import path
from .views import TopProductosView, RotacionView

app_name = "reportes"

urlpatterns = [
    path("top-productos/", TopProductosView.as_view(), name="top_productos"),
    path("rotacion/",      RotacionView.as_view(),     name="rotacion"),
]
