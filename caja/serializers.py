from rest_framework import serializers
from .models import Transaccion, CierreCaja, TipoTransaccion

class TransaccionSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.username', read_only=True)
    
    class Meta:
        model = Transaccion
        fields = ['id', 'fecha', 'tipo', 'tipo_display', 'monto', 'descripcion', 
                 'numero_factura', 'usuario', 'usuario_nombre']
        read_only_fields = ['usuario']
    
    def create(self, validated_data):
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)

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
