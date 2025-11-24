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
from almacen_refrigas import settings
from django.utils import timezone

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
    Acepta JSON con los datos de la notificación y envía emails con HTML.
    """
    from django.core.mail import EmailMultiAlternatives
    from cartera.models import Deuda
    
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
        
        def personalizar_mensaje(mensaje_original, cliente):
            """Reemplaza todas las variables del mensaje con datos reales del cliente"""
            mensaje_personalizado = mensaje_original
            
            # Variables básicas del cliente
            mensaje_personalizado = mensaje_personalizado.replace('[NOMBRE]', cliente.nombre)
            mensaje_personalizado = mensaje_personalizado.replace('[nombre]', cliente.nombre)
            mensaje_personalizado = mensaje_personalizado.replace('[EMAIL]', cliente.correo or '')
            mensaje_personalizado = mensaje_personalizado.replace('[TELEFONO]', cliente.telefono or '')
            
            # Buscar la deuda más reciente del cliente
            try:
                deuda = Deuda.objects.filter(
                    cliente=cliente, 
                    pagada=False
                ).order_by('-fecha_vencimiento').first()
                
                if deuda:
                    saldo = deuda.calcular_saldo_restante()
                    dias_vencidos = (timezone.now().date() - deuda.fecha_vencimiento).days if deuda.fecha_vencimiento < timezone.now().date() else 0
                    
                    # Reemplazar variables de deuda
                    mensaje_personalizado = mensaje_personalizado.replace('[MONTO]', f'{saldo:,.0f}')
                    mensaje_personalizado = mensaje_personalizado.replace('[monto]', f'{saldo:,.0f}')
                    mensaje_personalizado = mensaje_personalizado.replace('[FECHA]', deuda.fecha_vencimiento.strftime('%d/%m/%Y'))
                    mensaje_personalizado = mensaje_personalizado.replace('[fecha]', deuda.fecha_vencimiento.strftime('%d/%m/%Y'))
                    mensaje_personalizado = mensaje_personalizado.replace('[DIAS]', str(dias_vencidos) if dias_vencidos > 0 else '0')
                    mensaje_personalizado = mensaje_personalizado.replace('[dias]', str(dias_vencidos) if dias_vencidos > 0 else '0')
                else:
                    # Si no hay deuda, reemplazar con valores por defecto
                    mensaje_personalizado = mensaje_personalizado.replace('[MONTO]', '0')
                    mensaje_personalizado = mensaje_personalizado.replace('[monto]', '0')
                    mensaje_personalizado = mensaje_personalizado.replace('[FECHA]', 'N/A')
                    mensaje_personalizado = mensaje_personalizado.replace('[fecha]', 'N/A')
                    mensaje_personalizado = mensaje_personalizado.replace('[DIAS]', '0')
                    mensaje_personalizado = mensaje_personalizado.replace('[dias]', '0')
            except Exception as e:
                print(f"⚠️ Error obteniendo deuda: {str(e)}")
                # En caso de error, dejar valores por defecto
                mensaje_personalizado = mensaje_personalizado.replace('[MONTO]', 'N/A')
                mensaje_personalizado = mensaje_personalizado.replace('[FECHA]', 'N/A')
                mensaje_personalizado = mensaje_personalizado.replace('[DIAS]', 'N/A')
            
            return mensaje_personalizado
        
        def crear_html_email(asunto_email, mensaje_texto):
            """Crea el HTML del email con el mensaje personalizado"""
            # Convertir saltos de línea a HTML
            mensaje_html = mensaje_texto.replace('\n', '<br>')
            
            return f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f4;">
    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: #f4f4f4; padding: 40px 20px;">
        <tr>
            <td align="center">
                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" style="max-width: 600px; background-color: #ffffff; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); overflow: hidden;">
                    
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 30px; text-align: center;">
                            <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: bold;">
                                📢 {asunto_email}
                            </h1>
                            <p style="margin: 10px 0 0 0; color: #ffffff; font-size: 16px; opacity: 0.95;">
                                Almacén Refrigas
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Contenido del mensaje -->
                    <tr>
                        <td style="padding: 40px 30px;">
                            <div style="color: #333; font-size: 16px; line-height: 1.8;">
                                {mensaje_html}
                            </div>
                            
                            <!-- Caja de info adicional -->
                            <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-left: 5px solid #667eea; border-radius: 10px; padding: 20px; margin: 30px 0 20px 0;">
                                <p style="margin: 0; color: #666; font-size: 14px; line-height: 1.6;">
                                    💡 <strong>¿Necesita ayuda?</strong><br>
                                    Para más información o cualquier consulta, no dude en contactarnos.
                                </p>
                            </div>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f8f9fa; padding: 30px; text-align: center; border-top: 1px solid #e0e0e0;">
                            <p style="margin: 0 0 10px 0; color: #333; font-size: 16px; font-weight: bold;">
                                Almacén Refrigas
                            </p>
                            <p style="margin: 0 0 15px 0; color: #666; font-size: 14px;">
                                📞 Contacto: +57 123 456 7890<br>
                                📧 Email: info@refrigas.com
                            </p>
                            <p style="margin: 0; color: #999; font-size: 12px; line-height: 1.5;">
                                Este es un mensaje automático, por favor no responda a este correo.<br>
                                © 2025 Almacén Refrigas. Todos los derechos reservados.
                            </p>
                        </td>
                    </tr>
                    
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""
        
        # Si es "todos" los clientes
        if cliente_id == 'todos':
            from cartera.models import Cliente
            clientes = Cliente.objects.filter(correo__isnull=False).exclude(correo='')
            
            notificaciones_creadas = 0
            emails_enviados = 0
            
            for cliente in clientes:
                # Personalizar mensaje con datos reales del cliente
                mensaje_personalizado = personalizar_mensaje(mensaje, cliente)
                
                # Crear HTML del email
                html_email = crear_html_email(asunto, mensaje_personalizado)
                
                # Crear registro de notificación
                notificacion = Notificacion.objects.create(
                    cliente=cliente,
                    tipo=tipo,
                    asunto=asunto,
                    mensaje=mensaje_personalizado,
                    estado='PENDIENTE',
                    destinatario_email=cliente.correo
                )
                notificaciones_creadas += 1
                
                # Enviar email si no está programado
                if tipo == 'EMAIL' and not programado:
                    try:
                        print(f"📧 Enviando a {cliente.correo}...")
                        
                        email = EmailMultiAlternatives(
                            subject=asunto,
                            body=mensaje_personalizado,
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            to=[cliente.correo]
                        )
                        email.attach_alternative(html_email, "text/html")
                        email.send(fail_silently=False)
                        
                        emails_enviados += 1
                        notificacion.estado = 'ENVIADA'
                        notificacion.fecha_envio = timezone.now()
                        notificacion.save()
                        print(f"✅ Enviado exitosamente")
                        
                    except Exception as e:
                        print(f"❌ Error enviando a {cliente.correo}: {str(e)}")
                        notificacion.estado = 'FALLIDA'
                        notificacion.error_mensaje = str(e)
                        notificacion.save()
            
            return JsonResponse({
                'success': True,
                'mensaje': f'✅ Notificaciones creadas: {notificaciones_creadas}, Emails enviados: {emails_enviados}'
            })
        
        # Si es un cliente específico
        else:
            from cartera.models import Cliente
            try:
                cliente = Cliente.objects.get(id=cliente_id)
                
                # Personalizar mensaje con datos reales del cliente
                mensaje_personalizado = personalizar_mensaje(mensaje, cliente)
                
                # Crear HTML del email
                html_email = crear_html_email(asunto, mensaje_personalizado)
                
                # Crear registro de notificación
                notificacion = Notificacion.objects.create(
                    cliente=cliente,
                    tipo=tipo,
                    asunto=asunto,
                    mensaje=mensaje_personalizado,
                    estado='PENDIENTE',
                    destinatario_email=cliente.correo
                )
                
                # Enviar email si no está programado
                if tipo == 'EMAIL' and not programado and cliente.correo:
                    try:
                        print(f"📧 Enviando a {cliente.correo}...")
                        print(f"📋 Mensaje personalizado:\n{mensaje_personalizado}")
                        
                        email = EmailMultiAlternatives(
                            subject=asunto,
                            body=mensaje_personalizado,
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            to=[cliente.correo]
                        )
                        email.attach_alternative(html_email, "text/html")
                        email.send(fail_silently=False)
                        
                        notificacion.estado = 'ENVIADA'
                        notificacion.fecha_envio = timezone.now()
                        notificacion.save()
                        
                        print(f"✅ Email enviado exitosamente")
                        
                        return JsonResponse({
                            'success': True,
                            'mensaje': f'✅ Email enviado exitosamente a {cliente.nombre} ({cliente.correo})'
                        })
                    except Exception as e:
                        print(f"❌ Error: {str(e)}")
                        notificacion.estado = 'FALLIDA'
                        notificacion.error_mensaje = str(e)
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
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'error': str(e)
        }, status=500)