from django.db import models
from django.db.models import Sum
from django.utils import timezone
from decimal import Decimal

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True)
    direccion = models.CharField(max_length=200, blank=True, default='')

    def __str__(self):
        return self.nombre

class Deuda(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(auto_now_add=True)
    pagada = models.BooleanField(default=False)
    descripcion = models.CharField(max_length=200, blank=True, default='Deuda pendiente')
    fecha_vencimiento = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.cliente} - ${self.monto}"

    def calcular_saldo_restante(self):
        total_abonado = self.abono_set.aggregate(
            total=Sum('monto')
        )['total'] or Decimal('0.00')
        return self.monto - total_abonado

    def esta_vencida(self):
        if not self.fecha_vencimiento:
            return False
        hoy = timezone.now().date()
        saldo_restante = self.calcular_saldo_restante()
        return self.fecha_vencimiento < hoy and saldo_restante > 0 and not self.pagada

class Abono(models.Model):
    deuda = models.ForeignKey(Deuda, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(auto_now_add=True)
    descripcion = models.CharField(max_length=200, blank=True, default='Abono a deuda')

    def __str__(self):
        return f"Abono ${self.monto} - {self.deuda.cliente}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        saldo_restante = self.deuda.calcular_saldo_restante()
        
        if saldo_restante <= 0:
            self.deuda.pagada = True
            self.deuda.save()