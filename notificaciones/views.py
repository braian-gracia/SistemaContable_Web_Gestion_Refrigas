from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .services import NotificacionService
from .models import Notificacion
import os

def es_staff(user):
    return user.is_staff

@login_required
@user_passes_test(es_staff)
def enviar_notificaciones_deudas_vencidas(request):
    """Vista para enviar notificaciones manualmente de todas las deudas vencidas"""
    if request.method == 'POST':
        resultados = NotificacionService.verificar_y_notificar_deudas_vencidas()
        
        messages.success(
            request,
            f"Notificaciones enviadas: {resultados['notificaciones_clientes']} a clientes, "
            f"{resultados['notificaciones_admins']} a administradores. "
            f"Total de deudas vencidas: {resultados['total_deudas']}"
        )
        return redirect('admin:notificaciones_notificacion_changelist')
    
    return render(request, 'notificaciones/confirmar_envio.html')

@login_required
@user_passes_test(es_staff)
def historial_notificaciones(request):
    """Vista para ver el historial de notificaciones"""
    # Primero obtenemos el queryset completo (sin slice)
    notificaciones_completas = Notificacion.objects.select_related('cliente', 'deuda').all()
    
    # Calculamos estadísticas ANTES del slice
    total = notificaciones_completas.count()
    enviadas = notificaciones_completas.filter(estado='ENVIADA').count()
    fallidas = notificaciones_completas.filter(estado='FALLIDA').count()
    
    # Ahora sí aplicamos el slice para limitar resultados
    notificaciones = notificaciones_completas[:100]
    
    contexto = {
        'notificaciones': notificaciones,
        'total': total,
        'enviadas': enviadas,
        'fallidas': fallidas,
    }
    
    return render(request, 'notificaciones/historial.html', contexto)

@csrf_exempt
@require_http_methods(["POST", "GET"])
def webhook_verificar_deudas(request):
    """
    Endpoint que puede ser llamado externamente para verificar deudas
    Protegido con un token secreto
    
    Uso: 
    curl -X POST https://tudominio.com/notificaciones/webhook/verificar/ \
         -H "Authorization: Bearer TU_TOKEN_SECRETO"
    """
    # Verificar token de seguridad
    token_esperado = os.environ.get('WEBHOOK_SECRET_TOKEN', 'cambiar_este_token_123')
    token_recibido = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    if token_recibido != token_esperado:
        return JsonResponse({
            'error': 'No autorizado'
        }, status=401)
    
    try:
        resultados = NotificacionService.verificar_y_notificar_deudas_vencidas()
        return JsonResponse({
            'success': True,
            'mensaje': 'Notificaciones enviadas correctamente',
            'resultados': resultados
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)