from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from .models import Producto, MovimientoStock
from .forms import ProductoForm, MovimientoForm
from .services import get_productos_bajo_stock
from templates import *




class ProductoList(LoginRequiredMixin, ListView):
    model = Producto
    ordering = ["nombre"]
    paginate_by = 25
    queryset = Producto.objects.select_related("categoria")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["bajo_stock"] = get_productos_bajo_stock()
        return ctx


class ProductoCreate(LoginRequiredMixin, CreateView):
    form_class = ProductoForm
    success_url = reverse_lazy("inventario:productos")
    template_name = "inventario/producto_form.html"  
    def form_valid(self, form):
        """
        Guardamos el producto una única vez y redirigimos
        sin invocar el segundo form.save() de CreateView.
        """
        self.object = form.save(usuario=self.request.user)
        return HttpResponseRedirect(self.get_success_url())


class ProductoDetail(LoginRequiredMixin, DetailView):
    model = Producto

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["movimientos"] = (
            MovimientoStock.objects.filter(producto=self.object)
            .order_by("-timestamp")[:50]
        )
        return ctx


class MovimientoCreate(LoginRequiredMixin, CreateView):
    form_class = MovimientoForm
    success_url = reverse_lazy("inventario:productos")

    def form_valid(self, form):
        self.object = form.save(usuario=self.request.user)
        return HttpResponseRedirect(self.get_success_url())
