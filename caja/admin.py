from django.contrib import admin
from .models import Transaccion, CierreCaja

@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'tipo', 'monto', 'descripcion', 'numero_factura', 'usuario']
    list_filter = ['tipo', 'fecha', 'usuario']
    search_fields = ['descripcion', 'numero_factura']
    ordering = ['-fecha']

@admin.register(CierreCaja)
class CierreCajaAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'total_calculado', 'total_fisico', 'diferencia', 'cerrado']
    list_filter = ['cerrado', 'fecha']
    ordering = ['-fecha']
    readonly_fields = ['total_ventas_facturadas', 'total_ventas_no_facturadas', 
                      'total_otros_ingresos', 'total_calculado', 'diferencia']
