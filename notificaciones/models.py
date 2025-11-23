from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from cartera.models import Cliente, Deuda

class Notificacion(models.Model):
    TIPO_CHOICES = [
        ('DEUDA_VENCIDA_CLIENTE', 'Deuda Vencida - Cliente'),
        ('DEUDA_VENCIDA_ADMIN', 'Deuda Vencida - Administrador'),
        ('RECORDATORIO_PAGO', 'Recordatorio de Pago'),
    ]
    
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('ENVIADA', 'Enviada'),
        ('FALLIDA', 'Fallida'),
    ]
    
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    destinatario_email = models.EmailField()
    asunto = models.CharField(max_length=200)
    mensaje = models.TextField()
    deuda = models.ForeignKey(Deuda, on_delete=models.CASCADE, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='PENDIENTE')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_envio = models.DateTimeField(null=True, blank=True)
    error_mensaje = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
    
    def __str__(self):
        return f"{self.tipo} - {self.destinatario_email} - {self.estado}"