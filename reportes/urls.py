from django.urls import path
from . import views

urlpatterns = [
    path('', views.reportes_view, name='reportes'),
]
