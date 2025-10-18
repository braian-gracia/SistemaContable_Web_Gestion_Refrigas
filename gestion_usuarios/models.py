from django.db import models

# Create your models here.
from django.db import models

class UsuarioAutorizado(models.Model):
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.email
