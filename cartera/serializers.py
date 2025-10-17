from rest_framework import serializers
from .models import Cliente, Deuda, Abono

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class DeudaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deuda
        fields = '__all__'

class AbonoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Abono
        fields = '__all__'
