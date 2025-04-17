"""
Django settings for nexusmart_config project.

Generated by 'django-admin startproject' using Django 5.0.14.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-gsyd=m8hv1%o_m%i-ga=e1um12vw7p)uyn#8w$fqhk8hcu@))z'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    'rest_framework',
    'django_filters',

    # nexusmart apps
    'users.apps.UsersConfig',
    'products.apps.ProductsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'nexusmart_config.urls'

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

WSGI_APPLICATION = 'nexusmart_config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        # Use the PostgreSQL engine.
        'ENGINE': 'django.db.backends.postgresql',
        # Get the database connection details from environment variables.
        # These variables are set in the 'environment' section of the 'web' service
        # in the docker-compose.yml file. Using os.environ.get() is a secure
        # way to read them without hardcoding credentials in the settings file.
        'NAME': os.environ.get('DB_NAME'),          # e.g., 'nexusmart_db'
        'USER': os.environ.get('DB_USER'),          # e.g., 'nexususer'
        'PASSWORD': os.environ.get('DB_PASSWORD'),  # e.g., 'nexuspassword'
        'HOST': os.environ.get('DB_HOST'),          # e.g., 'db' (the service name in docker-compose)
        'PORT': os.environ.get('DB_PORT'),          # e.g., '5432'
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# --- Django REST Framework Settings ---

REST_FRAMEWORK = {
    # --- Default Filtering Settings ---
    # Set default filtering backend for all views/viewsets
    'DEFAULT_FILTER_BACKEND': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],

    # --- Default Pagination Settings ---
    # Sets the default pagination style for list views.
    # PageNumberPagination allows clients to request pages using '?page=...' query parameter.
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',

    # Sets the default number of items to include on each page.
    # Clients can potentially override this with a 'page_size' query parameter if allowed.
    'PAGE_SIZE': 10, # Show 10 items per page by default
}

# Optional: Configure Simple JWT settings (e.g., token lifetimes)
# Keep defaults for now
# SIMPLE_JWT = {
#     "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
#     "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
#     # ... other settings
# }

# --- Custom User Model Configuration ---
# Tells Django to use the User model defined in the 'users' app
# instead of the default django.contrib.auth.models.User.
# IMPORTANT: This MUST be set before running 'makemigrations' for the first time
# for the 'users' app or any app with a ForeignKey to the User model.
AUTH_USER_MODEL =  'users.User'