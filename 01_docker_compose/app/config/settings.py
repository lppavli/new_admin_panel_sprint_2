import os
from pathlib import Path
import environ
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env.dev'))
SECRET_KEY = env.str('SECRET_KEY', 'SECRET_KEY')
DEBUG = env.bool('DEBUG', False)
ALLOWED_HOSTS = env.str('DJANGO_ALLOWED_HOSTS', default='').split(' ')
INTERNAL_IPS = ['127.0.0.1', '0.0.0.0']
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda _request: DEBUG
}
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'config',
    'movies',
    'rest_framework',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'config.urls'
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
WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": env.str("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": env.str("SQL_DATABASE", BASE_DIR / "db.sqlite3"),
        "USER": env.str("SQL_USER", "user"),
        "PASSWORD": env.str("SQL_PASSWORD", "password"),
        "HOST": env.str("SQL_HOST", "localhost"),
        "PORT": env.str("SQL_PORT", "5432"),
    }
}
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
LANGUAGE_CODE = 'ru-RU'
LANGUAGES = [
    ('en', _('English')),
    ('ru', _('Russian')),
]
LANGUAGE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
    os.path.join(BASE_DIR, 'movies/locale')
]
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = 'staticfiles/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
REST_FRAMEWORK = {
    'DATETIME_FORMAT': '%Y-%m-%d',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
        },
    },
    'handlers': {
        'debug-console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'filters': ['require_debug_true'],
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['debug-console'],
            'propagate': False,
        }
    },
}
