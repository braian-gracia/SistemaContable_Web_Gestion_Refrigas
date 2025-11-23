from django.core.management.base import BaseCommand
from django.utils import timezone
from notificaciones.services import NotificacionService

class Command(BaseCommand):
    help = 'Verifica deudas vencidas y envía notificaciones automáticamente'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Verificando deudas vencidas...'))
        
        resultados = NotificacionService.verificar_y_notificar_deudas_vencidas()
        
        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Proceso completado:\n'
            f'  - Total de deudas vencidas: {resultados["total_deudas"]}\n'
            f'  - Notificaciones a clientes: {resultados["notificaciones_clientes"]}\n'
            f'  - Notificaciones a admins: {resultados["notificaciones_admins"]}\n'
        ))
        
        self.stdout.write(self.style.SUCCESS(f'Fecha: {timezone.now()}'))