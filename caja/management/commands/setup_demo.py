from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from caja.models import Transaccion, CierreCaja, TipoTransaccion
from decimal import Decimal
from datetime import date
import random

class Command(BaseCommand):
    help = 'Configura datos de demostración'
    
    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@refrigas.com', 'admin123')
            self.stdout.write('Superusuario creado: admin/admin123')
        
        if not User.objects.filter(username='cajero').exists():
            User.objects.create_user('cajero', 'cajero@refrigas.com', 'cajero123')
            self.stdout.write('Usuario cajero creado: cajero/cajero123')
        
        usuario = User.objects.get(username='admin')
        fecha_hoy = date.today()
        
        transacciones_ejemplo = [
            ('VF', 150000, 'Venta refrigerador Samsung', 'F001'),
            ('VF', 85000, 'Venta nevera mini', 'F002'),
            ('VNF', 25000, 'Reparación nevera cliente Juan', ''),
            ('VF', 200000, 'Venta aire acondicionado', 'F003'),
            ('VNF', 15000, 'Servicio técnico', ''),
            ('IO', 50000, 'Venta repuestos varios', ''),
        ]
        
        for tipo, monto, desc, factura in transacciones_ejemplo:
            if not Transaccion.objects.filter(descripcion=desc, fecha__date=fecha_hoy).exists():
                Transaccion.objects.create(
                    tipo=tipo,
                    monto=Decimal(str(monto)),
                    descripcion=desc,
                    numero_factura=factura if factura else None,
                    usuario=usuario
                )
        
        self.stdout.write('Datos de demostración creados exitosamente')
