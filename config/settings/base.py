import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEBUG = os.environ.get("DEBUG")
DOMEN_NAME = os.environ.get("DOMEN_NAME")

SECRET_KEY = os.environ.get("SECRET_KEY")
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third party
    "drf_spectacular",
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "djoser",
    # first party
    "apps.common",
    "apps.import",
    "apps.customers",
    "apps.posts",
    "apps.filters",
]

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework.authentication.TokenAuthentication",),
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Pusher API",
    "DESCRIPTION": "Pusher API documentations",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

# SIMPLE_JWT = {
#     "ACCESS_TOKEN_LIFETIME": timedelta(hours=24),
#     "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
#     "SLIDING_TOKEN_LIFETIME": timedelta(days=30),
#     "SLIDING_TOKEN_REFRESH_LIFETIME_LATE_USER": timedelta(days=1),
#     "SLIDING_TOKEN_LIFETIME_LATE_USER": timedelta(days=30),
#     "TOKEN_OBTAIN_SERIALIZER": "apps.tokens.serializers.TokenSerializer",
# }

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
    },
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.AllowAllUsersModelBackend",
    "apps.customers.backends.CaseInsensitiveModelBackend",
]

AUTH_USER_MODEL = "customers.Customer"

LANGUAGE_CODE = "ru"

TIME_ZONE = "Europe/Kiev"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

# Telegram bot creds
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_BOT_THREAD_COUNT = int(os.environ.get("TELEGRAM_BOT_THREAD_COUNT"))

# Redis creds
REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_DB = os.environ.get("REDIS_DB")
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

# Broadcaster settings
MAX_POSTS_PER_TIME = int(os.environ.get("MAX_POSTS_PER_TIME"))
MAX_IMAGES_PER_POST = int(os.environ.get("MAX_IMAGES_PER_POST"))
TIME_CHECK_PERIOD = int(os.environ.get("TIME_CHECK_PERIOD"))

# Celery setting
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

CELERY_TIMEZONE = "Europe/Kiev"

CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

CORS_ALLOWED_ORIGINS = [
    "https://localhost:3000",
    "https://localhost:5173",
    "http://localhost:3000",
    "http://localhost:5173",
]

CORS_ORIGIN_WHITELIST = [
    "https://localhost:3000",
    "https://localhost:5173",
    "http://localhost:3000",
    "http://localhost:5173",
]
