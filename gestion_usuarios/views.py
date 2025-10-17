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

def login_auth0(request):
    return redirect(f"https://{settings.AUTH0_DOMAIN}/authorize?"
                    f"response_type=code&client_id={settings.AUTH0_CLIENT_ID}"
                    f"&redirect_uri={settings.AUTH0_CALLBACK_URL}&scope=openid profile email")

def callback(request):
    code = request.GET.get('code')

    token_url = f"https://{settings.AUTH0_DOMAIN}/oauth/token"
    token_payload = {
        'grant_type': 'authorization_code',
        'client_id': settings.AUTH0_CLIENT_ID,
        'client_secret': settings.AUTH0_CLIENT_SECRET,
        'code': code,
        'redirect_uri': settings.AUTH0_CALLBACK_URL,
    }

    # Obtener el token de Auth0
    token_info = requests.post(token_url, json=token_payload).json()
    id_token = token_info.get('id_token')

    if not id_token:
        return HttpResponse("Error al autenticar con Auth0", status=400)

    # Decodificar el JWT sin verificar (Auth0 ya lo firmó)
    user_info = jwt.get_unverified_claims(id_token)
    user_email = user_info.get('email')

    # 🔒 Verificar si el usuario existe en Django
    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        return render(request, "no_autorizado.html", {"email": user_email})

    # ✅ Usuario válido → iniciar sesión
    login(request, user)
    return redirect('/')


def logout_auth0(request):
    logout(request)
    return_to = request.build_absolute_uri('/login/')
    params = {
        'client_id': settings.AUTH0_CLIENT_ID,
        'returnTo': return_to,
    }
    return redirect(f"https://{settings.AUTH0_DOMAIN}/v2/logout?{urlencode(params)}")

