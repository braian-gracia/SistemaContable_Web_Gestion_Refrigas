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
            html_content = render_to_string(f'notificaciones/emails/{template_name}', contexto)
            text_content = render_to_string(f'notificaciones/emails/{template_name.replace(".html", ".txt")}', contexto)
            
            email = EmailMultiAlternatives(
                subject=asunto,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[destinatario]
            )
            email.attach_alternative(html_content, "text/html")
            email.send()
            return True, None
        except Exception as e:
            logger.error(f"Error enviando email a {destinatario}: {str(e)}")
            return False, str(e)
    
    @staticmethod
    def notificar_deuda_vencida_cliente(deuda):
        """Notifica al cliente que tiene una deuda vencida"""
        cliente = deuda.cliente
        saldo_restante = deuda.calcular_saldo_restante()
        
        contexto = {
            'cliente_nombre': cliente.nombre,
            'monto_deuda': deuda.monto,
            'saldo_restante': saldo_restante,
            'fecha_vencimiento': deuda.fecha_vencimiento,
            'descripcion': deuda.descripcion,
            'dias_vencidos': (timezone.now().date() - deuda.fecha_vencimiento).days
        }
        
        asunto = f"Recordatorio: Deuda Vencida - {cliente.nombre}"
        
        notificacion = Notificacion.objects.create(
            tipo='DEUDA_VENCIDA_CLIENTE',
            destinatario_email=cliente.correo,
            asunto=asunto,
            mensaje=f"Deuda de ${saldo_restante} vencida desde {deuda.fecha_vencimiento}",
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
        admins = User.objects.filter(is_staff=True, is_active=True)
        
        contexto = {
            'cliente_nombre': cliente.nombre,
            'cliente_telefono': cliente.telefono,
            'cliente_correo': cliente.correo,
            'monto_deuda': deuda.monto,
            'saldo_restante': saldo_restante,
            'fecha_vencimiento': deuda.fecha_vencimiento,
            'descripcion': deuda.descripcion,
            'dias_vencidos': (timezone.now().date() - deuda.fecha_vencimiento).days
        }
        
        asunto = f"Alerta: Cliente {cliente.nombre} con deuda vencida"
        notificaciones_enviadas = []
        
        for admin in admins:
            if not admin.email:
                continue
                
            notificacion = Notificacion.objects.create(
                tipo='DEUDA_VENCIDA_ADMIN',
                destinatario_email=admin.email,
                asunto=asunto,
                mensaje=f"Cliente {cliente.nombre} tiene deuda vencida de ${saldo_restante}",
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