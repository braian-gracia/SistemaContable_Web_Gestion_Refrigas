from django.urls import path
from . import views

app_name = 'notificaciones'

urlpatterns = [
    path('enviar_deudas_vencidas/', views.enviar_notificaciones_deudas_vencidas, name='enviar_deudas_vencidas'),
    path('historial/', views.historial_notificaciones, name='historial'),
    path('webhook/verificar/', views.webhook_verificar_deudas, name='webhook_verificar'),
]