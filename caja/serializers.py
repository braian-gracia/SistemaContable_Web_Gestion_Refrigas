import pytz
from rest_framework import serializers
from .models import Transaccion, CierreCaja, TipoTransaccion

class TransaccionSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.username', read_only=True)
    
    # Agregar campo con fecha en zona horaria de Colombia
    fecha_colombia = serializers.SerializerMethodField()
    hora_colombia = serializers.SerializerMethodField()
    
    class Meta:
        model = Transaccion
        fields = ['id', 'fecha', 'fecha_colombia', 'hora_colombia', 'tipo', 'tipo_display', 
                 'monto', 'descripcion', 'numero_factura', 'usuario', 'usuario_nombre']
        read_only_fields = ['usuario']
    
    def get_fecha_colombia(self, obj):
        """Retorna la fecha en formato DD/MM/YYYY en zona horaria Colombia"""
        tz_colombia = pytz.timezone('America/Bogota')
        fecha_local = obj.fecha.astimezone(tz_colombia)
        return fecha_local.strftime('%d/%m/%Y')
    
    def get_hora_colombia(self, obj):
        """Retorna la hora en formato HH:MM AM/PM en zona horaria Colombia"""
        tz_colombia = pytz.timezone('America/Bogota')
        fecha_local = obj.fecha.astimezone(tz_colombia)
        return fecha_local.strftime('%I:%M %p')  # Ej: 10:47 PM
    
    def create(self, validated_data):
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)
    
    def to_representation(self, instance):
        """
        Sobrescribir to_representation para asegurar que 'fecha' 
        siempre se muestre en zona horaria de Colombia
        """
        representation = super().to_representation(instance)
        
        # Convertir fecha UTC a Colombia antes de serializar
        tz_colombia = pytz.timezone('America/Bogota')
        fecha_local = instance.fecha.astimezone(tz_colombia)
        
        # Actualizar el campo fecha con la hora correcta
        representation['fecha'] = fecha_local.isoformat()
        
        return representation

class CierreCajaSerializer(serializers.ModelSerializer):
    usuario_cierre_nombre = serializers.CharField(source='usuario_cierre.username', read_only=True)
    
    class Meta:
        model = CierreCaja
        fields = ['id', 'fecha', 'total_ventas_facturadas', 'total_ventas_no_facturadas',
                 'total_otros_ingresos', 'total_calculado', 'total_fisico', 'diferencia',
                 'cerrado', 'usuario_cierre', 'usuario_cierre_nombre', 'fecha_cierre', 
                 'observaciones']
        read_only_fields = ['total_ventas_facturadas', 'total_ventas_no_facturadas',
                           'total_otros_ingresos', 'total_calculado', 'diferencia',
                           'usuario_cierre', 'fecha_cierre']
