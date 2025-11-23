# GESTIÓN DE LA CONFIGURACIÓN DEL SOFTWARE (GCS)
## Sistema de Gestión Almacén Refrigas

**Institución:** Universidad de Ibagué  
**Tipo de Proyecto:** Académico - Ingeniería de Software  
**Versión del Documento:** 1.0  
**Fecha:** Noviembre 2024  

---

## 1. INTRODUCCIÓN

### 1.1 Propósito
Este documento establece el plan de Gestión de la Configuración del Software (GCS) para el Sistema de Gestión Almacén Refrigas, siguiendo los lineamientos de los estándares IEEE 828-2012 e ISO/IEC 12207. Define los procesos, responsabilidades y herramientas para controlar y gestionar los cambios del software durante su ciclo de vida.

### 1.2 Alcance
Este plan cubre todos los elementos de configuración del proyecto, incluyendo código fuente, documentación técnica, base de datos, archivos de configuración y dependencias.

### 1.3 Definiciones y Acrónimos
- **GCS**: Gestión de la Configuración del Software
- **CI**: Configuration Item (Elemento de Configuración)
- **PR**: Pull Request
- **VCS**: Version Control System (Sistema de Control de Versiones)
- **Baseline**: Línea base aprobada de configuración

---

## 2. IDENTIFICACIÓN DEL SOFTWARE

### 2.1 Información General
- **Nombre:** Sistema de Gestión Almacén Refrigas
- **Tipo:** Aplicación web contable
- **Versión Actual:** 1.0.0
- **Repositorio:** https://github.com/braian-gracia/SistemaContable_Web_Gestion_Refrigas
- **URL Producción:** https://sistemacontable-web-gestion-refrigas.onrender.com

### 2.2 Descripción General
Sistema web contable que automatiza el cierre de caja diario y el control de cartera del Almacén Refrigas. Permite registrar ingresos facturados y no facturados, egresos, pagos por datáfono, calcular sobrantes y faltantes, y generar reportes históricos exportables.

### 2.3 Stack Tecnológico
- **Lenguaje:** Python 3.11.9
- **Framework:** Django 4.2.7
- **Base de Datos:** PostgreSQL (Producción), SQLite (Desarrollo)
- **Servidor:** Gunicorn 22.0.0
- **Plataforma de Despliegue:** Render
- **Autenticación:** Auth0

---

## 3. EQUIPO Y RESPONSABILIDADES

### 3.1 Equipo de Desarrollo

| Nombre | Rol | Responsabilidades |
|--------|-----|-------------------|
| Braian Steven Gracia Ramírez | Líder de Proyecto / Configuration Manager | Gestión del repositorio, aprobación de merges, despliegues a producción |
| Juandiego Rodríguez | Desarrollador Backend | Desarrollo de módulos de caja y cartera, revisión de código |
| Juan Ávila | Desarrollador Backend | Desarrollo de reportes y notificaciones, pruebas |
| Daniel Vanegas | Desarrollador Full Stack | Desarrollo de gestión de usuarios, integración Auth0 |

### 3.2 Roles y Responsabilidades GCS

**Configuration Manager (Braian Gracia):**
- Gestionar el repositorio principal
- Aprobar cambios críticos
- Ejecutar despliegues a producción
- Mantener documentación GCS actualizada
- Crear releases y tags

**Desarrolladores (Todos los miembros):**
- Crear ramas para nuevas funcionalidades
- Realizar commits estructurados
- Crear Pull Requests
- Revisar código de compañeros
- Ejecutar pruebas locales antes de PR

---

## 4. ELEMENTOS DE CONFIGURACIÓN (CI)

### 4.1 Estructura de Items de Configuración

| ID | Elemento | Ubicación | Tipo |
|----|----------|-----------|------|
| CI-001 | Código Fuente | `/caja`, `/cartera`, `/gestion_usuarios`, `/notificaciones`, `/reportes` | Código Python/Django |
| CI-002 | Archivos de Configuración | `/almacen_refrigas/settings.py`, `.env.template` | Configuración |
| CI-003 | Dependencias | `requirements.txt` | Dependencias |
| CI-004 | Migraciones de BD | `/*/migrations/` | Base de Datos |
| CI-005 | Documentación Técnica | `/docs/`, `README.md`, `GCS.md` | Documentación |
| CI-006 | Templates HTML | `/*/templates/` | Frontend |
| CI-007 | Archivos Estáticos | `/static/`, `/media/` | Assets |
| CI-008 | Tests | `/*/tests.py` | Pruebas |

### 4.2 Nomenclatura de Archivos
- Módulos Python: `snake_case.py`
- Clases: `PascalCase`
- Funciones: `snake_case()`
- Templates: `nombre_modulo_accion.html`

---

## 5. CONTROL DE VERSIONES

### 5.1 Sistema de Control de Versiones
- **Herramienta:** Git + GitHub
- **Repositorio:** https://github.com/braian-gracia/SistemaContable_Web_Gestion_Refrigas

### 5.2 Estrategia de Versionado
**Semantic Versioning 2.0.0** (`MAJOR.MINOR.PATCH`)

- **MAJOR:** Cambios incompatibles con versiones anteriores
- **MINOR:** Nueva funcionalidad compatible con versiones anteriores
- **PATCH:** Correcciones de errores compatibles

**Ejemplo:** `1.0.0` → `1.1.0` (nueva funcionalidad) → `1.1.1` (bugfix)

### 5.3 Estrategia de Branching

**Modelo basado en Feature Branches**

```
main (producción estable)
  ├── braian-gracia (desarrollo Braian)
  ├── juandiego (desarrollo Juandiego)
  ├── juan-avila (desarrollo Juan)
  └── daniel-vanegas (desarrollo Daniel)
```

**Ramas:**
- `main`: Rama principal con código estable en producción
- `braian-gracia`: Rama personal de desarrollo de Braian
- `juandiego`: Rama personal de desarrollo de Juandiego
- `juan-avila`: Rama personal de desarrollo de Juan
- `daniel-vanegas`: Rama personal de desarrollo de Daniel

### 5.4 Convenciones de Commits

**Formato:**
```
tipo(alcance): descripción breve

[Descripción detallada opcional]

[Referencias a issues]
```

**Tipos permitidos:**
- `feat`: Nueva funcionalidad
- `fix`: Corrección de errores
- `docs`: Cambios en documentación
- `style`: Formato, espacios (sin cambio de lógica)
- `refactor`: Refactorización de código
- `test`: Agregar o modificar tests
- `chore`: Tareas de mantenimiento

**Ejemplos:**
```bash
feat(caja): agregar cálculo automático de cierre diario
fix(cartera): corregir alertas de vencimiento en años bisiestos
docs(readme): actualizar instrucciones de instalación
```

---

## 6. GESTIÓN DE CAMBIOS

### 6.1 Proceso de Control de Cambios

```mermaid
graph TD
    A[Identificar Necesidad de Cambio] --> B[Crear Issue en GitHub]
    B --> C[Crear Rama de Desarrollo]
    C --> D[Implementar Cambio]
    D --> E[Commit y Push]
    E --> F[Crear Pull Request]
    F --> G{Revisión de Código}
    G -->|Cambios Solicitados| D
    G -->|Aprobado| H[Merge a Main]
    H --> I[Despliegue a Producción]
```

### 6.2 Flujo de Trabajo Detallado

**Paso 1: Planificación**
- Identificar la necesidad del cambio
- Crear issue en GitHub (opcional pero recomendado)
- Asignar responsable

**Paso 2: Desarrollo**
```bash
# Actualizar rama local
git checkout main
git pull origin main

# Crear/actualizar rama personal
git checkout braian-gracia
git merge main

# Desarrollar funcionalidad
# ... código ...

# Commit
git add .
git commit -m "feat(modulo): descripción del cambio"
git push origin braian-gracia
```

**Paso 3: Pull Request**
- Crear PR desde rama personal hacia `main`
- Título descriptivo del cambio
- Descripción detallada de:
  - ¿Qué cambia?
  - ¿Por qué cambia?
  - ¿Cómo probarlo?
- Asignar revisores (mínimo 1)

**Paso 4: Revisión de Código**
- Cualquier miembro puede revisar
- Verificar:
  - Código funcional
  - Estándares de codificación
  - Sin conflictos con main
  - Tests pasando (cuando aplique)
- Aprobar o solicitar cambios

**Paso 5: Merge**
- Una vez aprobado, el Configuration Manager o el autor realiza el merge
- Eliminar rama temporal si aplica

**Paso 6: Despliegue**
- El Configuration Manager despliega a Render
- Verificar funcionamiento en producción

### 6.3 Criterios de Aprobación
- Mínimo 1 aprobación de otro miembro del equipo
- No tener conflictos con `main`
- Código debe seguir convenciones establecidas
- Funcionalidad debe ser probada localmente

### 6.4 Gestión de Conflictos
En caso de conflictos durante merge:
1. El desarrollador resuelve conflictos en su rama
2. Realiza commit de resolución
3. Solicita nueva revisión si los cambios son significativos

---

## 7. LÍNEAS BASE (BASELINES)

### 7.1 Definición de Baselines
Una baseline es una versión aprobada y congelada del sistema que sirve como referencia para futuros desarrollos.

### 7.2 Baselines Establecidas

| Versión | Fecha | Descripción | Tag Git |
|---------|-------|-------------|---------|
| 0.1.0 | Entrega 1 | Primera entrega académica con módulos básicos | `v0.1.0` |
| 0.2.0 | Entrega 2 | Segunda entrega con funcionalidades completas | `v0.2.0` |
| 1.0.0 | Release Final | Versión estable en producción | `v1.0.0` |

### 7.3 Creación de Baselines
```bash
# Crear tag anotado
git tag -a v1.0.0 -m "Release 1.0.0 - Sistema completo"
git push origin v1.0.0
```

---

## 8. AUDITORÍA Y TRAZABILIDAD

### 8.1 Auditorías de Configuración
- **Frecuencia:** Al final de cada entrega académica
- **Responsable:** Configuration Manager
- **Aspectos a verificar:**
  - Todos los cambios tienen commits asociados
  - PRs fueron revisados apropiadamente
  - Documentación está actualizada
  - Tags de versión corresponden con entregas

### 8.2 Trazabilidad
- **Commits:** Identifican quién, cuándo y qué cambió
- **Pull Requests:** Documentan el propósito y revisión de cambios
- **Issues:** (Recomendado) Vinculan cambios con requerimientos
- **Tags:** Marcan versiones importantes

### 8.3 Herramientas de Auditoría
```bash
# Ver historial de cambios
git log --oneline --graph --all

# Ver cambios de un archivo específico
git log -- ruta/al/archivo.py

# Ver diferencias entre versiones
git diff v0.1.0 v1.0.0

# Ver quién modificó cada línea
git blame archivo.py
```

---

## 9. GESTIÓN DE RELEASES

### 9.1 Proceso de Release

**Pre-release:**
1. Verificar que todos los PRs estén mergeados
2. Actualizar `requirements.txt` si hay nuevas dependencias
3. Revisar y actualizar documentación (README, GCS)
4. Ejecutar pruebas locales completas
5. Actualizar número de versión en documentación

**Release:**
1. Crear tag de versión en `main`
2. Crear Release en GitHub con notas de cambios
3. Desplegar a Render desde `main`
4. Verificar funcionamiento en producción

**Post-release:**
1. Notificar al equipo
2. Documentar issues encontrados
3. Planificar siguiente iteración

### 9.2 Notas de Release (Changelog)
Cada release debe incluir:
- Nuevas funcionalidades
- Correcciones de errores
- Cambios en dependencias
- Mejoras de rendimiento
- Cambios en configuración

**Ejemplo:**
```markdown
## [1.0.0] - 2024-11-22

### Agregado
- Módulo de caja con cierre automático
- Módulo de cartera con alertas de vencimiento
- Exportación de reportes en PDF/XLS
- Autenticación con Auth0

### Corregido
- Cálculo de años bisiestos en alertas
- Validación de montos negativos

### Cambiado
- Migración de SQLite a PostgreSQL en producción
```

### 9.3 Despliegue a Producción

**Plataforma:** Render (https://sistemacontable-web-gestion-refrigas.onrender.com)

**Proceso:**
1. Push a rama `main` activa despliegue automático en Render
2. Render ejecuta:
   - Instalación de dependencias (`requirements.txt`)
   - Migraciones de base de datos
   - Recolección de archivos estáticos
   - Inicio de Gunicorn
3. Verificar logs en Render Dashboard
4. Probar funcionalidades críticas en producción

**Configuración en Render:**
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn almacen_refrigas.wsgi:application`
- Variables de entorno configuradas en Render Dashboard

---

## 10. GESTIÓN DE AMBIENTES

### 10.1 Ambientes Definidos

| Ambiente | Propósito | Base de Datos | URL |
|----------|-----------|---------------|-----|
| Desarrollo Local | Desarrollo individual | SQLite | http://localhost:8000 |
| Pruebas Local | Testing en equipo | SQLite/PostgreSQL local | http://localhost:8000 |
| Producción | Sistema en vivo | PostgreSQL (Render) | https://sistemacontable-web-gestion-refrigas.onrender.com |

### 10.2 Configuración por Ambiente

**Desarrollo:**
```python
# settings.py
DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Producción:**
```python
# settings.py
DEBUG = False
DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}
```

### 10.3 Variables de Entorno

**Archivo `.env` (no versionado):**
```env
SECRET_KEY=your-secret-key
DEBUG=True
AUTH0_DOMAIN=dev-xxxxx.us.auth0.com
AUTH0_CLIENT_ID=your-client-id
AUTH0_CLIENT_SECRET=your-client-secret
AUTH0_CALLBACK_URL=http://localhost:8000/callback
DATABASE_URL=postgresql://user:password@host:port/database
```

**Archivo `.env.template` (versionado):**
Contiene las variables sin valores sensibles, como plantilla.

---

## 11. BACKUP Y RECUPERACIÓN

### 11.1 Estrategia de Backup

**Código Fuente:**
- **Repositorio principal:** GitHub
- **Frecuencia:** Continua (cada push)
- **Retención:** Indefinida
- **Recuperación:** `git clone` del repositorio

**Base de Datos:**
- **Producción (PostgreSQL en Render):**
  - Render realiza backups automáticos
  - Frecuencia: Diaria
  - Retención: Según plan de Render
- **Desarrollo:**
  - No requiere backup (datos de prueba)

### 11.2 Plan de Recuperación ante Desastres

**Escenario 1: Pérdida del Repositorio Local**
```bash
git clone https://github.com/braian-gracia/SistemaContable_Web_Gestion_Refrigas.git
cd SistemaContable_Web_Gestion_Refrigas
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en Windows
pip install -r requirements.txt
python manage.py migrate
```

**Escenario 2: Corrupción de Base de Datos en Producción**
1. Acceder a Render Dashboard
2. Restaurar desde backup automático
3. Verificar integridad de datos
4. Reiniciar servicio

**Escenario 3: Despliegue Fallido**
1. Revertir commit problemático: `git revert <commit>`
2. Push a `main` para redesplegar versión anterior
3. Investigar y corregir en rama de desarrollo

### 11.3 Procedimiento de Rollback
```bash
# Revertir al tag anterior
git checkout v0.9.0
git checkout -b hotfix-rollback
git push origin hotfix-rollback

# Merge a main después de verificar
git checkout main
git merge hotfix-rollback
git push origin main
```

---

## 12. DEPENDENCIAS Y LIBRERÍAS

### 12.1 Gestión de Dependencias
- **Archivo:** `requirements.txt`
- **Actualización:** Al agregar/actualizar librerías
- **Versionado:** Versiones específicas para reproducibilidad

### 12.2 Dependencias Principales
```
Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
gunicorn==22.0.0
whitenoise==6.11.0
psycopg[binary]==3.2.10
python-decouple
dj-database-url==2.1.0
```

### 12.3 Actualización de Dependencias
```bash
# Listar dependencias desactualizadas
pip list --outdated

# Actualizar dependencia específica
pip install --upgrade nombre-libreria

# Actualizar requirements.txt
pip freeze > requirements.txt
```

### 12.4 Control de Seguridad
- Revisar vulnerabilidades conocidas en dependencias
- Actualizar librerías con parches de seguridad prioritariamente
- Evitar dependencias abandonadas

---

## 13. DOCUMENTACIÓN

### 13.1 Documentación Requerida

| Documento | Responsable | Ubicación | Actualización |
|-----------|-------------|-----------|---------------|
| README.md | Braian Gracia | Raíz del repositorio | Por cada release |
| GCS (este documento) | Braian Gracia | `/docs/GCS.md` | Cuando cambien procesos |
| Manual Técnico | Equipo completo | `/docs/manual_tecnico.md` | Por cada release |
| Manual de Usuario | Juan Ávila | `/docs/manual_usuario.md` | Por cada release |
| Diagramas UML | Juandiego Rodríguez | `/docs/uml/` | Cuando cambie arquitectura |
| API Documentation | Daniel Vanegas | `/docs/api.md` | Por cada cambio en API |

### 13.2 Estándares de Documentación
- Formato: Markdown para documentos técnicos
- Lenguaje: Español
- Diagramas: Mermaid, PlantUML o Draw.io
- Código: Docstrings en español siguiendo PEP 257

### 13.3 Documentación en Código
```python
def calcular_cierre_caja(ingresos, egresos):
    """
    Calcula el cierre de caja diario.
    
    Args:
        ingresos (float): Total de ingresos del día
        egresos (float): Total de egresos del día
    
    Returns:
        dict: Diccionario con 'saldo', 'sobrante', 'faltante'
    
    Raises:
        ValueError: Si los valores son negativos
    """
    pass
```

---

## 14. HERRAMIENTAS Y TECNOLOGÍAS GCS

### 14.1 Herramientas Utilizadas

| Herramienta | Propósito | URL |
|-------------|-----------|-----|
| Git | Control de versiones local | - |
| GitHub | Repositorio remoto, PRs, Issues | https://github.com |
| Render | Hosting y despliegue | https://render.com |
| PostgreSQL | Base de datos producción | (Gestionada por Render) |
| VS Code / PyCharm | IDEs de desarrollo | - |

### 14.2 Extensiones y Plugins Recomendados
- **VS Code:**
  - Python
  - GitLens
  - Django
  - Prettier
- **PyCharm:**
  - Django Support (integrado)
  - .ignore

---

## 15. MÉTRICAS Y REPORTES

### 15.1 Métricas de Configuración

**Métricas a monitorear:**
- Número de commits por desarrollador
- Tiempo promedio de revisión de PRs
- Tasa de conflictos de merge
- Cobertura de código (si se implementan tests)
- Frecuencia de despliegues

**Herramientas:**
- GitHub Insights
- Análisis manual de `git log`

### 15.2 Reportes de Configuración
Al final de cada entrega académica:
1. Reporte de commits realizados
2. Reporte de PRs revisados y mergeados
3. Listado de cambios principales
4. Problemas encontrados y soluciones

---

## 16. CAPACITACIÓN Y ONBOARDING

### 16.1 Nuevo Miembro del Equipo
**Proceso de incorporación:**
1. Lectura de README.md
2. Lectura de este documento GCS
3. Configuración de ambiente local siguiendo README
4. Revisión de arquitectura y módulos
5. Primer commit supervisado

### 16.2 Recursos de Aprendizaje
- Documentación oficial de Django: https://docs.djangoproject.com
- Git Tutorial: https://git-scm.com/docs/gittutorial
- Convenciones del proyecto: Ver sección 5.4

---

## 17. CUMPLIMIENTO Y ESTÁNDARES

### 17.1 Estándares Seguidos
- **IEEE 828-2012:** Software Configuration Management Plans
- **ISO/IEC 12207:** Software Life Cycle Processes
- **PEP 8:** Style Guide for Python Code
- **Semantic Versioning 2.0.0**

### 17.2 Buenas Prácticas
- Code reviews obligatorias
- Commits atómicos y descriptivos
- No commitear credenciales o datos sensibles
- Mantener `.gitignore` actualizado
- Documentar cambios significativos

---

## 18. CONTACTO Y SOPORTE

### 18.1 Contactos del Equipo

| Rol | Nombre | Email/GitHub |
|-----|--------|--------------|
| Configuration Manager | Braian Steven Gracia Ramírez | @braian-gracia |
| Desarrollador | Juandiego Rodríguez | @juandiego |
| Desarrollador | Juan Ávila | @juan-avila |
| Desarrollador | Daniel Vanegas | @daniel-vanegas |

### 18.2 Reporte de Problemas
- **Issues de GitHub:** Para bugs, mejoras, preguntas
- **Email del Configuration Manager:** Para problemas críticos de configuración

---

## 19. APÉNDICES

### 19.1 Checklist de Release
- [ ] Todos los PRs mergeados
- [ ] Tests pasando (cuando apliquen)
- [ ] Documentación actualizada
- [ ] Versión actualizada en docs
- [ ] Tag creado en Git
- [ ] Release notes escritas
- [ ] Despliegue a producción exitoso
- [ ] Verificación en producción
- [ ] Equipo notificado

### 19.2 Comandos Git Útiles
```bash
# Ver estado del repositorio
git status

# Ver historial
git log --oneline --graph --all

# Crear rama
git checkout -b nombre-rama

# Cambiar de rama
git checkout nombre-rama

# Actualizar rama con main
git merge main

# Ver diferencias
git diff

# Deshacer cambios no commiteados
git checkout -- archivo.py

# Ver ramas remotas
git branch -r

# Eliminar rama local
git branch -d nombre-rama

# Actualizar referencias remotas
git fetch --all
```

### 19.3 Glosario
- **Baseline:** Versión aprobada y congelada del software
- **CI (Configuration Item):** Elemento bajo control de configuración
- **Commit:** Registro de cambios en el repositorio
- **Merge:** Integración de cambios de una rama a otra
- **PR (Pull Request):** Solicitud de integración de cambios
- **Tag:** Marcador de versión específica en Git
- **Branch:** Rama independiente de desarrollo

---

## 20. CONTROL DE CAMBIOS DEL DOCUMENTO

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | 2024-11-22 | Braian Gracia | Creación inicial del documento GCS completo |

---

**Aprobado por:**  
Braian Steven Gracia Ramírez - Configuration Manager  
Universidad de Ibagué - Proyecto Académico de Ingeniería de Software  

**Próxima Revisión:** Al final del semestre académico o ante cambios significativos en el proceso.