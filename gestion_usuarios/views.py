from django.shortcuts import render

# Create your views here.

from jose import jwt
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from urllib.parse import urlencode
import requests
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import UsuarioAutorizado  # importa tu nuevo modelo

def login_auth0(request):
    return redirect(f"https://{settings.AUTH0_DOMAIN}/authorize?"
                    f"response_type=code&client_id={settings.AUTH0_CLIENT_ID}"
                    f"&redirect_uri={settings.AUTH0_CALLBACK_URL}&scope=openid profile email")

def callback(request):
    # Si estás en modo debug, simplemente salta todo
    if settings.DEBUG:
        user, _ = User.objects.get_or_create(
            username="debug_user",
            defaults={"email": "debug@localhost", "first_name": "Debug"}
        )
        login(request, user)
        return redirect("/")

    # === Flujo real Auth0 ===
    code = request.GET.get('code')

    token_url = f"https://{settings.AUTH0_DOMAIN}/oauth/token"
    token_payload = {
        'grant_type': 'authorization_code',
        'client_id': settings.AUTH0_CLIENT_ID,
        'client_secret': settings.AUTH0_CLIENT_SECRET,
        'code': code,
        'redirect_uri': settings.AUTH0_CALLBACK_URL,
    }

    token_info = requests.post(token_url, json=token_payload).json()
    id_token = token_info.get('id_token')

    if not id_token:
        return HttpResponse("Error al autenticar con Auth0", status=400)

    user_info = jwt.get_unverified_claims(id_token)
    user_email = user_info.get('email')
    user_name = user_info.get('name', user_email.split('@')[0])

    # 🔒 Verificar si está autorizado en la base de datos
    try:
        UsuarioAutorizado.objects.get(email=user_email, activo=True)
    except UsuarioAutorizado.DoesNotExist:
        # En producción, bloquear
        if not settings.DEBUG:
            return render(request, "no_autorizado.html", {"email": user_email})
        # En debug, permitir igualmente
        else:
            user, _ = User.objects.get_or_create(
                username=user_email,
                defaults={'email': user_email, 'first_name': user_name}
            )
            login(request, user)
            return redirect("/")

    # ✅ Crear usuario local si no existe
    user, created = User.objects.get_or_create(
        email=user_email,
        defaults={'username': user_email, 'first_name': user_name}
    )

    login(request, user)
    return redirect("/")

def logout_auth0(request):
    logout(request)
    return_to = request.build_absolute_uri('/login/')
    params = {
        'client_id': settings.AUTH0_CLIENT_ID,
        'returnTo': return_to,
    }
    return redirect(f"https://{settings.AUTH0_DOMAIN}/v2/logout?{urlencode(params)}")

