from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'clientes', views.ClienteViewSet, basename='clientes')
router.register(r'deudas', views.DeudaViewSet, basename='deudas')
router.register(r'abonos', views.AbonoViewSet, basename='abonos')

urlpatterns = [
    path('', include(router.urls)),
    
    # URLs PARA EL MÓDULO CARTERA - VISTAS TEMPLATE
    path('cartera/', views.listado_deudas, name='listado_deudas'),
    path('cartera/marcar-pagada/<int:deuda_id>/', views.marcar_como_pagada, name='marcar_como_pagada'),
    path('cartera/agregar-abono/<int:deuda_id>/', views.agregar_abono, name='agregar_abono'),
    
    # APIs ADICIONALES
    path('cartera/deudas-con-saldo/', views.deudas_con_saldo, name='deudas_con_saldo'),
    path('cartera/estadisticas/', views.estadisticas_cartera, name='estadisticas_cartera'),
]