from django.contrib import admin
from .models import Cliente, Factura, LineaVenta

# Permite añadir líneas de venta desde la misma factura (inline)
class LineaVentaInline(admin.TabularInline):
    model = LineaVenta
    extra = 1  # Cantidad de líneas vacías que aparecerán por defecto

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'cliente', 'total')
    inlines = [LineaVentaInline]

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'rut')

@admin.register(LineaVenta)
class LineaVentaAdmin(admin.ModelAdmin):
    list_display = ('factura', 'producto', 'cantidad', 'precio')

