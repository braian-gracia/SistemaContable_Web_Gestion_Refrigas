import pytz
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import TruncDate
from datetime import datetime, time
from .models import Transaccion, CierreCaja, TipoTransaccion
from .serializers import TransaccionSerializer, CierreCajaSerializer


class TransaccionViewSet(viewsets.ModelViewSet):
    serializer_class = TransaccionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Transaccion.objects.select_related('usuario').all()
        fecha_str = self.request.query_params.get('fecha', None)
        
        if fecha_str:
            try:
                # Parsear la fecha recibida (formato: YYYY-MM-DD)
                fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d').date()
                
                # Crear rango de fechas en zona horaria de Colombia
                tz_colombia = pytz.timezone('America/Bogota')
                
                # Inicio del día: 00:00:00 Colombia
                inicio_dia = tz_colombia.localize(
                    datetime.combine(fecha_obj, time.min)
                )
                
                # Fin del día: 23:59:59 Colombia
                fin_dia = tz_colombia.localize(
                    datetime.combine(fecha_obj, time.max)
                )
                
                # Filtrar transacciones en ese rango
                queryset = queryset.filter(
                    fecha__gte=inicio_dia,
                    fecha__lte=fin_dia
                )
                
                print(f"📅 Filtrando transacciones del {fecha_obj}")
                print(f"🕐 Rango: {inicio_dia} a {fin_dia}")
                
            except ValueError as e:
                print(f"❌ Error parseando fecha: {e}")
        
        return queryset.order_by('-fecha')

    @action(detail=False, methods=['get'])
    def resumen_diario(self, request):
        fecha_param = request.query_params.get('fecha', None)

        if fecha_param:
            try:
                fecha_param = datetime.strptime(fecha_param, '%Y-%m-%d').date()
            except:
                fecha_param = timezone.localdate()
        else:
            fecha_param = timezone.localdate()

        transacciones = Transaccion.objects.annotate(
            fecha_local=TruncDate('fecha', tzinfo=timezone.get_current_timezone())
        ).filter(fecha_local=fecha_param)

        resumen = {
            'fecha': fecha_param,
            'ventas_facturadas': transacciones.filter(
                tipo=TipoTransaccion.VENTA_FACTURADA
            ).aggregate(Sum('monto'))['monto__sum'] or 0,
            'ventas_no_facturadas': transacciones.filter(
                tipo=TipoTransaccion.VENTA_NO_FACTURADA
            ).aggregate(Sum('monto'))['monto__sum'] or 0,
            'otros_ingresos': transacciones.filter(
                tipo=TipoTransaccion.INGRESO_OTRO
            ).aggregate(Sum('monto'))['monto__sum'] or 0,
            'total_transacciones': transacciones.count()
        }
        resumen['total'] = (
            resumen['ventas_facturadas'] +
            resumen['ventas_no_facturadas'] +
            resumen['otros_ingresos']
        )
        return Response(resumen)


class CierreCajaViewSet(viewsets.ModelViewSet):
    serializer_class = CierreCajaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return CierreCaja.objects.all()
    
    @action(detail=False, methods=['post'])
    def crear_cierre_hoy(self, request):
        fecha_hoy = timezone.localdate()

        cierre_existente = CierreCaja.objects.filter(fecha=fecha_hoy).first()
        if cierre_existente:
            return Response({
                'error': 'Ya existe un cierre de caja para hoy',
                'cierre_id': cierre_existente.id
            }, status=status.HTTP_400_BAD_REQUEST)
        
        cierre = CierreCaja.objects.create(fecha=fecha_hoy)
        cierre.calcular_totales()
        
        serializer = self.get_serializer(cierre)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def cerrar_caja(self, request, pk=None):
        cierre = self.get_object()
        
        if cierre.cerrado:
            return Response({
                'error': 'Esta caja ya está cerrada'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        total_fisico = request.data.get('total_fisico')
        observaciones = request.data.get('observaciones', '')
        
        if total_fisico is None:
            return Response({
                'error': 'Debe proporcionar el total físico'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        cierre.total_fisico = total_fisico
        cierre.observaciones = observaciones
        cierre.cerrado = True
        cierre.usuario_cierre = request.user
        cierre.fecha_cierre = timezone.now()
        cierre.calcular_totales()
        
        serializer = self.get_serializer(cierre)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def recalcular(self, request, pk=None):
        cierre = self.get_object()
        
        if cierre.cerrado:
            return Response({
                'error': 'No se puede recalcular una caja cerrada'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        cierre.calcular_totales()
        serializer = self.get_serializer(cierre)
        return Response(serializer.data)
