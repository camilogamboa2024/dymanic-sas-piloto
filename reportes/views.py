from datetime import date
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import FechaRangoForm
from .services import top_productos, rotacion_inventario

class TopProductosView(LoginRequiredMixin, TemplateView):
    template_name = "reportes/top_productos.html"

    def get_context_data(self, **kwargs):
        ctx  = super().get_context_data(**kwargs)
        form = FechaRangoForm(self.request.GET or None)
        if form.is_valid():
            inicio = form.cleaned_data["inicio"]
            fin    = form.cleaned_data["fin"]
        else:
            fin    = date.today()
            inicio = fin.replace(day=1)
        ctx["form"]      = form
        ctx["productos"] = top_productos(inicio, fin)
        return ctx

class RotacionView(LoginRequiredMixin, TemplateView):
    template_name = "reportes/rotacion.html"

    def get_context_data(self, **kwargs):
        ctx  = super().get_context_data(**kwargs)
        form = FechaRangoForm(self.request.GET or None)
        if form.is_valid():
            inicio = form.cleaned_data["inicio"]
            fin    = form.cleaned_data["fin"]
        else:
            fin    = date.today()
            inicio = fin.replace(day=1)
        ctx["form"]      = form
        ctx["productos"] = rotacion_inventario(inicio, fin)
        return ctx
