from django.test import TestCase
from django.urls import reverse

from .models import Producto


class CatalogoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Producto.objects.create(nombre="laptop dell", precio="2899.00", categoria="Laptops", stock=5)
        Producto.objects.create(nombre="mouse logitech", precio="59.90", categoria="Accesorios", stock=0)

    def test_home_responde_200(self):
        r = self.client.get(reverse("home"))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context["total"], 2)

    def test_catalogo_oculta_agotados_por_defecto(self):
        r = self.client.get(reverse("catalogo"))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context["productos"]), 1)

    def test_catalogo_muestra_agotados_si_se_pide(self):
        r = self.client.get(reverse("catalogo"), {"agotados": "1"})
        self.assertEqual(len(r.context["productos"]), 2)
        self.assertContains(r, "Agotado")

    def test_filtro_por_categoria(self):
        r = self.client.get(reverse("catalogo"), {"categoria": "laptops"})
        self.assertEqual([p.nombre for p in r.context["productos"]], ["laptop dell"])

    def test_precio_formateado(self):
        r = self.client.get(reverse("catalogo"))
        self.assertContains(r, "2,899.00")
