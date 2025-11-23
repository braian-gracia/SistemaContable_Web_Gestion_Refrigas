from django.contrib import admin

# Register your models here.

from django.utils.html import format_html
from .models import Notificacion

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'tipo',
        'destinatario_email',
        'asunto',
        'estado_badge',
        'fecha_creacion',
        'fecha_envio'
    )
    list_filter = ('tipo', 'estado', 'fecha_creacion')
    search_fields = ('destinatario_email', 'asunto', 'mensaje')
    readonly_fields = ('fecha_creacion', 'fecha_envio', 'error_mensaje')
    
    fieldsets = (
        ('Información General', {
            'fields': ('tipo', 'estado', 'destinatario_email', 'asunto')
        }),
        ('Contenido', {
            'fields': ('mensaje',)
        }),
        ('Relaciones', {
            'fields': ('deuda', 'cliente')
        }),
        ('Fechas y Estado', {
            'fields': ('fecha_creacion', 'fecha_envio', 'error_mensaje')
        }),
    )
    
    def estado_badge(self, obj):
        colores = {
            'ENVIADA': 'green',
            'PENDIENTE': 'orange',
            'FALLIDA': 'red'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            colores.get(obj.estado, 'gray'),
            obj.get_estado_display()
        )
    estado_badge.short_description = 'Estado'