from django.urls import path
from . import views

urlpatterns = [
    # URLs PARA EL MÓDULO CARTERA - VISTAS TEMPLATE
    path('', views.listado_deudas, name='listado_deudas'),
    path('marcar-pagada/<int:deuda_id>/', views.marcar_como_pagada, name='marcar_como_pagada'),
    path('agregar-abono/<int:deuda_id>/', views.agregar_abono, name='agregar_abono'),
    
    # NUEVAS PÁGINAS HTML - GESTIÓN DE DEUDAS Y DEUDORES
    path('crear-deuda/', views.crear_deuda_view, name='crear_deuda'),
    path('gestionar-deudores/', views.gestionar_deudores_view, name='gestionar_deudores'),
    
    # APIs ADICIONALES
    path('deudas-con-saldo/', views.deudas_con_saldo, name='deudas_con_saldo'),
    path('estadisticas/', views.estadisticas_cartera, name='estadisticas_cartera'),
]