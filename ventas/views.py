from decimal import Decimal
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render

from .models import Factura
from .forms import FacturaForm, LineaFormSet
from .services import crear_factura


class FacturaCreate(LoginRequiredMixin, CreateView):
    """
    Vista para crear una nueva factura con su formset de líneas.
    """
    model = Factura
    form_class = FacturaForm
    template_name = "ventas/factura_form.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["linea_formset"] = kwargs.get("linea_formset") or LineaFormSet()
        return ctx

    def form_valid(self, form):
        linea_formset = LineaFormSet(self.request.POST)
        if not linea_formset.is_valid():
            return self.render_to_response(
                self.get_context_data(form=form, linea_formset=linea_formset)
            )

        try:
            factura = crear_factura(
                cliente=form.cleaned_data["cliente"],
                line_items=linea_formset.cleaned_data,
                usuario=self.request.user,
            )
        except ValidationError as e:
            form.add_error(None, e.message)
            return self.render_to_response(
                self.get_context_data(form=form, linea_formset=linea_formset)
            )

        return HttpResponseRedirect(self.get_success_url(factura))

    def get_success_url(self, factura=None):
        # Si pasamos la factura recién creada, redirigimos a su detalle
        if factura:
            return factura.get_absolute_url()
        # Fallback
        return reverse_lazy("ventas:factura_list")


class FacturaDetail(LoginRequiredMixin, DetailView):
    """
    Vista para mostrar el detalle de una factura.
    """
    model = Factura
    template_name = "ventas/factura_detail.html"


class VentasResumen(PermissionRequiredMixin, TemplateView):
    """
    Vista de resumen diario de ventas.
    Requiere el permiso 'ventas.view_resumen'.
    """
    permission_required = "ventas.view_resumen"
    template_name = "ventas/resumen.html"

    def get_context_data(self, **kwargs):
        from django.db.models import Sum
        from datetime import date

        ctx = super().get_context_data(**kwargs)
        target = self.request.GET.get("date") or date.today().isoformat()
        qs = Factura.objects.filter(fecha=target)
        ctx.update({
            "target": target,
            "total_facturas": qs.count(),
            "total_unidades": qs.aggregate(total=Sum("lineas__cantidad"))["total"] or 0,
            "total_monto": qs.aggregate(total=Sum("total"))["total"] or Decimal("0"),
        })
        return ctx
