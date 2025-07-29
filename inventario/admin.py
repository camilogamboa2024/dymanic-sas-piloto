from django.contrib import admin
from .models import Categoria, Producto, MovimientoStock


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "descripcion")
    search_fields = ("nombre",)
    ordering = ("nombre",)
    list_per_page = 25


class MovimientoInline(admin.TabularInline):
    """
    Permite ver y añadir movimientos directamente
    desde la ficha del producto.
    """
    model = MovimientoStock
    extra = 0
    fields = ("tipo", "cantidad", "referencia", "usuario", "timestamp")
    readonly_fields = ("timestamp",)
    autocomplete_fields = ("usuario",)
    show_change_link = True


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        "sku",
        "nombre",
        "categoria",
        "stock_actual",
        "stock_minimo",
        "activo",
        "necesita_reposicion",
    )
    list_filter = ("categoria", "activo")
    search_fields = ("sku", "nombre",)
    autocomplete_fields = ("categoria",)
    readonly_fields = ("stock_actual", "necesita_reposicion", "created_at")
    inlines = [MovimientoInline]
    list_per_page = 25


    def necesita_reposicion(self, obj):
        return obj.necesita_reposicion
    necesita_reposicion.boolean = True
    necesita_reposicion.short_description = "Bajo Stock"


@admin.register(MovimientoStock)
class MovimientoStockAdmin(admin.ModelAdmin):
    list_display = ("producto", "tipo", "cantidad", "usuario", "referencia", "timestamp")
    list_filter = ("tipo", "timestamp")
    search_fields = ("producto__nombre", "producto__sku", "referencia")
    autocomplete_fields = ("producto", "usuario")
    readonly_fields = ("timestamp",)
    date_hierarchy = "timestamp"
    list_per_page = 50
