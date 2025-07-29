# dymanic/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # Panel de administración
    path("admin/", admin.site.urls),

    # Inventario
    path("inventario/", include("inventario.urls")),

    # Ventas (namespace 'ventas')
    path(
        "ventas/",
        include(("ventas.urls", "ventas"), namespace="ventas"),
    ),

    # Reportes (namespace 'reportes')
    path(
        "reportes/",
        include(("reportes.urls", "reportes"), namespace="reportes"),
    ),

    # Login / logout / password reset
    path("accounts/", include("django.contrib.auth.urls")),

    # Redirigir la raíz a inventario/productos/
    path(
        "",
        RedirectView.as_view(url="/inventario/productos/", permanent=False)
    ),
]
