from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .services import NotificacionService
from .models import Notificacion
import os
import json

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
        
        

@login_required
def enviar_anuncio_view(request):
    """
    Vista para renderizar la página de envío de anuncios de deuda.
    Template: templates/notificaciones/enviar_anuncio_deuda.html
    """
    return render(request, 'notificaciones/enviar_anuncio_deuda.html')


@login_required
def notificaciones_index(request):
    """
    Vista para renderizar la página principal de notificaciones.
    Template: templates/notificaciones.html
    """
    return render(request, 'notificaciones.html')

@login_required
@require_http_methods(["POST"])
def enviar_notificacion_api(request):
    """
    API para enviar notificaciones desde el formulario HTML.
    Acepta JSON con los datos de la notificación y envía emails reales.
    """
    from django.core.mail import send_mail
    from django.conf import settings
    
    try:
        data = json.loads(request.body)
        
        cliente_id = data.get('cliente_id')
        tipo = data.get('tipo', 'EMAIL')
        asunto = data.get('asunto')
        mensaje = data.get('mensaje')
        prioridad = data.get('prioridad', 'NORMAL')
        programado = data.get('programado', False)
        
        # Validar campos requeridos
        if not asunto or not mensaje:
            return JsonResponse({
                'error': 'El asunto y mensaje son requeridos'
            }, status=400)
        
        # Si es "todos" los clientes
        if cliente_id == 'todos':
            from cartera.models import Cliente
            clientes = Cliente.objects.all()
            
            notificaciones_creadas = 0
            emails_enviados = 0
            
            for cliente in clientes:
                # Crear registro de notificación
                notificacion = Notificacion.objects.create(
                    cliente=cliente,
                    tipo=tipo,
                    asunto=asunto,
                    mensaje=mensaje,
                    estado='ENVIADA' if not programado else 'PROGRAMADA'
                )
                notificaciones_creadas += 1
                
                # Enviar email si el tipo es EMAIL y no está programado
                if tipo == 'EMAIL' and not programado and cliente.correo:
                    print(f"🔔 Intentando enviar email a: {cliente.correo}")
                    print(f"📧 Asunto: {asunto}")
                    try:
                        result = send_mail(
                            subject=asunto,
                            message=mensaje,
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[cliente.correo],
                            fail_silently=False,
                        )
                        print(f"✅ Email enviado. Resultado: {result}")
                        emails_enviados += 1
                        notificacion.estado = 'ENVIADA'
                        notificacion.save()
                    except Exception as e:
                        print(f"❌ Error enviando email: {str(e)}")
                        notificacion.estado = 'FALLIDA'
                        notificacion.save()
            
            return JsonResponse({
                'success': True,
                'mensaje': f'Notificaciones creadas: {notificaciones_creadas}, Emails enviados: {emails_enviados}'
            })
        
        # Si es un cliente específico
        else:
            from cartera.models import Cliente
            try:
                cliente = Cliente.objects.get(id=cliente_id)
                
                # Crear registro de notificación
                notificacion = Notificacion.objects.create(
                    cliente=cliente,
                    tipo=tipo,
                    asunto=asunto,
                    mensaje=mensaje,
                    estado='ENVIADA' if not programado else 'PROGRAMADA'
                )
                
                # Enviar email si el tipo es EMAIL y no está programado
                if tipo == 'EMAIL' and not programado and cliente.correo:
                    print(f"🔔 Intentando enviar email a: {cliente.correo}")
                    print(f"📧 Asunto: {asunto}")
                    print(f"📝 De: {settings.DEFAULT_FROM_EMAIL}")
                    try:
                        result = send_mail(
                            subject=asunto,
                            message=mensaje,
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[cliente.correo],
                            fail_silently=False,
                        )
                        print(f"✅ Email enviado exitosamente. Resultado: {result}")
                        notificacion.estado = 'ENVIADA'
                        notificacion.save()
                        
                        return JsonResponse({
                            'success': True,
                            'mensaje': f'Email enviado exitosamente a {cliente.nombre} ({cliente.correo})'
                        })
                    except Exception as e:
                        print(f"❌ Error enviando email: {str(e)}")
                        notificacion.estado = 'FALLIDA'
                        notificacion.save()
                        return JsonResponse({
                            'error': f'Error al enviar email: {str(e)}'
                        }, status=500)
                else:
                    return JsonResponse({
                        'success': True,
                        'mensaje': f'Notificación programada para {cliente.nombre}'
                    })
                
            except Cliente.DoesNotExist:
                return JsonResponse({
                    'error': 'Cliente no encontrado'
                }, status=404)
        
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Formato JSON inválido'
        }, status=400)
    except Exception as e:
        print(f"❌ Error general: {str(e)}")
        return JsonResponse({
            'error': str(e)
        }, status=500)