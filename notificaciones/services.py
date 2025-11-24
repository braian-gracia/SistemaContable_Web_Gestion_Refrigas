from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Notificacion
from cartera.models import Cliente, Deuda
import logging

logger = logging.getLogger(__name__)

class NotificacionService:
    
    @staticmethod
    def enviar_email(asunto, destinatario, contexto, template_name):
        """Envía un email usando templates HTML"""
        try:
            print(f"🔵 Intentando enviar email a: {destinatario}")
            print(f"🔵 Asunto: {asunto}")
            print(f"🔵 Remitente: {settings.DEFAULT_FROM_EMAIL}")
            print(f"🔵 Backend: {settings.EMAIL_BACKEND}")
            
            # Renderizar template HTML
            html_content = render_to_string(f'notificaciones/emails/{template_name}', contexto)
            
            # Intentar renderizar versión texto plano (opcional)
            try:
                text_content = render_to_string(
                    f'notificaciones/emails/{template_name.replace(".html", ".txt")}', 
                    contexto
                )
            except Exception:
                # Si no existe template .txt, crear versión simple del HTML
                text_content = f"""
{asunto}

Estimado/a {contexto.get('cliente_nombre', 'Cliente')},

{contexto.get('mensaje_principal', 'Le informamos sobre su cuenta.')}

Detalles:
- Monto: ${contexto.get('saldo_restante', contexto.get('monto_deuda', 0))}
- Fecha: {contexto.get('fecha_vencimiento', 'N/A')}

Atentamente,
Almacén Refrigas
                """.strip()
            
            # Crear y enviar email
            email = EmailMultiAlternatives(
                subject=asunto,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[destinatario]
            )
            email.attach_alternative(html_content, "text/html")
            
            # Enviar con manejo de errores
            email.send(fail_silently=False)
            
            print(f"✅ Email enviado exitosamente a {destinatario}")
            logger.info(f"✅ Email enviado exitosamente a {destinatario}")
            return True, None
            
        except Exception as e:
            error_msg = f"Error enviando email a {destinatario}: {str(e)}"
            print(f"❌ {error_msg}")
            logger.error(f"❌ {error_msg}")
            return False, error_msg
    
    @staticmethod
    def notificar_deuda_vencida_cliente(deuda):
        """Notifica al cliente que tiene una deuda vencida"""
        cliente = deuda.cliente
        saldo_restante = deuda.calcular_saldo_restante()
        dias_vencidos = (timezone.now().date() - deuda.fecha_vencimiento).days
        
        contexto = {
            'cliente_nombre': cliente.nombre,
            'monto_deuda': f"{deuda.monto:,.0f}",  # Formatear con separador de miles
            'saldo_restante': f"{saldo_restante:,.0f}",
            'fecha_vencimiento': deuda.fecha_vencimiento.strftime('%d/%m/%Y'),
            'descripcion': deuda.descripcion or 'Deuda pendiente',
            'dias_vencidos': dias_vencidos,
            'mensaje_principal': f'Le recordamos que tiene una deuda vencida desde hace {dias_vencidos} días.',
            'es_urgente': dias_vencidos > 15,  # Más de 15 días = urgente
            'color_alerta': '#d9534f' if dias_vencidos > 15 else '#f0ad4e',
        }
        
        asunto = f"{'🚨 URGENTE' if dias_vencidos > 15 else '📋 Recordatorio'}: Deuda Vencida - Almacén Refrigas"
        
        notificacion = Notificacion.objects.create(
            tipo='DEUDA_VENCIDA_CLIENTE',
            destinatario_email=cliente.correo,
            asunto=asunto,
            mensaje=f"Deuda de ${saldo_restante:,.0f} vencida desde {deuda.fecha_vencimiento.strftime('%d/%m/%Y')}",
            deuda=deuda,
            cliente=cliente
        )
        
        exito, error = NotificacionService.enviar_email(
            asunto=asunto,
            destinatario=cliente.correo,
            contexto=contexto,
            template_name='deuda_vencida_cliente.html'
        )
        
        if exito:
            notificacion.estado = 'ENVIADA'
            notificacion.fecha_envio = timezone.now()
        else:
            notificacion.estado = 'FALLIDA'
            notificacion.error_mensaje = error
        
        notificacion.save()
        return notificacion
    
    @staticmethod
    def notificar_deuda_vencida_admins(deuda):
        """Notifica a todos los administradores sobre una deuda vencida"""
        cliente = deuda.cliente
        saldo_restante = deuda.calcular_saldo_restante()
        dias_vencidos = (timezone.now().date() - deuda.fecha_vencimiento).days
        admins = User.objects.filter(is_staff=True, is_active=True)
        
        contexto = {
            'cliente_nombre': cliente.nombre,
            'cliente_telefono': cliente.telefono or 'No registrado',
            'cliente_correo': cliente.correo or 'No registrado',
            'monto_deuda': f"{deuda.monto:,.0f}",
            'saldo_restante': f"{saldo_restante:,.0f}",
            'fecha_vencimiento': deuda.fecha_vencimiento.strftime('%d/%m/%Y'),
            'descripcion': deuda.descripcion or 'Deuda pendiente',
            'dias_vencidos': dias_vencidos,
            'mensaje_principal': f'El cliente {cliente.nombre} tiene una deuda vencida que requiere atención.',
            'es_urgente': dias_vencidos > 15,
            'color_alerta': '#d9534f' if dias_vencidos > 15 else '#f0ad4e',
        }
        
        asunto = f"🔔 Alerta: Cliente {cliente.nombre} con deuda vencida ({dias_vencidos} días)"
        notificaciones_enviadas = []
        
        for admin in admins:
            if not admin.email:
                continue
                
            notificacion = Notificacion.objects.create(
                tipo='DEUDA_VENCIDA_ADMIN',
                destinatario_email=admin.email,
                asunto=asunto,
                mensaje=f"Cliente {cliente.nombre} tiene deuda vencida de ${saldo_restante:,.0f}",
                deuda=deuda,
                cliente=cliente
            )
            
            exito, error = NotificacionService.enviar_email(
                asunto=asunto,
                destinatario=admin.email,
                contexto=contexto,
                template_name='deuda_vencida_admin.html'
            )
            
            if exito:
                notificacion.estado = 'ENVIADA'
                notificacion.fecha_envio = timezone.now()
            else:
                notificacion.estado = 'FALLIDA'
                notificacion.error_mensaje = error
            
            notificacion.save()
            notificaciones_enviadas.append(notificacion)
        
        return notificaciones_enviadas
    
    @staticmethod
    def verificar_y_notificar_deudas_vencidas():
        """Verifica todas las deudas vencidas y envía notificaciones"""
        deudas_vencidas = Deuda.objects.filter(
            pagada=False,
            fecha_vencimiento__lt=timezone.now().date()
        ).select_related('cliente')
        
        resultados = {
            'total_deudas': deudas_vencidas.count(),
            'notificaciones_clientes': 0,
            'notificaciones_admins': 0
        }
        
        for deuda in deudas_vencidas:
            saldo = deuda.calcular_saldo_restante()
            if saldo > 0:
                NotificacionService.notificar_deuda_vencida_cliente(deuda)
                resultados['notificaciones_clientes'] += 1
                
                NotificacionService.notificar_deuda_vencida_admins(deuda)
                resultados['notificaciones_admins'] += User.objects.filter(
                    is_staff=True, 
                    is_active=True
                ).exclude(email='').count()
        
        return resultados