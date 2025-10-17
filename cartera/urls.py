from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'clientes', views.ClienteViewSet, basename='clientes')
router.register(r'deudas', views.DeudaViewSet, basename='deudas')
router.register(r'abonos', views.AbonoViewSet, basename='abonos')

urlpatterns = [
    path('', include(router.urls)),
]
