# network_inventory/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-me-in-production')

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'drf_spectacular',
    'inventory',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'network_inventory.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'network_inventory.wsgi.application'

# ─────────────────────────────────────────────────────────────────
# DATABASE — SQLite3 by default, swap to PostgreSQL when ready
# ─────────────────────────────────────────────────────────────────
USE_POSTGRES = os.environ.get('USE_POSTGRES', 'False') == 'True'

if USE_POSTGRES:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME':     os.environ.get('DB_NAME', 'network_inventory'),
            'USER':     os.environ.get('DB_USER', 'postgres'),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST':     os.environ.get('DB_HOST', 'localhost'),
            'PORT':     os.environ.get('DB_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Tbilisi'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ─────────────────────────────────────────────────────────────────
# Django REST Framework
# ─────────────────────────────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}



CORS_ALLOW_ALL_ORIGINS = DEBUG  # allow all in dev; restrict in prod

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# For reverse proxy!
CSRF_COOKIE_SECURE = False
CSRF_USE_SESSIONS = False

# Reverse proxy settings
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_TRUSTED_ORIGINS = ['https://drf.itdev.ge']
SESSION_COOKIE_NAME = 'admin_sessionid'
LOGOUT_REDIRECT_URL = '/admin/'
LOGIN_REDIRECT_URL = '/api/'


# ─────────────────────────────────────────────────────────────────
# Swagger / API Documentation
# ─────────────────────────────────────────────────────────────────
SPECTACULAR_SETTINGS = {
    'TITLE': 'Network Inventory API',
    'DESCRIPTION': '''
## Network Inventory Management System

A REST API for managing network equipment across multiple city locations.

### How to authenticate
1. Use `POST /api/auth/login/` with your username and password
2. Copy the token from the response
3. Click **Authorize** button above and enter: `Token your_token_here`

### Permission levels
| Role | Permissions |
|------|-------------|
| **Admin** | Full CRUD on everything including cities, locations, users and equipment |
| **Regular User** | Read everything, add equipment, edit/delete only own equipment |

### Data hierarchy
```
City → Location (HQ or Branch) → Network Equipment
```
    ''',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'CONTACT': {
        'name': 'Lasha',
        'url': 'https://github.com/lasha1616/network_inventory',
    },
    'LICENSE': {
        'name': 'MIT License',
    },
    'TAGS': [
        {
            'name': 'auth',
            'description': 'Authentication — get your token here first',
        },
        {
            'name': 'cities',
            'description': 'Manage cities — admin only for write operations',
        },
        {
            'name': 'locations',
            'description': 'Manage HQ and branch locations inside cities — admin only for write operations',
        },
        {
            'name': 'equipment',
            'description': 'Manage network equipment (routers, switches, APs) — all users can add, owners can edit/delete',
        },
        {
            'name': 'users',
            'description': 'Manage users — admin only',
        },
    ],
}