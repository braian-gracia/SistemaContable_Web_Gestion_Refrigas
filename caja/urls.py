from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'transacciones', views.TransaccionViewSet, basename='transacciones')
router.register(r'cierres', views.CierreCajaViewSet, basename='cierres')

urlpatterns = [
    path('', include(router.urls)),
]
