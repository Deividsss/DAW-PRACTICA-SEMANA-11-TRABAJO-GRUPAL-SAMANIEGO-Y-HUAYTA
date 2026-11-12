from django.urls import path

from . import views

urlpatterns = [
    # FBV: página de bienvenida
    path('', views.home, name='home'),
    # CBV: listado de productos
    path('catalogo/', views.ProductoListView.as_view(), name='catalogo'),
]
