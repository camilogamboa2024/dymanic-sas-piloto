from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Categoria(models.Model):
    nombre = models.CharField(max_length=60, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = _("categoría")
        verbose_name_plural = _("categorías")

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    sku = models.CharField(_("SKU"), max_length=30, unique=True)
    nombre = models.CharField(max_length=120)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    stock_minimo = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.sku})"

    # Helpers
    @property
    def stock_actual(self):
        return self.movimientos.aggregate(total=models.Sum("cantidad"))["total"] or 0

    @property
    def necesita_reposicion(self):
        return self.stock_actual <= self.stock_minimo


class MovimientoStock(models.Model):
    class Tipo(models.TextChoices):
        IN = ("IN", _("Entrada"))
        OUT = ("OUT", _("Salida"))
        AJUSTE = ("ADJ", _("Ajuste"))

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="movimientos")
    tipo = models.CharField(max_length=3, choices=Tipo.choices)
    cantidad = models.IntegerField()
    referencia = models.CharField(max_length=120, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        signo = "+" if self.cantidad >= 0 else ""
        return f"{self.timestamp:%Y-%m-%d} {self.producto.sku} {signo}{self.cantidad}"