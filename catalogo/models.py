from django.db import models


class Producto(models.Model):
    """Producto tecnológico del catálogo."""

    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    categoria = models.CharField(max_length=50)
    stock = models.PositiveIntegerField()
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["-creado_en"]

    def __str__(self):
        # Texto legible para el admin y el shell: "Laptop Lenovo (Laptops)"
        return f"{self.nombre} ({self.categoria})"

    @property
    def agotado(self):
        return self.stock == 0

    @property
    def pocas_unidades(self):
        """True cuando quedan entre 1 y 5 unidades."""
        return 0 < self.stock <= 5

    @property
    def icono(self):
        iconos = {
            "laptops": "💻", "smartphones": "📱", "audio": "🎧",
            "monitores": "🖥️", "accesorios": "⌨️", "almacenamiento": "💾",
        }
        return iconos.get(self.categoria.lower(), "🔌")

    @property
    def nivel_stock(self):
        """Porcentaje (0-100) para la barra de stock; 20 unidades = barra llena."""
        return min(self.stock * 5, 100)
