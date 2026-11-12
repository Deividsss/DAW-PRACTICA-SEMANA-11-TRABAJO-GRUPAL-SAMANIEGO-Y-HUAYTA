from django.core.management.base import BaseCommand

from catalogo.models import Producto

DATOS = [
    # (nombre, precio, categoria, stock)
    ("Dell Inspiron 15", "2899.00", "Laptops", 14),
    ("Apple Macbook Air M2", "5199.00", "Laptops", 4),
    ("Asus Tuf Gaming F15", "3799.00", "Laptops", 0),
    ("Samsung Galaxy S24", "3299.00", "Smartphones", 22),
    ("Motorola Edge 40", "1899.00", "Smartphones", 3),
    ("Xiaomi Redmi Note 13", "899.00", "Smartphones", 40),
    ("Audifonos Sony Bluetooth", "1299.00", "Audio", 9),
    ("Parlante Anker Soundcore 2", "249.00", "Audio", 0),
    ("Monitor Samsung 27 Pulgadas", "1099.00", "Monitores", 7),
    ("Monitor Dell 24 Pulgadas", "699.00", "Monitores", 12),
    ("Teclado Logitech K380", "189.00", "Accesorios", 18),
    ("Mouse Logitech M170", "59.90", "Accesorios", 5),
    ("Disco Solido Kingston A400", "329.00", "Almacenamiento", 30),
    ("Pendrive Sandisk Ultra", "49.90", "Almacenamiento", 60),
]


class Command(BaseCommand):
    help = "Carga productos de ejemplo (idempotente: no duplica)."

    def handle(self, *args, **opts):
        nuevos = 0
        for nombre, precio, categoria, stock in DATOS:
            _, creado = Producto.objects.get_or_create(
                nombre=nombre,
                defaults={"precio": precio, "categoria": categoria, "stock": stock},
            )
            nuevos += creado
        self.stdout.write(self.style.SUCCESS(
            f"Productos nuevos: {nuevos} | Total en BD: {Producto.objects.count()}"
        ))
