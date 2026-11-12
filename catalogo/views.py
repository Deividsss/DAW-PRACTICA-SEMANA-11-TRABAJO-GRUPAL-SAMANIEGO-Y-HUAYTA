from django.db import OperationalError, ProgrammingError
from django.db.models import Count
from django.shortcuts import render
from django.views.generic import ListView

from .models import Producto


# ──────────────────────────── VISTA BASADA EN FUNCIÓN (FBV)
def home(request):
    """Página de bienvenida con un resumen del catálogo."""
    contexto = {
        "titulo": "Catálogo de Productos Tecnológicos",
        "total": 0,
        "disponibles": 0,
        "categorias": [],
        "error": None,
    }
    try:
        # QuerySets perezosos: solo tocan la BD cuando se evalúan (count/list).
        contexto["total"] = Producto.objects.count()
        contexto["disponibles"] = Producto.objects.filter(stock__gt=0).count()
        contexto["categorias"] = list(
            Producto.objects.values("categoria")
            .annotate(cantidad=Count("id"))
            .order_by("categoria")
        )
    except (OperationalError, ProgrammingError):
        # Manejo de errores: p. ej. si faltó ejecutar `migrate`.
        contexto["error"] = (
            "La base de datos aún no está lista. "
            "Ejecuta: python manage.py migrate"
        )
    return render(request, "home.html", contexto)


# ──────────────────────────── VISTA BASADA EN CLASE (CBV)
class ProductoListView(ListView):
    model = Producto
    template_name = "catalogo.html"
    context_object_name = "productos"

    def get_queryset(self):
        # QuerySet #1: solo productos con stock, ordenados por precio.
        qs = Producto.objects.filter(stock__gt=0).order_by("precio")

        # Si el usuario pide ver agotados, se parte de TODOS los productos.
        if self.request.GET.get("agotados") == "1":
            qs = Producto.objects.all().order_by("precio")

        # QuerySet #2: filtro por categoría (?categoria=Laptops).
        categoria = self.request.GET.get("categoria", "").strip()
        if categoria:
            qs = qs.filter(categoria__iexact=categoria)

        # Búsqueda por nombre (?q=lenovo).
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(nombre__icontains=q)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categorias"] = (
            Producto.objects.values_list("categoria", flat=True)
            .distinct()
            .order_by("categoria")
        )
        ctx["categoria_activa"] = self.request.GET.get("categoria", "")
        ctx["q"] = self.request.GET.get("q", "")
        ctx["ver_agotados"] = self.request.GET.get("agotados") == "1"
        return ctx
