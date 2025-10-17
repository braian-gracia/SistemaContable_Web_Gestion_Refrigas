from django.urls import path
from . import views

urlpatterns = [
    path('', views.notificaciones_view, name='notificaciones'),
]
