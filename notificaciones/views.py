from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required

@login_required

def notificaciones_view(request):
    return render(request, 'notificaciones/notificaciones.html') # toca aun crear el html

