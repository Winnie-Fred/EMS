"""
Django settings for estateX project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

LIVE = False


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'secret_key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not LIVE


ALLOWED_HOSTS = ['estateX.local', '.estateX.local']


TENANT_MODEL = "customers.Client"

# Application definition

SHARED_APPS = (
    'tenant_schemas',  # mandatory, should always be before any django app
    'customers', # you must list the app where your tenant model resides in

    'django.contrib.contenttypes',

    # everything below here is optional
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # cloudinary
    'cloudinary',

    # Local
    'users',
    'helper',
    'authentication',
    'estate_manager',
    'pages',
    'property',
    'fee',
)

TENANT_APPS = (
    'django.contrib.contenttypes',

    # your tenant-specific apps

    # everything below here is optional
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # cloudinary
    'cloudinary',

    # Local
    'users',
    'authentication',
    'estate_manager',
    'pages',
    'property',
    'fee',
)

INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]

PUBLIC_SCHEMA_NAME = 'public'

MIDDLEWARE = [
    'tenant_schemas.middleware.TenantMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'customers.dynamic_site.DynamicSiteMiddleware',
]

MIDDLEWARE_CLASSES = [
    'tenant_schemas.middleware.TenantMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'customers.dynamic_site.DynamicSiteMiddleware',
]

ROOT_URLCONF = 'estateX.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
            ],
        },
    },
]

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.template.context_processors.debug',
    'django.template.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.static',
)

AUTHENTICATION_BACKENDS = [
    
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
    
]

WSGI_APPLICATION = 'estateX.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'tenant_schemas.postgresql_backend',
        'NAME': os.getenv('DB_NAME', 'db_name'),
        'USER': os.getenv('DB_USER', 'db_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'db_password'),
        'HOST': os.getenv('HOST', 'localhost'),
        'PORT': os.getenv('PORT', 5432),
    }
}


DATABASE_ROUTERS = ("tenant_schemas.routers.TenantSyncRouter",)
DEFAULT_FILE_STORAGE = 'tenant_schemas.storage.TenantFileSystemStorage'


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/home'
LOGIN_URL = '/auth/login/'

# allauth
ACCOUNT_FORMS = {
    'signup': 'authentication.forms.CustomSignupForm',
    'login': 'authentication.forms.CustomLoginForm',
}

ACCOUNT_LOGOUT_REDIRECT_URL = '/home/'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED= True
ACCOUNT_ADAPTER = 'authentication.custom_adapters.tenant_account_adapter.TenantAccountAdapter'

if not LIVE:
    # Console Email Backend, which outputs the emails to the console instead of sending them
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    # Email settings for development, using the console backend
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 1025

else:
    # SMTP Email Backend, which sends emails using SMTP
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    # Email settings for production, using SMTP
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = os.getenv('EMAIL_PORT', 587)
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'myemail@gmail.com')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'yourpassword')
    EMAIL_USE_TLS = True


AUTH_USER_MODEL = 'users.CustomUser'
