from django.urls import path
from . import views

app_name = 'notificaciones'

urlpatterns = [
    path('enviar_deudas_vencidas/', views.enviar_notificaciones_deudas_vencidas, name='enviar_deudas_vencidas'),
    path('historial/', views.historial_notificaciones, name='historial'),
    path('webhook/verificar/', views.webhook_verificar_deudas, name='webhook_verificar'),
    
    # NUEVA PÁGINA HTML - ENVÍO DE ANUNCIOS DE DEUDA
    path('enviar-anuncio/', views.enviar_anuncio_view, name='enviar_anuncio'),
    
    # API para enviar notificaciones
    path('api/enviar/', views.enviar_notificacion_api, name='enviar_notificacion_api'),  # 👈 AGREGAR ESTA LÍNEA
    
    # Página principal de notificaciones
    path('', views.notificaciones_index, name='notificaciones_index'),
]