from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils import timezone
from django.db.models.functions import TruncDate

class TipoTransaccion(models.TextChoices):
    VENTA_FACTURADA = 'VF', 'Venta Facturada'
    VENTA_NO_FACTURADA = 'VNF', 'Venta No Facturada'
    INGRESO_OTRO = 'IO', 'Otro Ingreso'


class Transaccion(models.Model):
    fecha = models.DateField(default=timezone.localdate)
    tipo = models.CharField(
        max_length=3,
        choices=TipoTransaccion.choices,
        default=TipoTransaccion.VENTA_FACTURADA
    )
    monto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    descripcion = models.CharField(max_length=200)
    numero_factura = models.CharField(max_length=50, blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Transacción'
        verbose_name_plural = 'Transacciones'
    
    def __str__(self):
        return f"{self.get_tipo_display()} - ${self.monto} ({self.fecha.strftime('%Y-%m-%d %H:%M')})"


class CierreCaja(models.Model):
    fecha = models.DateField(unique=True)
    total_ventas_facturadas = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_ventas_no_facturadas = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_otros_ingresos = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_calculado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_fisico = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    diferencia = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cerrado = models.BooleanField(default=False)
    usuario_cierre = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    fecha_cierre = models.DateTimeField(blank=True, null=True)
    observaciones = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Cierre de Caja'
        verbose_name_plural = 'Cierres de Caja'
    
    def __str__(self):
        return f"Cierre {self.fecha} - ${self.total_calculado}"
    
    def calcular_totales(self):
        from django.db.models import Sum

        transacciones_del_dia = Transaccion.objects.annotate(
            fecha_local=TruncDate('fecha', tzinfo=timezone.get_current_timezone())
        ).filter(fecha_local=self.fecha)

        self.total_ventas_facturadas = transacciones_del_dia.filter(
            tipo=TipoTransaccion.VENTA_FACTURADA
        ).aggregate(Sum('monto'))['monto__sum'] or Decimal('0.00')

        self.total_ventas_no_facturadas = transacciones_del_dia.filter(
            tipo=TipoTransaccion.VENTA_NO_FACTURADA
        ).aggregate(Sum('monto'))['monto__sum'] or Decimal('0.00')

        self.total_otros_ingresos = transacciones_del_dia.filter(
            tipo=TipoTransaccion.INGRESO_OTRO
        ).aggregate(Sum('monto'))['monto__sum'] or Decimal('0.00')

        self.total_calculado = (
            self.total_ventas_facturadas +
            self.total_ventas_no_facturadas +
            self.total_otros_ingresos
        )

        if self.total_fisico is not None:
            self.diferencia = self.total_fisico - self.total_calculado

        self.save()
