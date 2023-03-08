# flake8: noqa
import socket

from .base import *
from .constants import ENVS

ENV = ENVS.DEV
HOST = "http://localhost:8000"
DEBUG = True
########################################
# DEBUG TOOLBAR
########################################
INSTALLED_APPS.append("debug_toolbar")
MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[:-1] + "1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]

########################################
# EMAIL
########################################
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

########################################
# SECURITY
########################################
ALLOWED_HOSTS = ["*"]

########################################
# MEDIA SETTINGS
########################################
MEDIA_ROOT = "/data/media"
MEDIA_URL = "/media/"
