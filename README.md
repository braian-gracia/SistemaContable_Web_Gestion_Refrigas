# Sistema de Gestión Almacén Refrigas

Sistema web contable diseñado para automatizar el cierre de caja diario, gestionar cartera, generar reportes financieros y mejorar el control administrativo del Almacén Refrigas.  
Desarrollado con **Python 3.11.9**, **Django 4.2.7** y base de datos **PostgreSQL** en despliegue.

---

# Características principales

- Registro de ingresos facturados y no facturados  
- Control de egresos, gastos y pagos por datáfono  
- Cálculo automático de sobrantes y faltantes en cierre de caja  
- Gestión de cartera y pagos pendientes  
- **Gestión completa de deudores (crear, editar, eliminar)**
- **Sistema de creación y seguimiento de deudas**
- Alertas de vencimiento (considerando días del mes y años bisiestos)  
- **Envío de anuncios y notificaciones de deuda**
- Reportes exportables en PDF y XLS  
- Historial de movimientos con filtros por rango de fechas  
- Sistema de usuarios con roles  
- Autenticación mediante **Auth0**

---

# Arquitectura del sistema

El proyecto está organizado por módulos (apps) en Django:

```
/caja                  → Registro de ingresos/egresos y cierres diarios
/cartera               → Gestión de cartera, deudas y deudores
/gestion_usuarios      → Administración de usuarios y roles
/notificaciones        → Alertas internas y envío de anuncios de deuda
/reportes              → Generación y exportación de reportes
```

## Páginas HTML principales

**Módulo de Cartera:**
- `crear_deuda.html` - Formulario para registrar nuevas deudas
- `gestionar_deudores.html` - CRUD completo de deudores

**Módulo de Notificaciones:**
- `historial.html` - Historial de notificaciones enviadas
- `enviar_anuncio_deuda.html` - Envío de anuncios y recordatorios de pago

---

# Tecnologías y versiones

**Lenguaje**
- Python 3.11.9

**Framework**
- Django 4.2.7  
- Django REST Framework 3.14.0  
- django-cors-headers 4.3.1  

**Base de datos**
- Desarrollo: SQLite  
- Producción: PostgreSQL  

**Servidor**
- Gunicorn 22.0.0  
- Whitenoise 6.11.0  

**Dependencias principales (requirements.txt)**
- psycopg[binary] 3.2.10  
- dj-database-url 2.1.0  
- python-decouple  
- python-dotenv  
- requests, rsa, ecdsa, etc.  

---

# Variables de entorno (.env)

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True

# Auth0
AUTH0_DOMAIN=dev-xxxxx.us.auth0.com
AUTH0_CLIENT_ID=your-client-id
AUTH0_CLIENT_SECRET=your-client-secret
AUTH0_CALLBACK_URL=http://localhost:8000/callback

```

---

# Instalación 

## 1. Clonar el repositorio

```bash
git clone https://github.com/braian-gracia/SistemaContable_Web_Gestion_Refrigas.git
cd SistemaContable_Web_Gestion_Refrigas
```

## 2. Crear entorno virtual

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS**
```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 4. Crear archivo `.env`

Usar la plantilla de variables de entorno previamente mostrada.

## 5. Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

## 6. Crear superusuario

```bash
python manage.py createsuperuser
```

### 7. Ejecutar servidor

```bash
python manage.py runserver
```

## 8. Acceso local

```
http://127.0.0.1:8000/
```

---

# Módulos principales

## Caja
- Registro de ingresos/egresos  
- Pagos por datáfono  
- Cierre diario automático  
- Cálculo de sobrante/faltante  

## Cartera
- Control de pagos pendientes  
- **Gestión completa de deudores (CRUD)**
- **Creación y seguimiento de deudas**
- Abonos y fechas límite  
- Alertas por vencimientos  

## Notificaciones
- **Envío de anuncios de deuda a clientes**
- **Historial de notificaciones enviadas**
- Alertas del sistema

## Reportes
- Reportes diarios y mensuales  
- Exportación PDF/XLS  
- Filtros avanzados  

## Gestión de usuarios
- Roles: administrador, cajero  
- Autenticación mediante Auth0  

---

# Despliegue (producción)

## Configuración PostgreSQL

```sql
CREATE DATABASE refrigas_db;
CREATE USER refrigas_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE refrigas_db TO refrigas_user;
```

Configurar `DATABASE_URL` en el `.env`.

### Ejecutar con Gunicorn

```bash
gunicorn almacen_refrigas.wsgi:application
```

Whitenoise gestiona los archivos estáticos.

---

# Mantenimiento y control de versiones

- Control de versiones mediante **GitHub**  
- Rama principal: `main`  
- Commits organizados y estructurados  
- Documentación adicional:  
  - **GCS**  
  - Manual técnico  
  - Manual de usuario  

---

# 📄 Licencia

Proyecto académico de Ingeniería de Software.