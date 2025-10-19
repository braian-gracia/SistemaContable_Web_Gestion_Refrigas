from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum, Q
from django.contrib import messages
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Cliente, Deuda, Abono
from .serializers import ClienteSerializer, DeudaSerializer, AbonoSerializer
from django.utils import timezone
from decimal import Decimal
from django.http import JsonResponse  

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class DeudaViewSet(viewsets.ModelViewSet):
    queryset = Deuda.objects.all()
    serializer_class = DeudaSerializer
    
    @action(detail=True, methods=['post'])
    def marcar_pagada(self, request, pk=None):
        deuda = self.get_object()
        deuda.pagada = True
        deuda.save()
        return Response({'status': 'deuda marcada como pagada'})
    
    @action(detail=True, methods=['get'])
    def saldo_restante(self, request, pk=None):
        deuda = self.get_object()
        saldo = deuda.calcular_saldo_restante()
        return Response({'saldo_restante': saldo})

class AbonoViewSet(viewsets.ModelViewSet):
    queryset = Abono.objects.all()
    serializer_class = AbonoSerializer

# =============================================================================
def listado_deudas(request):
    deudas = Deuda.objects.all()
    
    deudas_con_info = []
    total_deudas = Decimal('0.00')
    total_abonado_general = Decimal('0.00')
    deudas_vencidas_count = 0
    
    for deuda in deudas:
        saldo_restante = deuda.calcular_saldo_restante()
        total_abonado = deuda.monto - saldo_restante
        esta_vencida = deuda.esta_vencida()
        
        if esta_vencida:
            deudas_vencidas_count += 1
        
        total_deudas += deuda.monto
        total_abonado_general += total_abonado
        
        deudas_con_info.append({
            'deuda': deuda,
            'saldo_restante': saldo_restante,
            'total_abonado': total_abonado,
            'esta_vencida': esta_vencida
        })
    
    context = {
        'deudas_con_info': deudas_con_info,
        'total_deudas': total_deudas,
        'total_abonado_general': total_abonado_general,
        'saldo_pendiente_total': total_deudas - total_abonado_general,
        'deudas_vencidas_count': deudas_vencidas_count,
    }
    
    return render(request, 'cartera/listado.html', context)

def marcar_como_pagada(request, deuda_id):
    deuda = get_object_or_404(Deuda, id=deuda_id)
    
    if request.method == 'POST':
        deuda.pagada = True
        deuda.save()
        messages.success(request, f'Deuda de {deuda.cliente.nombre} marcada como pagada.')
    
    return redirect('listado_deudas')

def agregar_abono(request, deuda_id):
    deuda = get_object_or_404(Deuda, id=deuda_id)
    
    if request.method == 'POST':
        monto_abono = request.POST.get('monto')
        descripcion = request.POST.get('descripcion', 'Abono realizado')
        
        try:
            monto_abono = Decimal(monto_abono)
            saldo_restante = deuda.calcular_saldo_restante()
            
            if monto_abono <= 0:
                messages.error(request, 'El monto del abono debe ser mayor a cero.')
            elif monto_abono > saldo_restante:
                messages.error(request, f'El abono no puede ser mayor al saldo restante (${saldo_restante}).')
            else:
                Abono.objects.create(
                    deuda=deuda,
                    monto=monto_abono,
                    descripcion=descripcion
                )
                messages.success(request, f'Abono de ${monto_abono} registrado correctamente.')
                
        except (ValueError, TypeError):
            messages.error(request, 'Monto inválido. Ingrese un número válido.')
    
    return redirect('listado_deudas')


def deudas_con_saldo(request):
    deudas = Deuda.objects.all()
    resultado = []
    
    for deuda in deudas:
        saldo_restante = deuda.calcular_saldo_restante()
        resultado.append({
            'id': deuda.id,
            'cliente': deuda.cliente.nombre,
            'monto_total': deuda.monto,
            'saldo_restante': saldo_restante,
            'pagada': deuda.pagada,
            'vencida': deuda.esta_vencida()
        })
    
    return JsonResponse(resultado, safe=False)

def estadisticas_cartera(request):
    total_deudas = Deuda.objects.aggregate(total=Sum('monto'))['total'] or Decimal('0.00')
    total_abonado = Abono.objects.aggregate(total=Sum('monto'))['total'] or Decimal('0.00')
    
    deudas_vencidas = 0
    for deuda in Deuda.objects.all():
        if deuda.esta_vencida():
            deudas_vencidas += 1
    
    estadisticas = {
        'total_deudas': total_deudas,
        'total_abonado': total_abonado,
        'saldo_pendiente': total_deudas - total_abonado,
        'deudas_vencidas': deudas_vencidas,
        'total_clientes': Cliente.objects.count()
    }
    
    return JsonResponse(estadisticas)