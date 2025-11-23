from django.shortcuts import render

# Create your views here.

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .services import ReporteService
from cartera.models import Cliente

def es_staff(user):
    return user.is_staff

@login_required
@user_passes_test(es_staff)
def generar_reporte_view(request):
    """Vista principal para generar reportes con filtros"""
    clientes = Cliente.objects.all().order_by('nombre')
    
    contexto = {
        'clientes': clientes,
        'fecha_actual': timezone.now().date()
    }
    
    return render(request, 'reportes/generar_reporte.html', contexto)

@login_required
@user_passes_test(es_staff)
def descargar_reporte_general(request):
    """Descarga el reporte general en Excel con filtros aplicados"""
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    cliente_id = request.GET.get('cliente_id')
    incluir_pagadas = request.GET.get('incluir_pagadas') == 'on'
    
    # Convertir fechas
    if fecha_inicio:
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
    if fecha_fin:
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
    
    buffer = ReporteService.generar_reporte_general(
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        cliente_id=cliente_id,
        incluir_pagadas=incluir_pagadas
    )
    
    filename = f'reporte_general_{timezone.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    
    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response

@login_required
@user_passes_test(es_staff)
def descargar_reporte_clientes(request):
    """Descarga el reporte de clientes en Excel"""
    buffer = ReporteService.generar_reporte_clientes()
    
    filename = f'reporte_clientes_{timezone.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    
    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response

@login_required
@user_passes_test(es_staff)
def descargar_reporte_abonos(request):
    """Descarga el reporte de abonos en Excel con filtros de fecha"""
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    
    if fecha_inicio:
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
    if fecha_fin:
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
    
    buffer = ReporteService.generar_reporte_abonos(
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )
    
    filename = f'reporte_abonos_{timezone.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    
    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response