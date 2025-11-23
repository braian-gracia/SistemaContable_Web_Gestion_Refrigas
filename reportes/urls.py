from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    path('', views.generar_reporte_view, name='generar'),
    path('descargar/general/', views.descargar_reporte_general, name='descargar_general'),
    path('descargar/clientes/', views.descargar_reporte_clientes, name='descargar_clientes'),
    path('descargar/abonos/', views.descargar_reporte_abonos, name='descargar_abonos'),
]