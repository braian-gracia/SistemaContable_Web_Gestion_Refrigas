from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required

@login_required 

def reportes_view(request):
    return render(request, 'reportes/reportes.html') # toca aun crear el html
