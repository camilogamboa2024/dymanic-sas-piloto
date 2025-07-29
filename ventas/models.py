from django.db import models
from django.utils.translation import gettext_lazy as _
from inventario.models import Producto


class Cliente(models.Model):
    nombre = models.CharField(max_length=120)
    email = models.EmailField(blank=True)
    rut   = models.CharField("RUT/NIT", max_length=20, blank=True)

    def __str__(self):
        return self.nombre


class Factura(models.Model):
    fecha   = models.DateField(auto_now_add=True)
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="facturas",
    )
    total   = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"Fac #{self.id} – {self.fecha:%Y-%m-%d}"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("ventas:factura_detail", args=[self.pk])


class LineaVenta(models.Model):
    factura  = models.ForeignKey(
        Factura, on_delete=models.CASCADE, related_name="lineas"
    )
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio   = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ("factura", "producto")
