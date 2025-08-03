from decimal import Decimal
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ValidationError
from .models import Factura
from .forms import FacturaForm, LineaFormSet
from .services import crear_factura
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from datetime import date


# 1. Vista para crear facturas
class FacturaCreate(LoginRequiredMixin, CreateView):
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
            # 🔁 Limpiamos cada línea para evitar duplicados de 'factura'
            cleaned_items = []
            for item in linea_formset.cleaned_data:
                item.pop('factura', None)  # importante
                cleaned_items.append(item)

            factura = crear_factura(
                cliente=form.cleaned_data["cliente"],
                line_items=cleaned_items,
                usuario=self.request.user,
            )
        except ValidationError as e:
            form.add_error(None, e.message)
            return self.render_to_response(
                self.get_context_data(form=form, linea_formset=linea_formset)
            )

        return HttpResponseRedirect(self.get_success_url(factura))

    def get_success_url(self, factura=None):
        if factura:
            return factura.get_absolute_url()
        return reverse_lazy("ventas:factura_list")


# 2. Vista detalle de factura
class FacturaDetail(LoginRequiredMixin, DetailView):
    model = Factura
    template_name = "ventas/factura_detail.html"


# 3. Vista de resumen de ventas
class VentasResumen(PermissionRequiredMixin, TemplateView):
    permission_required = "ventas.view_resumen"
    template_name = "ventas/resumen.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        target = self.request.GET.get("date") or date.today().isoformat()
        facturas = Factura.objects.filter(fecha=target)

        ctx["target"] = target
        ctx["total_facturas"] = facturas.count()
        ctx["total_unidades"] = facturas.aggregate(total=Sum("lineas__cantidad"))["total"] or 0

        total_monto = facturas.aggregate(
            total=Sum(
                ExpressionWrapper(
                    F("lineas__cantidad") * F("lineas__precio"),
                    output_field=DecimalField()
                )
            )
        )["total"] or 0

        ctx["total_monto"] = total_monto

        ventas = []
        for factura in facturas:
            for linea in factura.lineas.all():
                ventas.append({
                    "fecha": factura.fecha,
                    "producto": linea.producto.nombre,
                    "cantidad": linea.cantidad,
                    "total": linea.cantidad * linea.precio,
                })

        ctx["ventas"] = ventas
        return ctx
