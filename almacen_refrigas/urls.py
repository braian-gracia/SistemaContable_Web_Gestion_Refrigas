from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from gestion_usuarios import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include('caja.urls')),
    path('api/', include('cartera.api_urls')),
    path('cartera/', include('cartera.urls')),
    
    path('reportes/', include('reportes.urls')),
    path('notificaciones/', include('notificaciones.urls')),

    path('login/', user_views.login_auth0, name='login'),
    path('callback/', user_views.callback, name='callback'),
    path('logout/', user_views.logout_auth0, name='logout'),

    path('', login_required(TemplateView.as_view(template_name='index.html')), name='home'),
]
