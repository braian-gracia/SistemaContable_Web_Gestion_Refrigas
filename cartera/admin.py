from django.contrib import admin

# Register your models here.
from .models import Cliente, Deuda, Abono

# ADMIN CLIENTE

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'correo', 'telefono')
    search_fields = ('nombre', 'correo', 'telefono')

# ADMIN DEUDA
@admin.register(Deuda)
class DeudaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cliente',
        'descripcion',
        'monto',
        'pagada',
        'fecha',
        'fecha_vencimiento',
    )
    search_fields = ('cliente__nombre', 'descripcion')
    list_filter = ('pagada', 'fecha_vencimiento')

# ADMIN ABONO
@admin.register(Abono)
class AbonoAdmin(admin.ModelAdmin):
    list_display = ('id', 'deuda', 'monto', 'fecha', 'descripcion')
    search_fields = ('deuda__cliente__nombre', 'descripcion')
    list_filter = ('fecha',)
