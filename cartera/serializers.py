from rest_framework import serializers
from .models import Cliente, Deuda, Abono

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class DeudaSerializer(serializers.ModelSerializer):
    saldo_restante = serializers.SerializerMethodField()
    esta_vencida = serializers.SerializerMethodField()
    
    class Meta:
        model = Deuda
        fields = '__all__'
    
    def get_saldo_restante(self, obj):
        # Calcula la suma de todos los abonos
        total_abonado = sum(abono.monto for abono in obj.abono_set.all())
        return obj.monto - total_abonado
    
    def get_esta_vencida(self, obj):
        from django.utils import timezone
        if hasattr(obj, 'fecha_vencimiento') and obj.fecha_vencimiento:
            hoy = timezone.now().date()
            saldo = self.get_saldo_restante(obj)
            return obj.fecha_vencimiento < hoy and saldo > 0 and not obj.pagada
        return False

class AbonoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Abono
        fields = '__all__'