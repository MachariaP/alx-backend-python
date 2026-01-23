#!/bin/bash
# clean_setup.sh

echo "Cleaning up and setting up for Render deployment..."

# 1. Backup original files
echo "Backing up original files..."
cp requirements.txt requirements.txt.backup 2>/dev/null || true

# 2. Create correct requirements.txt
echo "Creating correct requirements.txt..."
cat > requirements.txt << 'EOF'
# Core Django
Django==5.2.8
djangorestframework==3.16.1
django-filter==25.2

# Authentication
djangorestframework-simplejwt==5.5.1
PyJWT==2.10.1

# Database
mysqlclient==2.2.4
dj-database-url==2.1.0
psycopg2-binary==2.9.9

# API Documentation
drf-spectacular==0.27.2

# Environment variables
python-decouple==3.8

# Production
gunicorn==21.2.0
whitenoise==6.6.0

# Required dependencies
asgiref==3.10.0
sqlparse==0.5.3
typing_extensions==4.15.0
EOF

# 3. Update Dockerfile
echo "Updating Dockerfile..."
cat > Dockerfile << 'EOF'
FROM python:3.12-slim

# Install system dependencies (PostgreSQL client libraries)
RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Run migrations, collectstatic, and start server
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn --bind 0.0.0.0:8000 messaging_app.wsgi:application"]
EOF

# 4. Update settings_prod.py for PostgreSQL
echo "Updating production settings..."
cat > messaging_app/settings_prod.py << 'EOF'
"""
Django production settings for messaging_app project.
"""

import os
import dj_database_url
from datetime import timedelta

# Build paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-fallback-key-change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['messaging-app.onrender.com', 'localhost', '127.0.0.1', '.onrender.com']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party
    'rest_framework',
    'django_filters',
    'rest_framework_simplejwt',
    'drf_spectacular',

    # Local apps
    'chats',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'messaging_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'messaging_app.wsgi.application'

# Database configuration for Render (PostgreSQL)
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'ALX Messaging App API',
    'DESCRIPTION': 'Backend API for real-time messaging application',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': True,
    'SWAGGER_UI_SETTINGS': {
        'persistAuthorization': True,
    },
    'COMPONENT_NO_READ_ONLY_REQUIRED': True,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# Static files
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Custom User model
AUTH_USER_MODEL = 'chats.User'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Security settings for production
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
EOF

# 5. Update main settings.py to add DATABASE_URL fallback
echo "Updating main settings.py..."
# Create a backup first
cp messaging_app/settings.py messaging_app/settings.py.backup

# Update DATABASES section in settings.py
cat > temp_update.py << 'EOF'
import re

with open('messaging_app/settings.py', 'r') as f:
    content = f.read()

# Add import for dj_database_url if not present
if 'import dj_database_url' not in content:
    content = content.replace(
        'import os\nfrom datetime import timedelta\nfrom pathlib import Path\nfrom decouple import config',
        'import os\nimport dj_database_url\nfrom datetime import timedelta\nfrom pathlib import Path\nfrom decouple import config'
    )

# Replace DATABASES section to support both MySQL and PostgreSQL
new_databases = '''# Database configuration
if 'DATABASE_URL' in os.environ:
    # Render PostgreSQL database
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Local MySQL database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': config('MYSQL_DATABASE', default='messaging_app'),
            'USER': config('MYSQL_USER', default='root'),
            'PASSWORD': config('MYSQL_PASSWORD', default=''),
            'HOST': config('MYSQL_HOST', default='localhost'),
            'PORT': config('MYSQL_PORT', default=3306),
        }
    }'''

# Replace the DATABASES section
content = re.sub(r'DATABASES = \{[\s\S]*?\}', new_databases, content)

# Update DEBUG and ALLOWED_HOSTS
content = content.replace('DEBUG = True', "DEBUG = os.environ.get('DEBUG', 'False') == 'True'")
content = content.replace("ALLOWED_HOSTS = []", "ALLOWED_HOSTS = ['localhost', '127.0.0.1']")

with open('messaging_app/settings.py', 'w') as f:
    f.write(content)
EOF

python temp_update.py
rm temp_update.py

# 6. Update render.yaml with correct DATABASE_URL
echo "Updating render.yaml..."
cat > render.yaml << 'EOF'
services:
  - type: web
    name: messaging-app
    env: docker
    dockerfilePath: ./Dockerfile
    dockerContext: .
    envVars:
      - key: DATABASE_URL
        value: postgresql://messaging_db_wdtp_user:CrVGoDBg9vsd8DNQRflsISfmRuoXo5C8@dpg-d5pivf8gjchc73dvgtb0-a.oregon-postgres.render.com/messaging_db_wdtp
      - key: SECRET_KEY
        generateValue: true
      - key: ALLOWED_HOSTS
        value: messaging-app.onrender.com,localhost,127.0.0.1
      - key: DEBUG
        value: "False"
    healthCheckPath: /api/schema/swagger-ui/
    autoDeploy: true
    plan: free
    numInstances: 1
EOF

echo "✅ Clean setup complete!"
echo ""
echo "Files updated:"
echo "1. requirements.txt - Fixed with Django/PostgreSQL packages"
echo "2. Dockerfile - Optimized for PostgreSQL"
echo "3. settings_prod.py - Production PostgreSQL settings"
echo "4. settings.py - Added DATABASE_URL fallback"
echo "5. render.yaml - Updated with your PostgreSQL URL"
echo ""
echo "Next steps:"
echo "1. Test locally: python manage.py check"
echo "2. Commit changes: git add . && git commit -m 'Fix requirements and PostgreSQL setup'"
echo "3. Push to GitHub: git push origin main"
echo "4. Render will auto-deploy"
