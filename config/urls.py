"""URLs raíz del proyecto (config).

El proyecto solo delega: toda la lógica de rutas del catálogo vive en
catalogo/urls.py (modularización con include()).
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Prefijo vacío: '/' y '/catalogo/' se resuelven dentro de la app.
    path('', include('catalogo.urls')),
]
