"""
Django base settings file for dev and prod.
"""
from pathlib import Path

import environ
from django.urls import reverse_lazy

env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

########################################
# APPS
########################################
INSTALLED_APPS = [
    # django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.humanize",
    "django",
    "mozilla_django_oidc",
    'rest_framework',
    "users",
    "organisations",
    "sorbay",
    'recordings',

]

########################################
# MIDDLEWARE
########################################
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

########################################
# SECURITY
########################################
SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DJANGO_DEBUG")
ALLOWED_HOSTS = []

########################################
# OTHER
########################################
WSGI_APPLICATION = "wsgi.application"
SITE_ID = 1

########################################
# TEMPLATES
########################################
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
                "sorbay.context_processors.host",
            ]
        },
    }
]

########################################
# DATABASE
########################################
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env("POSTGRES_DATABASE"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": "5432",
    }
}

########################################
# CACHE
########################################
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://{env('REDIS_HOST')}:6379/{env('REDIS_DATABASE')}",
    },
}

########################################
# URLS
########################################
ROOT_URLCONF = "urls"
APPEND_SLASH = False

########################################
# PASSWORD VALIDATION
########################################
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

########################################
# INTERNATIONALISATION
########################################
LANGUAGE_CODE = "en-us"
TIME_ZONE = env("TIMEZONE")
USE_I18N = True
USE_TZ = True

########################################
# TIME_FORMATS
########################################
TIME_INPUT_FORMATS = [
    "%I:%M:%S %p",  # 6:22:44 PM
    "%I:%M %p",  # 6:22 PM
    "%I %p",  # 6 PM
    "%H:%M:%S",  # '14:30:59'
    "%H:%M:%S.%f",  # '14:30:59.000200'
    "%H:%M",  # '14:30'
]

########################################
# STATIC SETTINGS
########################################
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

########################################
# AUTHENTICATION
########################################
AUTH_USER_MODEL = "users.User"
AUTHENTICATION_BACKENDS = ["sorbay.auth_backend.CustomOIDCAuthenticationBackend"]
LOGIN_URL = reverse_lazy("oidc_authentication_init")
LOGOUT_REDIRECT_URL = reverse_lazy("home")
LOGIN_REDIRECT_URL = reverse_lazy("recordings:dashboard")
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

########################################
# CELERY
########################################
CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_URL = CACHES["default"]["LOCATION"]
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_TIME_LIMIT = 5 * 60
CELERY_TASK_SOFT_TIME_LIMIT = 2 * 60
CELERY_BEAT_SCHEDULE = {}

########################################
# S3
########################################
S3_ENDPOINT_URL = env("S3_ENDPOINT_URL")
S3_PUBLIC_ENDPOINT_URL = env("S3_PUBLIC_ENDPOINT_URL")
S3_ACCESS_KEY = env("S3_ACCESS_KEY")
S3_SECRET_KEY = env("S3_SECRET_KEY")

########################################
# OIDC
########################################
OIDC_RP_CLIENT_ID = env("OIDC_RP_CLIENT_ID")
OIDC_RP_CLIENT_SECRET = env("OIDC_RP_CLIENT_SECRET")
OIDC_RP_SIGN_ALGO = env("OIDC_RP_SIGN_ALGO")
OIDC_OP_JWKS_ENDPOINT = env("OIDC_OP_JWKS_ENDPOINT")
OIDC_OP_AUTHORIZATION_ENDPOINT = env("OIDC_OP_AUTHORIZATION_ENDPOINT")
OIDC_OP_TOKEN_ENDPOINT = env("OIDC_OP_TOKEN_ENDPOINT")
OIDC_OP_USER_ENDPOINT = env("OIDC_OP_USER_ENDPOINT")
OIDC_OP_LOGOUT_ENDPOINT = env("OIDC_OP_LOGOUT_ENDPOINT")
OIDC_OP_LOGOUT_URL_METHOD = 'sorbay.auth_backend.provider_logout'

########################################
# KEYCLOAK
########################################
KEYCLOAK_URL = env("DJANGO_KEYCLOAK_URL")
KEYCLOAK_REALM = env("DJANGO_KEYCLOAK_REALM")
KEYCLOAK_ADMIN_USER = env("KEYCLOAK_ADMIN")
KEYCLOAK_ADMIN_PASSWORD = env("KEYCLOAK_ADMIN_PASSWORD")

########################################
# DJANGO REST FRAMEWORK
########################################
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'sorbay.auth_backend.DeviceAPIAuthenticationBackend',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}
