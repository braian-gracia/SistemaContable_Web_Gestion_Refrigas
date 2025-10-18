from django.contrib import admin

# Register your models here.

from .models import UsuarioAutorizado

@admin.register(UsuarioAutorizado)
class UsuarioAutorizadoAdmin(admin.ModelAdmin):
    list_display = ('email', 'nombre', 'activo')
    search_fields = ('email',)
