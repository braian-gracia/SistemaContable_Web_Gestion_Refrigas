import os
from pathlib import Path
from decouple import config
import dj_database_url
from django.db.backends.signals import connection_created
from django.dispatch import receiver

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='django-insecure-development-key-only')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = ['localhost','127.0.0.1','sistemacontable-web-gestion-refrigas.onrender.com',]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # apps del proyecto 
    'rest_framework',
    'corsheaders',
    'caja',
    'cartera',
    'reportes',
    'notificaciones',
    'gestion_usuarios',
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'almacen_refrigas.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Si existe DATABASE_URL (Render/Producción), usar PostgreSQL
DATABASE_URL = config('DATABASE_URL', default=None)

if DATABASE_URL:
    DATABASES['default'] = dj_database_url.parse(DATABASE_URL, conn_max_age=600)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# Archivos estáticos (CSS, JS, imágenes)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # Archivos locales
STATIC_ROOT = BASE_DIR / 'staticfiles'    # Carpeta donde se recopilan todos los estáticos

# Activar compresión y cache con WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Redirecciones de login/logout
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# Variables de entorno para Auth0
AUTH0_DOMAIN = config('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = config('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = config('AUTH0_CLIENT_SECRET')
AUTH0_CALLBACK_URL = config('AUTH0_CALLBACK_URL')


# Forzar zona horaria en PostgreSQL
@receiver(connection_created)
def set_postgres_timezone(sender, connection, **kwargs):
    """
    Render/PostgreSQL siempre usa UTC por defecto.
    Esto fuerza que todas las conexiones usen la zona horaria de Colombia.
    Soluciona el problema de que el servidor cambia de día antes que tú.
    """
    if connection.vendor == 'postgresql':
        with connection.cursor() as cursor:
            cursor.execute("SET TIME ZONE 'America/Bogota';")


# ====== CONFIGURACIÓN DE EMAIL ======
SENDGRID_API_KEY = config('SENDGRID_API_KEY', default='')

if DEBUG and SENDGRID_API_KEY:
    # En desarrollo con SendGrid configurado, usar SMTP
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = 'apikey'
    EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
elif DEBUG:
    # En desarrollo sin SendGrid, mostrar en consola
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    # En producción, usar SendGrid
    EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
    SENDGRID_API_KEY = config('SENDGRID_API_KEY', default='')
    SENDGRID_SANDBOX_MODE_IN_DEBUG = False
    
# Configuración del remitente
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='braiansgracia@gmail.com')
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# Timeout para evitar bloqueos
EMAIL_TIMEOUT = 10



